from logging import Logger
from typing import override

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable

from memos_webhook.dependencies.config import ZhipuPluginConfig
from memos_webhook.dependencies.memos_cli import MemosCli
from memos_webhook.langchains.zhipu import ZhipuAIChatModel
from memos_webhook.proto_gen.memos.api.v1 import Memo, WebhookRequestPayload

from .base_plugin import BasePlugin, pluginLogger


class ZhipuPlugin(BasePlugin):
    logger: Logger = pluginLogger.getChild("ZhipuPlugin")
    cfg: ZhipuPluginConfig
    chain: RunnableSerializable

    def __init__(self, name: str, tag: str, cfg: ZhipuPluginConfig) -> None:
        super().__init__(name=name, tag=tag)
        self.cfg = cfg
        llm = ZhipuAIChatModel(api_key=cfg.api_key)
        self.chain = (
            {"content": RunnablePassthrough()}
            | PromptTemplate.from_template(self.cfg.prompt)
            | llm
            | StrOutputParser()
        )

    @override
    def activity_types(self) -> list[str]:
        return ["memos.memo.created"]

    @override
    async def task(self, payload: WebhookRequestPayload, memos_cli: MemosCli) -> Memo:
        self.logger.debug("start zhipu plugin task")
        content = payload.memo.content.replace(f"#{self.tag}", "")
        self.logger.debug(f"content: {content}")

        res: str = await self.chain.ainvoke(input=content)
        res_content = f"""{payload.memo.content}

---AI Generated---

{res}
"""

        payload.memo.content = res_content
        return payload.memo
