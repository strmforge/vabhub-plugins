# VabHub Plugins（官方插件 Hub & 规范中心）

这是 VabHub 官方插件 Hub（Official Plugin Hub）和插件索引规范中心，具备双重身份：

- **VabHub 官方插件 Hub**：维护官方和强关联插件的核心索引
- **插件 Hub 规范与示例**：提供 `plugins.json` 协议和完整示例，供第三方开发者自建插件 Hub

> **重要说明**：本仓库不再承担"所有社区插件索引"的维护工作。我们鼓励第三方开发者根据本仓库提供的规范创建独立的插件 Hub 仓库。VabHub 主程序支持从多个插件 Hub 拉取数据，本仓库只是其中的官方源之一。

## 什么是插件 Hub？

插件 Hub 是一个包含插件索引信息的 Git 仓库，具备以下特征：

- **结构简单**：根目录包含一个遵守 `PLUGIN_INDEX_SPEC` 规范的 `plugins.json` 文件
- **独立维护**：一个 Hub 可以列出一个或多个相关插件
- **灵活配置**：VabHub 主程序可以配置多个 Hub URL，将它们的 `plugins.json` 数据聚合成统一的插件市场视图

### 典型工作流程

```
第三方开发者 → 创建自己的 GitHub 仓库 → 放入 plugins.json → VabHub 主程序读取 → 合并到插件市场
```

VabHub 主程序只需要你的 `plugins.json` 的 URL（通常通过 GitHub Pages 或 Raw URL 访问），即可将你的插件列表集成到官方插件市场中。

## 数据结构总览

`plugins.json` 的顶层结构如下：

```json
{
  "hub_name": "VabHub Official Plugin Hub",
  "hub_version": 1,
  "plugins": [
    {
      "id": "example-plugin",
      "name": "Example Plugin",
      "version": "0.1.0",
      "repo_url": "https://github.com/...",
      "author_name": "Someone",
      "author_url": "https://github.com/someone",
      "channel": "community"
    }
  ]
}
```

- **hub_name**: Hub 的名称标识
- **hub_version**: 索引协议版本号（当前为 1）
- **plugins**: 插件条目数组，每个元素是一个 Plugin Entry

## 字段说明（简版）

本规范既适用于官方 Hub（本仓库），也适用于第三方自建 Hub。VabHub 主程序只要看到一个兼容的 `plugins.json`，就能把其中的插件合并到市场视图。

每个插件条目（Plugin Entry）包含以下字段：

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| **id** | string | 插件唯一 ID（字符串，建议使用 namespace-name 格式） | ✅ |
| **name** | string | 插件展示名称 | ✅ |
| **summary** | string | 简短摘要，出现在插件卡片上作为副标题 | ✅ |
| **description** | string | 更长的描述文字（可选） | 可选 |
| **version** | string | 当前版本号，字符串格式，遵循语义化版本 | ✅ |
| **repo_url** | string | 插件代码或说明仓库地址（HTTP(S) URL） | ✅ |
| **author_name** | string | 作者/维护者名称 | ✅ |
| **author_url** | string | 作者主页链接（GitHub 用户/组织页等） | ✅ |
| **channel** | string | 插件频道，`"official"` 或 `"community"` | ✅ |
| **tags** | string[] | 标签数组，用于分类和搜索 | 可选 |
| **homepage** | string | 插件主页 URL | 可选 |
| **readme_url** | string | 插件文档链接 | 可选 |
| **extra** | object | 额外的自定义信息（JSON 对象） | 可选 |
| **features** | string[] | 功能特性数组（如：["search", "bot_commands"]） | 可选 |

## 官方插件 vs 社区插件

### channel: "official"
- 插件由 VabHub 官方维护
- 通常仓库在官方组织（例如 strmforge）
- 升级策略、兼容性会尽量保持稳定
- 官方对插件质量和安全性负责

### channel: "community"
- 插件由第三方开发者维护
- 仓库不在官方组织下
- 官方仅在 Plugin Hub 中展示索引，不审查代码，不对行为负责
- 用户自行评估风险并决定是否安装

> 在 VabHub 主程序侧，管理员可以通过配置开关控制是否展示/允许一键安装社区插件。

## 第三方插件 Hub 指南（Quick Start）

如果你是第三方插件作者，我们建议你创建自己的插件 Hub 仓库：

### 步骤概览

1. **创建 GitHub 仓库**
   - 仓库名称可以自由选择，如 `yourname/vabhub-plugins` 或 `yourname/my-plugins`
   - 仓库公开访问即可，无需特殊配置

2. **创建 plugins.json**
   - 在仓库根目录创建 `plugins.json` 文件
   - 结构与本仓库完全一致（可参考下面的最小示例）

