"""
Config & Dashboard Demo Plugin

这是一个演示插件配置系统和 Dashboard 面板功能的示例插件。
展示了如何：
1. 使用 config_schema 定义配置
2. 通过 sdk.config 读取配置
3. 实现 get_dashboard 提供 UI 面板
4. 实现 get_routes 暴露 API
5. 订阅和处理事件
"""

from typing import Dict, Any, List
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType
from app.plugin_sdk.types import PluginRoute

class ConfigDashboardDemo:
    def __init__(self, ctx: PluginContext, bus: EventBus, sdk: VabHubSDK):
        self.ctx = ctx
        self.bus = bus
        self.sdk = sdk
        self.processed_count = 0
        self.last_processed_time = None
        self.error_count = 0

    async def initialize(self):
        """初始化插件"""
        config = await self.sdk.config.get()
        
        if not config.get("enabled", True):
            self.sdk.log.info("插件已被禁用，跳过初始化")
            return
        
        self.sdk.log.info("Config & Dashboard Demo 插件初始化完成")
        self.sdk.log.info(f"配置: {config}")
        
        # 订阅事件
        self.bus.subscribe(EventType.MANGA_UPDATED, self.on_manga_updated, source=self.ctx.plugin_id)
        self.bus.subscribe(EventType.DOWNLOAD_COMPLETED, self.on_download_completed, source=self.ctx.plugin_id)

    async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
        """处理漫画更新事件"""
        config = await self.sdk.config.get()
        
        # 检查媒体库是否已存在
        exists = await self.sdk.media.has_manga(series_id=payload.get("series_id"))
        if exists:
            self.sdk.log.info("漫画已存在于媒体库中，跳过处理")
            return
        
        # 模拟处理逻辑
        await self._process_item("manga", payload.get("title", "未知漫画"), config)

    async def on_download_completed(self, event: EventType, payload: Dict[str, Any]):
        """处理下载完成事件"""
        config = await self.sdk.config.get()
        
        status = payload.get("status", "unknown")
        file_path = payload.get("file_path", "")
        
        if status == "completed":
            await self._process_item("download", f"文件: {file_path}", config)
        else:
            self.error_count += 1
            self.sdk.log.warning(f"下载失败: {status}")

    async def _process_item(self, item_type: str, item_name: str, config: Dict[str, Any]):
        """通用处理逻辑"""
        processing_mode = config.get("processing_mode", "balanced")
        max_items = config.get("max_items_per_batch", 10)
        enable_notifications = config.get("enable_notifications", True)
        
        # 模拟处理时间
        import asyncio
        if processing_mode == "thorough":
            await asyncio.sleep(0.1)
        elif processing_mode == "fast":
            await asyncio.sleep(0.01)
        else:  # balanced
            await asyncio.sleep(0.05)
        
        self.processed_count += 1
        self.last_processed_time = "刚刚"
        
        self.sdk.log.info(f"已处理 {item_type}: {item_name} (模式: {processing_mode})")
        
        # 发送通知
        if enable_notifications:
            await self.sdk.notify.success(f"已处理 {item_type}: {item_name}")

def get_dashboard(sdk):
    """提供 Dashboard 面板"""
    # 这里从插件实例获取统计数据，实际实现中需要存储状态
    # 为示例简化，我们使用模拟数据
    
    import datetime
    
    return {
        "widgets": [
            {
                "id": "processed_count",
                "type": "stat_card",
                "title": "已处理项目",
                "value": "42",  # 实际应该从插件状态获取
                "unit": "个",
                "description": "插件启动以来处理的总数量"
            },
            {
                "id": "error_count",
                "type": "stat_card", 
                "title": "错误次数",
                "value": "3",  # 实际应该从插件状态获取
                "unit": "次",
                "description": "处理过程中遇到的错误"
            },
            {
                "id": "status_text",
                "type": "text",
                "title": "插件状态",
                "markdown": """
### 🟢 运行状态

插件正在正常运行，所有功能正常工作。

- **上次处理**: 2 分钟前
- **处理模式**: balanced
- **配置**: 启用状态
- **权限**: media.read

> 配置修改后会自动生效，无需重启插件。
                """
            },
            {
                "id": "recent_activity",
                "type": "table",
                "title": "最近活动",
                "columns": [
                    {"key": "time", "title": "时间", "width": "120px"},
                    {"key": "type", "title": "类型", "width": "80px"},
                    {"key": "name", "title": "项目"},
                    {"key": "status", "title": "状态", "width": "80px"}
                ],
                "rows": [
                    {"time": "10:30", "type": "漫画", "name": "Sample Manga Vol.1", "status": "✅"},
                    {"time": "10:25", "type": "下载", "name": "chapter_42.zip", "status": "✅"},
                    {"time": "10:20", "type": "漫画", "name": "Another Manga", "status": "⚠️"},
                    {"time": "10:15", "type": "下载", "name": "audio_book.mp3", "status": "✅"}
                ]
            },
            {
                "id": "refresh_button",
                "type": "action_button",
                "title": "操作",
                "text": "刷新统计",
                "action": "refresh_stats",
                "description": "重新加载插件统计数据"
            }
        ]
    }

def get_routes(sdk):
    """提供对外 API 接口"""
    
    async def stats_handler(request, sdk):
        """获取插件统计信息"""
        return {
            "processed_count": 42,
            "error_count": 3,
            "last_processed": "2024-01-15T10:30:00Z",
            "uptime": "2h 15m",
            "config": {
                "enabled": True,
                "processing_mode": "balanced",
                "max_items_per_batch": 10
            }
        }
    
    async def config_handler(request, sdk):
        """获取当前配置"""
        config = await sdk.config.get()
        return {
            "config": config,
            "config_schema": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean", "title": "启用"},
                    "max_items_per_batch": {"type": "integer", "title": "批次大小"},
                    "processing_mode": {"type": "string", "title": "处理模式"}
                }
            }
        }
    
    async def health_handler(request, sdk):
        """健康检查"""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": "2024-01-15T10:35:00Z",
            "plugin_id": "demo.config_dashboard"
        }
    
    async def test_handler(request, sdk):
        """测试处理器"""
        return {
            "message": "Plugin API is working!",
            "request_method": request.method,
            "timestamp": "2024-01-15T10:35:00Z"
        }

    return [
        PluginRoute(
            path="stats",
            method="GET",
            summary="获取插件统计信息",
            handler=stats_handler
        ),
        PluginRoute(
            path="config",
            method="GET", 
            summary="获取当前配置",
            handler=config_handler
        ),
        PluginRoute(
            path="health",
            method="GET",
            summary="健康检查",
            handler=health_handler
        ),
        PluginRoute(
            path="test",
            method="GET",
            summary="测试接口",
            handler=test_handler
        )
    ]

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """插件入口函数"""
    plugin = ConfigDashboardDemo(ctx, bus, sdk)
    
    # 异步初始化
    import asyncio
    asyncio.create_task(plugin.initialize())
    
    # 将插件实例保存到上下文中，供 dashboard 和 routes 使用
    ctx.set_plugin_instance(plugin)