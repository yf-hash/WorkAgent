---
name: pm-competitive-intel
description: 竞品情报采集方法论 — 供 /pm-competitive-scan 命令调用。含竞品发现方法（直接/间接/替代/自建 四类）、信源清单（官网/定价页/文档/Changelog/G2/Reddit/播客）、抓取规则、元信息抽取、情报可信度分级。
user-invocable: false
---

# pm-competitive-intel — 竞品情报采集工具箱

> 本 skill 被 `/pm-competitive-scan` 命令调用。

## 一、竞品发现方法（四类竞品）

不要只盯"同类型商用产品"，要把四类都覆盖：

| 类型 | 定义 | 举例（假设我方是 AI 写作助手） |
|---|---|---|
| **直接竞品** | 相同定位 + 相同目标用户 | Jasper / Copy.ai / Writesonic |
| **间接竞品** | 部分能力重叠 + 用户可选择 | ChatGPT / Claude / Notion AI |
| **替代方案** | 用户可能选择的非同类方案 | 雇佣写手 / 用模板 / 不做 |
| **自建方案** | 用户可能自己拼装的方案 | OpenAI API + Prompt 库 |

### 发现清单来源
1. **用户提及**（客户访谈 / 销售反馈）
2. **搜索引擎**（关键词 + "vs" / "alternatives" / "compare"）
3. **应用商店**（Chrome Web Store / App Store / GitHub Trending）
4. **行业评测**（G2 / Capterra / Gartner / IDC）
5. **社区讨论**（Reddit / Hacker News / V2EX / 知乎）
6. **投融资信息**（Crunchbase / IT 桔子 / 36Kr）

## 二、信源清单（按可信度分级）

### 🟢 高可信度（官方一手）
| 信源 | 抓什么 |
|---|---|
| 竞品官网 | 定位 slogan / 价值主张 / 主要能力 / 客户 case |
| 定价页 | 套餐结构 / 单价 / 计费维度 / 免费额度 |
| 产品文档 | 功能全清单 / API 能力 / 集成 |
| Changelog / Release Notes | 迭代节奏 / 最新方向 / 弃用功能 |
| 公司博客 | 战略方向 / 大客户案例 / GTM 叙事 |
| 官方视频 / Demo | 用户体验 / 界面 / 交互 |

### 🟡 中可信度（第三方评测）
| 信源 | 抓什么 |
|---|---|
| G2 / Capterra | 用户评分 + Top 3 / Bottom 3 特性 |
| Gartner / Forrester | 象限位置 / 分析师评价 |
| 独立评测博客 / Product Hunt | 使用感受 / 与竞品对比 |
| 第三方对比页 | 各厂商横向对比 |

### 🟠 中低可信度（社区口碑）
| 信源 | 抓什么 |
|---|---|
| Reddit / HN / V2EX | 用户抱怨 / 真实使用体验 / 隐藏坑 |
| Twitter / X / 微博 | 官方动态 / 用户情绪 |
| 播客 / YouTube | 创始人访谈 / 战略陈述 |
| 招聘信息 | 团队规模 / 技术栈 / 战略方向 |

### 🔴 低可信度（内部传闻）
| 信源 | 抓什么 |
|---|---|
| 销售同事口述 | 客户主观评价 |
| 前员工 LinkedIn | 内部动态（需交叉验证） |
| 内部销售培训材料 | 官方话术（未必客观） |

## 三、抓取规则

### 单个竞品情报卡（结构化 JSON）

