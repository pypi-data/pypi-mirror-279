import uuid
from abc import abstractmethod
from typing import Any, AsyncGenerator, Optional

from r2r.core import (
    AsyncState,
    GenerationConfig,
    LLMProvider,
    LoggableAsyncPipe,
    PipeType,
    PromptProvider,
)


class GeneratorPipe(LoggableAsyncPipe):
    class Config(LoggableAsyncPipe.PipeConfig):
        name: str
        task_prompt: str
        system_prompt: str = "default_system"

    def __init__(
        self,
        llm_provider: LLMProvider,
        prompt_provider: PromptProvider,
        type: PipeType = PipeType.GENERATOR,
        config: Optional[Config] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            type=type,
            config=config or self.Config(),
            *args,
            **kwargs,
        )
        self.llm_provider = llm_provider
        self.prompt_provider = prompt_provider

    @abstractmethod
    async def _run_logic(
        self,
        input: LoggableAsyncPipe.Input,
        state: AsyncState,
        run_id: uuid.UUID,
        rag_generation_config: GenerationConfig,
        *args: Any,
        **kwargs: Any,
    ) -> AsyncGenerator[Any, None]:
        pass

    @abstractmethod
    def _get_message_payload(
        self, message: str, *args: Any, **kwargs: Any
    ) -> list:
        pass
