---
type: dashboard
tags: [dashboard, waiting]
---

# ⏳ Waiting On — 等待中的事项

> 这里聚合所有 `status: waiting` 的笔记 + 含 `#status/waiting` 标签的笔记。
> 这是"球不在我这一侧"的所有事情。定期扫一遍，看哪些该催了。

## 📋 所有等待中的笔记

```dataview
TABLE
  type AS "类型",
  date AS "进入等待时间",
  (date(today) - date).days AS "已等待天数"
FROM ""
WHERE status = "waiting"
  AND !contains(file.folder, "ARCHIVE")
SORT date ASC
```

## 🚨 等待超过 7 天的（该催了）

```dataview
LIST "**" + file.link + "** — 已等 " + (date(today) - date).days + " 天"
FROM ""
WHERE status = "waiting"
  AND date <= date(today) - dur(7 days)
  AND !contains(file.folder, "ARCHIVE")
SORT date ASC
```

## 🏷️ 带 #status/waiting 标签的笔记

```dataview
LIST
FROM #status/waiting
WHERE !contains(file.folder, "ARCHIVE")
SORT file.mtime DESC
```

## 📦 按项目分组

```dataview
TABLE
  rows.file.link AS "等待项",
  rows.date AS "进入等待时间"
FROM ""
WHERE status = "waiting" AND !contains(file.folder, "ARCHIVE")
GROUP BY project AS "项目"
```
