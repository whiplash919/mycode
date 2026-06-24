---
tags: [半导体, TPU, Google, AI芯片, 供应链]
created: 2026-06-24
source: Semi Doped
---

# Google TPU Chip Blueprint

## 规格对比表

| 项目 | TPU 8t | TPU v8e (TBD) | TPU v8p (TBD) | TPU v9 (TBD) |
|---|---|---|---|---|
| **代号** | A5921 / Zebrafish | A5922 / Humufish | Pumafish | Triggerfish |
| **量产时间** | 4Q26 | 4Q27 | 4Q27 | 2028 |
| **设计 — 计算** | Google | Google | **Broadcom** | Google |
| **设计 — I/O** | MediaTek | MediaTek | **Broadcom** | MediaTek |
| **设计 — 后端** | MediaTek | MediaTek | **Broadcom** | MediaTek |
| **计算晶圆制程** | 1×N3P | 2nm | 2nm | Unknown |
| **I/O 晶圆制程** | 1×N3P | 3nm / 336G SerDes | 3nm | 3nm / 336G SerDes |
| **先进封装** | CoWoS | EMIB | CoWoS/SoIC | Unknown |

---

## 关键洞察

### 1. 设计伙伴格局分裂

- **Google + MediaTek 组合**：负责 TPU 8t / v8e / v9 的全栈设计（计算 + I/O + 后端）
  - Google 主导计算核心，MediaTek 承接 I/O 与后端整合
- **Broadcom 独揽 TPU v8p**：计算、I/O、后端均由 Broadcom 完成
  - 意味着 Google 在同一代芯片上同时押注两条设计路线（v8e vs v8p），进行竞争性验证

### 2. 制程节点进化

```
TPU 8t  → N3P（台积电 3nm Plus）         — 现役最先进节点
TPU v8e → 2nm 计算 + 3nm I/O             — 台积电 N2，预计 2026 量产
TPU v8p → 同上（2nm / 3nm）              — 与 v8e 同制程，差异在设计方
TPU v9  → 计算节点未知，I/O 沿用 3nm     — 2028 时间窗，节点可能为 A14/N14
```

### 3. 封装技术路线多元化

| 封装 | 用途 | 优势 |
|---|---|---|
| **CoWoS**（台积电）| TPU 8t / v8p | HBM 集成成熟，良率高 |
| **EMIB**（英特尔）| TPU v8e | 异构 Chiplet 互联，成本较低 |
| **CoWoS/SoIC** | TPU v8p | 3D 堆叠，带宽最大化 |

> Google 在 v8e 上采用英特尔 EMIB 封装，是对台积电 CoWoS 产能紧张的主动分散，也是英特尔代工（IFS）赢得重要 AI 客户的信号。

### 4. 供应链受益者

| 公司 | 角色 | 影响 |
|---|---|---|
| **台积电** | N3P / 2nm / 3nm 晶圆代工 | 核心受益，几乎全线制造 |
| **MediaTek** | I/O + 后端设计服务（8t / v8e / v9）| 设计服务收入持续扩大 |
| **Broadcom** | v8p 全栈设计 | ASIC 设计业务量增加 |
| **英特尔** | EMIB 封装（v8e）| IFS 获得 Google AI 订单背书 |

### 5. 时间线与竞争含义

```
2026 Q4  TPU 8t      → 对标 NVIDIA Blackwell Ultra / AMD MI350X
2027 Q4  TPU v8e/v8p → 对标 NVIDIA Rubin / AMD MI400 系列
2028     TPU v9      → 节点与架构均未知，长期战略储备
```

- 两款 v8 同期推出（v8e 效率型 vs v8p 性能型）说明 Google 在数据中心内部将细分 AI 训练与推理工作负载
- v9 代号 "Triggerfish" 距今仍有 ~2 年，细节保密程度高

---

## 相关链接 & 标签

- [[半导体供应链]]
- [[台积电 N2 制程]]
- [[NVIDIA vs Google TPU 竞争]]
- [[Broadcom ASIC 设计业务]]
- [[MediaTek 设计服务]]
