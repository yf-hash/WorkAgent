---
name: taskweaver
description: 数据分析与查询 Agent — 自然语言转 SQL（Chat2DB）+ Python 代码执行（TaskWeaver），覆盖数据库查询、SQL 优化、文件分析、自动化工作流，支持 MySQL/PostgreSQL/MongoDB 等主流数据库
user-invocable: true
argument-hint: "<任务描述> [--backend sql|python|auto] [--db mysql|postgresql|sqlite|oracle|mongodb] [--mode query|optimize|explain|analyze|schema] [--input <文件路径>] [--output <输出路径>] [--schema <表结构>] [--verify]"
allowed-tools: [Read, Write, Grep, Glob, WebSearch, WebFetch, AskUserQuestion]
harness:
  execute:
    preset: research
  constrain:
    profile: writing-safe
    gates: [before-write]
  loop:
    mode: parallel
    fanout: 3-5
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# /taskweaver — 数据分析 Agent

加载技能：
- `skills/research/taskweaver/SKILL.md`（Python 代码执行）
- `skills/research/chat2db/SKILL.md`（SQL 生成与优化）

---

## 后端路由

```
IF 任务含 "数据库/表/SQL/查询/索引/JOIN/Schema/慢查询"  → sql 后端（Chat2DB）
IF 任务含 "文件/CSV/Excel/JSON/读取/合并/清洗/可视化"  → python 后端（TaskWeaver）
IF 两者都有（"查数据库再用Python分析"）               → sql 导出数据 → python 分析
ELSE（模糊）                                          → auto：根据有无文件路径判断
  有 --input 文件 → python 后端
  无文件，描述偏数据库 → sql 后端
```

---

## 参数说明

### 公共参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `<任务描述>` | 自然语言描述的任务需求（必填） | — |
| `--backend` | 强制指定后端：`sql` / `python` / `auto` | `auto` |
| `--verify` | 执行前显示 SQL 或 Python 代码供确认 | `false` |
| `--output` | 输出文件路径 | 自动生成 |

### SQL 后端参数（`--backend sql`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--db` | 数据库类型：`mysql` / `postgresql` / `sqlite` / `oracle` / `mongodb` | `mysql` |
| `--mode` | 执行模式（见下表） | `query` |
| `--schema` | 表结构描述，提升 SQL 准确度 | — |

#### SQL 执行模式

| `--mode` 值 | 功能 | 典型用途 |
|------------|------|---------|
| `query` | 自然语言 → SQL | 快速查询数据 |
| `optimize` | SQL 性能优化 | 加速慢查询 |
| `explain` | 解释 SQL 含义 | 理解复杂 SQL |
| `analyze` | 分析查询结果 | 数据洞察 |
| `schema` | 分析表结构关系 | 数据库设计理解 |

### Python 后端参数（`--backend python`）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 输入文件路径（CSV/Excel/JSON 等） | — |
| `--plugin` | 指定 TaskWeaver 插件名称 | — |

---

## SQL 后端执行流程

### Query 模式（默认）
```
Step 1: 需求解析
  → 识别目标表、查询条件、聚合方式、排序规则
  → 确认是否需要 JOIN、子查询

Step 2: SQL 生成
  → 按 --db 数据库方言生成标准 SQL
  → 添加必要的索引提示
  → UPDATE/DELETE 操作先生成 SELECT 版本验证

Step 3: 安全检查
  → 标记高风险操作（无 WHERE 的 UPDATE/DELETE）
  → 建议先在测试环境执行

Step 4: 输出
  → 带语法高亮的 SQL
  → 执行说明和注意事项
```

### Optimize 模式
```
Step 1: 分析原始 SQL
  → 识别性能瓶颈（SELECT *、子查询、缺少索引等）

Step 2: 生成优化版本
  → 重写为高效 SQL
  → 给出索引建议

Step 3: 对比输出
  → 原始 vs 优化后 SQL
  → 预期性能提升说明
```

---

## Python 后端执行流程

