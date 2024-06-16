from memos_webhook.plugins.base_plugin import IPlugin, PluginExecutor
from memos_webhook.plugins.you_get_plugin import YouGetPlugin
from memos_webhook.plugins.zhipu_plugin import ZhipuPlugin

from .config import Config, PluginConfig, YouGetPluginConfig
from .memos_cli import MemosCli

_plugin_executor: PluginExecutor | None = None


_DEFAULT_PLUGIN_CFG = [
    PluginConfig(
        name="you-get",
        tag="hook/download",
        you_get_plugin=YouGetPluginConfig(
            patterns=[
                "https://twitter.com/\\w+/status/\\d+",
                "https://x.com/\\w+/status/\\d+",
            ],
        ),
    )
]


def new_plugin_executor(cfg: Config, memos_cli: MemosCli) -> PluginExecutor:
    global _plugin_executor
    plugins_cfgs = cfg.plugins
    if plugins_cfgs is None:
        plugins_cfgs = _DEFAULT_PLUGIN_CFG  # temp fake cfg

    plugins: list[IPlugin] = []
    for plugin_cfg in plugins_cfgs:
        if plugin_cfg.you_get_plugin is not None:
            plugins.append(
                YouGetPlugin(
                    plugin_cfg.name,
                    plugin_cfg.tag,
                    plugin_cfg.you_get_plugin,
                )
            )
        if plugin_cfg.zhipu_plugin is not None:
            plugins.append(
                ZhipuPlugin(
                    plugin_cfg.name,
                    plugin_cfg.tag,
                    plugin_cfg.zhipu_plugin,
                )
            )

    _plugin_executor = PluginExecutor(memos_cli, plugins)
    return _plugin_executor


def get_plugin_executor() -> PluginExecutor:
    assert _plugin_executor is not None, "plugin_executor not initialized"
    return _plugin_executor
