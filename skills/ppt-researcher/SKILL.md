---
name: ppt-researcher
description: >
  PPT专用多源内容搜集与归纳技能。触发词：PPT研究、内容搜集、资料调研、PPT素材、
  研究报告生成、多源搜索、官方媒体学术产业搜集。
  覆盖官方/媒体/学术/产业/社区五大渠道，输出结构化PPT素材包（大纲+数据+引用+案例）。
user-invocable: false
effort: high
---

# PPT Researcher — PPT专用多源内容搜集技能

## 职责

为 PPT 全流程生成提供高质量内容基础，覆盖官方、媒体、学术、产业实践、社区五大渠道，
输出经过整理、去重、验证的结构化素材包，供后续大纲设计和PPT制作直接使用。

---

## 搜索渠道矩阵

### 渠道1：官方权威来源

```
政府与监管机构
  ├── 中国：国务院、各部委官网、发改委报告、工信部白皮书
  ├── 美国：White House/FTC/FDA/SEC官方报告
  ├── 欧盟：European Commission/GDPR相关
  └── 关键词策略：site:gov.cn OR site:gov  [主题] report/white paper/policy

国际组织
  ├── 联合国体系：UN/WHO/UNESCO/FAO/IMF/World Bank
  ├── 标准组织：ISO/IEEE/IETF/NIST
  └── 智库：WEF/Brookings/RAND/CSIS

企业官方
  ├── 上市公司年报（10-K/20-F/年度报告）
  ├── 投资者关系页（IR）、业绩发布会实录
  ├── 官方博客/工程师博客（技术细节）
  └── 产品文档/技术白皮书
```

### 渠道2：媒体报道

```
财经与主流媒体
  ├── 全球：Reuters、Bloomberg、Financial Times、Wall Street Journal
  ├── 中国：财新、第一财经、界面、经济观察报、21世纪经济报道
  └── 搜索策略：过去2年内，带有具体数据的深度报道

科技与行业媒体
  ├── 技术类：MIT Technology Review、Wired、The Verge、TechCrunch
  ├── 中文技术：36氪、虎嗅、少数派、InfoQ中文
  ├── 学术科普：Quanta Magazine、Nature News
  └── 行业垂直媒体（按主题选择对应垂直媒体）

新闻发布与公告
  ├── PR Newswire、Business Wire、Globe Newswire
  ├── 企业公告汇总（CIK/SEC EDGAR）
  └── 发布会/峰会回顾报道
```

### 渠道3：学术研究

```
论文搜索引擎
  ├── Google Scholar：综合性最强，引用数排序
  ├── arXiv：预印本，技术类最新进展
  ├── PubMed：医学/生命科学
  ├── CNKI/万方/维普：中文学术
  └── Semantic Scholar：AI辅助文献筛选

顶级期刊与会议
  ├── 综合：Nature、Science、PNAS、Cell
  ├── 技术：IEEE Transactions、ACM、USENIX
  ├── AI/ML：NeurIPS、ICML、CVPR、ICLR、AAAI
  ├── 商业：HBR、Management Science、Strategic Management Journal
  └── 医学：NEJM、Lancet、JAMA、BMJ

搜索策略
  → 优先高引用综述（review/survey）：快速掌握领域全貌
  → 检索近2-3年顶会/顶刊论文：获取最新研究进展
  → 关键词：[主题] survey/review/state-of-the-art/benchmark
  → 引用追踪：从高引论文向外扩展相关研究
```

### 渠道4：产业实践与报告

```
顶级咨询机构
  ├── McKinsey Global Institute（MGI）：行业深度研究
  ├── Boston Consulting Group（BCG）：战略/创新
  ├── Gartner：技术成熟度曲线、魔力象限
  ├── IDC/Forrester/451 Research：IT市场数据
  └── 中国：艾瑞、易观、国泰君安研究院、中信证券研究

行业协会与机构
  ├── 中国：中国信通院、中国软件行业协会、中国互联网协会
  ├── 全球：Accenture Institute、Deloitte Insights
  └── 垂直行业协会白皮书

案例研究与最佳实践
  ├── Harvard Business School Cases
  ├── MIT Sloan Management Review
  ├── 各大咨询公司案例库
  └── 企业自发布的Case Study / Success Story

投融资与市场数据
  ├── CB Insights：创业/投资数据
  ├── Crunchbase：融资轮次/估值
  ├── PitchBook：VC/PE数据
  └── 东方财富/Wind：中国市场数据
```

### 渠道5：社区与用户声音

```
技术社区
  ├── GitHub：项目活跃度、Star数、issue讨论
  ├── Stack Overflow：技术问题频率（热点痛点）
  ├── Hacker News：技术从业者观点
  └── Reddit（r/technology、r/MachineLearning等）

专业社交平台
  ├── LinkedIn：行业领导者观点、职位变化信号
  ├── X/Twitter：实时讨论、KOL观点
  └── 知乎：中文专业讨论

视频与播客
  ├── TED Talks：权威演讲观点
  ├── YouTube：行业峰会录像、产品发布会
  ├── B站：中文技术分享
  └── 会议回放：NeurIPS/CVPR/re:Invent等
```

