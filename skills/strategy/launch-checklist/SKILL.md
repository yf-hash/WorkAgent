---
name: launch-checklist
description: >
  产品发布检查清单（Launch Readiness Checklist）知识库。覆盖产研测设市销
  6 大轨道、Soft/Hard Launch 选型、风险评估矩阵、回滚预案、
  D-7 / D-1 / D-Day / D+7 时间盒、内部和外部对齐 SOP、
  灰度策略、关键监控指标、危机响应流程。
  触发词：发布检查、Launch Readiness、上线清单、Go/No-Go、Soft Launch、
  Hard Launch、灰度发布、回滚预案、发布日历、D-Day、上线 SOP
user-invocable: false
effort: high
harness:
  execute:
    preset: writing-scoped
  constrain:
    profile: writing-safe
  loop:
    mode: pipeline
    gate-between: true
  memory:
    scope: project
    reads: [project-context]
  security:
    danger-level: low
---

# Launch Checklist — 产品发布检查清单知识库

把"上线"这件事从靠经验拍脑袋变成多轨道并行的 SOP。

---

# 一、Launch 类型与选型

| 类型 | 范围 | 典型场景 | 主要风险 |
|------|------|---------|---------|
| **Soft Launch** | 限定地区/用户群 | 大改版、新平台、新付费模型 | 范围控制 |
| **Hard Launch** | 全用户 + PR | 重大新功能 | 不可逆性 |
| **Gradual Rollout** | 分批灰度 1% → 10% → 50% → 100% | 几乎所有 | 灰度逻辑 |
| **Beta Launch** | 报名/邀请制 | 早期产品 | 反馈通路 |
| **Stealth Launch** | 不宣传，仅上线 | 调整 / 实验性功能 | 用户感知 |
| **Re-Launch** | 已上线产品的重新定位 | PMF 不达预期 | 老用户疑虑 |

选型决策树：
```
是否会影响付费/数据/合规？
  ├── 是 → Gradual Rollout（必须灰度）
  └── 否 → 继续

是否需要营销预热？
  ├── 是 → Hard Launch + 时间窗口锁定
  └── 否 → Soft / Stealth

是否需要早期用户反馈？
  ├── 是 → Beta（报名制）
  └── 否 → 普通发布
```

---

# 二、6 大轨道清单

## 2.1 Product 产品轨道

```
□ PRD 已批准、所有变更已落档
□ 验收标准全部通过（Given/When/Then）
□ 边界场景已覆盖（空态/错误/网络断开/权限）
□ 文案最终版（按钮/Toast/邮件/推送）
□ A/B 实验已设计（如有）
□ 北极星指标 + 输入指标 + 护栏指标已定义
□ 成功/失败定义已写入决策矩阵
```

## 2.2 Engineering 工程轨道

```
□ 主分支代码已 Code Review 通过
□ 单元测试 / 集成测试 / E2E 通过
□ 性能压测达标（P95 / 吞吐量）
□ 数据库迁移脚本已 Review + 演练
□ Feature Flag 已配置，可即时回滚
□ 服务依赖已确认（缓存/MQ/三方 API）
□ 配额 / 限流 / 熔断已就绪
□ 日志埋点 + 链路追踪已生效
□ 告警阈值已配置，On-Call 已轮值
□ 回滚 SOP 已演练，预计回滚时间 < N 分钟
```

## 2.3 QA 测试轨道

```
□ 测试计划已 Review
□ 主流程冒烟 + 回归全过
□ 兼容性矩阵覆盖（浏览器/系统/版本/分辨率）
□ 安全测试通过（OWASP / 越权 / 注入）
□ 性能回归对比 baseline
□ 上线后冒烟测试脚本已就位
```

## 2.4 Design 设计轨道

```
□ 视觉规范一致性检查
□ 暗黑模式 / 多语言 / RTL 验证
□ 可访问性 a11y（对比度 / 键盘 / Aria）
□ 关键页面图片 / 视频资产已准备
□ 应用商店截图 + 视频已制作
```

## 2.5 Marketing 市场轨道

```
□ 发布稿（PR / 公关稿）已批准
□ 落地页 / 详情页已上线
□ 社交媒体素材 + 文案排期
□ EDM / Push / In-App 推送排期
□ KOL / 媒体联络已沟通
□ Product Hunt / 行业社区发布计划（如适用）
□ FAQ + 帮助文档已发布
```

## 2.6 Sales / CS 销售客服轨道

