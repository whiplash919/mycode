---
type: dashboard
tags: [dashboard, weekly]
---

# 📅 本周 / This Week

## 📝 本周创建的笔记

```dataview
TABLE
  type AS "类型",
  status AS "状态",
  file.cday AS "创建"
FROM ""
WHERE file.cday >= date(today) - dur(7 days)
  AND !contains(file.folder, "SYSTEM")
  AND !contains(file.folder, "ARCHIVE")
SORT file.cday DESC
```

## 🗒️ 本周日记

```dataview
LIST
FROM "01 - NOTES/daily"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

## 🤝 本周会议

```dataview
TABLE
  attendees AS "参与人",
  decisions AS "决定"
FROM "01 - NOTES/meetings"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

## 💡 本周捕获的想法

```dataview
LIST
FROM ""
WHERE type = "idea"
  AND date >= date(today) - dur(7 days)
SORT date DESC
```

## 📚 本周阅读进展

```dataview
TABLE
  author AS "作者",
  rating AS "评分",
  status AS "状态"
FROM ""
WHERE type = "book"
  AND (status = "active" OR (status = "complete" AND finished >= date(today) - dur(7 days)))
SORT file.mtime DESC
```

## ⏭️ 本周更新的项目

```dataview
TABLE
  next_action AS "下一步",
  completion + "%" AS "进度"
FROM "02 - PROJECTS"
WHERE type = "project"
  AND status = "active"
  AND file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```
