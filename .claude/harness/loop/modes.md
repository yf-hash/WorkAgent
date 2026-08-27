# Loop — 五种执行模式

> 命令 frontmatter 用 `harness.loop.mode: <name>` 声明。

## 五种模式

### `one-shot`（默认）
- **语义**：一次问答一次输出，无内部循环
- **典型场景**：`/prd --mode lite` / `/marketing-copy` / `/battle-card` / 大多数原子命令
- **harness 表现**：命令跑完即结束，不启用任何自动迭代
- **配套字段**：无

### `pipeline`
- **语义**：固定阶段顺序执行，阶段间可插 gate
- **典型场景**：`/bid` 七阶段 / `/prd --flow discovery`（diagnose→concept→impl）
- **harness 表现**：把每阶段作为独立步骤，阶段完成用 AskUserQuestion 确认是否进入下一阶段
- **配套字段**：
  ```yaml
  loop:
    mode: pipeline
    stages: [analyze, clarify, outline, write, review, check, export]
    gate-between: true          # 阶段间是否必须人工确认
  ```

### `iterative`
- **语义**：写→评→改直到达标（Writer-Reviewer 互搏、Ralph Wiggum）
- **典型场景**：`/prd --validate` 生成后校验→修改→重跑 / `/pm-tech-spec` 指标校验循环
- **harness 表现**：用 `/loop` 自我调度，或用 max-iterations 限制轮数
- **配套字段**：
  ```yaml
  loop:
    mode: iterative
    max-iterations: 5
    convergence-check: "评审通过 / 达到 90 分 / 用户确认"
    budget-tokens: 200k         # 可选
  ```

### `parallel`
- **语义**：把独立子任务分派给多个子代理并发执行，收敛结果
- **典型场景**：`/pm-clarify` 三个子 Agent 并行（歧义识别 / 澄清问题 / 冲突检测）/ `/pm-tech-spec` 六大类指标并行梳理
- **harness 表现**：用 Agent 工具的批量并发调用（一条消息里多个 Agent 工具块）
- **配套字段**：
  ```yaml
  loop:
    mode: parallel
    fanout: 3-5                 # 建议并发数
    aggregation: dedupe-merge   # 合并策略
  ```

### `monitor`
- **语义**：常驻观察外部状态，事件触发再进一步
- **典型场景**：竞品跟踪 / CI 状态跟踪 / PR 评论轮询 / 日志监控
- **harness 表现**：用 Monitor 工具，persistent 模式，指定退出条件
- **配套字段**：
  ```yaml
  loop:
    mode: monitor
    trigger: "文件新增 / 日志匹配 error / CI status change"
    exit-when: "任务完成 / 用户 stop / 超时 1h"
  ```

## 决策树

```
需要多轮吗？
├─ 否 → one-shot
└─ 是 → 阶段固定？
    ├─ 是 → pipeline
    └─ 否 → 子任务独立？
        ├─ 是 → parallel
        └─ 否 → 需要等外部事件？
            ├─ 是 → monitor
            └─ 否 → iterative
```

## 反模式

- ❌ 把一个天然 pipeline 的命令声明成 iterative（会浪费轮次）
- ❌ 把一个 one-shot 的命令声明成 iterative（模型会自己纠结无止境）
- ❌ 用 monitor 代替 iterative（monitor 是等外部事件，不是主动迭代）
- ❌ parallel 不设 fanout 上限（子代理数量爆炸）

## 与其他能力的边界

- **不管权限**：那是 constrain
- **不管跨会话状态**：那是 memory
- **不管危险动作**：那是 security