```
□ 销售一页禅 / FAQ 已分发
□ 销售内训已完成
□ Demo 环境数据已准备
□ 客服话术 + 升级流程已就绪
□ 工单系统标签已配置（区分新功能反馈）
□ NPS / CSAT 调查已部署
```

---

# 三、时间盒 SOP

```
D-30：决策 Go/No-Go #1（确认发布日期 + 大方向）
D-21：所有轨道负责人接收清单
D-14：Code Freeze（仅 P0 Bug Fix）
D-10：Pre-Launch Review（跨轨道对齐会）
D-7：内测全过 + 灰度配置就绪 + Marketing 素材冻结
D-3：Go/No-Go #2（看 Pre-Launch 数据）
D-1：D-Day Briefing（On-Call / 应急通讯）
D-Day：分阶段上线
  - T-0：1% 灰度
  - T+2h：核查指标 → 10%
  - T+8h：核查指标 → 50%
  - T+24h：100%（如健康）
D+1：稳定性日报 + 主指标观察
D+7：Launch Retrospective（上线后复盘）
D+30：商业指标复盘
```

---

# 四、风险评估矩阵

```
影响 \ 概率 | 低         | 中         | 高
低         | 接受       | 接受       | 监测
中         | 监测       | 监测+预案  | 阻断发布前缓解
高         | 监测+预案  | 阻断发布   | 阻断发布
```

每个风险条目格式：
```
- 风险：[一句话描述]
  概率：低 / 中 / 高
  影响：低 / 中 / 高
  应对：[预防措施 + 触发条件下的执行步骤]
  Owner：[角色]
```

---

# 五、关键监控指标（D-Day）

```
基础设施：
  - QPS / 服务延迟 P50/P95/P99
  - 错误率 5xx / 4xx
  - 数据库 CPU / 慢查询 / 连接数

业务：
  - 主漏斗实时转化率
  - 实时活跃用户数 vs 历史同期
  - 主要业务事件（注册 / 下单 / 付费）

体验：
  - 客户端 Crash 率
  - 页面加载 P95
  - 客服工单激增检测

舆情：
  - 社区 / 微博 / Twitter 关键词监测
  - App Store / 应用市场负面评价
```

---

# 六、回滚预案

```
触发条件（任一发生即执行）：
  □ 核心服务 5xx 错误率 > 1%
  □ 主漏斗转化率下降 > 20%
  □ 数据库延迟 > baseline 3 倍
  □ 安全 / 数据泄露事件
  □ 法务/合规阻断信号

回滚流程（< 5 分钟）：
  1. On-Call 工程师拉群拉群 + 通知 PM/QA Lead
  2. Feature Flag → off（或灰度比例 → 0）
  3. CDN / 边缘缓存清理（如适用）
  4. 数据库 schema 回滚（如适用，预先准备好脚本）
  5. 客服话术 + 公告同步
  6. 复盘启动：1 小时内根因初判，48 小时内完整 PIR
```

---

# 七、Go/No-Go 决策模板

```
日期：YYYY-MM-DD HH:MM
出席：PM / EM / QA / DPM / Marketing / Sales

清单审计：
  - Product 轨道：[过 / 阻断 / 风险]
  - Engineering：[过 / 阻断 / 风险]
  - QA：[过 / 阻断 / 风险]
  - Design：[过 / 阻断 / 风险]
  - Marketing：[过 / 阻断 / 风险]
  - Sales / CS：[过 / 阻断 / 风险]

风险审议：
  - [风险 1]：[决策]
  - [风险 2]：[决策]

决策：
  □ Go：按计划发布
  □ Go (Conditional)：满足[条件]后发布
  □ Slip：推迟到 [日期]，原因 [...]
  □ No-Go：取消，原因 [...]

下一步：
  - [行动项 + Owner + 截止时间]
```

---

# 八、与其他知识库的关系

| 知识库 | 协作方式 |
|--------|---------|
| `gtm-strategy` | Marketing/Sales 轨道的内容来源 |
| `roadmap` | 发布日期来自路线图 |
| `product-release-note` / `product-training` | Release Notes / 培训 PPT 等资料 |
| `analytics` | D-Day 监控指标埋点设计 |
| `pm-qa-acceptance` | 上线阻断项与客户验收口径 |

---

# 九、配套模板

- `templates/release-note-template.md` — Release Note 标准模板（内部 + 客户两版）
- `templates/acceptance-checklist-template.md` — 上线前测试验收清单
- `@qa-acceptance-designer` Agent — 验收方案与上线阻断项
