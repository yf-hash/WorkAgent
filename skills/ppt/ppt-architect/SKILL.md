---
name: ppt-architect
description: >
  PPT场景专用图表构建技能。触发词：PPT配图、幻灯片图表、架构图生成、流程图生成、
  框架图、概念图、PPT可视化、图表素材。
  将PPT研究素材和大纲自动转化为架构图/流程图/框架图/时间线/关系图，
  输出适配PPT的PNG/SVG文件，整合Mermaid/PlantUML/diagrams三大引擎。
user-invocable: false
effort: medium
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: one-shot
  memory:
    scope: session
    reads: [project-context]
  security:
    danger-level: low
---

# PPT Architect — PPT场景图表构建技能

## 职责

为 PPT 全流程生成的第4阶段服务：读取研究归纳输出（outline.md/data.md），
自动识别需要可视化的内容，选择最合适的图表类型和引擎，
输出可直接嵌入 PPT 的标准格式图表文件。

---

## 图表类型决策树

```
输入内容类型
  │
  ├── 系统/技术架构、组件关系、模块依赖
  │    └── → PlantUML组件图 / diagrams云架构图
  │
  ├── 业务流程、工作步骤、决策路径
  │    └── → Mermaid flowchart（步骤≤8）
  │          PlantUML活动图（步骤>8或有泳道）
  │
  ├── 时间演进、历史里程碑、发展路线图
  │    └── → Mermaid timeline / 自定义SVG时间轴
  │
  ├── 多方交互、消息传递、API调用顺序
  │    └── → Mermaid sequenceDiagram / PlantUML sequence
  │
  ├── 对比分析、竞品矩阵、优劣势比较
  │    └── → 自定义SVG对比表格 / Mermaid quadrantChart
  │
  ├── 层级结构、知识框架、分类体系
  │    └── → Markmap思维导图 / PlantUML mindmap
  │
  ├── 数据关系、实体关联、数据库结构
  │    └── → Mermaid erDiagram
  │
  ├── 项目计划、阶段划分、时间安排
  │    └── → Mermaid gantt
  │
  ├── 用户旅程、体验路径、触点地图
  │    └── → Mermaid journey
  │
  ├── 概念框架、分析模型（如SWOT/4P/波特五力）
  │    └── → 自定义SVG框架图
  │
  └── 数量/趋势数据可视化
       └── → html-chart（ECharts/Chart.js截图）
```

---

## 引擎能力对比

| 引擎 | 最适合PPT场景 | 输出 | PPT嵌入方式 |
|------|------------|------|-----------|
| **Mermaid** | 流程图/时序图/甘特图/ER图/时间线 | SVG/PNG | 直接插图 |
| **PlantUML** | UML全系/组件图/活动图/泳道图 | PNG/SVG | 直接插图 |
| **diagrams** | AWS/GCP/Azure/K8s云架构图 | PNG | 直接插图 |
| **Markmap** | 知识树/内容框架/思维导图 | SVG/HTML | 截图或SVG嵌入 |
| **自定义SVG** | 概念框架/对比矩阵/品牌定制图 | SVG/PNG | 直接插图 |

---

## 执行流程

### Step 1: 内容扫描与图表需求识别

```
读取输入：outline.md + data.md

扫描信号词：
  架构/组件/模块/系统     → 架构图
  流程/步骤/流水线/过程  → 流程图
  年份/历史/里程碑/发展  → 时间线
  对比/VS/优劣势/比较    → 对比图
  关系/结构/分类/体系    → 层级图/思维导图
  数据/趋势/增长/比例    → 数据可视化
  交互/请求/响应/调用    → 时序图

输出：图表需求列表（含对应幻灯片页码和优先级）
```

### Step 2: 为每张图表生成代码

```python
# 根据图表类型选择模板

DIAGRAM_TEMPLATES = {
    "flowchart": """
        graph TD
            A[开始] --> B{{判断条件}}
            B -->|是| C[执行步骤]
            B -->|否| D[替代步骤]
            C --> E[结束]
    """,
    
    "sequence": """
        sequenceDiagram
            participant A as 参与者A
            participant B as 参与者B
            A->>B: 请求/消息
            B-->>A: 响应/结果
    """,
    
    "timeline_mermaid": """
        timeline
            title 发展历程
            section 阶段一
                2020 : 事件描述
                2021 : 事件描述
            section 阶段二
                2022 : 事件描述
                2023 : 事件描述
    """,
    
    "mindmap": """
        mindmap
          root((核心主题))
            分支一
              子节点A
              子节点B
            分支二
              子节点C
              子节点D
    """,
    
    "quadrant": """
        quadrantChart
            title 四象限分析
            x-axis 低价值 --> 高价值
            y-axis 低可行 --> 高可行
            quadrant-1 优先推进
            quadrant-2 重点关注
            quadrant-3 次要考虑
            quadrant-4 暂缓执行
    """,
    
    "gantt": """
        gantt
            title 项目计划
            dateFormat YYYY-MM
            section 阶段一
            任务名称 :a1, 2025-01, 3M
            section 阶段二
            任务名称 :b1, after a1, 2M
    """
}
```

### Step 3: PPT颜色适配

