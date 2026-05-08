---
type: index
created: 2026-05-08
---

# 会议纪要

按 **日历年 / 日历季度** 分层组织。文件名规范：`{TICKER}-{财季}.md`（财季按公司自身日历，可能与日历季不同）。

## 目录结构

```
会议纪要/
├── 2026/
│   ├── Q1/   ← 2026 年 1-3 月披露的财报会议纪要
│   ├── Q2/
│   ├── Q3/
│   └── Q4/
└── 2025/
    └── ...
```

## 当前内容

### 2026 / Q1（2026-04 ~ 2026-05 披露）

- [[LITE-Q3-FY26]] — Lumentum Holdings · 营收 8.084 亿美元 +90%、英伟达直投 20 亿美元到账
- [[ARM-Q4-FY26]] — Arm Holdings · 营收 14.9 亿美元 +20%、AGI CPU 需求 20 亿美元、2031 年目标 150 亿美元
- [[RKLB-Q1-2026]] — Rocket Lab · 营收 2.003 亿美元 +63.5%、积压订单 22 亿美元、史上最大单笔合同

## Frontmatter 字段约定

每份纪要以 YAML frontmatter 开头，便于 Obsidian Properties / Dataview 索引：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| ticker | 股票代码 | LITE |
| company | 公司中文名 | Lumentum |
| company_en | 公司英文全名 | Lumentum Holdings Inc |
| exchange | 交易所 | NASDAQ |
| fiscal_quarter | 财季 | Q3 FY26 |
| calendar_quarter | 日历季 | 2026-Q1 |
| report_date | 披露日期 | 2026-05-05 |
| period_end | 财季结束日 | 2026-03-28 |
| revenue | 营收 | 808.4M |
| yoy_growth | 同比增速 | +90% |
| tags | 主题标签 | [earnings-call, optical, AI-infra] |

## 模板与规范

完整模板见 `~/.claude/skills/earnings-call-digest/TEMPLATE.md`，写作规则见 `SKILL.md`。
