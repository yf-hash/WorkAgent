---
name: content-archive
description: 内容归档 + 多格式导出方法论工具箱 — 供 /content-archive 命令调用。含完整性检查规则、CHANGELOG 生成规则、多格式导出规范（Markdown/Word/PPT JSON）、跨流水线回写规则、freeze 规范。
user-invocable: false
---

# content-archive — 内容归档工具箱

> 本 skill 被 `/content-archive` 命令调用。

## 一、必备产物 checklist

| 文件 | 归属 | 必需 |
|---|---|---|
| `00-content-request.json` | M1 | ✅ 全场景 |
| `01-material-pool.md` | M2 | 有项目关联时必需 |
| `02-draft.md` | M3 | ✅ 全场景 |
| `02-draft.json` | M3 | 仅 PPT 类必需 |
| `03-validate-report.md` | M4 | ✅ 全场景 |

## 二、完整性检查

### 规则
1. 必备文件齐全（缺失 → 拒绝归档）
2. M4 校验状态：
   - ✅ 通过 / 🟡 有修改建议 → 允许归档
   - 🔴 需重写 → 拒绝归档（除非 --force）
3. content-request 与 draft 的 style 一致

### 校验输出
```markdown
# 归档检查报告

## 完整性 {✅/❌}
- 必备文件：{列表}
- 缺失文件：{列表}（如有）

## M4 校验状态
- 事实一致性：✅
- 合规风险：✅
- 文体风格：{score}/10
- 完整性：{✅/❌}
- 引用可追溯：{p}%

## 一致性
- style 一致：{✅/❌}
- 长度偏差：{δ}%

## 归档判定
- {允许 / 拒绝 / 强制允许}
```

## 三、多格式导出规范

### Markdown（`--export markdown`）
- 复制 `02-draft.md` → `_export/{topic-slug}.md`
- 保留内部链接（相对路径）

### Word（`--export word`）
- 使用 pandoc 将 `02-draft.md` 转为 `.docx`
- 命令：`pandoc 02-draft.md -o _export/{topic-slug}.docx --toc`
- 前提：本机安装 pandoc
- 如未安装 → 提示并只导 Markdown

### PPT JSON（`--export ppt-json`）
- 复制 `02-draft.json` → `_export/{topic-slug}.pptx.json`
- Schema 详见 skills/content/content-templates 里 PPT 章节

### PPT 二次生成（未来）
未来可扩展：`_export/{topic-slug}.pptx`（用 python-pptx 或 marp）

## 四、CHANGELOG 生成规则

### 初次归档

```markdown
# CHANGELOG

## v1.0.0 - 2026-08-27

### 初次归档
- [x] 文体：{style.name}
- [x] 关联项目：{project.path 或 无}
- [x] 篇幅：{final_length}（目标 {target}）
- [x] 校验：通过

### 关键素材来源
- {列出 M2 素材池的主要来源}

### 已知问题（记入 known-issues 如有）
- {从 M4 报告的 🟡 项汇总}
```

### 后续归档（--bump）

```markdown
## v1.0.1 - 2026-08-30

### 修改（patch）
- [x] 修改绝对化用词"最先进" → "领先"
- [x] 补 § 3.3 局限说明

### v1.1.0 - 2026-09-05

### 新增（minor）
- [x] 新增 § 6.3 案例 B
- [x] 补 ROI 定量测算章节

## v2.0.0 - 2026-09-15

### 重大变更（major）
- [x] 文体从 tech-whitepaper 改为 solution-whitepaper
- [x] 素材源从 PM 项目切换到 SA 项目
```

## 五、跨流水线回写规则

### 触发条件
- ContentRequest.project.linked = true
- `--writeback` 参数指定

### 回写路径规则

```
{project.path}/_content/{style-id}-{topic-slug}-{yyyymmdd}/
```

例：
```
./output/pm-pipeline/vulnhunter-20260827/_content/solution-whitepaper-vulnhunter-solution-20260828/
```

### 回写内容
- 只回写：`02-draft.md`、`_export/*`、`README.md`
- 不回写：`00-content-request.json`、`01-material-pool.md`、`03-validate-report.md`（这些留在 content-pipeline 目录）

### 安全约束
- **只能创建新子目录**，不能覆盖原项目任何文件
- **不能修改原项目主流水线产物**（04-PRD.md 等）
- 回写后在原项目 CHANGELOG 追加：
  ```
  ### 附属产物新增
  - {yyyy-mm-dd} 挂载内容包：_content/{style}-{topic}-{date}/
  ```

## 六、Freeze 规范

### freeze 场景
| 场景 | 目录命名 |
|---|---|
| 对外发布版 | `v1.0-发布版` |
| 客户交付版 | `v1.0-客户版` |
| 媒体正式版 | `v1.0-媒体版` |
| 内部评审版 | `v1.0-评审版` |
| 归档留档版 | `v1.0-归档版` |

### freeze 只读设置

**Windows PowerShell**：
```powershell
Get-ChildItem -Path "_frozen/v1.0-发布版" -Recurse -File | ForEach-Object {
    $_.IsReadOnly = $true
}
```

**POSIX Bash**：
```bash
find _frozen/v1.0-发布版 -type f -exec chmod a-w {} \;
find _frozen/v1.0-发布版 -type d -exec chmod a-w {} \;
```

### freeze 内容
- 复制主目录所有主产物到 `_frozen/{tag}/`
- 加 `FROZEN_AT.txt`（时间戳 + 归档人）
- 主目录仍可继续编辑（用于 v1.1 迭代）

## 七、版本号策略

| 变更类型 | Bump |
|---|---|
| 换文体 / 换素材 / 全文重写 | major |
| 新增章节 / 新增案例 / 大幅修改论点 | minor |
| 文案微调 / 修错 / 合规改写 | patch |

## 八、目录命名规则

### {style-id}-{topic-slug}-{yyyymmdd}

- style-id：manifest.yaml 中的 8 类之一
- topic-slug：从 topic 提取（≤ 20 字符，英文小写连字符）
- yyyymmdd：生成日期

例：
- `solution-whitepaper-vulnhunter-solution-20260827`
- `pr-vulnhunter-v2-launch-20260830`
- `ppt-quarterly-review-20260901`

## 九、常见归档失败

| 症状 | 修复 |
|---|---|
| M4 校验"需重写" | 修 🔴 项后重跑 M4 |
| 缺 02-draft.md | 回 M3 生成 |
| 缺 01-material-pool.md（有项目关联） | 回 M2 素材抽取 |
| pandoc 未安装 | 只导 Markdown / PPT JSON |
| --writeback 目标不存在 | 检查 project.path |

## 十、反模式

- ❌ 归档时无视 M4 校验 —— 违规
- ❌ 修改 `_frozen/` —— 违规
- ❌ 回写覆盖原项目文件 —— 严重违规
- ❌ 版本号乱跳 —— 违规
- ❌ CHANGELOG 遗漏关键变更 —— 违规
- ❌ 目录名含中文导致导出失败 —— 建议改为英文
