# 十八、阶段产物 → 销售资产 → CRM 字段映射

> 来自 `skills/gtm-strategy/SKILL.md` 的次要章节，按需 Read。


> 实战中最痛的是"产物在哪、谁负责、CRM 怎么对得上"。
> 下表给出"GTM 产物 → 销售资产库 → CRM 字段"三段映射，让产物可执行、可追踪、可治理。

### 产物落盘约定

```
workspace/gtm/<product>/
├── 00-prep/
│   ├── icp.md                    # ICP 客户画像
│   ├── scenarios.md              # 核心场景清单
│   ├── pain-map.md               # 痛点地图
│   ├── competitor-matrix.xlsx    # 竞品对比表
│   └── positioning.md            # 一句话定位 + 3 个卖点
├── 01-package/
│   ├── website-copy.md           # 官网文案
│   ├── sales-deck.pptx           # 销售 PPT
│   ├── solution-deck-<行业>.pptx # 行业解决方案 PPT
│   ├── whitepaper.md             # 技术白皮书
│   ├── demo-script.md            # Demo 脚本
│   ├── faq.md                    # 客户 FAQ
│   ├── pricing.xlsx              # 报价单
│   └── contract-template.docx    # 合同模板
├── 02-pilot/
│   ├── pilot-customers.xlsx      # 种子客户名单
│   ├── poc-template.md           # POC 标准方案模板
│   ├── poc-acceptance.md         # POC 验收标准
│   ├── feedback-log.xlsx         # 客户反馈记录
│   ├── objection-library.md      # 销售反对意见库
│   └── case-studies/             # 样板案例
├── 03-launch/
│   ├── launch-article.md         # 发布长文
│   ├── poster.png                # 产品海报
│   ├── landing-page.md           # 官网落地页文案
│   ├── demo-video-script.md      # Demo 视频脚本
│   ├── press-release.md          # 媒体稿
│   ├── sales-battlecard.md       # 销售作战表
│   ├── channel-kit.md            # 渠道传播包
│   └── launch-checklist.md       # 发布检查清单
├── 04-convert/
│   ├── lead-tiering.xlsx         # 线索分级（A/B/C）
│   ├── opportunity-pipeline.md   # 商机漏斗
│   ├── decision-chain-map.md     # 客户决策链图谱
│   ├── meddic-cards/             # 每个 A 类商机一张卡
│   ├── discovery-template.md     # 需求调研模板
│   ├── proposal-template.md      # 售前方案模板
│   ├── quote-template.xlsx       # 报价模板
│   └── contract-tracking.xlsx    # 合同与回款跟踪
└── 05-scale/
    ├── standard-solutions/       # 标准方案包
    ├── industry-playbooks/       # 行业打法
    ├── channel-policy.md         # 渠道政策
    ├── cs-sop.md                 # 客户成功 SOP
    ├── roadmap.md                # 产品 Roadmap
    └── quarterly-review.md       # GTM 季度复盘
```

### CRM 字段映射（销售可追踪）

| GTM 产物 | CRM 字段 | 责任人 | 更新频率 |
|---------|---------|--------|---------|
| 线索分级 | Lead Score / Lead Stage (A/B/C) | SDR | 实时 |
| ICP 匹配度 | ICP Fit Score | SDR + 销售 | 进入商机时 |
| MEDDIC 资格卡 | Custom Fields (M/E/D/D/I/C 6 项) | 销售 + 售前 | 每周 |
| 客户决策链 | Contacts 含角色字段（EB/TB/Champion） | 销售 | 每次拜访 |
| 商机阶段 | Opportunity Stage（线索 → 商机 → POC → 报价 → 合同 → 回款） | 销售 | 每阶段流转 |
| 销售周期天数 | Time-in-Stage | 销售运营 | 自动 |
| 赢单原因 | Win Reason / Loss Reason | 销售 | 商机关闭时 |
| 客户健康度 | Customer Health Score | CSM | 每月 |
| 续费 / 扩容机会 | Renewal Risk / Expansion Opportunity | CSM | 每季度 |

### 销售资产库结构（建议落到 SharePoint / 飞书 / 钉钉）

```
销售资产库/
├── 01-产品介绍/        # 阶段 1 产物
├── 02-行业解决方案/    # 按行业组织
├── 03-技术材料/        # 白皮书 / 架构图 / 部署方案
├── 04-客户案例/        # 阶段 2-5 沉淀
├── 05-竞品对比/        # Battle Card / 反对意见库
├── 06-商务材料/        # 报价 / 合同 / 法务文件
├── 07-销售工具/        # MEDDIC 卡 / Discovery 模板 / 提案模板
├── 08-培训材料/        # 新销售上手 / 月度培训
└── 09-合规资质/        # 等保 / 信创 / 行业资质
```

---

