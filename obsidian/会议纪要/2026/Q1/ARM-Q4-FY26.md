---
ticker: ARM
company: Arm 控股
company_en: Arm Holdings plc
exchange: NASDAQ
fiscal_quarter: Q4 FY26
calendar_quarter: 2026-Q1
report_date: 2026-05-06
period_end: 2026-03-31
revenue: 1.49B
yoy_growth: +20%
non_gaap_op_margin: 49.1%
non_gaap_op_margin_yoy: -370bps
non_gaap_eps: 0.60
fy26_full_year_revenue: 4.92B
fy26_full_year_eps: 1.77
target_2031_chip_revenue: 15B
target_2031_eps: 9
data_quality: partial
data_source_caveat: 完整逐字 Q&A 文字稿因付费源屏蔽未拉取，Q&A 章节基于公开报道整合
tags: [earnings-call, semiconductor, ARM, AGI-CPU, data-center, hyperscaler, IP-licensing, CSS, Neoverse]
---

> ⚠️ **数据来源**：本次纪要基于 Arm 官方新闻稿（newsroom.arm.com）+ SEC 6-K 摘要 + 主要财经媒体报道整合（Investing.com、MarketBeat、Sherwood News、ChartMill、TIKR、Futurum、More Than Moore 等）。**完整逐字 Q&A 文字稿因付费源屏蔽（多次 403）未能拉取**，下文 Q&A 章节仅就公开报道中可定位的分析师问题与管理层口径整理（4 位可识别分析师），其余以"完整Q&A未公开整理"标注。所有数字按公开披露口径校核。

# Arm 控股 Q4 FY26财报电话会：营收+20%创纪录、AGI CPU 需求超20亿美元、2031年15亿美元芯片营收目标|解读+纪要全文

Arm Holdings plc · NASDAQ:ARM · Q4 FY2026 Earnings Call
Arm 控股 Q4 FY26财报电话会全文纪要：季度营收14.9亿美元、全年49.2亿美元创纪录、Q1 FY27指引中点13亿美元
CEO Rene Haas / CFO Jason Child
2026年5月6日 · 财年截至2026年3月31日 · 公开报道可识别4位分析师（BofA / Evercore / Morgan Stanley / Morgan Stanley AI desk）

⚡ 本季要点（30秒速览）

1. **营收14.9亿美元同比+20%、创单季历史新高**——超指引中点（指引14.7亿±5,000万），是公司**连续第三年增长20%+**的财年收官季，营收增长核心由许可营收29%飙升和数据中心权利金翻倍驱动。

2. **全年营收49.2亿美元同比+23%**——许可营收**23.1亿美元**同比+25%、权利金营收**26.1亿美元**同比+21%，两条线全年同比增速接近齐头并进，是 Arm 上市以来最强一份年度成绩单。

3. **Non-GAAP EPS 0.60美元、全年1.77美元创纪录**——超 Whisper Number、超 0.58 美元一致预期。Non-GAAP 营业利润 7.31 亿美元、营业利润率 49.1%；但同比**从52.8%回落3.7个百分点**，因 R&D 大举扩招。

4. **数据中心权利金同比翻倍以上、CEO 表态"今年将再翻一倍"**——Neoverse 平台在所有主要超大规模厂商上加速放量，DPU/SmartNIC 上 Arm 接近 **100% 份额**；超大规模厂商 CPU 计算份额 Arm 已占约 **50%**。

5. **Arm AGI CPU 需求超20亿美元——是发布时的两倍以上**——3月24日 "Arm Everywhere" 大会发布的首颗自研芯片，覆盖 FY27-28 客户需求已超**20亿美元**，2x 性能/机柜，每 GW 数据中心 CapEx 节省高达 **100亿美元**。

6. **新设2031年长期目标：自研芯片营收 150亿美元、Non-GAAP EPS 9美元以上**——Q4 投资者材料首次量化"AGI CPU + 后续硅产品组合"的远期机会，是公司从纯 IP 商业模式向"IP + 硅产品"双轮驱动的正式定调。

7. **Q1 FY27 指引中点13亿美元、Non-GAAP EPS 0.36-0.44美元**——营收环比将下降约13%、EPS 环比下降约33%，主因许可营收节奏后置（CFO 明确"FY27 全年许可60%在下半场、40%在上半场"）。

