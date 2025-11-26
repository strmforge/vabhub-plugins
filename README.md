# VabHub Plugins（官方插件仓库 & 插件索引）

这是 **VabHub 官方插件仓库 & 插件索引（Plugin Hub）**。

定位：

1. 作为 VabHub 的「插件市场」索引：提供一个 `plugins.json`，被主程序读取和展示。
2. 可选地存放官方或示例插件的代码仓库链接（插件代码本身可以在其他仓库）。

> 当前阶段，这个仓库主要提供 `plugins.json` 索引文件，后续如有需要再扩展为托管插件源码。

## 仓库结构

```text
vabhub-plugins/
  README.md
  plugins.json              # 插件索引（主程序读取这个文件作为"插件市场目录"）

  docs/
    PLUGIN_INDEX_SPEC.md    # 插件索引格式说明
```

## 插件索引（plugins.json）

plugins.json 是一个简单的 JSON 文件，描述可用插件列表，例如：

- 插件 id / 名称 / 描述
- 作者 / 标签
- 插件主页 / 仓库地址
- 下载地址（zip/tar.gz），方便主程序将插件下载到本地 plugins/ 目录
- 兼容的 VabHub 核心版本
- 支持的扩展点（搜索 / Bot 命令 / UI 面板 / Workflow 等）

主程序可以通过环境变量 APP_PLUGIN_HUB_URL 配置这个 JSON 的 URL，例如：

```
https://raw.githubusercontent.com/<你的 GitHub 用户名或组织>/vabhub-plugins/main/plugins.json
```

## 将来

- 可以在这里维护官方插件列表（官方维护）
- 社区作者的插件也可以通过 PR 方式追加到 plugins.json