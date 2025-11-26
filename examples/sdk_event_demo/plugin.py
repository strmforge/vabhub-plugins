from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    sdk.log.info("sdk_event_demo plugin loaded")

    async def on_manga_updated(event: EventType, payload: dict) -> None:
        sdk.log.info(f"[sdk_event_demo] Manga updated: {payload}")

    bus.subscribe(EventType.MANGA_UPDATED, on_manga_updated, source=ctx.plugin_id)