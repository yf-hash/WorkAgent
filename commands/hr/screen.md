---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion, Skill
description: 简历智能筛选 — 解析简历文档，基于岗位描述（JD）进行多维度语义匹配与评分，生成候选人排名报告
argument-hint: "--jd <jd-file> [--top <n>] [--weights <preset>] [--hard-filter] <resume-path...>"
---

# /screen

简历智能筛选命令。解析简历文档，基于岗位描述（JD）进行多维度语义匹配与评分，生成候选人排名报告。

## 用法

```
/screen --jd <岗位描述文件> [选项] <简历文件或目录>
```

## 示例

```
# 单份简历 vs JD 匹配
/screen --jd jd_backend_engineer.md resume_zhangsan.pdf

# 批量筛选目录下所有简历
/screen --jd jd_product_manager.md ./resumes/

# 技术岗批量筛选，只看前5名，保存报告
/screen --jd jd_senior_engineer.md --weights tech --top 5 --output report.md ./resumes/

# 校招模式，要求本科及以上，最低B级
/screen --jd jd_campus.md --weights campus --min-edu bachelor --grade B ./campus_resumes/

# 必须有Python和机器学习经验，最少3年
/screen --jd jd_ml.md --require-skill Python --require-skill 机器学习 --min-exp 3 ./resumes/

# 生成面试准备报告（仅看前3名）
/screen --jd jd.md --top 3 --format interview --interview-prep ./resumes/

# 匿名化筛选报告
/screen --jd jd.md --anonymize --output anonymous_report.md ./resumes/
```

## 参数说明

### 必填参数

- `--jd <文件路径>` - 岗位描述文件（支持 .md/.txt/.pdf/.docx）

### 简历输入

- `<文件路径>` - 单份简历文件
- `<目录路径>` - 批量处理目录下所有简历（自动识别 .pdf/.docx/.md/.txt）
- 支持同时传入多个文件

### 输出选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--top <n>` | 仅展示排名前 N 的候选人 | 全部展示 |
| `--output <路径>` | 将报告保存为 Markdown 文件 | 输出到对话 |
| `--format <格式>` | `full`(完整) / `table`(仅排名表) / `brief`(简要) / `interview`(面试准备) | `full` |

### 评分权重选项

| 预设 | 说明 | 权重分配 |
|------|------|----------|
| `balanced` | 均衡模式（默认） | 技能30% 经验25% 教育15% 项目15% 成就10% 素质5% |
| `tech` | 技术岗 | 技能35% 经验30% |
| `management` | 管理岗 | 经验35% 成就15% |
| `campus` | 校招模式 | 教育30% 项目20% |
| `custom` | 自定义权重 | 需配合 `--weight-*` 参数 |

### 过滤选项

| 参数 | 说明 |
|------|------|
| `--min-score <分数>` | 最低综合分数线 |
| `--grade <等级>` | 最低推荐等级过滤（S/A/B/C） |
| `--hard-filter <规则文件>` | 加载 YAML 格式硬性过滤规则文件 |
| `--require-skill <技能>` | 必备技能（可多次使用），不具备则直接淘汰 |
| `--min-exp <年数>` | 最低工作年限要求 |
| `--min-edu <学历>` | 最低学历要求（bachelor/master/phd） |

### 功能开关

| 参数 | 说明 |
|------|------|
| `--extract-only` | 仅提取结构化信息，不进行 JD 匹配（用于人才库建设） |
| `--interview-prep` | 为每位推荐候选人生成定制面试问题 |
| `--highlight-gaps` | 重点标注技能差距与培养潜力 |
| `--anonymize` | 匿名化输出（隐藏姓名、联系方式） |
| `--lang <语言>` | 报告输出语言（`zh` 中文，`en` 英文） |

## 执行流程

```
Phase 1: 输入解析
  读取 JD 文件 → 解析岗位名称、核心职责、技能要求、学历经验要求
  读取简历文件 → 自动识别格式，提取文本内容

Phase 2: 结构化提取
  提取：基本信息 / 教育背景 / 工作经历 / 技能清单 / 项目经历 / 其他

Phase 3: 硬性过滤
  检查：学历 / 工作年限 / 必备技能 / 地理位置 / 黑名单关键词
  不通过者记录原因并移入淘汰名单

Phase 4: 六维度评分
  技能匹配度（0-100）/ 工作经验（0-100）/ 教育背景（0-100）
  项目相关度（0-100）/ 成就影响力（0-100）/ 综合素质（0-100）

Phase 5: 报告生成
  按综合分降序排列 → 按 --format 格式生成报告
  为 A/S 级候选人生成面试建议问题（如启用 --interview-prep）
  输出淘汰名单及原因 → 生成整体筛选总结
```

## 输出报告示例

```markdown
# 简历筛选报告

**岗位**：高级后端工程师
**筛选时间**：2026-03-24
**收到简历**：15份 | 通过硬性过滤：12份 | 推荐面试（A级及以上）：4份

## 候选人排名表

| 排名 | 姓名 | 综合分 | 等级 | 技能 | 经验 | 教育 | 核心亮点 |
|------|------|--------|------|------|------|------|---------|
| 1 | 张三 | 91 | **S** | 95 | 90 | 85 | 7年大厂，主导过千万DAU系统 |
| 2 | 李四 | 83 | **A** | 88 | 80 | 90 | 985硕士，Go/K8s经验丰富 |

## 详细分析

### 张三 - 91分（S级）⭐ 强烈推荐

**基本信息**：10届，清华大学计算机系，现居北京
**技能匹配**：Go ✅ Python ✅ K8s ✅ 微服务 ✅
**经验亮点**：字节跳动 7年，主导抖音推荐系统重构，QPS 提升 3倍
**潜在不足**：金融行业经验较少

**建议面试问题**：
1. 推荐系统重构中，如何处理数据一致性挑战？
2. 在高 QPS 场景下，如何设计服务降级和熔断策略？
```

## 硬性过滤规则文件格式（YAML）

```yaml
min_education: bachelor
min_years_experience: 3
required_skills:
  - Python
  - 机器学习
required_industry_any:
  - 互联网
  - 金融科技
blacklist_keywords:
  - 在职不考虑
```

## 注意事项

1. 简历隐私：默认保留候选人姓名，如需匿名化处理请使用 `--anonymize`
2. 评分仅供参考：本命令的评分结果应作为初筛参考，最终录用决策需结合人工判断
3. 批量上限：单次建议处理不超过 50 份简历，过多时请分批处理
4. 文件格式：PDF 扫描件（非文字 PDF）无法直接解析，请使用文字版 PDF

## 关联 Skills

- `resume-screener` - 简历筛选核心能力

## 相关命令

- `/article-writer` - 撰写岗位描述（JD）文档
