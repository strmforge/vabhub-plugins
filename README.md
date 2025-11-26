# VabHub Plugins（官方插件索引 & 插件市场）

这是 VabHub 官方插件索引 & 插件市场（Plugin Hub）仓库。

## 仓库定位

此仓库是 VabHub 的官方插件索引市场，**仓库本身不运行代码**，只维护 `plugins.json` 插件列表。VabHub 主程序会从这里拉取 JSON，并在 Web UI 的「Plugin Hub / 插件市场」页面展示。

- **官方插件索引**：提供完整的插件列表，供 VabHub 主程序读取和展示
- **插件市场入口**：用户可以在这里发现和了解可用插件
- **开发者指南**：为插件作者提供提交规范和流程

> 所有插件代码都在各自的独立仓库中，本仓库仅维护索引信息。

## 仓库结构

```text
vabhub-plugins/
  README.md                    # 插件市场说明 + 开发者指南
  plugins.json                 # 插件索引文件（核心数据）
  docs/
    PLUGIN_INDEX_SPEC.md       # 详细的插件索引格式规范
```

## plugins.json 字段说明

`plugins.json` 中的每个插件条目包含以下字段：

| 字段 | 类型 | 说明 | 必填 |
|------|------|------|------|
| **id** | string | 插件唯一 ID（与插件在 VabHub 内部的 plugin_id 对应） | ✅ |
| **name** | string | 展示名称 | ✅ |
| **summary** | string | 简短摘要，作为卡片副标题 | ✅ |
| **description** | string | 更长的文字说明 | 可选 |
| **version** | string | 当前版本号，遵循语义化版本 | ✅ |
| **repo_url** | string | 插件代码仓库地址（GitHub 仓库地址或说明仓库） | ✅ |
| **author_name** | string | 作者/维护者显示名 | ✅ |
| **author_url** | string | 作者主页 | ✅ |
| **channel** | string | `official`（官方）或 `community`（社区插件） | ✅ |
| **tags** | string[] | 标签数组，用于分类和搜索 | 可选 |
| **homepage** | string | 插件主页 | 可选 |
| **readme_url** | string | 插件文档链接 | 可选 |
| **extra** | object | 额外的自定义信息（JSON 对象） | 可选 |

主程序可通过环境变量配置此索引的 URL：
```
APP_PLUGIN_HUB_URL=https://raw.githubusercontent.com/strmforge/vabhub-plugins/main/plugins.json
```

## 如何将你的插件加入 Plugin Hub

我们欢迎社区开发者贡献插件！请按以下步骤操作：

### 步骤概览

1. **开发插件**
   - 在你自己的 GitHub 仓库中开发 VabHub 插件
   - 插件代码放在自己的仓库，不要放到本仓库
   - 确保插件符合 VabHub 插件开发规范

2. **Fork 本仓库**
   - Fork [strmforge/vabhub-plugins](https://github.com/strmforge/vabhub-plugins) 到你的 GitHub 账户
   - 克隆到本地进行修改

3. **编辑 plugins.json**
   - 在 `plugins.json` 中新增一条插件记录
   - 填写 id/name/version/repo_url 等必填字段
   - **channel 必须设置为 "community"**
   - author_name/author_url 填写你自己的信息

4. **提交 Pull Request**
   - 提交 PR 到本仓库的 main 分支
   - 等待官方审核和合并

### 注意事项

- **ID 唯一性**：插件 id 不要与已有插件重复，避免冲突
- **内容合规**：插件不能包含违法/违规内容（例如破解认证、灰黑产等）
- **质量保证**：确保插件功能正常，不影响主程序稳定性
- **文档完善**：建议提供详细的使用说明和 API 文档

官方保留拒绝/移除某些插件索引的权利，以确保插件市场的质量和安全性。

### 渠道分类规则

- **官方插件**：使用 `channel: "official"`，且 `repo_url` 必须在 `APP_PLUGIN_OFFICIAL_ORGS` 定义的组织下
- **社区插件**：统一使用 `channel: "community"`

## 示例条目

以下是 `plugins.json` 中的 Hello World 示例插件条目，供开发者参考：

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

社区开发者可以照着这个格式填写自己的插件信息，只需将：
- `channel` 改为 `"community"`
- `id`、`name`、`summary`、`description` 改为插件的实际信息
- `repo_url` 改为你的插件仓库地址
- `author_name`、`author_url` 改为你的信息

## 联系我们

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发起 Pull Request
- 查看 [文档](docs/PLUGIN_INDEX_SPEC.md) 了解更多技术细节