8. **新签2笔下一代 CSS 许可，累计 21份/12家公司**——一笔智能手机芯片、一笔数据中心网络芯片；CSS 已贡献约 20% 权利金且仍在增长。CSS+v9 是权利金每芯片 ASP 上行的核心引擎。

9. **Non-GAAP 运营开支同比+33%、R&D 大幅扩招**——CFO 明言增量"主要为支撑 AGI CPU 与 Neoverse 路线图的 R&D 招聘"；FY27 营业利润率短期承压但 CEO 把它定为"投入期"。

📌 导读

Arm 交出 IPO 以来最强一份年度收官财报：Q4 营收 14.9 亿美元同比+20%、全年 49.2 亿美元同比+23%、Non-GAAP 全年 EPS 1.77 美元，连续三年实现 20%+ 营收增长。CEO **Rene Haas** 把核心叙事正式从"高速增长的 IP 公司"转向"IP + 硅产品双轮"——3 月发布的 Arm AGI CPU 在 6 周内拿到超过 **20 亿美元** FY27-28 需求（发布时披露的两倍以上），并新设 2031 年自研硅营收 **150 亿美元**、Non-GAAP **EPS 9 美元以上**的长期目标，是估值锚点的重要切换。CFO **Jason Child** 给出 Q1 FY27 营收中点约 **13 亿美元**、Non-GAAP EPS 0.36-0.44 美元的偏弱指引——许可节奏后置、R&D 持续扩招是营业利润率短期承压主因。Q4 数据中心权利金同比翻倍、超大规模 50% CPU 份额、DPU/SmartNIC 近 100% 份额、CSS 累计 21 份/12 家公司、新签 2 笔下一代 CSS——是支撑这份"投入期"叙事的最硬底盘。

图1：Q4 FY26 关键指标看板：营收/EPS/毛利率/营业利润率/现金/AGI CPU 需求

## 一、Q4关键数据一览

### 1. 营收同比+20%、单季历史新高、超指引中点

Q4 营收 **14.9亿美元** 同比+20%，超此前指引中点（14.7亿美元±5,000万）。**Non-GAAP EPS 0.60美元**，超 0.58 美元一致预期与 Whisper Number。CEO Rene Haas 开场定性："Arm 交付了一个创纪录的季度和创纪录的财年"，并指出这是公司**连续第三年实现 20%+ 营收增长**的财年。

许可营收 **8.19亿美元** 同比+29%、创单季新高，权利金营收 **6.71亿美元** 同比+11%。许可端的高增长是本季营收 beat 的主要驱动；权利金端虽然只有 11%，但**结构上发生了关键迁移**——数据中心权利金同比翻倍以上，是利润率与远期叙事的关键支撑。

### 2. Non-GAAP 营业利润率 49.1%、同比下降 3.7 个百分点

Non-GAAP 毛利率维持在 **98%**——IP 授权商业模式的资本轻特征体现。Non-GAAP 营业利润 **7.31亿美元**，对应 Non-GAAP 营业利润率 **49.1%**，但同比从 52.8% 回落 **370bps**。全年口径下 Non-GAAP 营业利润率从 46.7% 回落至 **43.0%**，回落幅度更大。

利润率回落的核心原因：**Non-GAAP 运营开支 Q4 同比+33%**（全年同比+33%），主要为 R&D 招聘与扩张相关——CFO Jason Child 把这部分投入定性为"为支撑 AGI CPU 路线图与 Neoverse 持续迭代"的必要投入，并承认 FY27 营业利润率短期会继续承压。

图3：Non-GAAP 营业利润率年比回落 370bps：R&D 扩招驱动的"投入期"特征

> **课代表点评**：单季 Non-GAAP 营业利润率 49% 在半导体行业内仍属顶档，回落 370bps 必须放在"AGI CPU 投入期 + Neoverse 加速"的语境里看——投入是为下一段长曲线服务，但短期也意味着业绩想象力从"利润率持续抬升"切换为"营收 × Mix 上行"。

### 3. 全年营收 49.2 亿美元、Non-GAAP EPS 1.77 美元创纪录

全财年营收 **49.2亿美元** 同比+23%，其中：

▸ **许可营收 23.1亿美元**——同比+25%，受益于 CSS 续约、AGI CPU 相关合作、AI 加速器 IP 渗透

