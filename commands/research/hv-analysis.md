---
name: hv-analysis
description: 用横纵分析法深度研究产品/公司/概念/人物，输出 PDF 报告（10000-30000字）
user-invocable: true
argument-hint: "[研究对象] [--title 标题] [--author 作者]"
---

# /hv-analysis

横纵分析法深度研究，输出排版精美的 PDF 报告。

## 用法

```
/hv-analysis [研究对象]
/hv-analysis --title "报告标题" --author "作者名"
```

## 示例

```
/hv-analysis 帮我用横纵分析法研究 Hermes Agent
/hv-analysis 深度研究一下 Claude Code 这个产品
/hv-analysis 竞品分析：Cursor vs Claude Code vs Windsurf
/hv-analysis 研究一下 Anthropic 这家公司
```

## 执行流程

1. 加载 `skills/hv-analysis/SKILL.md` 完整方法论
2. 明确研究对象（产品/公司/概念/人物）
3. 联网信息收集（并行搜索：纵向历史 + 横向竞品 + 补充信息）
4. 纵向分析（6000-15000 字）：起源追溯 → 诞生节点 → 演进历程 → 决策逻辑 → 阶段划分
5. 横向分析（3000-10000 字）：竞品识别 → 核心差异对比 → 用户视角 → 生态位分析 → 趋势判断
   - 开源项目优先使用 [ossinsight.io](https://ossinsight.io) 获取 Star/贡献者/PR 等量化数据
   - 需要全面竞品报告时调用 `competitor-analysis`（Valyu Deep Research，fast/standard/heavy 三档）
   - 需深挖竞品官网产品内容时使用 `Comperator`（爬虫→LLM分类→词云→对比）
6. 横纵交汇洞察（1500-3000 字）：历史如何塑造当下 → 优劣势根源 → 未来推演
7. 生成 PDF 报告（使用 `scripts/md_to_pdf.py`）

## 方法论溯源

横纵分析法融合了：
- 索绪尔的历时-共时分析（Saussure）
- 社会科学的纵向-横截面研究设计
- 商学院案例研究法
- 竞争战略分析

核心原则：纵向追时间深度，横向追同期广度，最终交汇出判断。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--title <标题>` | 报告标题 | 自动提取 |
| `--author <作者>` | 报告作者 | （空） |

## 输出格式

- Markdown 报告：`[研究对象]_横纵分析报告.md`
- PDF 报告：`[研究对象]_横纵分析报告.pdf`（A4 排版，深蓝/绿/浅蓝配色，自动封面页）

## 依赖

PDF 生成需要安装：
```bash
pip install weasyprint markdown --break-system-packages
```
