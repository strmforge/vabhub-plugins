# VabHub Plugins（官方插件索引 & 插件市场）

这是 **VabHub 官方插件索引 & 展示仓库（Plugin Hub）**。

## 仓库定位

此仓库是 VabHub 的官方插件索引市场，**仓库本身不包含插件代码**，只维护 `plugins.json` 索引列表。所有插件代码都在各自的独立仓库中。

- **官方插件索引**：提供完整的插件列表，供 VabHub 主程序读取和展示
- **插件市场入口**：用户可以在这里发现和了解可用插件
- **开发者指南**：为插件作者提供提交规范和流程

> 当前阶段，此仓库专注于维护 `plugins.json` 索引文件，后续可根据需要扩展其他功能。

## 仓库结构

```text
vabhub-plugins/
  README.md                    # 插件市场说明 + 开发者指南
  plugins.json                 # 插件索引文件（核心数据）
  docs/
    PLUGIN_INDEX_SPEC.md       # 详细的插件索引格式规范
```

## 插件索引字段说明

`plugins.json` 中的每个插件条目包含以下字段：

### 基础信息
- **id**: 插件唯一标识符（建议使用 `namespace-name` 格式）
- **name**: 插件显示名称
- **summary**: 插件简短描述（一句话）
- **description**: 插件详细描述
- **version**: 插件版本号（遵循语义化版本）

### 作者信息
- **author_name**: 作者或组织名称
- **author_url**: 作者主页或 GitHub 地址

### 仓库信息
- **repo_url**: 插件代码仓库地址
- **channel**: 插件渠道（`official` 或 `community`）

### 分类和标签
- **tags**: 标签数组，用于分类和搜索
- **features**: 功能特性数组（可选）
- **homepage**: 插件主页（可选）
- **readme_url**: 插件文档链接（可选）
- **extra**: 额外的自定义信息（可选，JSON 对象）

主程序可通过环境变量配置此索引的 URL：
```
APP_PLUGIN_HUB_URL=https://raw.githubusercontent.com/strmforge/vabhub-plugins/main/plugins.json
```

## 如何把你的插件加入 Plugin Hub

我们欢迎社区开发者贡献插件！请按以下步骤操作：

### 步骤概览

1. **准备插件仓库**
   - 在你自己的 GitHub 仓库中开发和维护插件代码
   - 确保插件符合 VabHub 插件开发规范

2. **Fork 本仓库**
   - Fork strmforge/vabhub-plugins 到你的 GitHub 账户
   - 克隆到本地进行修改

3. **添加插件条目**
   - 在 `plugins.json` 中新增一条插件记录（见下方示例）
   - 确保所有必填字段完整且格式正确

4. **提交 Pull Request**
   - 提交 PR 到本仓库的 main 分支
   - 等待官方审核和合并

### 渠道分类规则

- **官方插件**：使用 `channel: "official"`，且 `repo_url` 必须在 `APP_PLUGIN_OFFICIAL_ORGS` 定义的组织下
- **社区插件**：统一使用 `channel: "community"`

### 内容规范

插件内容必须合法合规，禁止包含：
- 破解认证、绕过授权的功能
- 灰黑产业相关内容
- 恶意代码或安全漏洞
- 侵犯他人知识产权的内容

### 完整插件条目示例

```json
{
  "id": "example-plugin",
  "name": "示例插件",
  "summary": "这是一个示例插件的简短描述",
  "description": "这里是插件的详细说明，可以介绍功能特性、使用方法等。",
  "version": "1.0.0",
  "repo_url": "https://github.com/your-username/your-plugin-repo",
  "author_name": "Your Name",
  "author_url": "https://github.com/your-username",
  "channel": "community",
  "tags": ["utility", "example"],
  "homepage": "https://github.com/your-username/your-plugin-repo#readme",
  "readme_url": "https://raw.githubusercontent.com/your-username/your-plugin-repo/main/README.md",
  "extra": {
    "license": "MIT",
    "min_vabhub_version": "1.0.0"
  }
}
```

## 示例条目

以下是 `plugins.json` 中的 Hello World 示例插件条目，供参考：

```json
{
  "id": "hello-world",
  "name": "Hello World 示例插件",
  "summary": "最小可用的演示条目，用于说明 plugins.json 写法。",
  "description": "此条目仅作为文档示例使用，对应的插件实现可根据未来实际仓库地址补全。",
  "version": "0.1.0",
  "repo_url": "https://github.com/strmforge/vabhub-plugin-hello-world",
  "author_name": "VabHub 官方",
  "author_url": "https://github.com/strmforge",
  "channel": "official",
  "tags": ["example", "hello-world"],
  "extra": {}
}
```

## 联系我们

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发起 Pull Request
- 查看 [文档](docs/PLUGIN_INDEX_SPEC.md) 了解更多技术细节