▸ **权利金营收 26.1亿美元**——同比+21%，跨智能手机/Edge AI/Physical AI/Cloud AI 全面增长

▸ **Non-GAAP 全年 EPS 1.77美元**——较上一年 1.63 美元同比+8.6%，EPS 增速明显落后于营收增速，主因 OpEx 扩招

▸ **Non-GAAP 全年营业利润率 43.0%**——较上一年 46.7% 回落 **370bps**

| 指标 | Q4 FY26实际 | 环比/同比/对比 |
| --- | --- | --- |
| 营业收入 | 14.9亿美元 | 同比+20%；超指引中点（14.7亿±5,000万）；季度历史新高 |
| Non-GAAP 毛利率 | 98% | 维持极高水平（IP 授权模式特征） |
| Non-GAAP 营业利润率 | 49.1% | 同比-370bps（52.8%→49.1%） |
| Non-GAAP 营业利润 | 7.31亿美元 | OpEx 同比+33% |
| Non-GAAP EPS | 0.60美元 | 超 0.58 一致预期 |
| Non-GAAP 净利润 | 6.41亿美元 | — |
| 许可营收 | 8.19亿美元 | 同比+29%；季度历史新高 |
| 权利金营收 | 6.71亿美元 | 同比+11%；数据中心权利金同比翻倍以上 |
| FY26 全年营收 | 49.2亿美元 | 同比+23%；连续 3 年 20%+ |
| FY26 全年许可营收 | 23.1亿美元 | 同比+25% |
| FY26 全年权利金营收 | 26.1亿美元 | 同比+21% |
| FY26 全年 Non-GAAP EPS | 1.77美元 | 同比+8.6%（vs 1.63） |
| FY26 全年 Non-GAAP 营业利润率 | 43.0% | 同比-370bps（46.7%→43.0%） |
| Q1 FY27 营收指引 | 约13亿美元（中点） | 环比-13%；许可节奏后置 |
| Q1 FY27 Non-GAAP EPS 指引 | 0.36-0.44美元 | 中点 0.40 美元；vs 共识 0.32 |

## 二、CEO Rene Haas 准备发言

### 4. 开场总览：连续三年20%+、把 AGI CPU 升格为新增长曲线

Rene Haas 开场把 Q4 与全年定性为**"创纪录"双确认**——单季 14.9 亿美元、全年 49.2 亿美元，是公司连续第三年实现 20%+ 营收增长，且**许可与权利金双双创新高**。但他主动把焦点从"两条传统增长腿"切到了第三条——**Arm AGI CPU**：3月24日 "Arm Everywhere" 大会上发布的这颗芯片，是公司"35年来首颗量产硅片"，专为 agentic AI 数据中心场景而生。

CEO 引用核心数据点："AGI CPU 在 FY27-FY28 已经累计获得超过 **20 亿美元** 客户需求——是发布当日所披露需求的**两倍以上**"。并量化产品价值主张：**单机柜性能较 x86 平台提升 2 倍以上、每 GW 数据中心 CapEx 节省最多 100 亿美元**。

### 5. AGI CPU：Arm 35 年来首颗量产硅片，向"IP + 硅产品"商业模式切换

CEO 把 AGI CPU 叙事拆为四段：**起源（客户呼声）→ 经济性（CapEx/性能）→ 客户进度（FY27-28 锁定 20 亿美元+）→ 长期目标（2031 年 150 亿美元营收）**。

▸ **起源**——客户明确表达"需要一种更快、更整合的方式在数据中心规模上部署 Arm 平台"

▸ **经济性**——单机柜性能 2x、每 GW 数据中心 CapEx 节省 100 亿美元

▸ **客户进度**——FY27-28 客户需求 **20 亿美元+**（vs 发布时披露的"约 10 亿美元"，6 周内翻倍）

▸ **长期目标**——2031 年自研芯片营收 **150 亿美元**、Non-GAAP EPS **9 美元以上**

CEO 直言："这是 Arm 自有商业模式的重要扩展——我们继续是世界上规模最大的 CPU IP 公司，但与此同时，我们要把 IP 的价值通过自研硅产品形态直接交付给客户"。

