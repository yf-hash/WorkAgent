---
name: visio-builder
description: >
  Visio 图表构建技能，整合 python-visio（跨平台 .vsdx XML 操作）和 Visio.NET/COM（Windows
  原生自动化）两大后端，支持流程图/网络拓扑/组织架构/泳道图/ER图/机架图的创建、编辑、
  转换和导出，可将 Mermaid/PlantUML 语法双向转换为 Visio 格式，批量处理 .vsdx 文件
user-invocable: false
effort: medium
---

# visio-builder — Visio 图表构建技能

## 能力范围

### 支持的后端

**python-visio / vsdx（跨平台）**
- 读写 .vsdx 文件的 XML 结构（ZIP 容器）
- 操作 Pages、Shapes、Connectors、Stencils
- 无需安装 Visio，适合 CI/CD 和服务器端处理

**Visio.NET / COM 自动化（Windows）**
- 通过 `win32com.client` 调用完整 Visio API
- 支持所有 Visio 内置形状库（Stencil）
- 可调用 Visio 的布局引擎和主题系统

---

## 核心操作

### 1. 创建图表（python 后端）

```python
import vsdx

# 创建新文档
with vsdx.VisioFile('output.vsdx') as vis:
    page = vis.get_page(0)

    # 添加形状
    shape = page.add_shape(x=2, y=2, width=1.5, height=0.75,
                           text='开始', shape_type='process')
    # 添加连接器
    page.connect_shapes(shape1_id, shape2_id, label='是')

    vis.save()
```

### 2. 读取和分析

```python
import vsdx

with vsdx.VisioFile('diagram.vsdx') as vis:
    for page in vis.pages:
        print(f"页面: {page.name}")
        for shape in page.shapes:
            print(f"  形状: {shape.text} @ ({shape.x}, {shape.y})")
        for conn in page.connects:
            print(f"  连接: {conn.from_id} → {conn.to_id}")
```

### 3. COM 自动化（Windows）

```python
import win32com.client

visio = win32com.client.Dispatch('Visio.Application')
visio.Visible = False

doc = visio.Documents.Add('')
page = doc.Pages[1]

# 打开 Stencil
stencil = visio.Documents.OpenEx(
    'FLOWCHT.VSSX',
    win32com.client.constants.visOpenDocked
)

# 放置形状
master = stencil.Masters('Process')
shape = page.Drop(master, 2.0, 2.0)
shape.Text = '处理步骤'

doc.SaveAs('output.vsdx')
visio.Quit()
```

---

## Mermaid → Visio 转换规则

| Mermaid 语法 | Visio 形状 | 说明 |
|-------------|-----------|------|
| `A[文本]` | Rectangle | 普通处理框 |
| `A(文本)` | Rounded Rectangle | 圆角处理框 |
| `A{文本}` | Diamond | 判断框 |
| `A([文本])` | Oval | 开始/结束 |
| `A-->B` | Dynamic Connector | 单向箭头 |
| `A<-->B` | Dynamic Connector | 双向箭头 |
| `subgraph X` | Group/Container | 分组容器 |

## PlantUML → Visio 转换规则

| PlantUML 元素 | Visio 形状 |
|--------------|-----------|
| `actor` | Person |
| `component` | Component |
| `database` | Database |
| `node` | Server |
| `rectangle` | Rectangle |
| `-->` | Connector（实线） |
| `..>` | Connector（虚线） |
| `package` | Group |

---

## 布局算法

```
flowchart  → 层次布局（Hierarchical）：从上到下，自动对齐
network    → 力导向布局（Force-directed）：节点均匀分布
org        → 树形布局（Tree）：根节点居上，子节点展开
swimlane   → 泳道布局：水平/垂直泳道，跨道连接器
er         → 实体关系布局：实体居中，关系线标注基数
rack       → 机架布局：U 位对齐，设备垂直堆叠
```

---

## 导出格式处理

```python
# python 后端导出 SVG（通过 XML 转换）
def export_svg(vsdx_path, output_path):
    # 解压 .vsdx（ZIP 格式）提取页面 XML
    # 转换 Visio XML → SVG 坐标系
    pass

# COM 后端导出（支持所有格式）
def export_com(vsdx_path, output_path, fmt='svg'):
    formats = {'svg': 'visSaveAsFixedFormat', 'png': 32, 'pdf': 'visSaveAsFixedFormat'}
    doc.ExportAsFixedFormat(formats[fmt], output_path, 0, 0)
```

---

## 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| `vsdx not found` | 未安装 vsdx 库 | `pip install vsdx` |
| `win32com not found` | 未安装 pywin32 | `pip install pywin32` |
| `Visio not installed` | COM 后端无 Visio | 自动切换 python 后端 |
| `Stencil not found` | 形状库路径错误 | 使用内置基础形状 |
| `Invalid XML` | .vsdx 文件损坏 | 尝试修复 ZIP 结构 |

---

## 与其他技能的协同

- `mermaid-chart`：提供 Mermaid 语法解析，供转换使用
- `diagram-suite`：统一图表路由，visio-builder 作为 visio 引擎
- `html-chart`：HTML 图表可导出为图片后嵌入 Visio