3. **填写插件信息**
   - 为每个插件填写至少这些必填字段：
     - `id`, `name`, `summary`, `version`, `repo_url`, `author_name`, `author_url`, `channel`（一般为 `"community"`）
   - 推荐添加 `tags`, `features` 等字段以便用户发现

4. **配置到 VabHub**
   - 未来 VabHub 主程序会支持通过配置添加你的 Hub URL
   - URL 格式：`https://raw.githubusercontent.com/yourname/your-repo/main/plugins.json`
   - 主程序将自动从多个 Hub 拉取数据并在 UI 中显示"来自某某 Hub"的标签

### 最小示例

```json
{
  "hub_name": "My Plugin Hub",
  "hub_version": 1,
  "plugins": [
    {
      "id": "myname-awesome-plugin",
      "name": "Awesome Plugin",
      "summary": "一个很棒的插件示例",
      "description": "详细描述插件的功能和用途",
      "version": "1.0.0",
      "repo_url": "https://github.com/myname/awesome-plugin",
      "author_name": "My Name",
      "author_url": "https://github.com/myname",
      "channel": "community",
      "tags": ["utility", "example"],
      "extra": {}
    }
  ]
}
```

> **参考资源**：
> - [详细规范文档](docs/PLUGIN_INDEX_SPEC.md)
> - [插件开发指南](docs/PLUGIN_DEV_GUIDE.md) - SDK 和事件系统使用教程
> - [第三方 Hub 完整指南](docs/THIRD_PARTY_HUB_GUIDE.md)
> - [示例插件 Skeleton](examples/sdk_event_demo/) - 完整的开发示例
> - 本仓库的 `plugins.json` 作为参考示例

## 插件开发概览（基于 VabHub 插件 SDK）

### 插件运行环境

VabHub 插件是运行在 VabHub 主程序中的 Python 包，主程序在加载插件时，会寻找并调用它的入口函数：

```python
def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    """插件初始化入口函数"""
    pass
```

插件通过 `sdk` 调用主系统能力，通过 `bus` 订阅业务事件。

### 核心概念

VabHub 插件 SDK 基于以下三个核心概念：

| 概念 | 说明 |
|------|------|
| **PluginContext** | 插件上下文，提供插件的运行环境信息和配置 |
| **EventBus** | 事件总线，用于订阅和发布系统事件 |
| **VabHubSDK** | 插件 API 接口，提供日志、配置、HTTP 客户端等功能 |

### 最小插件示例

以下是一个完整的插件最小实现：

```python
from app.plugin_sdk.context import PluginContext
from app.plugin_sdk.api import VabHubSDK
from app.plugin_sdk.events import EventBus, EventType

def setup_plugin(ctx: PluginContext, bus: EventBus, sdk: VabHubSDK) -> None:
    sdk.log.info("Plugin loaded!")

    async def on_manga_updated(event: EventType, payload: dict) -> None:
        sdk.log.info(f"Manga updated: {payload}")

    # source 用于在卸载插件时清理订阅，建议传 ctx.plugin_id
    bus.subscribe(EventType.MANGA_UPDATED, on_manga_updated, source=ctx.plugin_id)
```

**重要提示**：本文只介绍概念与示例，完整的 SDK API 和功能列表请参见 VabHub 主仓库文档：`docs/PLUGIN_SDK_OVERVIEW.md`。

### 插件权限（sdk_permissions）与宿主服务

从 SDK v2 起，插件可以通过 `sdk_permissions` 声明自己需要使用的宿主能力，例如下载、媒体库查询、115 操作；主程序根据 `sdk_permissions` 决定是否允许插件调用对应 `sdk.download` / `sdk.media` / `sdk.cloud115` 方法。

在 `plugin.json` 中声明权限示例：

```json
{
  "id": "vabhub.my_plugin",
  "name": "我的插件",
  "version": "0.1.0",
  "sdk_permissions": [
    "media.read",
    "download.write"
  ],
  "backend": {
    "entry_module": "my_plugin.main"
  }
}
```

**sdk_permissions** 支持的值列表，以及对应的风险等级，请以主仓库文档 `PLUGIN_SDK_OVERVIEW.md` 为准；本仓库只给出概念性的说明。

插件作者只需了解：有 `sdk_permissions` 这回事，想用宿主服务必须先声明权限。

### 高级能力一览

VabHub 插件系统提供丰富的高级功能：

