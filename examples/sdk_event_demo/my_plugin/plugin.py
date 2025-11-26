"""
VabHub SDK Event Demo Plugin - 插件主逻辑

这个文件演示了如何使用 VabHub 插件 SDK：
1. 使用 setup_plugin 函数作为插件入口
2. 订阅系统事件
3. 使用 SDK 提供的各种功能
4. 实现自定义业务逻辑
"""

from typing import Dict, Any
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType


class SDKEventDemo:
    """
    插件主类，演示 SDK 和事件系统的使用
    """
    
    def __init__(self, ctx: PluginContext, bus: EventBus, sdk: VabHubSDK):
        self.ctx = ctx
        self.bus = bus
        self.sdk = sdk
        self.config = ctx.get_config()
        
        # 记录插件加载
        self.sdk.log.info("SDK Event Demo 插件实例已创建")
        self.sdk.log.info(f"插件 ID: {ctx.plugin_id}")
        self.sdk.log.info(f"插件版本: {ctx.version}")
        
    async def initialize(self):
        """
        插件初始化函数
        订阅感兴趣的事件并执行初始化逻辑
        """
        self.sdk.log.info("SDK Event Demo 插件开始初始化...")
        
        # 订阅各种事件
        await self._setup_event_subscriptions()
        
        # 执行初始化任务
        await self._perform_initialization()
        
        self.sdk.log.info("SDK Event Demo 插件初始化完成")
    
    async def _setup_event_subscriptions(self):
        """设置事件订阅"""
        
        # 订阅漫画更新事件
        self.bus.subscribe(EventType.MANGA_UPDATED, self.on_manga_updated)
        self.sdk.log.info("已订阅漫画更新事件")
        
        # 订阅下载完成事件
        self.bus.subscribe(EventType.DOWNLOAD_COMPLETED, self.on_download_completed)
        self.sdk.log.info("已订阅下载完成事件")
        
        # 订阅自定义事件（如果支持）
        if hasattr(EventType, 'USER_LOGIN'):
            self.bus.subscribe(EventType.USER_LOGIN, self.on_user_login)
            self.sdk.log.info("已订阅用户登录事件")
    
    async def _perform_initialization(self):
        """执行初始化任务"""
        
        # 获取插件配置
        debug_mode = self.config.get('debug', False)
        notification_enabled = self.config.get('notifications', True)
        
        self.sdk.log.info(f"调试模式: {debug_mode}")
        self.sdk.log.info(f"通知功能: {'启用' if notification_enabled else '禁用'}")
        
        # 获取数据目录
        data_dir = self.ctx.data_directory
        self.sdk.log.info(f"插件数据目录: {data_dir}")
        
        # 可以在这里执行其他初始化任务
        # 例如：创建配置文件、建立数据库连接等
        
        if debug_mode:
            # 发布一个自定义事件，演示事件发布功能
            await self._publish_demo_event()
    
    async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
        """
        处理漫画更新事件
        
        Args:
            event: 事件类型
            payload: 事件数据，包含漫画相关信息
        """
        self.sdk.log.info(f"收到漫画更新事件: {event}")
        self.sdk.log.info(f"事件数据: {payload}")
        
        # 提取关键信息
        manga_id = payload.get('manga_id')
        title = payload.get('title', '未知漫画')
        chapter_count = payload.get('chapter_count', 0)
        
        self.sdk.log.info(f"漫画 '{title}' (ID: {manga_id}) 已更新，章节数: {chapter_count}")
        
        # 执行自定义业务逻辑
        await self._process_manga_update(payload)
    
    async def on_download_completed(self, event: EventType, payload: Dict[str, Any]):
        """
        处理下载完成事件
        
        Args:
            event: 事件类型
            payload: 事件数据，包含下载相关信息
        """
        self.sdk.log.info(f"收到下载完成事件: {event}")
        
        # 提取下载信息
        download_id = payload.get('download_id')
        status = payload.get('status', 'completed')
        file_path = payload.get('file_path')
        
        self.sdk.log.info(f"下载任务 {download_id} 状态: {status}")
        
        if file_path:
            self.sdk.log.info(f"文件保存路径: {file_path}")
        
        # 执行下载后处理
        await self._process_download_completion(payload)
    
    async def on_user_login(self, event: EventType, payload: Dict[str, Any]):
        """
        处理用户登录事件（如果支持）
        
        Args:
            event: 事件类型
            payload: 事件数据，包含用户信息
        """
        self.sdk.log.info(f"收到用户登录事件: {event}")
        
        user_id = payload.get('user_id')
        username = payload.get('username', '未知用户')
        
        self.sdk.log.info(f"用户 {username} (ID: {user_id}) 已登录")
        
        # 可以在这里执行用户相关的初始化逻辑
        await self._welcome_user(username)
    
    async def _process_manga_update(self, manga_data: Dict[str, Any]):
        """处理漫画更新数据的业务逻辑"""
        
        # 示例：检查是否需要发送通知
        if self.config.get('notifications', True):
            title = manga_data.get('title', '未知漫画')
            self.sdk.log.info(f"准备发送漫画更新通知: {title}")
            # 实际的通知发送逻辑会在这里实现
        
        # 示例：更新本地缓存
        # await self._update_local_cache(manga_data)
        
        # 示例：触发相关检查
        # await self._run_manga_checks(manga_data)
    
    async def _process_download_completion(self, download_data: Dict[str, Any]):
        """处理下载完成数据的业务逻辑"""
        
        status = download_data.get('status', 'completed')
        
        if status == 'completed':
            self.sdk.log.info("下载任务成功完成")
            # 可以执行后处理，如文件整理、质量检查等
        else:
            self.sdk.log.warning(f"下载任务异常结束，状态: {status}")
    
    async def _welcome_user(self, username: str):
        """向用户发送欢迎消息"""
        self.sdk.log.info(f"欢迎 {username} 使用 VabHub！")
        
        # 如果 SDK 支持 UI 功能，可以显示欢迎通知
        # await self.sdk.ui.show_notification(f"欢迎回来，{username}！")
    
    async def _publish_demo_event(self):
        """发布演示事件（调试用）"""
        try:
            # 发布自定义事件，演示事件发布功能
            demo_payload = {
                'plugin_id': self.ctx.plugin_id,
                'message': 'SDK Event Demo 插件初始化完成',
                'timestamp': 'demo-timestamp',
                'debug_info': {
                    'python_version': '3.x',
                    'sdk_version': 'unknown'
                }
            }
            
            # 发布到自定义事件类型
            self.bus.publish('demo_plugin_initialized', demo_payload)
            self.sdk.log.info("已发布插件初始化演示事件")
            
        except Exception as e:
            self.sdk.log.error(f"发布演示事件失败: {e}")


def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """
    插件入口函数
    
    这是 VabHub 主程序在加载插件时调用的函数。
    在这里创建插件实例并进行初始化。
    
    Args:
        ctx: 插件上下文，提供环境信息
        bus: 事件总线，用于事件订阅和发布
        sdk: 插件 API 接口，提供各种功能调用
    """
    sdk.log.info("SDK Event Demo 插件开始加载...")
    sdk.log.info("这是一个演示 VabHub 插件 SDK 和事件系统使用的示例插件")
    
    # 创建插件实例
    plugin = SDKEventDemo(ctx, bus, sdk)
    
    # 异步初始化插件
    import asyncio
    
    async def async_init():
        try:
            await plugin.initialize()
            sdk.log.info("SDK Event Demo 插件加载并初始化完成")
        except Exception as e:
            sdk.log.error(f"插件初始化失败: {e}")
            raise
    
    # 创建异步任务但不等待，让插件在后台初始化
    asyncio.create_task(async_init())
    
    # 将插件实例保存到上下文中，方便后续使用
    ctx.set_plugin_instance(plugin)
    
    sdk.log.info("SDK Event Demo 插件加载函数执行完成")