# VabHub 插件索引规范（plugins.json）

本文档是 VabHub 官方 Plugin Hub 索引文件 `plugins.json` 的权威规范。主程序通过读取这个 JSON 来获取插件列表、元数据和能力声明。

## 概述

`plugins.json` 是 VabHub 插件市场的核心索引文件，包含所有可用插件的元数据。该文件采用 JSON 格式，遵循严格的结构和字段定义。

主程序会定期拉取此文件并解析其中的插件信息，用于在 Web UI 的「Plugin Hub」页面展示插件列表、支持搜索、分类等功能。

## 顶层结构

`plugins.json` 的顶层结构如下：

```json
{
  "hub_name": "VabHub Official Plugin Hub",
  "hub_version": 1,
  "plugins": [ /* PluginEntry[] */ ]
}
```

### 顶层字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **hub_name** | string | ✅ | Hub 的名称标识，用于标识此索引文件的用途 |
| **hub_version** | number | ✅ | 索引协议版本号（当前为 1） |
| **plugins** | PluginEntry[] | ✅ | 插件条目数组，包含所有插件的详细信息 |

### 版本与兼容性

- **hub_version**: 用于主程序识别索引协议版本
- **当前版本 1**: 支持基础的插件元数据和功能声明
- **兼容策略**: 
  - 主程序支持读取当前版本及更低版本的索引格式
  - 未来升级到 2/3 版本时，将保持向后兼容
  - 新增字段不会导致旧版本主程序解析失败

## PluginEntry 字段定义

每个插件条目（PluginEntry）包含以下字段：

### 核心字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **id** | string | ✅ | 插件唯一标识符，建议使用 namespace-name 格式 |
| **name** | string | ✅ | 插件展示名称 |
| **summary** | string | ✅ | 简短摘要，出现在插件卡片上作为副标题 |
| **description** | string | 可选 | 更长的描述文字，详细介绍插件功能 |
| **version** | string | ✅ | 当前版本号，字符串格式，遵循语义化版本 |
| **repo_url** | string | ✅ | 插件代码或说明仓库地址，必须是有效的 HTTP(S) URL |

### 作者信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **author_name** | string | ✅ | 作者/维护者显示名 |
| **author_url** | string | ✅ | 作者主页链接，通常是 GitHub 用户/组织页 |

### 分类信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **channel** | string | ✅ | 插件频道，必须是 `"official"` 或 `"community"` |
| **tags** | string[] | 可选 | 标签数组，用于分类和搜索 |
| **features** | string[] | 可选 | 功能特性数组，声明插件支持的功能类型 |

### 链接信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **homepage** | string | 可选 | 插件主页 URL，可以是 null |
| **readme_url** | string | 可选 | 插件文档链接，必须是有效的 HTTP(S) URL，可以是 null |

### 扩展信息

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| **extra** | object | 可选 | 额外的自定义信息，JSON 对象格式，用于扩展字段 |

### 字段详细说明

#### id
- **格式**: 建议使用 `namespace-name` 格式，如 `vabhub-hello-world`
- **唯一性**: 在整个 Plugin Hub 中必须唯一
- **用途**: 主程序内部插件标识符

#### channel
- **可选值**: 
  - `"official"`: 官方插件，由 VabHub 官方维护
  - `"community"`: 社区插件，由第三方开发者维护
- **用途**: 主程序可能根据此字段控制插件展示和安装权限

#### features
- **常用值**: 
  - `"search"`: 搜索扩展
  - `"bot_commands"`: Bot 命令扩展
  - `"ui_panels"`: UI 面板扩展
  - `"workflows"`: Workflow 扩展
- **用途**: 声明插件支持的功能类型，便于主程序按需加载

#### extra
- **常用字段**: 
  - `min_core_version`: 最低支持的 VabHub 核心版本
  - `enabled_by_default`: 是否默认启用
  - `supports`: 详细的扩展点支持信息
  - `panels`: UI 面板挂载位置
- **用途**: 存储插件的扩展信息，不参与核心功能判断

## 示例

### 规范推荐写法

以下是一个完整的 PluginEntry 示例：

```json
{
  "id": "example-plugin",
  "name": "Example Plugin",
  "summary": "这是一个示例插件，演示标准格式",
  "description": "更详细的插件描述，介绍功能特性、使用方法等。",
  "version": "1.0.0",
  "repo_url": "https://github.com/owner/plugin-repo",
  "author_name": "Plugin Author",
  "author_url": "https://github.com/author",
  "channel": "community",
  "tags": ["utility", "example"],
  "features": ["search", "ui_panels"],
  "homepage": "https://github.com/owner/plugin-repo#readme",
  "readme_url": "https://raw.githubusercontent.com/owner/plugin-repo/main/README.md",
  "extra": {
    "min_core_version": "1.0.0",
    "enabled_by_default": false,
    "supports": {
      "search": true,
      "ui_panels": true
    },
    "panels": [
      "home_dashboard"
    ]
  }
}
```

### 最小化示例

```json
{
  "id": "minimal-plugin",
  "name": "Minimal Plugin",
  "summary": "最小化示例",
  "version": "0.1.0",
  "repo_url": "https://github.com/owner/plugin-repo",
  "author_name": "Author",
  "author_url": "https://github.com/author",
  "channel": "community",
  "tags": [],
  "extra": {}
}
```

## 字段默认行为

当某些字段缺失或为 null 时，主程序的处理方式：

- **summary**: 使用 name 的值
- **description**: 使用 summary 的值
- **homepage**: 使用 repo_url 的值
- **readme_url**: 尝试使用 `${repo_url}/blob/main/README.md`
- **tags**: 视为空数组 `[]`
- **features**: 视为空数组 `[]`
- **extra**: 视为空对象 `{}`

## 与 README 的关系

- **README.md**: 提供简化说明与操作指南，面向开发者快速上手
- **本文档**: 是 plugins.json 的详细规范，优先级更高，用于精确理解和实现

## 更新日志

### v1.0
- 定义基础的插件索引结构
- 支持官方和社区插件分类
- 提供完整的插件元数据字段
- 支持扩展点声明和自定义扩展信息