```json
{
  "competitor": {
    "name": "Jasper",
    "type": "direct",
    "url": "https://jasper.ai",
    "discovered_at": "2026-08-27",
    "confidence": "high"
  },
  "positioning": {
    "slogan": "AI Content Platform for Enterprise",
    "target_audience": ["Marketing teams", "Enterprise"],
    "value_prop": "生成高质量、品牌一致的内容"
  },
  "pricing": {
    "model": "seat + credit",
    "tiers": [
      { "name": "Creator", "price_per_month_usd": 39, "features": [...] },
      { "name": "Pro", "price_per_month_usd": 59, "features": [...] },
      { "name": "Business", "price": "custom", "features": [...] }
    ],
    "free_tier": true,
    "free_tier_limit": "7 天试用"
  },
  "capabilities": {
    "core": ["长文生成", "品牌语气训练", "SEO 优化"],
    "unique": ["Brand Voice", "Knowledge Base"],
    "integrations": ["Chrome Extension", "Google Docs", "Zapier"]
  },
  "tech": {
    "underlying_model": "GPT-4 + 自研 fine-tune",
    "deployment": "SaaS only",
    "api_available": true
  },
  "traction": {
    "customers_claimed": "100000+",
    "notable_clients": ["Airbnb", "IBM", "HP"],
    "funding": "$125M Series A (2022)",
    "valuation": "$1.5B"
  },
  "community_signals": {
    "g2_rating": 4.7,
    "g2_reviews_count": 1234,
    "top_complaints": [
      "价格贵",
      "生成质量不稳定",
      "定制学习曲线陡"
    ],
    "top_praises": [
      "Brand Voice 好用",
      "长文生成质量高"
    ]
  },
  "recent_changes": [
    { "date": "2026-08", "change": "推出 Jasper Studio (v3)" },
    { "date": "2026-06", "change": "收购 Content Marketing 工具 XX" }
  ],
  "gaps_observed": [
    "缺乏中文支持",
    "对亚太市场投入少",
    "无私有部署方案"
  ]
}
```

## 四、元信息抽取规则

### 定位（Positioning）
- 从官网 hero + 关于页
- 一句 slogan + 三个价值主张

### 定价（Pricing）
- 计费模式（seat / usage / hybrid / flat / freemium）
- 套餐档位（数量 + 单价）
- 计费维度（用户数 / 生成量 / API 调用 / 存储）
- 免费额度是否存在

### 能力（Capabilities）
- **核心能力**：官网 hero 提到的
- **独有能力**：竞品有而我方没有的
- **通用能力**：大家都有的（不重要）

### 客户（Traction）
- 客户 logo 墙
- 具体客户案例
- 用户数 / 营收（如披露）
- 融资信息

## 五、情报可信度分级

对每条采集到的信息打标：

| 级别 | 判定 | 处理 |
|---|---|---|
| 🟢 高 | 官方一手 + 有出处 | 直接引用 |
| 🟡 中 | 三方评测 + 有交叉 | 引用 + 注明出处 |
| 🟠 低 | 单一来源 / 无法验证 | 加"据报道"限定 |
| 🔴 极低 | 传闻 / 竞品刻意宣传 | 不用 or 标"待验证" |

**规则**：任何写入正式报告的信息，必须来自 🟢 或 🟡；🟠 需注明；🔴 不用。

## 六、常见采集陷阱

| 陷阱 | 症状 | 修正 |
|---|---|---|
| 只看官网自说自话 | 全是营销词 | 交叉 G2 / Reddit 真实反馈 |
| 忽略间接竞品 | 只列同类型 | 强制四类都填 |
| 定价页只看首档 | 只报"$9/月" | 列完整套餐结构 + 单价维度 |
| 用旧数据 | 引用 2 年前融资 | 时间戳 + 优先近 12 个月 |
| 把宣传当能力 | "AI 驱动" 也算能力 | 只算具体功能 |

## 七、采集频率建议

| 场景 | 频率 |
|---|---|
| 首次立项 | 一次深度 |
| 季度规划前 | 全量刷新（重跑 /pm-competitive） |
| 上线前 | 目标竞品刷新 |
| 客户投标前 | 客户可能对比的竞品刷新 |
| 常态 monitor | 每月轻量更新（新 Changelog / 大新闻） |

## 八、反模式

- ❌ 只列 3 家直接竞品 —— 违规，四类都要覆盖
- ❌ 采集信息不标可信度 —— 违规
- ❌ 引用 🔴 传闻 —— 违规
- ❌ 定价只报单一数字 —— 违规，套餐结构才是关键
- ❌ 情报卡不做结构化 —— 违规，下游 skill 依赖 JSON