```
从PPT设计规范提取主色调，注入图表颜色：

Mermaid颜色注入：
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#[主色]',
  'primaryTextColor': '#ffffff',
  'primaryBorderColor': '#[主色深]',
  'lineColor': '#[辅助色]',
  'background': '#ffffff',
  'fontSize': '14px'
}}}%%

PlantUML颜色注入：
skinparam {
  BackgroundColor white
  BorderColor #[主色]
  ArrowColor #[主色]
  FontSize 14
  FontName "Microsoft YaHei"
}

风格预设对应色彩：
  mckinsey    → #003087 (深蓝)
  google      → #4285F4 (Google蓝)
  zen         → #2C3E50 (深灰蓝)
  tech-dark   → #00D4AA (霓虹绿)
  academic    → #1565C0 (学术蓝)
  government  → #CC0000 (政务红)
```

### Step 4: 渲染与导出

```bash
# Mermaid → PNG/SVG
mmdc -i diagram.mmd -o diagram.png -w 1920 -H 1080 --backgroundColor white
mmdc -i diagram.mmd -o diagram.svg --backgroundColor white

# PlantUML → PNG
java -jar plantuml.jar -tpng diagram.puml -o ./output/

# diagrams → PNG
python arch_diagram.py  # 输出PNG

# Markmap → SVG（通过CLI）
markmap --no-open input.md --output mindmap.svg

# 转换为PPT标准尺寸（16:9 = 25.4cm × 14.29cm @ 150DPI）
# 目标：1905 × 1071 px（150DPI）或 3810 × 2143 px（300DPI）
```

### Step 5: 输出整理

```
输出目录结构：
diagrams/
  ├── 01_[页码]_[类型]_[主题].png     渲染图（供PPT插入）
  ├── 01_[页码]_[类型]_[主题].svg     矢量版（可缩放）
  ├── 01_[页码]_[类型]_[主题].mmd     Mermaid源码
  ├── 02_[页码]_...
  └── diagram_index.md               图表清单和使用说明

diagram_index.md 内容：
  | 文件名 | 图表类型 | 对应幻灯片 | 说明 | 修改提示 |
```

---

## PPT图表规范

### 尺寸标准

```
输出分辨率：
  标准（Office内嵌）：150 DPI，1905×1071 px（16:9）
  高清（打印/大屏）：300 DPI，3810×2143 px
  4:3格式：1440×1080 px（150DPI）

文字大小换算（PPT内显示）：
  图表内字体 14px → PPT内约 12pt（可读）
  图表内字体 18px → PPT内约 16pt（舒适）
  最小可接受：12px（最终PPT内不低于10pt）
```

### 内容精简原则

```
节点控制：
  ├── 流程图：≤ 10个节点（超出则拆分为子流程图）
  ├── 架构图：≤ 15个组件
  ├── 思维导图：≤ 3层，每分支 ≤ 5个节点
  └── 时序图：≤ 6个参与者，≤ 12条消息

标签规范：
  ├── 节点标签：≤ 8字（中文）/ ≤ 15字（英文）
  ├── 边标签：≤ 6字
  └── 避免缩写（PPT受众不一定是专业人员）

颜色使用：
  ├── 主色系：与PPT一致（来自ppt-master风格配置）
  ├── 强调色：只用于最关键的1-2个节点/流程
  └── 背景：白色（明亮模式PPT）/ 透明（灵活嵌入）
```

---

## 自定义SVG框架图

对于咨询类、商务类PPT中常见的概念框架图，使用SVG直接生成：

```python
# 支持的框架类型
FRAMEWORK_TEMPLATES = {
    "swot": "SWOT四象限（优势/劣势/机会/威胁）",
    "4p":   "营销4P（产品/价格/渠道/推广）",
    "pestel": "PESTEL宏观分析六维度",
    "porter5": "波特五力模型",
    "pyramid": "金字塔结构（麦肯锡结论先行）",
    "iceberg": "冰山模型（表象与根因）",
    "funnel": "漏斗模型（转化/筛选）",
    "flywheel": "飞轮效应（循环增强）",
    "matrix2x2": "自定义2×2矩阵",
    "circle3": "三圆交集（维恩图/三要素）",
    "step5": "五步骤阶梯图",
    "arrow_process": "箭头流程（3-6步）",
    "timeline_vertical": "纵向时间线",
}

# 生成规则：
# 1. 框架名称 + 内容填充
# 2. 颜色与PPT风格一致
# 3. 输出SVG + PNG两个版本
```

---

## 调用示例

```python
# 从outline.md自动识别并生成所有所需图表
ppt_architect.auto_generate(
    outline="outline.md",
    data="data.md",
    style="mckinsey",     # PPT风格（决定颜色）
    output_dir="diagrams/",
    format="png+svg"      # 同时输出两种格式
)

# 生成单张指定图表
ppt_architect.generate_single(
    type="flowchart",
    content="用户注册→验证→激活→使用的完整流程",
    style="mckinsey",
    page=5                # 对应第5页幻灯片
)

# 生成框架图
ppt_architect.generate_framework(
    framework="swot",
    content={
        "strength": ["优势1", "优势2"],
        "weakness": ["劣势1"],
        "opportunity": ["机会1", "机会2"],
        "threat": ["威胁1"]
    },
    style="mckinsey"
)
```
