from typing import Any, Dict, List, Optional

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.embeddings.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import LLM
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic.v1 import root_validator
from pydantic.v1.main import BaseModel
from zhipuai import ZhipuAI
from zhipuai.api_resource.chat.completions import Completions


class ZhipuAIChatModel(BaseChatModel):
    api_key: str = ""
    temperature: float = 0.9
    top_p: float = 0.7
    client: ZhipuAI = None
    max_tokens: int = 1024
    model_name: str = "chatglm_turbo"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        from zhipuai import ZhipuAI
        from zhipuai.api_resource.chat.completions import Completions

        # if values["client"] is None:
        values["client"] = ZhipuAI(api_key=values["api_key"])
        return values

    @property
    def _llm_type(self) -> str:
        return "zhipuai"

    def _generate(self,
                  messages: List[BaseMessage],
                  stop: List[str] | None = None,
                  run_manager: CallbackManagerForLLMRun | None = None,
                  **kwargs: Any) -> ChatResult:
        completions = Completions(client=self.client)
        zhipuMessages = [self._langchainMsgToZhipuMsg(m) for m in messages]
        print(f"{zhipuMessages=}")
        response = completions.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            messages=zhipuMessages,
            temperature=self.temperature,
            top_p=self.top_p,
        )
        print(f"{response=}")
        generation = ChatGeneration(message=AIMessage(
            content=response.choices[0].message.content))

        return ChatResult(generations=[generation],
                          llm_output=response.model_dump())

    def _langchainMsgToZhipuMsg(self, message: BaseMessage) -> Dict:
        if isinstance(message, AIMessage):
            return {"role": "assistant", "content": message.content}
        if isinstance(message, HumanMessage):
            return {"role": "user", "content": message.content}
        if isinstance(message, SystemMessage):
            return {"role": "system", "content": message.content}

        # fallback to human message
        return {"role": "user", "content": message.content}


class ZhipuAIEmbedding(BaseModel, Embeddings):
    api_key: str = ""
    client: Any
    model_name: str = "embedding-2"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        from zhipuai import ZhipuAI
        values["client"] = ZhipuAI(api_key=values["api_key"])
        return values

    def embed_query(self, text: str) -> List[float]:
        print(f"[embed_query] {text=}")
        embeddings = self.client.embeddings.create(
            model=self.model_name,
            input=text,
        )
        return embeddings.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        print(f"[embed_documents] {texts=}")
        return [self.embed_query(text) for text in texts]
