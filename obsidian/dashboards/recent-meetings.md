---
type: dashboard
tags: [dashboard, meetings]
---

# 会议面板

## 最近 14 天的会议

```dataview
TABLE
  attendees AS "参与人",
  decisions AS "关键决定"
FROM "01 - NOTES/meetings"
WHERE date >= date(today) - dur(14 days)
SORT date DESC
```

## 待执行的行动项
<!-- 从会议笔记 frontmatter 的 actions 字段聚合 -->

```dataview
TABLE WITHOUT ID
  file.link AS "会议",
  date AS "会议日期",
  actions AS "行动项"
FROM "01 - NOTES/meetings"
WHERE actions != null AND length(actions) > 0
  AND date >= date(today) - dur(30 days)
SORT date DESC
```

## 按项目分组的会议

```dataview
TABLE
  rows.file.link AS "会议",
  rows.date AS "日期"
FROM "01 - NOTES/meetings"
WHERE project != null
GROUP BY project AS "项目"
SORT length(rows) DESC
```

## 与某人开的所有会
<!-- 改下面的 "Alice" 为实际人名 -->

```dataview
LIST
FROM "01 - NOTES/meetings"
WHERE contains(attendees, "Alice")
SORT date DESC
```

## 没填 decisions 的会议（不完整）

```dataview
LIST
FROM "01 - NOTES/meetings"
WHERE date >= date(today) - dur(30 days)
  AND (decisions = null OR length(decisions) = 0)
SORT date DESC
```
