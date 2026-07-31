---
name: ppt-web-researcher
description: >
  PPT 多源联网研究技能。从五大渠道（官方/媒体/学术/产业/社区）联网收集 PPT 主题相关素材，
  输出与 Phase 3-9 衔接的结构化素材包。含搜索渠道矩阵、并行多源搜索、过滤验证、质量基准。
  触发词：PPT 联网研究、ppt research、PPT 资料调研、PPT 素材搜集、多源搜索
user-invocable: false
effort: high
---

# PPT Web Researcher — 多源联网研究

> 单一职责：联网搜集 PPT 主题的高质量素材（无本地资料前提下）。
> 不做：本地资料索引（→ `ppt-rag-indexer`）、写大纲（→ `ppt-architect`）、生成 PPT 内容（→ `ppt-master` 等）

## 搜索渠道矩阵

### 渠道 1：官方权威来源
```
政府与监管机构
  ├── 中国：国务院、各部委官网、发改委报告、工信部白皮书
  ├── 美国：White House/FTC/FDA/SEC 官方报告
  └── 关键词策略：site:gov.cn OR site:gov [主题] report/white paper

国际组织：联合国体系 / WEF / McKinsey Global Institute
企业官方：年报 (10-K) / IR 页 / 工程师博客 / 技术白皮书
```

### 渠道 2：媒体报道
```
财经主流：Reuters / Bloomberg / FT / WSJ / 财新 / 第一财经
科技行业：MIT Technology Review / Wired / TechCrunch / 36 氪 / 虎嗅
```

### 渠道 3：学术研究
```
搜索引擎：Google Scholar / arXiv / PubMed / CNKI / 万方
顶会/顶刊：NeurIPS / ICML / Nature / Science / HBR
策略：优先高引用综述，检索近 2-3 年顶会论文
```

### 渠道 4：产业实践与报告
```
咨询机构：McKinsey / BCG / Gartner / IDC / 艾瑞 / 易观
数据来源：CB Insights / Crunchbase / PitchBook
案例库：Harvard Business School Cases / MIT Sloan
```

### 渠道 5：社区与用户声音
```
技术社区：GitHub / Stack Overflow / Hacker News / Reddit
专业社交：LinkedIn / X(Twitter) / 知乎
视频平台：TED Talks / YouTube / B 站
```

## 执行工作流

### Step 1：任务拆解

```
主题类型 → 主力渠道映射：
  技术/AI 类   → 学术(arXiv) + 媒体(TechCrunch) + 社区(GitHub/HN)
  商业/战略类  → 咨询报告(McKinsey/BCG) + 媒体(FT/WSJ) + 案例(HBS)
  政策/监管类  → 官方(gov.cn) + 媒体(Reuters) + 智库
  医疗/科学类  → 学术(PubMed/Nature) + 官方(WHO/FDA)
  市场/行业类  → 咨询(IDC/Gartner) + 数据(CB Insights) + 媒体
```

### Step 2：并行多源搜索

```
Thread A: 官方渠道（政府+国际组织+企业官方）
Thread B: 媒体渠道（主流+科技+行业媒体）
Thread C: 学术搜索（综述+顶会+近期论文）
Thread D: 产业报告（咨询机构+行业协会）
Thread E: 社区信号（GitHub+社交+视频）

每渠道收集：标题 / 来源 / 时间 / 摘要（50-100 字）/ URL / 核心数据点 / 代表性引语
```

### Step 3：内容过滤与验证

```
过滤标准：时效性（优先 2 年内）/ 权威性（官方>学术>咨询>媒体）/ 相关性 / 唯一性
数据验证：重要数据点需至少 2 个独立来源交叉验证
```

### Step 4：内容分类整理

按子主题归组（与 PPT 大纲对应），每章节包含：数据点列表（含来源）/ 代表性案例 / 权威引语

## 质量基准

```
数量基准（20 页 PPT 对应）：
  ├── 数据点：≥ 20 个量化数据
  ├── 学术来源：≥ 5 篇论文/报告
  ├── 官方来源：≥ 3 个权威机构
  ├── 案例：≥ 3 个具体实践案例
  └── 代表性引语：≥ 5 条可引用观点
```

## 统一输出格式

与 `ppt-rag-indexer` 完全相同：

```
ppt_assets/
  ├── outline.md        幻灯片大纲（含每页建议内容类型）
  ├── data.md           数据点（来源引用到具体 URL）
  ├── quotes.md         精选引语和案例（保留原文+出处）
  └── refs.md           参考文献列表（APA/IEEE 格式）
```

## 与 ppt-rag-indexer 配合（Combined 场景）

当用户既有本地资料又需要联网补充：

1. 先调用 `ppt-rag-indexer` 索引内部资料，生成覆盖度报告
2. 对覆盖率 < 70% 的章节，调用本 Skill 联网补充
3. 合并两路素材，去重后输出统一素材包

> 编排逻辑由调用方（如 `@ppt-generator` Agent）实现，本 Skill 仅负责联网研究本身。
