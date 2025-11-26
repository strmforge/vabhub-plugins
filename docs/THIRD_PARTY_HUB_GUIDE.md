# 第三方插件 Hub 建设指南

本指南帮助第三方开发者创建自己的 VabHub 插件 Hub 仓库，以便独立维护和管理插件列表。

## 简介

### 为什么选择自建插件 Hub？

- **完全控制权**：自由管理插件版本、更新节奏和内容
- **快速迭代**：无需等待官方审核，自主发布更新
- **主题专注**：按需组织特定领域或用途的插件集合
- **减少官方负担**：降低官方仓库的维护压力，让社区生态更健康

### 官方与第三方 Hub 的关系

- **官方 Hub**（strmforge/vabhub-plugins）：维护官方插件和核心规范
- **第三方 Hub**：社区开发者自建的插件仓库，专注特定领域或个人作品
- **用户选择**：VabHub 用户可以自行配置添加多个 Hub 源

## 目录结构建议

### 最小结构

```
your-plugin-hub/
├── plugins.json    # 必需：插件索引文件
└── README.md       # 推荐：Hub 介绍和使用说明
```

### 完整结构

```
your-plugin-hub/
├── README.md              # Hub 介绍和说明
├── plugins.json           # 插件索引（核心文件）
├── LICENSE               # 开源协议（可选）
└── .github/
    └── workflows/
        └── validate.yml   # 可选的 JSON 校验 CI
```

### 文件说明

- **plugins.json**：核心索引文件，必须遵循 [PLUGIN_INDEX_SPEC](PLUGIN_INDEX_SPEC.md) 规范
- **README.md**：介绍你的 Hub 主题、维护范围、联系方式
- **LICENSE**：明确你的 Hub 内容使用许可
- **CI 配置**：可选的自动化校验，确保 plugins.json 格式正确

## plugins.json 示例

### 基础示例

以下是一个包含单个插件的示例：

```json
{
  "hub_name": "My VabHub Plugins",
  "hub_version": 1,
  "plugins": [
    {
      "id": "myname-awesome-plugin",
      "name": "Awesome Plugin",
      "summary": "一个很棒的 VabHub 插件",
      "description": "这个插件提供了强大的功能，帮助用户提高工作效率。主要特性包括自动化处理、智能推荐等。",
      "version": "1.2.0",
      "repo_url": "https://github.com/myname/awesome-plugin",
      "author_name": "My Name",
      "author_url": "https://github.com/myname",
      "channel": "community",
      "tags": ["utility", "automation", "productivity"],
      "features": ["search", "ui_panels"],
      "homepage": "https://github.com/myname/awesome-plugin#readme",
      "readme_url": "https://raw.githubusercontent.com/myname/awesome-plugin/main/README.md",
      "extra": {
        "min_vabhub_version": "1.0.0",
        "compatibility_notes": "需要 VabHub 1.0.0 或更高版本"
      }
    }
  ]
}
```

### 多插件示例

```json
{
  "hub_name": "Developer Tools Hub",
  "hub_version": 1,
  "plugins": [
    {
      "id": "devtools-code-formatter",
      "name": "Code Formatter",
      "summary": "自动格式化代码的工具插件",
      "description": "支持多种编程语言的代码格式化，可自定义格式化规则。",
      "version": "2.1.0",
      "repo_url": "https://github.com/devtools/code-formatter",
      "author_name": "DevTools Team",
      "author_url": "https://github.com/devtools",
      "channel": "community",
      "tags": ["development", "formatting", "tools"],
      "features": ["ui_panels"],
      "extra": {}
    },
    {
      "id": "devtools-snippet-manager",
      "name": "Snippet Manager",
      "summary": "代码片段管理器",
      "description": "管理和复用常用代码片段，提高开发效率。",
      "version": "1.0.0",
      "repo_url": "https://github.com/devtools/snippet-manager",
      "author_name": "DevTools Team",
      "author_url": "https://github.com/devtools",
      "channel": "community",
      "tags": ["development", "snippets", "productivity"],
      "features": ["ui_panels", "bot_commands"],
      "extra": {}
    }
  ]
}
```

## 命名与版本约定

### 插件 ID 命名建议

- **格式推荐**：`作者简写-插件名` 或 `领域-功能名`
- **避免重复**：确保在所有 Hub 中 ID 唯一
- **语义清晰**：ID 能体现插件的用途和归属

**示例**：
- ✅ `myname-search-enhancer`
- ✅ `devtools-code-formatter`
- ✅ `ai-assistant-gpt4`
- ❌ `plugin1`（不够明确）
- ❌ `search`（过于通用）

### 版本号规范

- **格式**：遵循语义化版本 `x.y.z`
- **主版本号 (x)**：不兼容的 API 修改
- **次版本号 (y)**：向下兼容的功能性新增
- **修订号 (z)**：向下兼容的问题修正

