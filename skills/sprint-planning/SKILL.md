---
name: sprint-planning
description: >
  Sprint 规划知识库。覆盖 Scrum / Kanban / Shape Up 三种迭代模式、
  Sprint Goal 设计、Story Pointing（斐波那契 / Planning Poker）、
  Capacity Planning、Backlog Refinement、Definition of Ready/Done、
  Burndown / Velocity 跟踪、Sprint 反模式识别。
  触发词：Sprint 规划、迭代规划、Story Point、Planning Poker、Velocity、
  Backlog 梳理、Definition of Done、DoR、DoD、Scrum、Kanban、Shape Up
user-invocable: false
effort: high
---

# Sprint Planning — 迭代规划知识库

把"怎么把这两周/六周的活儿排清楚"变成可复用的规划流程。

---

# 一、迭代模式选择

| 模式 | 周期 | 颗粒度 | 适合 |
|------|------|--------|------|
| **Scrum** | 1-4 周（多为 2 周） | Story Point | 已知功能、稳定团队 |
| **Kanban** | 流式无固定周期 | 事项数 | 运维 / 客服 / 不可预测工作 |
| **Shape Up** | 6 周 + 2 周冷却 | "Pitch + Bet" | Basecamp 模式、产品研发 |
| **ScrumBan** | Scrum + WIP 限制 | 混合 | 转型期团队 |

选型决策：
```
工作可预测吗？
  ├── 是（稳定需求） → Scrum
  └── 否（不可预测） → Kanban

团队对终态有共识？
  ├── 是 → Scrum
  └── 否（探索期） → Shape Up

需要严格 WIP 控制？
  └── ScrumBan
```

---

# 二、Sprint Goal（迭代目标）

## 2.1 Goal 必备特性

```
✅ 单一聚焦（一句话讲清）
✅ 用户/业务价值驱动（不是任务列表）
✅ 可衡量是否达成
✅ 任何成员都能背诵

❌ "完成 12 个故事"  ← 只是任务量
❌ "提升用户体验"    ← 没法衡量
✅ "让新用户在第一次访问的 5 分钟内完成第一次有效操作"
```

## 2.2 Goal 起草模板

```
本 Sprint 我们要 [动作 / 交付内容]
以便 [用户 / 业务收益]
我们将通过 [可观测信号] 验证目标达成
```

例：
```
本 Sprint 我们要让导出功能支持 PDF / Excel / CSV 三种格式
以便企业用户能将报表共享给客户和上级
我们将通过"导出操作的成功率 ≥ 99% + 平均完成时间 < 5s"验证
```

---

# 三、Backlog Refinement（Backlog 梳理）

## 3.1 Definition of Ready（DoR）

故事进入 Sprint 前必须满足：

```
□ 故事描述完整（As/I want/So that）
□ 验收标准清晰（Given/When/Then）
□ 设计稿/线框已就位
□ 依赖项已识别
□ 技术方案已对齐（Three Amigos）
□ 估算已完成
□ 故事 ≤ 1 个 Sprint 可完成
□ 可独立交付（不锁死其他故事）
```

## 3.2 故事拆分技巧

| 拆分维度 | 适用 | 例 |
|---------|------|----|
| 工作流步骤 | 多步骤功能 | 注册 → 邮件验证 → 完善资料 拆 3 个 |
| 业务规则 | 规则复杂 | 定价 = 基础 + 优惠 + 税费，先做基础 |
| 数据类型 | 多类型支持 | 先支持图片，再支持视频 |
| CRUD 操作 | 数据管理 | 先 Read，再 Create，再 Update/Delete |
| 简单 → 复杂 | 算法可分级 | 先按时间排序，再加权重排序 |
| 接口分离 | 端分离 | 先 API，再前端 |
| 无界面版本 | 内部使用 | 后端先跑通，前端后做 |

## 3.3 颗粒度参考

```
1 SP ≈ 半天工作量
2 SP ≈ 1 天
3 SP ≈ 2 天（"经典故事"大小）
5 SP ≈ 3-4 天
8 SP ≈ 1 周（已经是上限了）
13+ SP → 必须拆分
```

---

# 四、估算方法

## 4.1 Planning Poker

```
1. PM/PO 念故事
2. 团队成员各自挑卡片（斐波那契：1/2/3/5/8/13/21）
3. 同时翻牌
4. 最高 + 最低分讨论分歧
5. 重新出牌，最多 3 轮
```

## 4.2 T-Shirt Sizing（粗估）

```
XS / S / M / L / XL
  ↓
1  / 3 / 5 / 8 / 13
```