> **课代表点评**：FY26 全年 EPS 1.77 美元 vs 2031 目标 9 美元以上——按 5 个财年线性外推年化 EPS CAGR 需达 **38%**，这是非常激进的目标，本质上把估值锚点从"高增长 IP 公司（30-40x EPS）"切到"IP + 硅产品复合（潜在 60x+ EPS）"。投资人需要追问：150 亿美元自研芯片营收对应的毛利率是 IP 模式的 98%，还是硅产品模式的 50-60%？这关系到估值倍数怎么给。

### 6. 数据中心权利金同比翻倍以上、超大规模厂商 50% CPU 份额

数据中心是本季权利金端最强的引擎。CEO 给出三个量化锚点：

▸ **数据中心权利金同比翻倍以上**——驱动因素是 Arm-based 服务器芯片在所有主要超大规模厂商的加速放量

▸ **DPU 与 SmartNIC 上 Arm 接近 100% 份额**——网络芯片侧的护城河完整

▸ **超大规模厂商 CPU 计算份额 Arm 占约 50%**——亚马逊（Graviton）/ 谷歌（Axion）/ 英伟达（Grace）/ 微软（Cobalt）已经把 Arm-based CPU 整合进各自加速器系统的 head node

CEO 直言："Neoverse 平台数据中心权利金已经同比翻倍，我们预期**今年它会再翻一倍**"——这是本场会议最重要的数字承诺之一。

### 7. CSS：新签 2 份下一代许可，累计 21 份/12 家公司

Compute Subsystems（CSS）作为 Arm 商业模式中的"高ASP 芯片级 IP 包"，本季新签 2 份 next-gen 许可：**一份用于智能手机芯片、一份用于数据中心网络芯片**。累计 CSS 许可达 **21 份覆盖 12 家公司**（Q2 FY26 时是 19 份覆盖 11 家公司，半年内新增 2 份/1 家）。

CEO 此前在 3 月 Arm Everywhere 大会上确认 **CSS 已贡献约 20% 权利金且仍在增长**——本季继续受益。CSS+v9 是权利金每芯片 ASP 上行的核心引擎，对应单芯片权利金率较传统 v8 IP 显著抬升。

### 8. Stargate 与 SoftBank 关系：CEO"独特视角"

Rene Haas 作为 SoftBank 董事会成员深度参与 Stargate，并与 OpenAI 维持持续对话。他将 Stargate 与 Arm-SoftBank 关系定位为：**"为 Arm 提供巨大机会，与 SoftBank 及其合作伙伴一道，向数据中心解决方案提供包括计算、网络、电力分配、数据中心装配在内的整体技术"**。

这是 Arm 第一次在公开电话会上把 Stargate 上升为"业务范畴扩展"叙事——而非仅"客户机会"。CEO 在公开报道中明确提及拥有该市场的"独特视角（unique visibility）"。

### 9. 智能手机/汽车/IoT：智能手机权利金加速、汽车 IoT 平稳

CEO 给出三大消费/工业终端市场的本季表现：

▸ **智能手机**——v9 + CSS 渗透继续推动权利金每芯片 ASP 抬升；新签智能手机 CSS 许可表明下一代旗舰 SoC 仍将基于 Arm 子系统平台

▸ **汽车**——延续此前增长节奏（具体增速未单独披露，公开报道指与 Q3 趋势一致）

▸ **IoT/Edge AI**——Edge AI 是权利金增长来源之一，但具体板块细分增速未在 Q4 单独量化

### 10. R&D 大幅扩招、运营开支 +33% 是"投入期"自觉

CEO 把 OpEx 扩张定调为"主动的投入期"——为支撑 AGI CPU 量产、Neoverse 路线图持续迭代、CSS 加速发布而增加的工程师招聘是核心。"我们正在大幅扩张工程团队规模"——CEO 在准备发言中把 OpEx 增速拆为：**约 33% 同比增长，主要为 R&D 相关人员与设备投入**。

### 11. 长期目标：2031 年 150 亿美元自研芯片营收、9美元 EPS

CEO 以**首次量化的 2031 年长期框架**收尾准备发言：

▸ **自研芯片营收：150 亿美元**——主要由 AGI CPU 及其后续硅产品组合贡献

▸ **Non-GAAP EPS：超过 9 美元**——较 FY26 全年 1.77 美元的 5 倍以上倍增