**更新原则**：
- 功能变更时：增加 `y` 版本号
- Bug 修复时：增加 `z` 版本号
- 破坏性变更时：增加 `x` 版本号

## 在 VabHub 中使用你的 Hub

### URL 格式

VabHub 主程序支持以下格式的 Hub URL：

```
https://raw.githubusercontent.com/yourname/your-hub/main/plugins.json
```

### 配置方式

**预期行为**（VabHub 主程序实现）：
1. 用户在设置中添加你的 Hub URL
2. 主程序定期从配置的多个 Hub 拉取数据
3. 合并所有插件数据到统一的市场视图
4. 在插件卡片上标注来源 Hub（如"来自 Developer Tools Hub"）
5. 支持按 Hub 筛选和搜索插件

### 用户配置示例

```
插件源配置：
- ☑ 官方插件 Hub (https://raw.githubusercontent.com/strmforge/vabhub-plugins/main/plugins.json)
- ☑ Developer Tools Hub (https://raw.githubusercontent.com/devtools/my-plugins/main/plugins.json)
- ☑ AI Tools Hub (https://raw.githubusercontent.com/ai-team/vabhub-plugins/main/plugins.json)
```

## 维护最佳实践

### 内容管理

1. **插件质量把控**
   - 确保列表中的插件功能正常
   - 定期检查插件仓库是否仍然活跃
   - 移除不再维护的插件或标记废弃状态

2. **信息准确性**
   - 定期更新插件版本信息
   - 确保 repo_url 和文档链接有效
   - 保持插件描述与实际功能一致

3. **版本同步**
   - 插件仓库发布新版本时，及时更新 Hub 中的版本号
   - 避免版本信息过时导致用户无法获取最新功能

### Hub 推广

1. **README 优化**
   - 清晰说明你的 Hub 主题和特色
   - 提供详细的配置说明
   - 包含联系方式和更新日志

2. **社区参与**
   - 在 VabHub 社区介绍你的 Hub
   - 收集用户反馈并持续改进
   - 与其他 Hub 维护者交流经验

3. **持续更新**
   - 定期检查和更新插件信息
   - 及时响应社区问题和建议
   - 保持 Hub 的活跃性和可靠性

## 可选的 CI 配置

### GitHub Actions 示例

```yaml
name: Validate plugins.json

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Validate JSON
      run: |
        # 安装 jq（如果需要）
        sudo apt-get update && sudo apt-get install -y jq
        
        # 校验 JSON 格式
        if jq '.' plugins.json > /dev/null; then
          echo "✅ JSON 格式有效"
        else
          echo "❌ JSON 格式错误"
          exit 1
        fi
        
        # 检查必填字段
        jq -r '.plugins[] | [(.id // "missing"), (.name // "missing"), (.version // "missing")] | @tsv' plugins.json | while IFS=$'\t' read -r id name version; do
          if [[ "$id" == "missing" || "$name" == "missing" || "$version" == "missing" ]]; then
            echo "❌ 插件缺少必填字段: $id"
            exit 1
          fi
        done
        
        echo "✅ 所有插件条目包含必填字段"
```

## 常见问题

### Q: 我需要官方收录我的 Hub 吗？

A: 不需要。VabHub 采用开放的 Hub 机制，用户可以自行添加任何符合规范的 Hub 源。你只需要确保你的 `plugins.json` 可以通过公开 URL 访问即可。

### Q: 如何处理重复的插件 ID？

A: 建议在 ID 中包含作者标识前缀（如 `myname-plugin`），这样可以最大程度避免与其他 Hub 的插件 ID 冲突。

### Q: Hub 数据多久更新一次？

A: VabHub 主程序会定期拉取 Hub 数据（可能是每次启动时或按配置的间隔），用户也可以手动触发更新。作为 Hub 维护者，你应该随时保持 `plugins.json` 的最新状态。

### Q: 可以包含商业插件吗？

A: 可以，但需要明确标注收费信息，并遵守相关法律法规。建议在插件的 `description` 或 `extra` 字段中说明付费情况。

### Q: 如何处理插件的安全问题？

A: 作为 Hub 维护者，你应该：
- 审查收录插件的安全性
- 及时移除发现安全问题的插件
- 建立安全问题的报告机制
- 定期检查插件仓库的安全性

## 技术支持

- **规范问题**：参考 [PLUGIN_INDEX_SPEC.md](PLUGIN_INDEX_SPEC.md)
- **Hub 建设问题**：在本仓库提交 Issue
- **VabHub 主程序问题**：联系 VabHub 官方团队

---

**开始构建你自己的插件 Hub，为 VabHub 生态贡献特色内容！**