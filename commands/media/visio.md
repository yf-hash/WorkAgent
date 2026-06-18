---
name: visio
description: >
  Visio 图表创建与转换命令，整合 python-visio（.vsdx 读写）、Visio.NET（Windows COM 自动化）
  两大后端，支持流程图/网络拓扑/组织架构/泳道图创建，并与 Mermaid/PlantUML 双向互转，
  导出 SVG/PNG/PDF，适合企业级图表文档化和 Visio 文件批量处理
user-invocable: true
argument-hint: "<描述或.vsdx文件> [--mode create|edit|convert|export|analyze] [--backend python|dotnet|auto] [--type flowchart|network|org|swimlane|er|rack] [--from mermaid|plantuml|text] [--output vsdx|svg|png|pdf]"
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# /visio — Visio 图表创建与转换

加载技能：`skills/visio-builder/SKILL.md`

## 触发条件
需要创建/编辑 .vsdx 文件、将 Mermaid/PlantUML 转为 Visio 格式、批量导出 Visio 图表为图片，
或在 Windows 环境下通过 COM 自动化操作 Visio 时。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<描述或文件>` | 图表内容描述 或 .vsdx/.vsd 文件路径（必填） | — |
| `--mode` | 执行模式 | `create` |
| `--backend` | 后端引擎 | `auto` |
| `--type` | 图表类型 | 自动判断 |
| `--from` | 输入格式（转换模式） | — |
| `--output` | 输出格式 | `vsdx` |

### 执行模式（--mode）
| 值 | 说明 |
|----|------|
| `create` | 从文本描述生成新 Visio 图表 |
| `edit` | 读取并修改已有 .vsdx 文件 |
| `convert` | 将 Mermaid/PlantUML/文本转为 Visio |
| `export` | 将 .vsdx 导出为 SVG/PNG/PDF |
| `analyze` | 解析 .vsdx 结构，输出形状/连接器清单 |

### 后端引擎（--backend）
| 值 | 引擎 | 适用场景 |
|----|------|---------|
| `python` | python-visio / vsdx | 跨平台，读写 .vsdx XML 结构 |
| `dotnet` | Visio.NET / COM 自动化 | Windows 专属，完整 Visio API |
| `auto` | 自动选择 | 有 Visio 安装用 dotnet，否则用 python |

### 图表类型（--type）
| 值 | 类型 | 典型形状 |
|----|------|---------|
| `flowchart` | 流程图 | 开始/结束/判断/处理/连接器 |
| `network` | 网络拓扑 | 服务器/路由器/防火墙/交换机 |
| `org` | 组织架构图 | 职位框/汇报线 |
| `swimlane` | 泳道图 | 泳道容器/跨泳道连接 |
| `er` | ER 图 | 实体/属性/关系 |
| `rack` | 机架图 | 机架单元/设备 |

### 输出格式（--output）
| 值 | 说明 |
|----|------|
| `vsdx` | Visio 原生格式（可继续编辑） |
| `svg` | 矢量图（推荐用于文档嵌入） |
| `png` | 位图（指定 --dpi 控制分辨率） |
| `pdf` | PDF 文档 |

---

## 执行流程

```
Step 1: 模式路由
  → create：解析描述 → 规划形状和连接器 → 生成 .vsdx
  → edit：读取 .vsdx → 定位目标元素 → 应用修改
  → convert：解析源格式（Mermaid/PlantUML）→ 映射到 Visio 形状库
  → export：打开 .vsdx → 调用导出 API → 输出目标格式
  → analyze：解析 XML 结构 → 输出形状/页面/连接器清单

Step 2: 后端选择
  → auto：检测 Visio 是否安装（win32com.client）
  → python 后端：使用 vsdx 库操作 XML
  → dotnet 后端：通过 win32com 调用 Visio.Application

Step 3: 图表构建（create/convert 模式）
  → 选择对应 Stencil（形状模板库）
  → 布局算法：层次布局（流程图）/ 力导向（网络图）/ 树形（组织图）
  → 生成连接器，设置箭头样式和标签

Step 4: 输出
  → 保存 .vsdx 文件
  → 按 --output 导出附加格式
  → 输出文件路径和形状统计摘要
```

---

## 安装依赖

```bash
# python 后端
pip install vsdx python-visio

# dotnet 后端（Windows + Visio 已安装）
pip install pywin32
```

---

## 使用示例

```bash
# 从描述创建流程图
/visio 用户注册流程：填写信息→邮箱验证→完善资料→激活 --type flowchart

# 将 Mermaid 转为 Visio
/visio diagram.mmd --mode convert --from mermaid --output vsdx

# 将 PlantUML 转为 Visio 并导出 SVG
/visio arch.puml --mode convert --from plantuml --output svg

# 导出已有 Visio 文件为 PNG
/visio network.vsdx --mode export --output png

# 解析 Visio 文件结构
/visio complex.vsdx --mode analyze

# Windows COM 自动化创建网络拓扑
/visio 三层网络架构：互联网→防火墙→DMZ→内网 --type network --backend dotnet

# 创建组织架构图
/visio CEO→CTO,CFO,CMO; CTO→研发总监,架构师 --type org
```

---

## 与其他命令的协同

```
/visio ←→ /diagram-uml  → Mermaid/PlantUML ↔ Visio 双向转换
/visio  →  /illustrate  → 将 Visio 导出图嵌入文章配图
/visio  →  /ppt         → 将 Visio 图表插入 PPT
@diagram-architect      → 统一图表编排 Agent，自动选择最优格式
```
