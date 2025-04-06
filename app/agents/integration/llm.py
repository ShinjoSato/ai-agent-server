from llama_index.core.base.llms.types import ChatMessage, ChatResponse
from llama_index.core.llms import LLM, LLMMetadata


class CustomLLM(LLM):
    def chat(self, messages: list[ChatMessage], **kwargs) -> ChatResponse:
        raise NotImplementedError("Not Implemented Error")

    def complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def stream_chat(self, messages: list[ChatMessage], **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def stream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=8192,
            num_output=1024,
            is_chat_model=True,
            is_function_calling_model=False,
        )

    def achat(self, messages: list[ChatMessage], **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def acomplete(self, prompt: str, **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def astream_chat(self, messages: list[ChatMessage], **kwargs):
        raise NotImplementedError("Not Implemented Error")

    def astream_complete(self, prompt: str, **kwargs):
        raise NotImplementedError("Not Implemented Error")
