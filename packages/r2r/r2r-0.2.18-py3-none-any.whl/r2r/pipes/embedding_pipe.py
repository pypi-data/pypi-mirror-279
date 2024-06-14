import asyncio
import copy
import json
import logging
import uuid
from abc import abstractmethod
from typing import Any, AsyncGenerator, Optional

from r2r.core import (
    AsyncState,
    EmbeddingProvider,
    Extraction,
    Fragment,
    FragmentType,
    KVLoggingSingleton,
    LoggableAsyncPipe,
    PipeType,
    TextSplitter,
    Vector,
    VectorEntry,
    generate_id_from_label,
)

logger = logging.getLogger(__name__)


class EmbeddingPipe(LoggableAsyncPipe):
    class Input(LoggableAsyncPipe.Input):
        message: AsyncGenerator[Extraction, None]

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        pipe_logger: Optional[KVLoggingSingleton] = None,
        type: PipeType = PipeType.INGESTOR,
        config: Optional[LoggableAsyncPipe.PipeConfig] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            pipe_logger=pipe_logger,
            type=type,
            config=config,
            *args,
            **kwargs,
        )
        self.embedding_provider = embedding_provider

    @abstractmethod
    async def fragment(
        self, extraction: Extraction
    ) -> AsyncGenerator[Fragment, None]:
        pass

    @abstractmethod
    async def transform_fragments(
        self, fragments: list[Fragment], metadatas: list[dict]
    ) -> AsyncGenerator[Fragment, None]:
        pass

    @abstractmethod
    async def embed(self, fragments: list[Fragment]) -> list[list[float]]:
        pass

    @abstractmethod
    async def _run_logic(
        self,
        input: AsyncGenerator[Extraction, None],
        state: AsyncState,
        run_id: uuid.UUID,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncGenerator[VectorEntry, None]:
        pass


class R2REmbeddingPipe(EmbeddingPipe):
    """
    Embeds and stores documents using a specified embedding model and database.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        text_splitter: TextSplitter,
        embedding_batch_size: int = 1,
        id_prefix: str = "demo",
        pipe_logger: Optional[KVLoggingSingleton] = None,
        type: PipeType = PipeType.INGESTOR,
        config: Optional[LoggableAsyncPipe.PipeConfig] = None,
        *args,
        **kwargs,
    ):
        """
        Initializes the embedding pipe with necessary components and configurations.
        """
        super().__init__(
            embedding_provider=embedding_provider,
            pipe_logger=pipe_logger,
            type=type,
            config=config
            or LoggableAsyncPipe.PipeConfig(name="default_embedding_pipe"),
        )
        self.text_splitter = text_splitter
        self.embedding_batch_size = embedding_batch_size
        self.id_prefix = id_prefix
        self.pipe_run_info = None

    async def fragment(
        self, extraction: Extraction, run_id: uuid.UUID
    ) -> AsyncGenerator[Fragment, None]:
        """
        Splits text into manageable chunks for embedding.
        """
        if not isinstance(extraction, Extraction):
            raise ValueError(
                f"Expected an Extraction, but received {type(extraction)}."
            )
        if not isinstance(extraction.data, str):
            raise ValueError(
                f"Expected a string, but received {type(extraction.data)}."
            )
        text_chunks = [
            ele.page_content
            for ele in self.text_splitter.create_documents([extraction.data])
        ]
        for iteration, chunk in enumerate(text_chunks):
            fragment = Fragment(
                id=generate_id_from_label(f"{extraction.id}-{iteration}"),
                type=FragmentType.TEXT,
                data=chunk,
                metadata=copy.deepcopy(extraction.metadata),
                extraction_id=extraction.id,
                document_id=extraction.document_id,
            )
            yield fragment
            fragment_dict = fragment.dict()
            await self.enqueue_log(
                run_id=run_id,
                key="fragment",
                value=json.dumps(
                    {
                        "data": fragment_dict["data"],
                        "document_id": str(fragment_dict["document_id"]),
                        "extraction_id": str(fragment_dict["extraction_id"]),
                        "fragment_id": str(fragment_dict["id"]),
                    }
                ),
            )
            iteration += 1

    async def transform_fragments(
        self, fragments: list[Fragment], metadatas: list[dict]
    ) -> AsyncGenerator[Fragment, None]:
        """
        Transforms text chunks based on their metadata, e.g., adding prefixes.
        """
        async for fragment, metadata in zip(fragments, metadatas):
            if "chunk_prefix" in metadata:
                prefix = metadata.pop("chunk_prefix")
                fragment.data = f"{prefix}\n{fragment.data}"
            yield fragment

    async def embed(self, fragments: list[Fragment]) -> list[float]:
        return await self.embedding_provider.async_get_embeddings(
            [fragment.data for fragment in fragments],
            EmbeddingProvider.PipeStage.BASE,
        )

    async def _process_batch(
        self, fragment_batch: list[Fragment]
    ) -> list[VectorEntry]:
        """
        Embeds a batch of fragments and yields vector entries.
        """
        vectors = await self.embed(fragment_batch)
        return [
            VectorEntry(
                id=fragment.id,
                vector=Vector(data=raw_vector),
                metadata={
                    "document_id": fragment.document_id,
                    "extraction_id": fragment.extraction_id,
                    "text": fragment.data,
                    **fragment.metadata,
                },
            )
            for raw_vector, fragment in zip(vectors, fragment_batch)
        ]

    async def _run_logic(
        self,
        input: EmbeddingPipe.Input,
        state: AsyncState,
        run_id: uuid.UUID,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncGenerator[VectorEntry, None]:
        """
        Executes the embedding pipe: chunking, transforming, embedding, and storing documents.
        """
        batch_tasks = []
        fragment_batch = []

        fragment_info = {}
        async for extraction in input.message:
            async for fragment in self.fragment(extraction, run_id):
                if extraction.document_id in fragment_info:
                    fragment_info[extraction.document_id] += 1
                else:
                    fragment_info[extraction.document_id] = 1
                extraction.metadata["chunk_order"] = fragment_info[
                    extraction.document_id
                ]
                fragment_batch.append(fragment)
                if len(fragment_batch) >= self.embedding_batch_size:
                    # Here, ensure `_process_batch` is scheduled as a coroutine, not called directly
                    batch_tasks.append(
                        self._process_batch(fragment_batch.copy())
                    )  # pass a copy if necessary
                    fragment_batch.clear()  # Clear the batch for new fragments

        logger.info(
            f"Fragmented the input document ids into counts as shown: {fragment_info}"
        )

        if fragment_batch:  # Process any remaining fragments
            batch_tasks.append(self._process_batch(fragment_batch.copy()))

        # Process tasks as they complete
        for task in asyncio.as_completed(batch_tasks):
            batch_result = await task  # Wait for the next task to complete
            for vector_entry in batch_result:
                yield vector_entry