- **插件配置系统**：通过 `config_schema` 自动生成 Web 表单 + `sdk.config` 运行时读取
- **Dashboard 面板 DSL**：通过 `get_dashboard` 提供统计卡片、表格、文本、按钮等组件
- **插件对外 API**：通过 `get_routes` 暴露自定义 HTTP API，挂载到统一前缀
- **权限机制**：`sdk_permissions` 声明所需权限，区分安全能力和高危能力
- **安全 & 审计**：错误隔离、审计日志、健康状态监控
- **远程插件**：`plugin_type=remote` 支持，事件 HTTP 推送模式，跨语言支持

## 如何参与本仓库（官方 Hub）的贡献

我们欢迎以下类型的贡献：

### 🎯 官方插件条目
- **新增官方插件**：需要事先在 Issue 中沟通，由核心维护者确认后再提 PR
- **更新官方插件**：修正版本信息、描述等

### 📚 文档和规范改进
- 改进 README.md、`docs/PLUGIN_INDEX_SPEC.md` 等文档
- 完善插件开发规范
- 修正文档中的错误或过时信息

### 🔧 工具和流程优化
- 完善 CI/CD 工作流
- 添加验证工具
- 改进开发流程文档

> **推荐路线**：如果你是第三方插件作者，优先选择自建插件 Hub 仓库，而非直接将插件条目提交到官方仓库。

## 示例条目

以下是本仓库中的官方插件条目示例：

```json
{
  "id": "hello-world",
  "name": "Hello World 示例插件",
  "summary": "用于文档示例的条目，不代表实际可安装插件。",
  "description": "此条目仅作为文档示例使用，实际插件实现可在未来单独仓库中提供。主要用于演示 plugins.json 的标准写法和字段结构。",
  "version": "0.1.0",
  "repo_url": "https://github.com/strmforge/vabhub-plugin-hello-world",
  "author_name": "VabHub 官方",
  "author_url": "https://github.com/strmforge",
  "channel": "official",
  "tags": ["example", "docs-only", "hello-world"],
  "homepage": null,
  "readme_url": null,
  "extra": {}
}
```

> **说明**：`hello-world` 这一项主要用于演示 plugins.json 的写法，是文档示例条目。

## FAQ / 常见问题

**Q: 这个仓库里为什么没有插件代码？**
A: 本仓库是插件索引仓库，只维护插件列表和元数据。实际插件代码在各自的独立仓库中，这样便于管理和维护。

**Q: 如何关闭所有社区插件？**
A: 在 VabHub 主程序的配置中有相应的开关，可以控制是否展示和允许安装社区插件。请参考主程序的文档说明。

**Q: 为什么推荐自建插件 Hub？**
A: 自建插件 Hub 让开发者拥有完全的控制权，可以自由管理插件版本、更新节奏和内容，同时降低官方仓库的维护压力。

**Q: VabHub 主程序如何处理多个插件 Hub？**
A: 主程序会从配置的多个 Hub URL 拉取数据，合并后在统一的插件市场视图中展示，并在插件卡片上标明来源 Hub。

## 仓库结构

```text
vabhub-plugins/
  README.md                    # 官方 Hub 说明 + 规范指南
  plugins.json                 # 官方插件索引（核心数据）
  LICENSE                      # 开源协议
  CONTRIBUTING.md              # 官方 Hub 贡献指南
  docs/
    PLUGIN_INDEX_SPEC.md       # 详细的插件索引格式规范
    THIRD_PARTY_HUB_GUIDE.md   # 第三方 Hub 建设指南
  .github/
    workflows/                 # CI 工作流
      validate-plugins.yml     # JSON 格式校验
```

## 开发者文档

- [插件索引规范](docs/PLUGIN_INDEX_SPEC.md) - 完整的 plugins.json 字段规范，包含配置、Dashboard、远程插件等
- [插件开发指南](docs/PLUGIN_DEV_GUIDE.md) - 基础 SDK + 事件系统 + 配置 + Dashboard + API + 安全
- [远程插件开发指南](docs/PLUGIN_REMOTE_GUIDE.md) - 远程 HTTP 插件的完整开发协议和示例
- [第三方 Hub 指南](docs/THIRD_PARTY_HUB_GUIDE.md) - 创建和维护自己的插件 Hub
- [示例插件](examples/sdk_event_demo/) - 基础事件订阅示例

## 联系我们

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发起 Pull Request
- 查看 [规范文档](docs/PLUGIN_INDEX_SPEC.md) 了解更多技术细节
- 阅读 [插件开发指南](docs/PLUGIN_DEV_GUIDE.md) 学习 SDK 使用
- 阅读 [第三方 Hub 指南](docs/THIRD_PARTY_HUB_GUIDE.md) 获取完整教程
- 参考 [示例插件](examples/sdk_event_demo/) 开始开发