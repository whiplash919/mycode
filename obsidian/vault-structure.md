# Vault 结构、命名与标签规范

## 一、顶层文件夹结构

```
00 - INBOX/                临时收件箱（任何不确定归属的笔记先进这）
01 - NOTES/                有明确时间戳的捕获
    daily/                 每日日记
    meetings/              会议记录
    books/                 读书笔记
    courses/               课程笔记
02 - PROJECTS/             有截止日期、有明确产出的项目
    [项目名]/              每个项目一个子文件夹
03 - AREAS/                持续负责的领域（无结束日期）
    health/
    finances/
    relationships/
    career/
    learning/
04 - RESOURCES/            参考资料（个人 Wikipedia）
    topics/                按主题
    people/                按人物
    places/                按地点
    tools/                 按工具
05 - ARCHIVE/              所有不再活跃的内容（不删除）
06 - SYSTEM/               vault 的基础设施
    templates/             模板
    dashboards/            Dataview 仪表盘
    MOC/                   Maps of Content
```

### 各文件夹用途

| 文件夹 | 内容 | 进入条件 | 离开条件 |
|---|---|---|---|
| 00 - INBOX | 临时存放 | 没想清楚归属时 | 每日清空 |
| 01 - NOTES | 时间戳捕获 | 与具体时间事件绑定 | 1 年后归档 |
| 02 - PROJECTS | 进行中项目 | 有截止日期+明确产出 | 完成 → ARCHIVE |
| 03 - AREAS | 持续责任 | 长期关注的领域 | 不再关心 → ARCHIVE |
| 04 - RESOURCES | 参考资料 | 可能反复查阅 | 过时 → ARCHIVE |
| 05 - ARCHIVE | 归档 | 不再活跃 | 永不删除 |
| 06 - SYSTEM | 基础设施 | vault 本身的配置 | - |

### 编号前缀的作用
数字前缀让文件夹按固定顺序排列在文件浏览器中，每次打开 vault 都看到相同的导航顺序。

---

## 二、文件命名规范

### 通用格式
```
YYYY-MM-DD-[type]-[topic].md
```

### 示例
- `2026-05-27-daily-wednesday.md`
- `2026-05-27-meeting-client-quarterly-review.md`
- `2026-05-27-project-website-launch-kickoff.md`
- `2026-05-27-book-thinking-fast-and-slow.md`
- `2026-05-27-resource-claude-prompting-techniques.md`
- `2026-05-27-area-finances-q2-review.md`
- `2026-05-27-course-deep-learning-week3.md`
- `2026-05-27-idea-newsletter-pricing.md`

### 例外：长期不变的核心文档
某些笔记不是"事件"而是"常驻文档"（如 MOC、领域主页），可以不带日期：
- `productivity-MOC.md`
- `health-area-overview.md`
- `_inbox-dashboard.md`（下划线开头让它排在最前）

### 日期前缀的三个作用
1. 自动按时间排序，最新笔记永远在顶部
2. 大概记得"什么时候写的"时能用日期范围搜索
3. 同主题不同时间的笔记不会重名

---

## 三、YAML Properties（所有笔记必填）

### 通用字段
```yaml
---
type: daily | meeting | project | area | resource | book | course | idea
status: active | complete | archived | reference | waiting
date: 2026-05-27
tags: [topic1, topic2]
---
```

### 按类型追加字段

**project：**
```yaml
deadline: 2026-06-15
priority: high | medium | low
next_action: 写项目简报
completion: 35
```

**book：**
```yaml
author: 作者名
finished: 2026-05-10
rating: 4
key_insight: 一句话概括最重要的洞察
```

**meeting：**
```yaml
attendees: [Alice, Bob]
decisions: [关键决定]
actions: [行动项及负责人]
```

**resource：**
```yaml
topic: 主要主题
source: 信息来源
reliability: high | medium | low
```

**course：**
```yaml
provider: 平台/讲师
progress: 40
finished: false
```

### 为什么 `status` 最重要
检索时最常问的两个问题：
- "我现在在做的所有项目？" → `type=project AND status=active`
- "我读完的所有书？" → `type=book AND status=complete`

`status` 是把"全部笔记"切片成"现在相关"的唯一字段。

---

## 四、三类标签系统

### 类别 1：主题（topic）
**无前缀**。代表内容关于什么。

```
#productivity
#machine-learning
#real-estate
#stoicism
#prompt-engineering
```

### 类别 2：状态（status）
**前缀 `status/`**。代表工作流位置。

```
#status/active
#status/waiting
#status/someday
#status/complete
#status/blocked
```

### 类别 3：项目（project）
**前缀 `project/`**。把笔记关联到具体项目。

```
#project/website-launch
#project/book-writing
#project/client-acme
```

### 黄金规则
**一个标签必须用在至少 5 条笔记上**，否则就是噪音，季度复盘时删掉。

### 标签 vs Properties
- **Properties** 用于结构化字段（type / status / date / deadline）→ 给 Dataview 查询用
- **Tags** 用于灵活的横向关联（主题、临时分类）→ 给 Obsidian 内置搜索和图谱用

两者可以重叠（如 `status` 既是 property 也是 `#status/active` 标签），重叠是有意的，让两种检索方式都能用。

---

## 五、Maps of Content（MOC）

当某个主题超过 20 条笔记，建一个 MOC：
- 不是文件夹，不移动笔记
- 只用 `[[ ]]` 链接其他笔记
- 放在 `06 - SYSTEM/MOC/`
- 命名：`[主题]-MOC.md`，如 `productivity-MOC.md`

模板见 `MOC/_MOC-template.md`。

---

## 六、归档原则

**永远归档，不要删除。** 存储几乎免费，误删重要内容代价很高。

### 触发归档的时机
- 项目标记 complete → 立即从 `02 - PROJECTS/` 移到 `05 - ARCHIVE/projects/`
- daily 笔记超过 1 年 → 移到 `05 - ARCHIVE/daily/`
- resource 过时但可能历史参考 → 移到 `05 - ARCHIVE/resources/`

### 归档时要做的事
1. 把 `status` 改为 `archived`
2. 移动到 `05 - ARCHIVE/` 对应子目录
3. 保留所有 `[[ ]]` 链接（被链接的归档笔记仍然可点击）
