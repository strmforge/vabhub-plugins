# VabHub 插件开发指南

本文档面向准备为 VabHub 编写插件的开发者，提供从项目创建到插件发布的完整开发流程。

## 适用对象

- 熟悉 Python 编程的开发者
- 了解 Git/GitHub 基础操作
- 希望为 VabHub 生态贡献功能的用户

## 前置条件

- Python 3.8+ 开发环境
- Git 和 GitHub 账户
- 熟悉 VabHub 基本功能和插件概念

## 项目创建方式

### 方式一：自建插件 Hub（推荐）

适合需要维护多个插件的开发者或团队：

1. **创建 Hub 仓库**
   ```bash
   # 在 GitHub 上创建新仓库，如 myname/vabhub-plugins
   git clone https://github.com/myname/vabhub-plugins.git
   cd vabhub-plugins
   ```

2. **创建 plugins.json**
   参考 [PLUGIN_INDEX_SPEC](PLUGIN_INDEX_SPEC.md) 规范创建索引文件：
   ```json
   {
     "hub_name": "My Plugin Hub",
     "hub_version": 1,
     "plugins": []
   }
   ```

3. **添加插件到索引**
   开发完插件后，将插件信息添加到 `plugins.json` 中。

### 方式二：单插件仓库

适合只开发单个插件的开发者：

1. **创建插件仓库**
   ```bash
   # 创建插件仓库，如 myname/awesome-plugin
   ```

2. **申请加入官方 Hub**
   通过 PR 将插件添加到官方 Hub 的 `plugins.json` 中。

## 插件目录结构

推荐的标准目录结构：

```
my-awesome-plugin/
├── README.md              # 插件说明文档
├── pyproject.toml         # Python 包配置
├── plugin.json            # 插件元数据（可选，未来可能需要）
├── my_awesome_plugin/
│   ├── __init__.py
│   └── plugin.py          # 主要插件逻辑
└── tests/                 # 测试文件（可选）
    └── test_plugin.py
```

### 核心文件说明

- **my_awesome_plugin/plugin.py**: 包含 `setup_plugin` 函数的主逻辑文件
- **README.md**: 插件功能、安装、使用说明
- **pyproject.toml**: Python 包的元数据和依赖配置

## 插件入口函数

### setup_plugin 函数签名

```python
def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """
    插件初始化函数，在插件加载时被主程序调用
    
    Args:
        ctx: 插件上下文，提供环境信息
        bus: 事件总线，用于事件订阅/发布
        sdk: 插件 API 接口，提供各种功能调用
    """
    pass
```

### 参数说明

#### PluginContext
提供插件的运行环境信息：
```python
# 示例用法
plugin_id = ctx.plugin_id          # 插件 ID
plugin_version = ctx.version      # 插件版本
config = ctx.get_config()         # 插件配置
data_dir = ctx.data_directory     # 插件数据目录
```

#### EventBus
事件总线用于系统事件通信：
```python
# 订阅事件
async def on_manga_updated(event, payload):
    sdk.log.info(f"漫画更新: {payload}")

bus.subscribe(EventType.MANGA_UPDATED, on_manga_updated)

# 发布事件
bus.publish(EventType.CUSTOM_EVENT, {"data": "my_data"})
```

#### VabHubSDK
插件 API 接口，提供各种功能：
```python
# 日志记录
sdk.log.info("插件启动")
sdk.log.error("发生错误")

# HTTP 客户端
response = await sdk.http.get("https://api.example.com")

# 数据库访问（如果支持）
results = await sdk.db.query("SELECT * FROM table")

# UI 相关（如果支持）
sdk.ui.show_notification("通知消息")
```

## 完整插件示例

以下是一个功能完整的插件示例：

```python
# my_awesome_plugin/plugin.py
from typing import Dict, Any
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

class MyAwesomePlugin:
    def __init__(self, ctx: PluginContext, bus: EventBus, sdk: VabHubSDK):
        self.ctx = ctx
        self.bus = bus
        self.sdk = sdk
        self.config = ctx.get_config()
        
    async def initialize(self):
        """插件初始化"""
        self.sdk.log.info("我的超棒插件初始化中...")
        
        # 订阅感兴趣的事件
        self.bus.subscribe(EventType.MANGA_UPDATED, self.on_manga_updated)
        self.bus.subscribe(EventType.DOWNLOAD_COMPLETED, self.on_download_completed)
        
        # 可以在这里执行初始化任务
        await self.setup_periodic_tasks()
    
    async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
        """处理漫画更新事件"""
        manga_id = payload.get('manga_id')
        title = payload.get('title')
        self.sdk.log.info(f"检测到漫画更新: {title} (ID: {manga_id})")
        
        # 自定义处理逻辑
        await self.process_manga_update(payload)
    
    async def on_download_completed(self, event: EventType, payload: Dict[str, Any]):
        """处理下载完成事件"""
        self.sdk.log.info("下载任务完成")
        
        # 可以在这里执行后处理，如通知、统计等
        await self.send_notification(payload)
    
    async def process_manga_update(self, manga_data: Dict[str, Any]):
        """处理漫画更新数据"""
        # 自定义业务逻辑
        pass
    
    async def send_notification(self, data: Dict[str, Any]):
        """发送通知"""
        if self.config.get('enable_notifications', False):
            message = f"任务完成: {data.get('title', '未知')}"
            # 使用 SDK 发送通知（如果支持）
            # sdk.ui.show_notification(message)
            self.sdk.log.info(f"通知已发送: {message}")
    
    async def setup_periodic_tasks(self):
        """设置定期任务"""
        # 示例：设置定期检查任务
        pass

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """插件入口函数"""
    plugin = MyAwesomePlugin(ctx, bus, sdk)
    
    # 异步初始化插件
    import asyncio
    asyncio.create_task(plugin.initialize())
    
    # 将插件实例保存到上下文中（如果需要）
    ctx.set_plugin_instance(plugin)
```

