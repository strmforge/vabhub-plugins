# VabHub SDK Event Demo Plugin

这是一个完整的 VabHub 插件开发示例，演示了如何使用 VabHub 插件 SDK 和事件系统。

## 📋 功能演示

本示例插件演示了以下核心功能：

### ✨ 插件生命周期
- 使用 `setup_plugin(ctx, bus, sdk)` 作为插件入口
- 异步初始化和错误处理
- 插件实例管理

### 🔄 事件系统使用
- 订阅系统事件（漫画更新、下载完成等）
- 事件处理和数据提取
- 自定义事件发布

### 🛠 SDK 功能
- 日志记录（info、warning、error）
- 插件配置访问
- 数据目录管理
- 上下文信息获取

## 📁 目录结构

```
sdk_event_demo/
├── my_plugin/
│   ├── __init__.py        # 包初始化文件
│   └── plugin.py          # 主要插件逻辑
└── README.md              # 本说明文件
```

## 🚀 快速开始

### 1. 复制到你的插件项目

将 `sdk_event_demo/` 目录复制为你的新插件项目：

```bash
# 复制示例目录
cp -r sdk_event_demo my_awesome_plugin

# 进入新项目目录
cd my_awesome_plugin

# 重命名包目录
mv my_plugin my_awesome_plugin
```

### 2. 修改基础信息

编辑 `my_awesome_plugin/__init__.py`：

```python
__version__ = "1.0.0"
__author__ = "你的名字"
```

### 3. 自定义插件逻辑

编辑 `my_awesome_plugin/plugin.py`：

- 修改类名：`SDKEventDemo` → `MyAwesomePlugin`
- 更新日志消息和文档
- 根据需要添加或修改事件处理逻辑
- 实现你的自定义业务逻辑

### 4. 添加配置文件（可选）

创建 `pyproject.toml`：

```toml
[project]
name = "my-awesome-plugin"
version = "1.0.0"
description = "我的超棒 VabHub 插件"
authors = [
    {name = "你的名字", email = "your.email@example.com"}
]
dependencies = []

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

## 📖 核心代码解析

### 插件入口函数

```python
def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """插件入口函数"""
    plugin = SDKEventDemo(ctx, bus, sdk)
    
    import asyncio
    asyncio.create_task(plugin.initialize())
    
    ctx.set_plugin_instance(plugin)
```

### 事件订阅示例

```python
async def _setup_event_subscriptions(self):
    """设置事件订阅"""
    
    # 订阅漫画更新事件
    self.bus.subscribe(EventType.MANGA_UPDATED, self.on_manga_updated)
    
    # 订阅下载完成事件
    self.bus.subscribe(EventType.DOWNLOAD_COMPLETED, self.on_download_completed)
```

### 事件处理示例

```python
async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
    """处理漫画更新事件"""
    manga_id = payload.get('manga_id')
    title = payload.get('title', '未知漫画')
    
    self.sdk.log.info(f"漫画 '{title}' (ID: {manga_id}) 已更新")
    
    # 执行自定义业务逻辑
    await self._process_manga_update(payload)
```

### SDK 使用示例

```python
# 日志记录
self.sdk.log.info("插件启动")
self.sdk.log.error("发生错误")

# 配置访问
debug_mode = self.config.get('debug', False)

# 上下文信息
plugin_id = self.ctx.plugin_id
data_dir = self.ctx.data_directory
```

## 🔧 自定义开发指南

### 添加新的事件处理

1. 在 `_setup_event_subscriptions()` 中添加订阅：
```python
self.bus.subscribe(EventType.YOUR_EVENT, self.on_your_event)
```

2. 实现处理函数：
```python
async def on_your_event(self, event: EventType, payload: Dict[str, Any]):
    """处理你的自定义事件"""
    self.sdk.log.info(f"收到事件: {event}")
    # 你的处理逻辑
```

### 发布自定义事件

```python
# 发布自定义事件
custom_payload = {
    'data': 'your_data',
    'timestamp': 'current_time'
}
self.bus.publish('your_custom_event', custom_payload)
```

### 使用 HTTP 客户端

```python
# 发送 HTTP 请求（如果 SDK 支持）
response = await self.sdk.http.get("https://api.example.com/data")
data = response.json()
```

### 数据持久化

```python
# 使用数据目录保存文件
import json
import os

data_file = os.path.join(self.ctx.data_directory, 'my_data.json')
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 📚 相关文档

- [插件开发指南](../../docs/PLUGIN_DEV_GUIDE.md) - 完整的开发流程和最佳实践
- [插件索引规范](../../docs/PLUGIN_INDEX_SPEC.md) - plugins.json 格式规范
- [SDK API 参考](../../docs/PLUGIN_SDK_OVERVIEW.md) - 完整的 SDK API 文档（主仓库）

## 🤝 贡献指南

如果你对示例插件有改进建议，或者发现了问题：

1. 提交 Issue 描述问题或建议
2. 提交 Pull Request 贡献代码
3. 在讨论中分享你的使用经验

## 📝 许可证

本示例插件遵循 MIT 许可证，可以自由使用和修改。

---

**提示**：这个示例插件主要用于学习和开发参考。在实际部署时，请根据具体需求修改和优化代码。