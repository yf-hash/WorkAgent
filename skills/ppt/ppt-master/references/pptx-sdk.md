# PPTX SDK — 编程式幻灯片生成参考

> 本文件为 `ppt-master` 技能的编程后端参考模块。
> 原独立 skill `skills/pptx-sdk/` 已删除（v2.7），能力完全内嵌于此。

## 概述
覆盖 `python-pptx`（Python）和 `PptxGenJS`（JavaScript/Node.js）两个 PPTX 编程库，用于需要精确控制每个元素的自动化幻灯片生成场景。适合：批量报表生成、数据驱动幻灯片、自定义 CI/CD 输出。

## 两库对比

| 特性 | python-pptx | PptxGenJS |
|------|-------------|-----------|
| 语言 | Python | JavaScript / Node.js |
| 输出 | .pptx | .pptx |
| 图表 | 通过 EMF/SVG | 原生 Chart 对象 |
| 最适合 | 数据分析后生成报告 | Web 应用/API 生成 |
| 学习曲线 | 中等 | 低 |
| 文档质量 | 详尽 | 详尽 |

## python-pptx

### 安装
```bash
pip install python-pptx Pillow
```

### 基础使用
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# 创建新演示文稿
prs = Presentation()

# 或加载模板
prs = Presentation('template.pptx')

# 选择幻灯片布局
slide_layout = prs.slide_layouts[1]  # 0=title, 1=title+content

# 添加幻灯片
slide = prs.slides.add_slide(slide_layout)

# 设置标题
title = slide.shapes.title
title.text = "幻灯片标题"

# 设置内容
content = slide.placeholders[1]
tf = content.text_frame
tf.text = "第一行内容"
tf.add_paragraph().text = "第二行内容"

# 保存
prs.save('output.pptx')
```

### 添加图片
```python
from pptx.util import Inches

pic = slide.shapes.add_picture(
    'chart.png',
    left=Inches(1),
    top=Inches(2),
    width=Inches(6),
    height=Inches(4)
)
```

### 添加文本框
```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

txBox = slide.shapes.add_textbox(
    Inches(1), Inches(1), Inches(8), Inches(1)
)
tf = txBox.text_frame
tf.word_wrap = True

p = tf.add_paragraph()
p.text = "自定义文本"
p.font.size = Pt(24)
p.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
p.font.bold = True
```

### 添加表格
```python
rows, cols = 3, 4
table = slide.shapes.add_table(
    rows, cols,
    Inches(1), Inches(2),
    Inches(8), Inches(3)
).table

data = [
    ["指标", "Q1", "Q2", "Q3"],
    ["销售额", "100万", "120万", "150万"],
    ["增长率", "—", "+20%", "+25%"],
]
for r, row in enumerate(data):
    for c, val in enumerate(row):
        table.cell(r, c).text = val
```

### 数据驱动批量生成
```python
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt

def generate_report(df, output_path):
    prs = Presentation()
    
    for _, row in df.iterrows():
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"{row['product']} — 月度报告"
        
        tf = slide.placeholders[1].text_frame
        tf.text = f"销售额：{row['revenue']}"
        tf.add_paragraph().text = f"增长率：{row['growth']}%"
        tf.add_paragraph().text = f"客户数：{row['customers']}"
    
    prs.save(output_path)

df = pd.read_csv('monthly_data.csv')
generate_report(df, 'monthly_report.pptx')
```

## PptxGenJS

### 安装
```bash
npm install pptxgenjs
```

### 基础使用
```javascript
const PptxGenJS = require('pptxgenjs');
const pptx = new PptxGenJS();

pptx.layout = 'LAYOUT_WIDE';  // 16:9

const slide = pptx.addSlide();

slide.addText('幻灯片标题', {
  x: 0.5, y: 0.5, w: 9, h: 1.5,
  fontSize: 36,
  fontFace: 'Arial',
  color: '1F4E79',
  bold: true
});

slide.addText([
  { text: '要点一', options: { bullet: true, fontSize: 20 } },
  { text: '要点二', options: { bullet: true, fontSize: 20 } },
  { text: '要点三', options: { bullet: true, fontSize: 20 } }
], { x: 0.5, y: 2, w: 9, h: 4 });

pptx.writeFile({ fileName: 'output.pptx' });
```

### 添加图表
```javascript
slide.addChart(pptx.ChartType.bar, [
  {
    name: '销售额',
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    values: [100, 120, 150, 180]
  }
], {
  x: 1, y: 1.5, w: 8, h: 4,
  chartColors: ['1F4E79', '2E75B6']
});
```

### Express API 集成
```javascript
const express = require('express');
const PptxGenJS = require('pptxgenjs');
const app = express();

app.post('/generate-ppt', async (req, res) => {
  const { title, data } = req.body;
  const pptx = new PptxGenJS();
  
  const buffer = await pptx.stream();
  res.setHeader('Content-Type', 
    'application/vnd.openxmlformats-officedocument.presentationml.presentation');
  res.setHeader('Content-Disposition', `attachment; filename="${title}.pptx"`);
  res.send(buffer);
});
```

## 使用场景矩阵

| 场景 | 推荐库 | 原因 |
|------|-------|------|
| Python 数据分析后生成报告 | python-pptx | 与 pandas/matplotlib 无缝集成 |
| Node.js 后端 API 生成 | PptxGenJS | 无需 Python 环境 |
| 批量生成销售报表 | python-pptx | 数据处理能力强 |
| Web 应用一键下载 | PptxGenJS | 浏览器/服务器通用 |
| 精确复制模板格式 | python-pptx | 可读取并修改现有 .pptx |
| 动态图表（来自 API 数据） | PptxGenJS | 原生 Chart 对象更稳定 |

## 相关资源
- python-pptx 文档: https://python-pptx.readthedocs.io/
- python-pptx GitHub: https://github.com/scanny/python-pptx
- PptxGenJS 文档: https://gitbrent.github.io/PptxGenJS/
- PptxGenJS GitHub: https://github.com/gitbrent/PptxGenJS
