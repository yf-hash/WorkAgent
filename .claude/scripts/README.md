# .claude/scripts — 维护脚本

## 现有脚本

| 脚本 | 用途 | 何时用 |
|---|---|---|
| [migrate.py](migrate.py) | 批量补齐 commands/agents/skills 的 `harness:` 元数据 | 新组件加入后 / 域默认档变更后 |
| [validate-harness.py](validate-harness.py) | 校验所有 harness 块的结构合法性（枚举/缩进/section 齐全） | CI/pre-commit 前 / 手动修改后 |
| [templates-index.py](templates-index.py) | 扫描 templates/ 生成 README 索引 + used-by 溯源 | 增删 template 后 |

## 常用命令

```bash
# 检查所有组件是否需要补齐（dry-run）
python .claude/scripts/migrate.py --target all

# 实际写入
python .claude/scripts/migrate.py --target all --apply

# 只处理某一类
python .claude/scripts/migrate.py --target skills --apply

# 幂等检验：如果还有 updated 就退出码 1（可用作 CI 门）
python .claude/scripts/migrate.py --target all --strict

# 结构校验
python .claude/scripts/validate-harness.py

# 校验并作 CI 门（有错就退出 1）
python .claude/scripts/validate-harness.py --strict

# 重生 templates 索引
python .claude/scripts/templates-index.py
```

## 添加新场景

改 `migrate.py` 里两处：

1. **域默认档**：新加子域到 `CMD_DEFAULTS` / `SKILL_DEFAULTS`
2. **特殊覆盖**：某文件需要非默认的 loop mode / preset，加到对应的 `SPECIAL_*`

修改后重跑 `--apply`，只补新增字段（幂等，不覆盖已有）。

## 添加新枚举值

改 `validate-harness.py` 顶部的 `EXECUTE_PRESETS` / `CONSTRAIN_PROFILES` / `LOOP_MODES` / `MEMORY_SCOPES` / `DANGER_LEVELS` / `GATE_KEYS`；同步更新对应的 `.claude/harness/*/*.md` 文档。

## 幂等保证

两个脚本都幂等：
- `migrate.py`：只处理"缺 `harness:` 或缺 `allowed-tools`"的文件；已有的不动
- `validate-harness.py`：只读，无副作用

## 已废弃的脚本

以下脚本历史存在过，v3.1 合并 / 修完 bug 后已移除，仅在此备忘：

- `migrate-harness.py`（v3.0 首版，处理 commands + agents） → 并入 `migrate.py`
- `migrate-harness-skills.py`（v3.0，处理 skills） → 并入 `migrate.py`
- `fix-harness-indent.py`（v3.0 一次性修 YAML 缩进 bug） → bug 已修，不会重现
