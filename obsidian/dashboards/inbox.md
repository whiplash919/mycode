---
type: dashboard
tags: [dashboard, inbox]
---

# 📥 INBOX 处理面板

> 每日花 15 分钟把这里清空。
> 对每条笔记问：**类型？归属？独立成文还是并入已有？**

## 📋 INBOX 中所有笔记

```dataview
TABLE WITHOUT ID
  file.link AS "笔记",
  file.cday AS "创建日期",
  type AS "类型",
  tags AS "标签"
FROM "00 - INBOX"
SORT file.cday ASC
```

## 🆘 在 INBOX 超过 3 天的（需立即处理）

```dataview
LIST "**" + file.link + "** — 已停留 " + (date(today) - file.cday).days + " 天"
FROM "00 - INBOX"
WHERE file.cday <= date(today) - dur(3 days)
SORT file.cday ASC
```

## ❌ 没有 type 字段的（基础信息缺失）

```dataview
LIST
FROM ""
WHERE (type = null OR type = "")
  AND !contains(file.folder, "SYSTEM")
  AND !contains(file.folder, "ARCHIVE")
SORT file.mtime DESC
LIMIT 30
```

## ❌ 没有 status 字段的

```dataview
LIST
FROM ""
WHERE (status = null OR status = "")
  AND !contains(file.folder, "SYSTEM")
  AND !contains(file.folder, "ARCHIVE")
SORT file.mtime DESC
LIMIT 30
```

## 🏷️ 没有 tags 的（命中检索的关键）

```dataview
LIST
FROM ""
WHERE (tags = null OR length(tags) = 0)
  AND !contains(file.folder, "SYSTEM")
  AND !contains(file.folder, "ARCHIVE")
  AND !contains(file.folder, "daily")
SORT file.mtime DESC
LIMIT 30
```

---

## 处理三问（贴在屏幕上）

1. **这是什么类型？** → 决定顶层文件夹
2. **它已经有家了吗？** → 是否已有项目/主题关联？
3. **独立成文还是并入？** → 单条想法 → 并入已有笔记往往更好
