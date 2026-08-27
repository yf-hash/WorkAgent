# Content Workflows — 内容创作剧本详解（v1.0）

> `manifest.yaml` 中每个 `workflow.<name>` 的详细展开。
> 本 role 服务内容 / 市场 / 品牌场景，与 `/pm`（内部 PRD）+ `/sa`（对外方案）互补。

---

## 1. end-to-end-content｜端到端内容创作流水线（核心）

### 场景说明

从一句自然语言到完整可交付内容物料。适用于：
- 市场人员写产品推广文 / 活动推文 / PR 稿
- 售前工程师基于项目产出对外白皮书
- 技术布道写科普文 / 技术白皮书
- 产品经理为立项 / 上市准备 PPT
- 客户成功团队做解决方案宣讲物料

### 执行步骤（5 模块）

#### M1 内容请求网关 — `/content-intake {raw_input}`
- **输入**：一句自然语言描述
  - 例："基于 VulnHunter 漏洞猎人产品，写一篇面向企业安全负责人的解决方案白皮书，突出沙箱能力，8000 字左右"
- **处理**：
  - 文体识别（八大文体分类器）
  - 关联项目 ID 抽取（`PM-xxx` / `SA-xxx` 或路径）
  - 目标受众提取
  - 篇幅 / 语气 / 重点 / 禁止项 / 输出格式 解析
- **产出**：`00-content-request.json`（ContentRequest 标准化对象）
- **Gate**：确认文体 / 受众 / 篇幅 / 关键约束

#### M2 项目素材抽取 — `/content-materials 00-content-request.json`
- **触发条件**：请求含 project-id 或本地项目目录路径
- **处理**：
  - 读取 PM / SA 项目库中 PRD / 技术规格 / 方案 / 痛点报告
  - 过滤无关内容
  - 提取产品能力、架构、优势、客户痛点、技术指标
  - 整理成结构化素材池
- **产出**：`01-material-pool.md`（含引用出处，可追溯）
- **Gate**：确认核心事实素材（避免文案与产品实际不一致）
- **跳过**：无关联项目 ID 时自动跳过，直接进入 M3

#### M3 八大文体专项生成 — `/content-generate --style {id}`
- **输入**：ContentRequest + 素材池
- **处理**：调用 `skills/content/content-templates` 里对应文体的模板 + 语气 + 长度规范
- **产出**：`02-draft.md`（初稿）

#### M4 内容校验 — `/content-validate 02-draft.md 01-material-pool.md`
- **五类校验**：
  1. **事实一致性**（对比素材池，识别夸大 / 与产品不符）
  2. **合规风险**（绝对化用词、宣传风险、敏感词）
  3. **文体风格**（PR 稿不能推文风、白皮书不能太口语）
  4. **完整性**（白皮书章节齐全、PPT 逻辑闭环）
  5. **引用可追溯**（指标 / 规格 是否来自素材池，标记自定义假设）
- **产出**：`03-validate-report.md`
- **Gate**：审核卡点（编辑 / 驳回重跑 / 通过）

#### M5 归档 + 导出 — `/content-archive`
- **多格式导出**：Markdown / Word / PPT JSON
- **PM/SA 回写**：如关联项目，作为附属产物挂载到项目目录
- **版本管理**：语义化版本 + 版本对比
- **产出**：`README.md` + `CHANGELOG.md` + `_export/*`

### 一键统一入口

```bash
# 最常见
/content "基于 VulnHunter 漏洞猎人产品，写一篇面向企业安全负责人的解决方案白皮书，突出沙箱能力，8000 字左右"

# 关联 PM/SA 项目
/content "写解决方案白皮书" \
  --project ./output/pm-pipeline/vulnhunter-20260827/ \
  --style solution-whitepaper \
  --audience 政企安全负责人 \
  --length 8000 \
  --format-out word

# 关联售前项目
/content "写 PR 稿" \
  --project ./output/sa-pipeline/vulnhunter-mfg-20260830/ \
  --style pr \
  --topic "新版本发布，新增分布式沙箱调度"
```

### 局部重写

```bash
# 只重写第 3 章
/content ./output/content-pipeline/xxx/ --rewrite-section 3

# 只重跑 M3 生成阶段
/content ./output/content-pipeline/xxx/ --from M3

# 驳回回到素材抽取
/content ./output/content-pipeline/xxx/ --from M2 --reason "素材池缺少 XX 案例"
```

### 何时不用完整流水线

- **只想解析文体** → `/content-intake` 单跑
- **只做校验**（已有稿件） → `/content-validate <path>`
- **只做导出格式转换** → `/content-archive --export word|ppt-json`

---

## 剧本编写规范

新增 workflow 时的要求：

1. **trigger 关键词 3-8 个**：太少覆盖不到用户表达，太多容易误触发
2. **步骤要有 produces**：产出文件路径明确，方便下一步 --input
3. **每步 gate 类型**：human-review / none / 条件跳过
4. **说明"何时不用"**：帮助 LLM 判断边界
5. **content 特有约束**：M4 校验必须过才能归档；关联项目时素材池必须先建
