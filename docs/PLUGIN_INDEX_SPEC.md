# VabHub 插件索引规范（plugins.json）

本文件说明 `plugins.json` 的基本结构，供插件作者和主程序开发者参考。

## 顶层结构

```json
{
  "hub_name": "VabHub Official Plugin Hub",
  "hub_version": 1,
  "plugins": [ /* PluginItem[] */ ]
}
```

- **hub_name**: 当前插件索引的名称。
- **hub_version**: 索引格式版本号（整数），预留以后升级格式使用。
- **plugins**: 插件数组。

## PluginItem 字段说明

一个典型的 PluginItem 示例：

```json
{
  "id": "vabhub-hello-world",
  "name": "Hello World 示例插件",
  "description": "简要描述",
  "author": "插件作者",
  "tags": ["official", "example"],

  "homepage": "https://example.com",
  "repo": "https://github.com/owner/repo",
  "download_url": "https://github.com/owner/repo/archive/refs/heads/main.zip",

  "min_core_version": "0.9.0",
  "enabled_by_default": false,

  "supports": {
    "search": true,
    "bot_commands": true,
    "ui_panels": true,
    "workflows": false
  },

  "panels": [
    "home_dashboard",
    "admin_dashboard"
  ]
}
```

### 必填字段

- **id**: 插件唯一 ID（建议使用 namespace-name 形式，如 vabhub-hello-world）。
- **name**: 插件显示名称。
- **description**: 短描述。
- **author**: 作者名称（可以是组织）。
- **download_url**: 插件压缩包的下载地址（zip/tar.gz 均可）。
- **min_core_version**: 兼容的 VabHub 最低核心版本。

### 建议字段

- **tags**: 标签数组，用于分类和搜索。
- **homepage**: 插件主页。
- **repo**: 插件代码仓库地址。

## 扩展点声明

- **supports.search**: 插件是否提供搜索扩展。
- **supports.bot_commands**: 是否提供 Bot 命令扩展。
- **supports.ui_panels**: 是否提供前端 UI 面板扩展。
- **supports.workflows**: 是否提供 Workflow 扩展。

## 面板挂载位置

`panels` 是一个字符串数组，表示这个插件可能在 UI 的哪些位置挂载面板，例如：

- `home_dashboard`
- `admin_dashboard`
- `task_center`
- `reading_center`
- `dev_plugin`
- `custom:*`（预留）

主程序可以按需选择在对应页面加载这些面板。