适合 Backlog 早期粗估。

## 4.3 Reference Story（参照法）

挑一个团队都做过的"3 SP 故事"作为锚点，新故事跟它对比：
- 比它简单 → 1 / 2
- 类似 → 3
- 比它复杂 → 5 / 8

---

# 五、Capacity Planning（容量规划）

## 5.1 容量公式

```
Sprint Capacity = Σ(每人可用工作日 × 每日有效产能)

人均扣减项：
  - 周末 / 假期
  - 培训 / 会议（每天 ~15-20%）
  - 跨项目支持
  - 历史代码 维护 / On-Call

经验公式：
  Capacity ≈ 团队人数 × Sprint 工作日 × 0.6 (有效率系数)
```

## 5.2 速度（Velocity）

```
Velocity = 过去 3-5 个 Sprint 完成 SP 平均值

注意：
  - 第一个 Sprint 没有历史 → 团队估算个起点
  - 节假日 / 人员变动 → 单独标注
  - 不要拿 Velocity 做团队 KPI（会扭曲估算）
```

---

# 六、Sprint Planning 会议流程（标准 Scrum）

```
Part 1：Why & What（What will we deliver?）
  耗时：1.5 小时（2 周 Sprint）
  
  Step 1：PO 介绍 Sprint Goal 候选
  Step 2：团队问答 + 调整 Goal
  Step 3：PO 介绍 Backlog 顶部故事
  Step 4：团队判断哪些故事符合 Goal 且 DoR 通过

Part 2：How（How will we get this done?）
  耗时：1.5 小时

  Step 5：团队拆分故事为子任务
  Step 6：领取任务（Pull，不 Push）
  Step 7：检查 Capacity vs SP，调整范围
  Step 8：识别风险 / 依赖 / 阻塞预案
  Step 9：确认 Sprint Backlog 冻结

Part 3：Commit（Sprint Goal Commitment）
  Step 10：团队公开承诺 Sprint Goal
```

---

# 七、Definition of Done（DoD）

故事算完成必须满足：

```
代码层面：
  □ 代码已 Code Review 合并主干
  □ 单元测试 + 集成测试通过
  □ 无新增 P0/P1 Bug
  □ 性能指标无回归
  □ 安全扫描通过

文档层面：
  □ 用户文档 / 帮助中心已更新
  □ API 文档已更新（如有变更）
  □ Release Notes 待发布列表已加入

体验层面：
  □ QA 已签字
  □ 设计师已签字
  □ PM 验收通过
  □ 关键路径埋点已上线

发布层面：
  □ Feature Flag 默认 off（如适用）
  □ 灰度配置就绪
  □ 监控告警已配置
```

---

# 八、Sprint 反模式

| 反模式 | 表现 | 修正 |
|--------|------|------|
| 范围爆炸 | Sprint 中频繁加新故事 | PO 守门，新故事进 Backlog |
| 估算游戏 | 团队为了"达成 KPI"故意高估 | Velocity 不做考核 |
| 故事过大 | 13+ SP 的"巨石故事" | 强制拆分，否则不进 Sprint |
| 隐性返工 | 故事完成后又被打回 | DoD 严格，验收前置 |
| 进度日报化 | 每天复述昨天做了啥 | Standup 关注阻塞而非汇报 |
| 计划僵化 | 计划定了不调整 | 中段重审，触发条件下调整 |
| Sprint 没目标 | 一堆零散故事 | Sprint Goal 必填 + 公开承诺 |

---

# 九、Burndown / Burnup 跟踪

```
Burndown（剩余工作量随时间下降）：
  适合识别"是否能按时完成"
  
Burnup（已完成工作量随时间上升 + 总范围线）：
  适合识别"范围是否在变化"
```

健康曲线特征：
- 缓慢下降，最后 1-2 天清零
- 中间有平台期（QA 阶段）

异常曲线：
- 一开始就平 → Sprint 没启动
- 中段平 → 阻塞 / 范围变更
- 临近末段陡降 → 可能在赶工 / 砍范围

---

# 十、与其他知识库的关系

| 知识库 | 协作方式 |
|--------|---------|
| `roadmap` | 路线图季度目标 → Sprint Goal |
| `user-story-mapping` | 故事地图 R1 → Sprint Backlog |
| `product-spec` | PRD 拆分为可估算故事 |
| `retrospective` | Sprint 末复盘 |
| `launch-checklist` | Sprint 中后期可触发发布清单 |
| `okr` | Sprint Goal ↔ 季度 OKR 对齐 |
