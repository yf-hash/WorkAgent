---
name: pm-artifact-archive
description: 产物归档方法论工具箱 — 供 /pm-archive 命令调用。含目录扫描规则、交叉引用检查规则、语义化版本号策略、freeze 快照规范。
user-invocable: false
---

# pm-artifact-archive — 归档工具箱

> 本 skill 被 `/pm-archive` 命令调用。

## 一、必备产物 checklist

| 文件路径（相对目录根） | 归属 | 是否必需 | 缺失后果 |
|---|---|---|---|
| `01-clarify-report.md` | M2 | 必需 | 无澄清 → 下游有假设无依据 |
| `02-business-solution.md` | M3 | 必需 | 无方案 → 无 P0/P1/P2 |
| `03-prototype/03-prototype-desc.md` | M4 | 必需 | 无原型描述 → 设计无参考 |
| `03-prototype/03-prototype.json` | M4 | 必需 | 无结构化 → 无法导入工具 |
| `03-prototype/03-flow.mmd` | M4 | 必需 | 无主流程图 |
| `03-prototype/03-validate.md` | M4 | 必需 | 无逻辑校验 |
| `03-prototype/03-flow-exception.mmd` | M4 | 强烈建议 | 无异常流程 |
| `04-PRD.md` | M5 | 必需 | 无 PRD → 无法交付研发 |
| `04-PRD-validate.md` | M5 | 强烈建议 | 无校验 → 质量无保障 |
| `05-tech-metrics.md` | M6 | 必需 | 无指标 → 无验收依据 |
| `05-tech-spec.md` | M6 | 必需 | 无规格 → 无对外承诺 |
| `05-tech-spec-validate.md` | M6 | 强烈建议 | 无校验 |

## 二、交叉引用检查规则

### 规则 R1：PRD → 业务方案功能对齐
从 04-PRD.md 提取所有功能名，检查是否都在 02-business-solution.md § 功能清单中。

**冲突输出**：
```
【R1】PRD § 3.2 "批量导出" 在业务方案中未找到
建议：在业务方案 § 5. 功能清单 中补充，或从 PRD 移除
```

### 规则 R2：PRD → 原型页面对齐
从 04-PRD.md 提取所有 "页面 ID" 引用（如 P1 / P2），检查是否都在 03-prototype.json 的 pages[*].id 中。

### 规则 R3：技术规格 → PRD 模块对齐
从 05-tech-spec.md § 各模块详细规格 提取模块名，检查是否都在 04-PRD.md 中出现。

### 规则 R4：M2 假设项响应度
从 01-clarify-report.md § 7. 假设项 提取所有假设，检查是否在下游文档（M3/M4/M5/M6）中被引用或响应。

**统计输出**：
```
【R4】M2 澄清 12 条假设：
  - 已在 M3 响应：8 条 ✅
  - 已在 M5 记录到风险：3 条 ✅
  - 未响应：1 条 ⚠️
    - "假设客户接受 30 天试用期"（未在 M5 商业条款中出现）
建议：至少在 M5 § 风险与假设 中显式提及
```

### 规则 R5：时间戳先后
读取每个文件的 git log 或文档 metadata 时间戳，验证：M2 < M3 < M4 < M5 < M6。

**冲突输出**：
```
【R5】时间线倒置：
  M3 生成时间：2026-08-27 18:05
  M2 生成时间：2026-08-27 18:33
建议：说明 M2 是修订版；或考虑回退 M3
```

## 三、语义化版本号策略

### 三段号：MAJOR.MINOR.PATCH

#### MAJOR（不兼容变更）
- 目标用户变了（从"财务专员" → "全公司员工"）
- 需求范围反向（P0 移到 P2 或反之）
- 商业模式变了（免费 → 付费）
- 合规基线变了（等保二级 → 三级）

#### MINOR（新增功能，向后兼容）
- 新增一个 P1/P2 功能
- 新增一个页面
- 新增一类指标
- 新增一个第三方依赖

#### PATCH（修正 & 微调）
- 文案 / 提示语调整
- 指标数值微调（P95 500ms → 400ms）
- 校验发现的小问题修复
- 补充一个异常场景

### 版本号触达组件
每次归档时同步更新：
- 每个文档头部的 `> 版本：v1.X.X`
- VERSION 文件（纯文本）
- CHANGELOG.md 加一节
- README.md 顶部版本号

### 版本号建议算法
```python
def suggest_bump(diff):
    if any([
        "目标用户" in diff.changed_fields,
        "需求范围" in diff.reversed,
        "商业模式" in diff.changed,
    ]):
        return "major"

    if any([
        len(diff.added_features) > 0,
        len(diff.added_pages) > 0,
        len(diff.added_metric_categories) > 0,
    ]):
        return "minor"

    return "patch"
```

## 四、freeze 快照规范

### freeze 流程
1. 用户运行 `/pm-archive ... --freeze --tag "v1.0-上线版"`
2. 二次确认（AskUserQuestion）
3. 创建目录 `_frozen/{tag}/`
4. 拷贝当前所有产物到 `_frozen/{tag}/`
5. 使用 `attrib +R`（Windows）或 `chmod -R -w`（POSIX）设置只读
6. 在主目录 CHANGELOG 记一笔 "Frozen as {tag}"

### freeze 目录结构
```
_frozen/
  v1.0-上线版/
    ├── 01-clarify-report.md    (只读)
    ├── 02-business-solution.md (只读)
    ├── 03-prototype/           (只读)
    ├── 04-PRD.md               (只读)
    ├── 05-tech-metrics.md      (只读)
    ├── 05-tech-spec.md         (只读)
    ├── README.md               (只读)
    ├── CHANGELOG.md            (只读)
    └── FROZEN_AT.txt            (只读) — 时间戳 + 归档人
  v2.0-上线版/
    └── ...
```

### freeze 后续修改
- 主目录仍可继续编辑（用于 v1.1 迭代）
- 若要修改 v1.0-frozen → 必须新起 v1.1.0
- freeze 目录严禁 rm -rf（属于审计留档）

## 五、README 模板

见 `commands/product/pm-archive.md` § 步骤 2 输出。

## 六、CHANGELOG 模板

见 `commands/product/pm-archive.md` § 步骤 3 输出。

## 七、Windows / POSIX 只读设置

### Windows PowerShell
```powershell
Get-ChildItem -Path "_frozen/v1.0-上线版" -Recurse -File | ForEach-Object {
    $_.IsReadOnly = $true
}
```

### POSIX Bash
```bash
find _frozen/v1.0-上线版 -type f -exec chmod a-w {} \;
find _frozen/v1.0-上线版 -type d -exec chmod a-w {} \;
```

## 八、常见归档失败原因

| 症状 | 修复 |
|---|---|
| M4 缺 JSON | 回 `/pm-prototype --refine` 补 |
| PRD 引用了未定义页面 | 回 `/prd --mode update` 或 `/pm-prototype` 补页面 |
| 时间戳倒置 | 说明有回退操作，加 `--allow-time-conflict` 或人工修 |
| 校验状态"需重写" | 强制不允许归档，回上游修 |
| 目录名 topic 含中文 | 建议改为英文小写连字符（可选强制） |
