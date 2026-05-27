# Obsidian Vault System / Obsidian 仓库系统

一套以"检索优先"为原则的 Obsidian 组织方案。包含文件夹结构、命名规范、模板、Dataview 仪表盘和迁移计划。

## 核心原则

> 你不是为了把东西收好而组织 vault，而是为了能快速取回。
> 每个文件夹、标签、命名都要回答："未来我找它时，会知道关于它的什么？"

未来你能记起一条笔记的四个维度：
1. **类型**（type）：日记 / 会议 / 项目 / 书摘 / 资源
2. **时间**（date）
3. **主题**（tags / topic）
4. **状态**（status）

四个维度任意组合 = 30 秒内找到任何笔记。

## 仓库内容

```
obsidian/
├── README.md                 ← 本文件，整体说明
├── vault-structure.md        ← 完整文件夹结构 + 命名规范 + 标签系统
├── migration-plan.md         ← 4 周渐进式迁移计划
├── templates/                ← 8 种笔记模板（含 YAML frontmatter）
│   ├── daily.md
│   ├── meeting.md
│   ├── project.md
│   ├── book.md
│   ├── resource.md
│   ├── area.md
│   ├── course.md
│   └── idea.md
├── dashboards/               ← Dataview 仪表盘（直接复制到 vault）
│   ├── active-projects.md
│   ├── this-week.md
│   ├── inbox.md
│   ├── books-dashboard.md
│   ├── waiting-on.md
│   └── recent-meetings.md
└── MOC/                      ← Map of Content 模板与示例
    ├── _MOC-template.md
    └── productivity-MOC.md
```

## 快速开始

### 1. 在 Obsidian 中启用必要插件
- **核心 Templates 插件**（内置，无需安装）—— 模板里的 `{{date}}` `{{title}}` 等占位符靠它自动填充
- **Dataview**（社区插件，仪表盘查询必装）
- **Daily Notes 核心插件**（内置）—— 用于每日笔记
- *可选*：**Templater**（如果想要更强的脚本占位符，比如自动算"昨天/明天"日期）

### 2. 创建 vault 顶层结构
按 `vault-structure.md` 创建 7 个顶层文件夹（编号开头，自动排序）。

### 3. 复制模板
把 `templates/` 下所有文件复制到 vault 的 `06 - SYSTEM/templates/` 文件夹。在 Templater 设置中把模板目录指向该路径。

### 4. 复制仪表盘
把 `dashboards/` 下所有文件复制到 vault 的 `06 - SYSTEM/dashboards/`。这些文件已经写好了 Dataview 查询，打开就能看到聚合视图。

### 5. 按迁移计划推进
打开 `migration-plan.md`，按 4 周节奏渐进式整理现有笔记。**不要一次性重组所有笔记**。

## 关键约定速查

### 命名规范
```
YYYY-MM-DD-[type]-[topic].md
```
例：`2026-05-27-meeting-client-quarterly-review.md`

### YAML Properties（所有笔记必填）
```yaml
---
type: daily | meeting | project | area | resource | book | course | idea
status: active | complete | archived | reference | waiting
date: 2026-05-27
tags: [topic1, topic2]
---
```

### 标签三类
| 类别 | 前缀 | 例子 |
|---|---|---|
| 主题 | 无 | `#productivity` |
| 状态 | `status/` | `#status/active` |
| 项目 | `project/` | `#project/website-launch` |

**铁律**：一个标签至少用在 5 条笔记，否则删掉。

## 维护节奏

- **每日**：15 分钟清空 INBOX
- **每周**：更新进行中项目的 `next_action`
- **每季度**：30 分钟–2 小时复盘（见 `migration-plan.md` 末尾）