---

## 执行工作流

### Step 1: 任务拆解

```
输入：PPT主题 + 受众 + 目的 + 页数预估

输出：结构化研究任务
  ├── 核心问题列表（5-10个需要回答的关键问题）
  ├── 关键词矩阵（中英文 × 各渠道专用关键词）
  └── 优先渠道排序（按主题类型选择主力渠道）

主题类型 → 主力渠道映射：
  技术/AI类    → 学术(arXiv) + 媒体(TechCrunch) + 社区(GitHub/HN)
  商业/战略类  → 咨询报告(McKinsey/BCG) + 媒体(FT/WSJ) + 案例(HBS)
  政策/监管类  → 官方(gov.cn/EUR-Lex) + 媒体(Reuters) + 智库
  医疗/科学类  → 学术(PubMed/Nature) + 官方(WHO/FDA) + 媒体(NEJM)
  市场/行业类  → 咨询(IDC/Gartner) + 数据(CB Insights) + 媒体
```

### Step 2: 并行多源搜索

```
并行执行（每个渠道独立搜索）：
  Thread A: 官方渠道搜索（政府+国际组织+企业官方）
  Thread B: 媒体渠道搜索（主流+科技+行业媒体）
  Thread C: 学术搜索（综述+顶会+近期论文）
  Thread D: 产业报告搜索（咨询机构+行业协会）
  Thread E: 社区信号搜索（GitHub+社交+视频）

每渠道收集：
  → 标题、来源、时间、摘要（50-100字）、URL
  → 核心数据点（数字/百分比/规模）
  → 代表性引语（直接引用）
```

### Step 3: 内容过滤与验证

```
过滤标准：
  ├── 时效性：优先2年内内容（历史回顾例外）
  ├── 权威性：官方>学术>咨询>主流媒体>其他
  ├── 相关性：直接回答核心问题（评分0-5）
  └── 唯一性：去重，合并相似内容

数据验证：
  → 重要数据点需至少2个独立来源交叉验证
  → 标注数据年份（避免使用过时数据）
  → 矛盾数据：两者均保留并标注来源差异
```

### Step 4: 内容分类整理

```
按子主题归组（与PPT大纲对应）：
  Section 1: 背景与现状
    - 数据点列表（含来源）
    - 代表性案例
    - 权威引语

  Section 2: 趋势与驱动因素
    - 核心趋势（3-5条，每条配数据支撑）
    - 预测数据（2025-2030前瞻）

  Section 3: 挑战与风险
    - 主要障碍与挑战
    - 典型失败案例

  Section 4: 最佳实践与案例
    - 企业/机构成功案例（STAR格式）
    - 可量化的ROI/成果

  Section 5: 未来展望
    - 专家观点
    - 技术/市场预测
```

### Step 5: 归纳输出

```
输出素材包（4个文件）：

1. outline.md — 幻灯片大纲
   # 主标题（建议）
   ## 目录结构
   ### 每页：[页码] [标题] | [核心信息一句话] | [关键数据/图表建议]

2. data.md — 数据与引用库
   | 数据点 | 数值 | 来源 | 时间 | URL |
   所有量化数据、统计数字、市场规模

3. quotes.md — 精选引语与案例
   [引语内容] — [人物/机构], [时间]
   [案例名称]: [背景] → [做法] → [结果] (来源：...)

4. refs.md — 参考文献列表（APA/IEEE格式）
   分类：官方 / 学术 / 产业 / 媒体
```

---

## 输出质量标准

```
数量基准（20页PPT对应）：
  ├── 数据点：≥ 20个量化数据
  ├── 学术来源：≥ 5篇论文/报告
  ├── 官方来源：≥ 3个权威机构
  ├── 案例：≥ 3个具体实践案例
  └── 代表性引语：≥ 5条可引用观点

质量检查：
  □ 所有数据点均有来源URL
  □ 核心数据已完成交叉验证
  □ 时效性：>80%内容来自近2年
  □ 多样性：至少覆盖3个不同渠道
  □ 大纲与PPT目标受众和目的匹配
```

---

## 关键词生成策略

```python
# 为任意主题生成多语言多渠道关键词矩阵

def generate_keywords(topic: str, lang: str = "zh+en") -> dict:
    return {
        "core":      [f"{topic}", f"{topic} overview", f"{topic} 概述"],
        "data":      [f"{topic} statistics", f"{topic} 数据", f"{topic} market size"],
        "academic":  [f"{topic} survey", f"{topic} review", f"{topic} research 2024"],
        "industry":  [f"{topic} industry report", f"{topic} 行业报告", f"{topic} white paper"],
        "trend":     [f"{topic} trend 2025", f"{topic} future", f"{topic} 未来趋势"],
        "case":      [f"{topic} case study", f"{topic} 案例", f"{topic} best practice"],
        "challenge": [f"{topic} challenge", f"{topic} risk", f"{topic} 挑战 问题"],
    }
```