```
Step 1: 任务拆解
  → 将复杂任务分解为可执行的子步骤
  → 识别所需的 Python 库和数据格式
  → 规划执行顺序和中间状态

Step 2: 代码生成
  → 为每个子步骤生成 Python 代码
  → 添加错误处理和数据验证
  → 选用最合适的库（pandas/numpy/matplotlib/requests 等）

Step 3: 代码执行（沙箱环境）
  → 在隔离的 Python 环境中运行代码
  → 捕获输出、错误信息、生成的文件
  → 自动重试失败步骤（最多 3 次）

Step 4: 结果验证
  → 检查输出是否符合预期
  → 生成执行摘要

Step 5: 输出交付
  → 返回执行结果、生成的文件路径
  → 提供关键发现和数据洞察
```

---

## 代码模板

### 数据清洗
```python
import pandas as pd

df = pd.read_csv('data.csv')
original_count = len(df)
df = df.drop_duplicates().dropna()
df.to_csv('cleaned.csv', index=False)

print(f"原始: {original_count} 行 → 清洗后: {len(df)} 行")
print(f"删除了 {original_count - len(df)} 行")
```

### 数据分析 + 可视化
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sales.csv')
df['date'] = pd.to_datetime(df['date'])
monthly = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()

plt.figure(figsize=(12, 6))
monthly.plot(kind='bar')
plt.title('Monthly Sales')
plt.savefig('monthly_sales.png', dpi=150, bbox_inches='tight')
print(monthly.to_string())
```

### 批量文件处理
```python
import pandas as pd
import glob

files = glob.glob('data/*.xlsx')
dfs = [pd.read_excel(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)
combined.to_csv('combined.csv', index=False)
print(f"合并了 {len(files)} 个文件，共 {len(combined)} 行")
```

---

## 输出格式

### SQL 后端 — Query 模式
```markdown
## SQL 查询

**需求**：[用户的自然语言描述]

**生成的 SQL**（[数据库类型]）：
```sql
SELECT [字段] FROM [表名] WHERE [条件] ORDER BY [排序] LIMIT [限制];
```

**执行说明**：
- 适用数据库：[MySQL / PostgreSQL / ...]
- 预期返回：[结果结构说明]
- ⚠️ 注意：[高风险操作标注]

**索引建议**：[性能相关建议]
```

### SQL 后端 — Optimize 模式
```markdown
## SQL 优化

**原始 SQL**：
```sql
[原始 SQL]
```

**优化后 SQL**：
```sql
[优化后的 SQL]
```

**优化点**：
1. [优化说明 1]
2. [优化说明 2]

**建议添加的索引**：
```sql
CREATE INDEX idx_xxx ON table_name(column_name);
```
```

### Python 后端
```markdown
## 任务执行结果

**任务**：[用户的任务描述]

**执行步骤**：
1. ✅ [步骤 1]
2. ✅ [步骤 2]

**生成的代码**：
```python
[完整 Python 代码]
```

**执行结果**：[输出内容 / 文件路径 / 数据摘要]

**关键发现**：
- [数据洞察 1]
- [数据洞察 2]

**输出文件**：`[路径]`
```

---

## 使用示例

```
# SQL 后端
/taskweaver 查询最近 30 天新注册的用户数量
/taskweaver 统计每个产品类别的销售额，按降序取前 10 --db postgresql
/taskweaver 将这个慢查询优化：SELECT * FROM orders WHERE status='pending' --mode optimize
/taskweaver 解释这个 SQL 是什么意思 --mode explain
/taskweaver 分析 users、orders、products 三张表的关系 --mode schema --schema "users(id,name,email), orders(id,user_id,amount,status)"

# Python 后端
/taskweaver 读取 sales.csv 并统计每个产品类别的总销售额
/taskweaver 将 data/ 目录下所有 Excel 文件合并并去重 --output combined.csv
/taskweaver 分析 log.txt 中的错误模式，统计每种错误出现次数 --input log.txt

# 联合模式（SQL 导出 → Python 分析）
/taskweaver 从订单表查出上季度数据，用 Python 生成销售趋势图
```

---

## 安全规则

### SQL 后端
- `UPDATE` / `DELETE` 操作：自动先生成 `SELECT` 版本供验证
- 无 `WHERE` 的修改操作：添加 ⚠️ 警告，要求确认
- 建议查询账号使用只读权限
- 不在 SQL 中包含明文密码或敏感凭证

### Python 后端
- 代码在沙箱中执行，不影响系统文件
- 默认不允许：`os.system`、`subprocess`、`eval`、`exec`
- 网络访问：仅允许白名单域名（可配置）
- 文件访问：限定在指定工作目录内
