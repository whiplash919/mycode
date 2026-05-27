---
type: dashboard
tags: [dashboard, projects]
---

# 🚀 进行中的项目 / Active Projects

> 此仪表盘只显示 `type=project` 且 `status=active` 的笔记。
> 按截止日期升序排列，最紧迫的在最上面。

## 📋 项目总表

```dataview
TABLE
  priority AS "优先级",
  next_action AS "下一步",
  deadline AS "截止",
  completion + "%" AS "进度"
FROM "02 - PROJECTS"
WHERE type = "project" AND status = "active"
SORT deadline ASC
```

## ⚠️ 本月到期

```dataview
LIST "**" + file.link + "** — 截止 " + deadline + " — 下一步：" + next_action
FROM "02 - PROJECTS"
WHERE type = "project"
  AND status = "active"
  AND deadline >= date(today)
  AND deadline <= date(today) + dur(30 days)
SORT deadline ASC
```

## 🔥 高优先级

```dataview
TABLE
  next_action AS "下一步",
  deadline AS "截止"
FROM "02 - PROJECTS"
WHERE type = "project"
  AND status = "active"
  AND priority = "high"
SORT deadline ASC
```

## 🚫 无下一步的项目（需立即处理）
<!-- next_action 为空 = 这个项目实际上没在推进 -->

```dataview
LIST
FROM "02 - PROJECTS"
WHERE type = "project"
  AND status = "active"
  AND (next_action = null OR next_action = "")
```

## ✅ 最近完成的项目（最近 30 天）

```dataview
TABLE
  date AS "完成日期"
FROM "02 - PROJECTS" OR "05 - ARCHIVE"
WHERE type = "project"
  AND status = "complete"
  AND date >= date(today) - dur(30 days)
SORT date DESC
```
