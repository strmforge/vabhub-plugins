# Config & Dashboard Demo Plugin

这是一个完整的示例插件，展示了 VabHub 插件系统的高级功能：

- **插件配置系统**：通过 `config_schema` 自动生成 Web 表单
- **Dashboard 面板**：通过 `get_dashboard` 提供丰富的 UI 组件
- **对外 API**：通过 `get_routes` 暴露自定义 HTTP 接口
- **事件处理**：结合配置处理系统事件

## 功能特性

### 1. 配置系统

插件通过 `config_schema` 定义了完整的配置表单：

```json
{
  "config_schema": {
    "type": "object", 
    "properties": {
      "enabled": {"type": "boolean", "title": "启用插件"},
      "max_items_per_batch": {
        "type": "integer",
        "title": "每批最大处理数量",
        "minimum": 1,
        "maximum": 100
      },
      "processing_mode": {
        "type": "string",
        "title": "处理模式",
        "enum": ["fast", "balanced", "thorough"]
      }
    }
  }
}
```

**在 VabHub UI 中的效果**：
- 自动渲染配置表单
- 支持各种输入类型（文本、数字、布尔、下拉选择）
- 实时验证和默认值
- 配置变更后插件自动重载

### 2. Dashboard 面板

通过 `get_dashboard()` 提供多种 UI 组件：

```python
def get_dashboard(sdk):
    return {
        "widgets": [
            {
                "type": "stat_card",
                "title": "已处理项目",
                "value": "42",
                "unit": "个"
            },
            {
                "type": "table",
                "title": "最近活动",
                "columns": [...],
                "rows": [...]
            },
            {
                "type": "action_button",
                "title": "操作",
                "text": "刷新统计",
                "action": "refresh_stats"
            }
        ]
    }
```

**支持的组件类型**：
- `stat_card`：统计卡片，显示数值和单位
- `text`：文本/Markdown 内容
- `table`：数据表格，支持自定义列
- `action_button`：操作按钮，可触发特定动作

### 3. 对外 API

通过 `get_routes()` 暴露 REST API：

```python
def get_routes(sdk):
    return [
        PluginRoute(path="stats", method="GET", handler=stats_handler),
        PluginRoute(path="config", method="GET", handler=config_handler),
        PluginRoute(path="health", method="GET", handler=health_handler)
    ]
```

**API 访问地址**：
- `GET /api/plugin/demo.config_dashboard/stats` - 获取统计信息
- `GET /api/plugin/demo.config_dashboard/config` - 获取配置信息
- `GET /api/plugin/demo.config_dashboard/health` - 健康检查

### 4. 事件处理

结合配置和权限处理系统事件：

```python
async def on_manga_updated(self, event: EventType, payload: Dict[str, Any]):
    config = await self.sdk.config.get()
    
    # 检查媒体库
    exists = await self.sdk.media.has_manga(series_id=payload.get("series_id"))
    
    # 根据配置处理
    processing_mode = config.get("processing_mode", "balanced")
    await self._process_item("manga", title, config)
```

## 在 VabHub UI 中的效果

### 配置页面

用户可以在 VabHub 的插件管理页面看到：
- 自动生成的配置表单
- 实时验证和提示
- 保存后立即生效

### Dashboard 页面

插件专用的 Dashboard 面板显示：
- 📊 实时统计卡片
- 📋 最近活动表格
- 📝 状态信息和 Markdown 文本
- 🔘 操作按钮

### API 访问

管理员可以通过以下方式访问插件 API：
```bash
# 获取插件统计
curl -H "Authorization: Bearer <token>" \
     https://your-vabhub.com/api/plugin/demo.config_dashboard/stats

# 健康检查
curl https://your-vabhub.com/api/plugin/demo.config_dashboard/health
```

## 开发要点

### 1. 配置读取

```python
config = await sdk.config.get()
if not config.get("enabled", True):
    sdk.log.info("插件已禁用")
    return
```

### 2. Dashboard 数据更新

Dashboard 组件的数据是动态获取的，每次页面刷新都会调用 `get_dashboard()`。

### 3. API 安全

- 所有插件 API 默认需要管理员权限
- 建议不要在插件内部实现鉴权逻辑
- API 调用会被记录审计日志

### 4. 错误处理

```python
try:
    # 业务逻辑
    await process_item(payload)
except Exception as e:
    sdk.log.error(f"处理失败: {e}")
    # 可选择发送通知
    await sdk.notify.error("处理失败", str(e))
```

## 学习建议

1. **先理解基础**：熟悉 `sdk_event_demo` 示例中的事件处理
2. **添加配置**：在插件中添加 `config_schema` 并使用 `sdk.config`
3. **创建 Dashboard**：实现 `get_dashboard()` 提供可视化界面
4. **暴露 API**：通过 `get_routes()` 提供外部接口
5. **权限声明**：在 `plugin.json` 中正确声明 `sdk_permissions`

## 扩展方向

基于这个示例，你可以：

- 添加更多配置选项（API 密钥、服务地址等）
- 实现 Dashboard 的交互功能（按钮点击后执行操作）
- 提供更丰富的 API（CRUD 操作、文件上传等）
- 集成第三方服务（AI 处理、云存储等）
- 添加更多 Dashboard 组件（图表、进度条等）

## 相关文档

- [插件开发指南](../../docs/PLUGIN_DEV_GUIDE.md) - 详细的开发说明
- [插件索引规范](../../docs/PLUGIN_INDEX_SPEC.md) - 完整的字段定义
- [基础示例](../sdk_event_demo/) - 简单的事件处理示例

---

这个示例展示了 VabHub 插件系统的强大能力，为开发功能丰富的插件提供了完整的参考。