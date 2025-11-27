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

## 宿主服务与 sdk_permissions（可选高级功能）

### 权限声明基础

插件默认只可用：日志、HTTP、通知、事件订阅等"安全能力"；

想调用「下载 / 媒体库 / 115」等高权限操作，需要在 `plugin.json` 的 `sdk_permissions` 里显式声明：

```json
{
  "id": "my_awesome_plugin",
  "name": "My Awesome Plugin",
  "version": "1.0.0",
  "sdk_permissions": [
    "media.read",
    "download.write"
  ],
  "channel": "community",
  "repo_url": "https://github.com/myname/awesome-plugin",
  "author_name": "My Name",
  "author_url": "https://github.com/myname"
}
```

**重要提醒**：不声明就调用高权限方法，会在日志中看到拒绝，并收到明确错误。推荐插件作者只申请真正用得到的权限。

### 宿主服务概览（摘要级）

#### 下载服务：sdk.download

**核心方法**：
- `sdk.download.add_task(url: str) -> task_id`：创建下载任务
- `sdk.download.get_task(task_id) -> TaskInfo`：获取任务详情
- `sdk.download.list_tasks() -> List[TaskInfo]`：列出所有任务

**示例用途**：插件检测到新资源后，触发一个下载任务。

**需要权限**：
- `download.write`：用于 `add_task`
- `download.read`：用于 `get_task` 和 `list_tasks`

#### 媒体库查询：sdk.media

**核心方法**：
- `sdk.media.has_movie(...)`：检查电影是否存在
- `sdk.media.has_tv(...)`：检查剧集是否存在
- `sdk.media.has_audiobook(...)`：检查有声书是否存在
- `sdk.media.has_manga(...)`：检查漫画是否存在
- `sdk.media.search_media(...)`：根据关键字在媒体库中搜索

**示例用途**：用于"避免重复下载 / 入库"的检查。

**需要权限**：`media.read`

#### 115 集成：sdk.cloud115

**核心方法**：
- `sdk.cloud115.is_available() -> bool`：检查主系统是否配置了 115
- `sdk.cloud115.add_offline_task(url: str) -> task_id`：创建 115 离线任务
- `sdk.cloud115.list_dir(path: str) -> List[FileInfo]`：列出目录内容
- `sdk.cloud115.get_storage_info() -> StorageInfo`：获取存储空间信息

**示例用途**：配合 VabHub 的 115 云存储功能，自动离线下载或管理文件。

**需要权限**：
- `cloud115.task`：用于 `add_offline_task`
- `cloud115.read`：用于 `list_dir` 和 `get_storage_info`

> **注意**：更详细的参数 & 返回值，请参见主仓库 `PLUGIN_SDK_OVERVIEW.md` 中的「宿主服务封装」章节。

### 综合示例

以下是一个结合了宿主服务的示例插件逻辑：

```python
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

async def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    sdk.log.info("My auto-download plugin loaded")

    async def on_manga_updated(event: EventType, payload: dict) -> None:
        # 1. 检查媒体库是否已存在
        exists = await sdk.media.has_manga(series_id=payload.get("series_id"))
        if exists:
            sdk.log.info("Manga already in library, skip download.")
            return

        # 2. 若不存在，发起一个下载任务（具体资源 URL 由插件逻辑决定）
        url = payload.get("download_url")
        if not url:
            sdk.log.warning("No download_url in payload, skip.")
            return

        task_id = await sdk.download.add_task(url)
        sdk.log.info(f"Created download task: {task_id}")

    bus.subscribe(EventType.MANGA_UPDATED, on_manga_updated, source=ctx.plugin_id)
```

**重要**：这个示例需要在 `plugin.json` 中声明：
```json
"sdk_permissions": ["media.read", "download.write"]
```

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