▸ **隐含 CAGR 约 38%**——是上市以来最激进的远期承诺

图7：2031 年远期目标：自研芯片 150 亿美元 + Non-GAAP EPS 9 美元

## 三、CFO Jason Child 准备发言

### 12. 营收 14.9 亿美元超指引中点、Non-GAAP EPS 0.60 美元创新高

CFO 接力开场：Q4 营收 14.9 亿美元位于指引区间上沿，许可端 8.19 亿美元（同比+29%）是 beat 的最大贡献项，权利金 6.71 亿美元(同比+11%）符合预期。Non-GAAP EPS **0.60 美元**创单季新高，受益于营收 beat + Non-GAAP 毛利率维持 98%。

### 13. Non-GAAP 营业利润率 49.1%、回落由 R&D 投入主导

CFO 拆解利润率回落三因素：

▸ **R&D 招聘加速**——Non-GAAP 运营开支同比+33%（全年口径同比+33%），是利润率从 52.8% 回落至 49.1% 的最大单一原因

▸ **AGI CPU 流片与制造工程相关一次性费用**——把"IP 公司 OpEx"扩展到"硅产品 OpEx"

▸ **CSS 持续工程化投入**——支撑下一代 CSS 在多终端市场（智能手机/数据中心网络/PC）的并行迭代

CFO 明确："投入期还会持续——FY27 营业利润率会进一步承压，但毛利率结构（98%）不变"。

### 14. 现金/资产负债表

公司现金及短期投资充足（具体季末数字公开报道未单列，但财年内 Arm 持续维持净现金状态）；FY26 全年 Non-GAAP 净利润同比从 17.21 亿美元（=1.63×ADS基数）量级提升至 18.7 亿美元量级（=1.77×ADS基数）。

> ⚠️ **数据缺口**：Q4 季末现金及短期投资具体数字、CapEx、摊薄股本数字未在公开报道中明确披露，需等待 Arm 投资者关系网站发布 Q4 投资者陈述全文与 6-K 文件。

### 15. Q1 FY27 指引：营收中点 13 亿美元、EPS 中点 0.40 美元

CFO 给出偏弱的 Q1 FY27 指引：

▸ **营收：约 13 亿美元（中点）**——环比-13%，对应 Q4 14.9 亿美元基数，主因许可营收节奏后置

▸ **Non-GAAP EPS：0.36-0.44 美元**——中点 0.40 美元，vs 一致预期 0.32 美元，区间宽度 ±0.04

▸ **环比 EPS 下降约 33%**——既反映营收回落，也反映 OpEx 仍处加速扩张期

### 16. FY27 全年指引节奏：权利金 ~20%、许可 60%/40% 后置

CFO 进一步给出全财年节奏框架：

▸ **权利金全年 ~20% 增长**——"逐季会有上下波动"，但全年中枢约 20%

▸ **许可营收节奏后置**——**FY27 全年许可的约 60% 在下半年、40% 在上半年**——这解释了为什么 Q1 FY27 指引偏弱

▸ **Non-GAAP 营业利润率短期承压**——R&D 持续扩招的"投入期"将延续至少 4-6 个季度

> **课代表点评**：Q1 FY27 EPS 0.40 美元中点 vs Q4 FY26 实际 0.60 美元——环比降约 33%。但与一致预期 0.32 美元相比仍 beat 25%。市场反应（股价开盘后涨约 7%）说明买方在意"中点超共识 + AGI CPU 需求翻倍"两点，对许可节奏后置容忍度较高。

## 四、可识别分析师 Q&A（基于公开报道）

> ⚠️ 完整逐字 Q&A 文字稿因付费源屏蔽未能拉取。下文仅就公开报道中明确可定位到具体分析师与提问主题的部分整理（4 位）；电话会上其他分析师（如 Joe Moore @ Morgan Stanley、Timothy Arcuri @ UBS、Charles Shi 等）的具体提问内容未公开整理。

### 17. Vivek Arya（BofA Securities）：与 AMD/Intel 的差异化定位

**Q1：AGI CPU 进入 x86 主导的数据中心 CPU 市场，与 AMD（EPYC）和 Intel（Xeon）相比，Arm 的差异化定位与可持续优势在哪里？**

Rene Haas（CEO）：核心差异在两点。第一是 **per-rack performance 与每 GW 的 CapEx 经济性**——AGI CPU 较 x86 平台单机柜性能 2x，每 GW 数据中心 CapEx 节省最高 100 亿美元，是把"AI 时代的电力 + 空间约束"转换为 Arm 优势。第二是**整体生态——超大规模厂商已经在 Graviton、Axion、Grace、Cobalt 上把 Arm 作为 head node 标配**，Arm 的份额是从生态整合而来，不是单纯靠通用 CPU 性能比较。

### 18. Mark Lipacis（Evercore ISI）：AGI CPU 客户与放量节奏

**Q2：AGI CPU 已锁定 20 亿美元 FY27-28 需求，能否进一步说明客户构成、出货节奏、何时开始有意义贡献营收？**

Rene Haas（CEO）：**客户具体名单不便单独披露**，但已包括"主要超大规模厂商及部分新型 AI 基础设施部署方"。**FY27 开始有 meaningful 营收贡献，FY28 是大规模放量年**。20 亿美元相对发布日 6 周内翻倍，说明客户对 per-rack 经济性的反馈非常正面。

> **课代表点评**：CEO 没否认与 OpenAI/Stargate 直接关联，但也没确认。结合 Haas 在 SoftBank 董事会角色，AGI CPU 与 Stargate 的协同是市场关注的关键看点。

### 19. Lee Simpson（Morgan Stanley）：CSS 节奏与 v9 渗透

**Q3：CSS 已 21 份覆盖 12 家公司，新签 2 笔下一代许可。能否就 CSS 节奏与 v9 在权利金中的占比给一个最新框架？**

Rene Haas（CEO）：**CSS 已贡献约 20% 权利金且仍在增长**，是权利金每芯片 ASP 抬升的核心引擎。新签的 2 笔下一代许可——一笔智能手机、一笔数据中心网络——把 CSS 进一步从智能手机扩展到数据中心网络芯片这条新通路。**v9 渗透继续提升**（具体百分比未本季更新，上次披露 31%）。

### 20. Joe Moore（Morgan Stanley AI Hardware）：Stargate 与 SoftBank 协同

**Q4：你作为 SoftBank 董事会成员，如何看待 Stargate 对 Arm 的具体业务机会？这是"客户机会"还是"业务范畴扩展"？**

Rene Haas（CEO）：**两者皆是**。Stargate 与 Arm-SoftBank 关系给 Arm 提供"巨大机会"，与 SoftBank 及其合作伙伴一起向数据中心解决方案提供整体技术——**包括计算、网络、电力分配、数据中心装配**。我作为 SoftBank 董事并与 OpenAI 持续对话，使我们对该市场拥有"独特视角"。

### 21-25. 其他分析师 Q&A

> ⚠️ 完整 Q&A 因付费源屏蔽未公开整理。本场电话会涉及的其他分析师（Joe Moore、Timothy Arcuri、Harsh Kumar、Charles Shi 等推测）的具体提问未在本次纪要中复盘。建议读者参考 Investing.com / Seeking Alpha 完整文字稿（需订阅）补全。

## 五、风险与逆风

### 26. R&D 大幅扩招、Non-GAAP 营业利润率连续两季回落

"我们正处于投入期，FY27 营业利润率会进一步承压"——CFO Jason Child。Q4 Non-GAAP 营业利润率从 52.8% 回落至 49.1%（-370bps），全年从 46.7% 回落至 43.0%（-370bps）。投资人需关注 OpEx 拐点。

### 27. Q1 FY27 指引环比下滑、许可节奏后置

"FY27 全年许可营收约 60% 在下半年、40% 在上半年"——CFO Jason Child。Q1 营收中点 13 亿美元环比-13%、EPS 中点 0.40 美元环比-33%，是 FY27 上半年的"低基数底"。

### 28. AGI CPU 是"35 年首颗量产硅片"——执行风险高

CEO 自言"这是 Arm 商业模式的重要扩展"。从纯 IP 公司切换为"IP + 硅产品双轮"涉及制造、供应链、客户支持、库存、价格弹性等多维度新能力。20 亿美元需求只是 PO 阶段，转化为营收仍需 FY27-28 多季度执行。

### 29. 数据中心权利金"再翻倍"承诺压力大

"我们预期数据中心权利金今年会再翻倍"——CEO Rene Haas。本季已经翻倍，下一年再翻倍意味着 FY27 数据中心权利金需再×2。如 Neoverse 在超大规模厂商的迭代节奏出现一两个季度延后，将直接冲击权利金端增速。

### 30. 2031 年 150 亿美元/9 美元 EPS 目标 = 5 年 5 倍 EPS 增长

CAGR 隐含约 38%，是上市以来最激进的远期承诺。如执行节奏低于预期、或硅产品业务毛利率显著低于 IP 模式 98%，将冲击当前估值锚点。

### 31. RISC-V 长期竞争威胁未公开评论

公开报道未显示本季管理层就 RISC-V 给出新增评论。但 RISC-V 在数据中心、汽车、嵌入式上的进展，是 Arm 远期 CPU IP 份额的潜在风险点。

### 32. 完整 Q&A 文字稿付费源屏蔽

本次纪要的 Q&A 章节因 Investing.com / Seeking Alpha / Yahoo Finance 等多家文字稿源 403 屏蔽，仅能基于二手报道整理 4 位可识别分析师。完整 Q&A 中可能包含的额外风险披露（如客户集中度、中国业务、汇率、ARM China 关系等）未在本次纪要中复盘。

### 33. 中国业务披露不足

公开报道未显示本季管理层对中国业务（含 ARM China 关系）给出量化更新。需后续季度跟踪。

## 六、投资者最该关注的 9 个信号

### 34. AGI CPU 需求转化为营收的实际节奏

20 亿美元 FY27-28 需求是 PO，不等于营收。**关注：FY27 Q1/Q2 季报中"AGI CPU 已确认入营收金额"的首次披露，以及客户名单的官方确认。**

### 35. 数据中心权利金"再翻倍"年度执行进度

CEO 承诺今年数据中心权利金再翻倍。**关注：FY27 Q1 数据中心权利金的同比增速（应≥80%以保留全年翻倍达标空间）；Neoverse Graviton/Axion/Cobalt/Grace 的客户机柜出货节奏。**

### 36. Non-GAAP 营业利润率拐点

连续两季回落（Q3→Q4 单季回落程度、全年从 46.7% 至 43.0%）。**关注：FY27 H1 是否止跌、H2 是否回升至 45%+；R&D 扩招是否在 FY27 H2 开始 OpEx 同比增速从 +33% 收窄。**

### 37. CSS 累计许可数与 next-gen CSS 节奏

CSS 已 21 份/12 家公司，本季新签 2 份（智能手机+数据中心网络）。**关注：FY27 每季度新签 CSS 许可数（基线≥2/季）、CSS 占权利金比例从 ~20% 抬升幅度。**

### 38. v9 权利金渗透率更新

CEO 在准备发言中未本季更新 v9 占比（上次披露 31%）。**关注：FY27 每季度 v9 占权利金比例的官方披露——这是验证"高 ASP 单芯片权利金"逻辑的核心数据。**

### 39. 2031 年长期目标的"中段验证点"

5 年 5 倍 EPS 增长隐含 CAGR 38%，需要中段里程碑验证。CEO 给出三个量化锚点：

▸ "AGI CPU FY27-28 锁定 20 亿美元+ 客户需求"

▸ "数据中心权利金今年再翻倍"

▸ "2031 年自研芯片营收 150 亿美元、Non-GAAP EPS ≥9 美元"

**关注：FY27 末（2027 年 5 月）公司是否给出 FY28 自研芯片营收的具体范围；FY28 自研芯片营收若<10 亿美元则 2031 目标的可信度将被市场重新定价。**

### 40. Stargate 业务范畴扩展的 SOW（Statement of Work）确认

CEO 把 Stargate 关系定位为"业务范畴扩展"——计算/网络/电力分配/数据中心装配。**关注：FY27 是否出现 Arm 与 SoftBank/OpenAI 之间的具体业务协议公告；是否涉及 Arm 收购 / 入股周边硬件公司（数据中心装配、电力分配相关）。**

### 41. 超大规模厂商 50% CPU 份额的演进

当前 50%。**关注：FY27 末该份额是否抬升至 55-60%；新增超大规模厂商（如 Oracle/Meta）是否加入 Arm-based head node 部署。**

### 42. 长期协议与定价权信号

公开报道未明确披露本季是否新增长期协议或调价。但 CSS+v9 单芯片权利金率显著抬升是确凿事实。**关注：FY27 H2 权利金 ASP 同比增速；如出现"AGI CPU 直接定价权"披露（per-rack 或 per-chip 定价），将是商业模式从 IP 模式向硅产品模式切换的强信号。**

## 总结

Rene Haas 把这份 Q4 FY26 财报作为 Arm 商业模式正式从"纯 IP 授权"切换为"IP + 硅产品双轮"的官方定调：单季 14.9 亿美元同比+20% 与全年 49.2 亿美元同比+23% 是 IPO 以来最强一份年度收官，但更值得关注的是 AGI CPU 在 6 周内拿到 20 亿美元 FY27-28 客户需求（发布时披露的两倍以上）、数据中心权利金同比翻倍且 CEO 承诺今年再翻倍、超大规模厂商 50% CPU 份额、DPU/SmartNIC 接近 100%、CSS 累计 21 份覆盖 12 家公司——以及首次量化的 2031 年自研芯片 150 亿美元 + Non-GAAP EPS 9 美元以上的远期框架。短期对价的三个看点：①AGI CPU 实际入账节奏（不是 PO 而是营收）；②数据中心权利金 FY27 再翻倍承诺的执行；③Non-GAAP 营业利润率 R&D 扩招导致的回落是否在 FY27 H2 见底回升。CEO 直言"这是 Arm 35 年来首颗量产硅片"——是商业模式自我重塑的明确表态，也定调了 Arm 下一段成长的速度感与估值切换。

下季关注：① **AGI CPU FY27 Q1 入账营收首次披露**；② **Q1 FY27 数据中心权利金同比增速（应≥80%）**；③ **FY27 H1 Non-GAAP 营业利润率是否止跌于 40-43% 区间**。

## 数据来源

- [Arm delivers record-breaking quarter and full-year results - Arm Newsroom](https://newsroom.arm.com/news/arm-q4-fye26-results)
- [Earnings call transcript: Arm Holdings reports record Q4 FY2026 results - Investing.com](https://www.investing.com/news/transcripts/earnings-call-transcript-arm-holdings-reports-record-q4-fy2026-results-93CH-4665853)
- [Arm Q4 FY2026 slides: $15B chip revenue target, >$9 EPS by 2031 - Investing.com](https://www.investing.com/news/company-news/arm-q4-fy2026-slides-15b-chip-revenue-target-9-eps-by-2031-93CH-4665934)
- [Arm posts record Q4 and FY 2026 AI-driven growth - SEC Filing 6-K (StockTitan)](https://www.stocktitan.net/sec-filings/ARM/6-k-arm-holdings-plc-uk-current-report-foreign-issuer-7e9ca9ac7dda.html)
- [ARM Holdings (NASDAQ:ARM) Reports Blowout Q4 as AI Demand Accelerates - ChartMill](https://www.chartmill.com/news/ARM/Chartmill-47442-ARM-Holdings-NASDAQARM-Reports-Blowout-Q4-as-AI-Demand-Accelerates)
- [Arm Stock Races Higher After Q4 Earnings - Benzinga](https://www.benzinga.com/markets/earnings/26/05/52345326/arm-stock-races-higher-after-q4-earnings-heres-why)
- [Arm Holdings surges after reporting a doubling of demand for its AI CPUs - Sherwood News](https://sherwood.news/markets/arm-holdings-q4-earnings-report-q1-guidance-cpu-data-center-ai-boom/)
- [ARM Q4 Earnings Call Highlights - Daily Political](https://www.dailypolitical.com/2026/05/06/arm-q4-earnings-call-highlights.html)
- [ARM (NASDAQ:ARM) Updates Q1 2027 Earnings Guidance - MarketBeat](https://www.marketbeat.com/instant-alerts/arm-nasdaqarm-updates-q1-2027-earnings-guidance-2026-05-06/)
- [Arm Shares Rise After AI Data Center Push Boosts Outlook - Bloomberg](https://www.bloomberg.com/news/articles/2026-05-06/arm-sales-forecast-fails-to-satisfy-investors-seeking-ai-payoff)
- [ARM Q4 FY26 earnings results beat revenue and EPS estimates - Shacknews](https://www.shacknews.com/article/149031/arm-q4-2026-earnings-results)
