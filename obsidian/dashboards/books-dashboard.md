---
type: dashboard
tags: [dashboard, books]
---

# 读书面板

## 正在读

```dataview
TABLE
  author AS "作者",
  date AS "开始"
FROM "01 - NOTES/books"
WHERE type = "book" AND status = "active"
SORT date DESC
```

## 已读完（最近一年）

```dataview
TABLE
  author AS "作者",
  rating AS "评分",
  finished AS "读完",
  key_insight AS "一句话核心"
FROM "01 - NOTES/books" OR "05 - ARCHIVE"
WHERE type = "book"
  AND status = "complete"
  AND finished >= date(today) - dur(365 days)
SORT finished DESC
```

## 高分书（≥4 星）

```dataview
TABLE
  author AS "作者",
  rating AS "评分",
  key_insight AS "核心洞察"
FROM ""
WHERE type = "book"
  AND status = "complete"
  AND rating >= 4
SORT rating DESC, finished DESC
```

## 按主题分组

```dataview
TABLE
  rows.file.link AS "书",
  rows.rating AS "评分"
FROM ""
WHERE type = "book" AND status = "complete"
GROUP BY tags AS "主题"
SORT length(rows) DESC
```

## 阅读节奏（按月）

```dataview
TABLE
  length(rows) AS "本月读完的书数",
  rows.file.link AS "书目"
FROM ""
WHERE type = "book" AND status = "complete" AND finished != null
GROUP BY dateformat(finished, "yyyy-MM") AS "月份"
SORT 月份 DESC
LIMIT 12
```

## 待读 / Reading List

```dataview
LIST
FROM ""
WHERE type = "book" AND status = "someday"
```
