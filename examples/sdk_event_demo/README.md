# SDK Event Demo Plugin

这是一个"最小监听漫画更新事件并写日志"的示例插件，展示了 VabHub 插件 SDK 的基本使用方法。

## 功能说明

- 插件加载时记录启动日志
- 订阅 `EventType.MANGA_UPDATED` 事件
- 当漫画更新事件发生时，在日志中记录事件数据

## 代码结构

```python
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    sdk.log.info("sdk_event_demo plugin loaded")

    async def on_manga_updated(event: EventType, payload: dict) -> None:
        sdk.log.info(f"[sdk_event_demo] Manga updated: {payload}")

    bus.subscribe(EventType.MANGA_UPDATED, on_manga_updated, source=ctx.plugin_id)
```

## 关键要点

1. **入口函数**: 使用标准的 `setup_plugin(ctx, bus, sdk)` 函数作为插件入口
2. **事件订阅**: 通过 `bus.subscribe()` 订阅系统事件
3. **source 参数**: 传入 `ctx.plugin_id` 以便插件卸载时自动清理订阅
4. **异步处理**: 事件处理函数必须是 `async` 函数

## 使用指南

插件作者可以复制这段结构到自己的插件项目中，作为开发起点。

## 进一步学习

实际的事件类型、payload 字段详情请参见主仓库文档 `docs/PLUGIN_SDK_OVERVIEW.md`。

更完整的开发指南请参考：
- [插件开发指南](../../docs/PLUGIN_DEV_GUIDE.md)
- [插件索引规范](../../docs/PLUGIN_INDEX_SPEC.md)