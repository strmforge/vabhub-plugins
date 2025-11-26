# VabHub 插件开发指南（基于 SDK + 事件系统）

本文档面向插件作者，介绍如何使用 VabHub 插件 SDK 和事件系统开发插件。

## 插件开发整体流程

### 1. 创建插件仓库

在本地或自己的 GitHub 建一个插件仓库，比如 `yourname/vabhub-my-plugin`。

### 2. 创建插件包和入口函数

建议的目录结构：

```
vabhub-my-plugin/
├── README.md              # 插件说明文档
├── pyproject.toml         # Python 包配置（可选）
└── my_plugin/             # 插件包目录
    ├── __init__.py
    └── plugin.py          # 包含 setup_plugin
```

### 3. 实现插件逻辑

在 `plugin.py` 里实现 `setup_plugin(ctx, bus, sdk)`。

### 4. 使用 SDK 和事件系统

通过 `sdk` & `bus` 使用主系统能力、订阅事件。

### 5. 发布插件

把该插件发布到某个插件 Hub 的 `plugins.json`（可以是自己的 Hub，也可以通过官方流程挂到 `vabhub-plugins`）。

## 入口函数解释

### 函数签名

```python
def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """
    插件初始化入口函数
    
    Args:
        ctx: 插件上下文，包含插件环境信息
        bus: 全局事件总线，用于订阅业务事件  
        sdk: 与主系统交互的官方 SDK 实例
    """
    pass
```

### 参数含义

- **ctx**: 插件上下文（包含 `plugin_id`、`data_dir`、logger 名称等）
- **bus**: 全局事件总线，可以订阅业务事件
- **sdk**: 与主系统交互的官方 SDK 实例，内含日志、环境信息、HTTP 客户端、通知接口等

### 重要原则

插件应尽量只依赖这三个入口（`ctx`/`bus`/`sdk`），不要直接 import 主系统内部 service/model，这些属于不稳定内部实现。

## SDK 能力简要版（v1 摘要）

### `sdk.log`：插件专用 Logger

```python
sdk.log.info("Plugin started")
sdk.log.warning("Something might be wrong") 
sdk.log.error("Something went wrong")
```

### `sdk.paths.data_dir`：插件数据目录

可用于存放缓存/配置文件：

```python
import json
cfg_file = sdk.paths.data_dir / "config.json"

# 读取配置
if cfg_file.exists():
    config = json.loads(cfg_file.read_text())

# 保存配置
cfg_file.write_text(json.dumps(config, indent=2))
```

### `sdk.http`：统一 HTTP 客户端

使用主系统的 User Agent、代理设置等：

```python
# GET 请求
response = await sdk.http.get("https://api.example.com/data")
data = response.json()

# POST 请求
response = await sdk.http.post(
    "https://api.example.com/submit",
    json={"key": "value"}
)
```

### `sdk.notify`：发送通知

用于向用户发送通知：

```python
# 发送成功通知
await sdk.notify.success("操作完成")

# 发送错误通知  
await sdk.notify.error("操作失败", "详细信息")

# 发送信息通知
await sdk.notify.info("提示信息")
```

**注意**：SDK 能力的完整列表及参数说明，请参见 VabHub 主仓库：`docs/PLUGIN_SDK_OVERVIEW.md`。

## 事件系统摘要

### 事件类型

所有可订阅的事件由 `EventType` 枚举定义，常见的有：

- `EventType.MANGA_UPDATED` - 漫画更新
- `EventType.DOWNLOAD_COMPLETED` - 下载完成
- `EventType.USER_LOGIN` - 用户登录
- `EventType.SYSTEM_SHUTDOWN` - 系统关闭

### 事件订阅

事件总线使用 `EventBus` 提供的 `subscribe/unsubscribe` 接口：

```python
async def on_event(event: EventType, payload: dict) -> None:
    sdk.log.info("Got event %s: %s", event.value, payload)

# 订阅事件（使用 source 标明插件来源，便于卸载清理）
bus.subscribe(EventType.MANGA_UPDATED, on_event, source=ctx.plugin_id)
```

### 重要注意事项

1. **事件 handler 必须是 async 函数**
2. **handler 里不要执行特别重的阻塞操作，必要时自己启动 Task**
3. **使用 `source=ctx.plugin_id` 以便插件卸载时自动清理订阅**

### 事件发布

插件也可以发布自定义事件：

```python
# 发布自定义事件
bus.subscribe("my_custom_event", {
    "plugin_id": ctx.plugin_id,
    "data": "custom_data"
})
```

**当前可用的事件类型列表及 payload 字段说明，请参见主仓库 `docs/PLUGIN_SDK_OVERVIEW.md` 中的「事件列表」章节。**

## 完整插件示例

以下是一个完整的插件示例，展示基本的开发模式：

```python
from typing import Dict, Any
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

class MyAwesomePlugin:
    def __init__(self, ctx: PluginContext, bus: EventBus, sdk: VabHubSDK):
        self.ctx = ctx
        self.bus = bus
        self.sdk = sdk
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载插件配置"""
        config_file = self.sdk.paths.data_dir / "config.json"
        if config_file.exists():
            import json
            return json.loads(config_file.read_text())
        return {"enabled": True, "debug": False}
    
    async def initialize(self):
        """初始化插件"""
        self.sdk.log.info("插件初始化中...")
        
        # 订阅感兴趣的事件
        self.bus.subscribe(EventType.MANGA_UPDATED, self.on_manga_updated, source=self.ctx.plugin_id)
        self.bus.subscribe(EventType.DOWNLOAD_COMPLETED, self.on_download_completed, source=self.ctx.plugin_id)
        
        self.sdk.log.info("插件初始化完成")
    
    async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
        """处理漫画更新事件"""
        manga_id = payload.get('manga_id')
        title = payload.get('title', '未知漫画')
        
        self.sdk.log.info(f"漫画更新: {title} (ID: {manga_id})")
        
        if self.config.get("debug"):
            await self.sdk.notify.info(f"检测到漫画更新: {title}")
    
    async def on_download_completed(self, event: EventType, payload: Dict[str, Any]):
        """处理下载完成事件"""
        status = payload.get('status', 'completed')
        
        if status == 'completed':
            self.sdk.log.info("下载任务完成")
            await self.sdk.notify.success("下载完成")
        else:
            self.sdk.log.warning(f"下载异常: {status}")

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """插件入口函数"""
    plugin = MyAwesomePlugin(ctx, bus, sdk)
    
    # 异步初始化
    import asyncio
    asyncio.create_task(plugin.initialize())