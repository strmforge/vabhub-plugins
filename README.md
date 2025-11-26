# VabHub Plugins（官方插件索引 & 插件市场）

这是 VabHub 官方插件索引 & 插件市场（Plugin Hub）仓库。

## 项目简介

本仓库是 VabHub 官方插件索引 & 插件市场（Plugin Hub），**仓库本身不包含插件代码**，只维护 `plugins.json` 插件列表。VabHub 主程序会从这里拉取 `plugins.json`，并在 Web UI 的「Plugin Hub」页面展示插件列表和元数据。

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

## 如何把你的插件加入 Plugin Hub（PR 指南）

我们欢迎社区开发者贡献插件！请按以下步骤操作：

### 步骤概览

1. **开发插件**
   - 在你自己的 GitHub 仓库中开发 VabHub 插件
   - 插件代码在你自己的 repo 中，不要放到本仓库
   - 确保插件符合 VabHub 插件开发规范

2. **Fork 本仓库**
   - Fork [strmforge/vabhub-plugins](https://github.com/strmforge/vabhub-plugins) 到你的 GitHub 账户
   - 克隆到本地进行修改

3. **修改 plugins.json**
   - 在 `plugins.json` 中新增一条插件条目，填好字段：
     - `id`、`name`、`version`、`repo_url` 等必填字段
     - `channel` 必须设置为 `"community"`
     - `author_name`/`author_url` 为你的信息

4. **提交 Pull Request**
   - 提交 PR 到本仓库的 main 分支
   - 等待维护者审核

### 注意事项

- **内容合规**：插件不得包含违法/违规用途（例如破解付费网站认证、灰黑产业等）
- **ID 唯一性**：插件 id 不要与已有插件重复
- **仓库权限**：repo_url 应该是你维护或有权维护的项目地址
- **质量保证**：确保插件功能正常，不影响主程序稳定性

## 示例条目

以下是 `plugins.json` 中的示例插件条目，供开发者参考：

```json
{
  "id": "hello-world",
  "name": "Hello World 示例插件",
  "summary": "最小可用的示例条目，用于说明 plugins.json 的写法。",
  "description": "此条目仅作为文档示例使用，实际插件实现可在未来单独仓库中提供。",
  "version": "0.1.0",
  "repo_url": "https://github.com/strmforge/vabhub-plugin-hello-world",
  "author_name": "VabHub 官方",
  "author_url": "https://github.com/strmforge",
  "channel": "official",
  "tags": ["example", "hello-world"],
  "homepage": null,
  "readme_url": null,
  "extra": {}
}
```

> **说明**：`hello-world` 这一项主要用于演示 plugins.json 的写法，是文档示例条目。

社区开发者可以照着这个格式填写自己的插件信息，只需将：
- `channel` 改为 `"community"`
- `id`、`name`、`summary`、`description` 改为插件的实际信息
- `repo_url` 改为你的插件仓库地址
- `author_name`、`author_url` 改为你的信息

## FAQ / 常见问题

**Q: 这个仓库里为什么没有插件代码？**
A: 本仓库是插件索引仓库，只维护插件列表和元数据。实际插件代码在各自的独立仓库中，这样便于管理和维护。

**Q: 如何关闭所有社区插件？**
A: 在 VabHub 主程序的配置中有相应的开关，可以控制是否展示和允许安装社区插件。请参考主程序的文档说明。

## 仓库结构

```text
vabhub-plugins/
  README.md                    # 插件市场说明 + 开发者指南
  plugins.json                 # 插件索引文件（核心数据）
  LICENSE                      # 开源协议
  CONTRIBUTING.md              # 贡献指南
  .github/
    workflows/                 # CI 工作流
      validate-plugins.yml     # JSON 格式校验
  docs/
    PLUGIN_INDEX_SPEC.md       # 详细的插件索引格式规范
```

## 联系我们

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发起 Pull Request
- 查看 [文档](docs/PLUGIN_INDEX_SPEC.md) 了解更多技术细节