## 在官方 Hub 中登记插件

### 插件信息准备

在将插件添加到官方 Hub 之前，确保具备以下信息：

- **仓库地址**: 插件源码仓库的 URL
- **插件信息**: 名称、描述、版本、作者等
- **功能特性**: 支持的功能类型（search, bot_commands, ui_panels 等）

### plugins.json 条目示例

```json
{
  "id": "myname-awesome-plugin",
  "name": "My Awesome Plugin",
  "summary": "一个很棒的插件，提供XXX功能",
  "description": "详细描述插件的功能、特性和使用方法...",
  "version": "1.0.0",
  "repo_url": "https://github.com/myname/awesome-plugin",
  "author_name": "Your Name",
  "author_url": "https://github.com/myname",
  "channel": "community",
  "tags": ["utility", "example"],
  "features": ["ui_panels", "search"],
  "homepage": "https://github.com/myname/awesome-plugin",
  "readme_url": "https://raw.githubusercontent.com/myname/awesome-plugin/main/README.md",
  "extra": {
    "min_core_version": "1.0.0",
    "enabled_by_default": false,
    "supports": {
      "search": true,
      "bot_commands": false,
      "ui_panels": true,
      "workflows": false
    }
  }
}
```

### 提交到官方 Hub

1. **Fork 官方仓库**: `strmforge/vabhub-plugins`
2. **创建分支**: 如 `add-my-awesome-plugin`
3. **修改 plugins.json**: 添加你的插件条目
4. **提交 PR**: 确保通过所有 CI 检查
5. **等待审核**: 维护者会审核并合并你的 PR

## 最佳实践

### 代码质量

- **异常处理**: 使用 try-except 处理可能出现的异常
- **日志记录**: 使用 `sdk.log` 记录重要操作和错误
- **性能优化**: 避免阻塞操作，合理使用异步编程

### 事件处理

- **只订阅必要事件**: 避免订阅过多不相关的事件
- **轻量处理**: 事件处理函数应该快速执行，避免阻塞
- **错误隔离**: 事件处理中的异常不应影响其他插件

### 配置管理

- **提供默认值**: 为所有配置项提供合理的默认值
- **配置验证**: 验证用户输入的配置是否有效
- **配置文档**: 在 README 中详细说明配置选项

## 常见问题

### Q: 如何调试插件？
A: 使用 `sdk.log` 记录调试信息，查看主程序的日志文件。开发时可以启用更详细的日志级别。

### Q: 插件如何持久化数据？
A: 可以通过 `ctx.data_directory` 获取插件专用的数据目录，用于存储持久化数据。

### Q: 如何与其他插件交互？
A: 通过事件总线 `bus.publish` 发布自定义事件，其他插件可以订阅这些事件进行交互。

### Q: 插件可以访问文件系统吗？
A: 插件只能访问指定的数据目录，不能访问系统其他文件，这是出于安全考虑。

## 进阶开发

### 自定义事件类型

插件可以定义和使用自己的事件类型：

```python
# 发布自定义事件
bus.publish("my_custom_event", {"data": "custom_data"})

# 其他插件可以订阅
bus.subscribe("my_custom_event, handler_function)
```

### 插件间通信

通过事件总线实现插件间的松耦合通信：

```python
# 插件 A：发布状态更新
bus.publish("plugin_a_status", {"status": "ready", "data": {...}})

# 插件 B：监听状态变化
async def on_plugin_a_status(event, payload):
    if payload["status"] == "ready":
        sdk.log.info("插件 A 已就绪，可以开始协作")
```

### 依赖管理

在 `pyproject.toml` 中声明依赖：

```toml
[project]
name = "my-awesome-plugin"
version = "1.0.0"
dependencies = [
    "requests>=2.25.0",
    "aiohttp>=3.8.0"
]
```

## 发布和维护

### 版本管理

- 遵循语义化版本规则（Semantic Versioning）
- 在更新插件时同步更新 `plugins.json` 中的版本号
- 保持向后兼容性，重大变更需要升级主版本号

### 测试

- 编写单元测试覆盖核心功能
- 测试与主程序的集成
- 验证事件处理的正确性

### 文档维护

- 及时更新 README.md 中的功能说明
- 记录配置变更和新功能
- 提供使用示例和故障排除指南

## 获取帮助

- **文档**: [PLUGIN_INDEX_SPEC](PLUGIN_INDEX_SPEC.md) 了解插件索引规范
- **主仓库文档**: `docs/PLUGIN_SDK_OVERVIEW.md` 了解完整的 SDK API
- **GitHub Issues**: 在官方仓库提交问题或建议
- **社区**: 参与社区讨论，分享开发经验

通过本指南，你应该能够开始开发自己的 VabHub 插件了。欢迎为 VabHub 生态贡献力量！