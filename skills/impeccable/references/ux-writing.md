# ux-writing.md — Impeccable UX 文案参考

> 微文案 / 空状态模板 / 错误消息公式 / 按钮文案。**任何可见文字加载。**

---

## 1. 第一原则：用户视角的动词

```
✗ 系统视角："Order has been successfully submitted"
✓ 用户视角："订单已提交"

✗ 模糊："Action completed"
✓ 具体："已发送 3 封邀请邮件"

✗ 系统术语："Validation error: field 'email' must match regex"
✓ 人话："邮箱格式不对，例如 you@example.com"
```

---

## 2. 按钮文案（最高频）

### 公式：动词 + 名词（或动词单独）

```
✓ 创建账号
✓ 发送
✓ 保存更改
✓ 取消
✓ 删除项目
✗ 提交
✗ 确认
✗ OK / 好的
✗ 点击这里
```

### 长度

- 一句话 button：≤ 3 个词（"开始使用" / "立即下载" / "查看演示"）
- 单动词 button：≤ 12px padding 内（"保存"）
- 永远不要让 button 文字换行

### 表单提交

```
✗ 默认 "Submit"
✓ 表单是注册 → "创建账号"
✓ 表单是登录 → "登录"
✓ 表单是反馈 → "发送反馈"
✓ 表单是设置 → "保存"
```

---

## 3. 空状态（Empty State）

四要素，缺一不可：

```
[图示 or 简单 icon]
标题（一句话说"为什么空"）
副标题（一句话说"接下来做什么"）
[Primary CTA]（带用户走到下一步）
```

### 反模式

```
✗ "暂无数据"（用户：所以呢？）
✗ "Nothing here yet"（同上）
✗ 一张全屏的 illustration + 三段文案
✗ 单独一个 "+" 按钮没文字
```

### 推荐范式

```
[empty box icon]
还没有项目
创建你的第一个项目，几秒钟开始追踪
[创建项目]   [查看示例]
```

---

## 4. 错误信息

### 公式：什么错了 + 怎么修

```
✗ "Invalid input"
✓ "邮箱格式不对，例如 you@example.com"

✗ "Required field"
✓ "请填写密码"

✗ "Server error 500"
✓ "保存失败，请重试。如持续出现，请联系我们 →"

✗ "Network error"
✓ "网络似乎断了。检查连接后再试。"
```

### 五级错误对照

| 级别 | 例子 | 视觉 |
|------|------|------|
| Info | "5 条结果" | 中性灰 |
| Tip | "使用 / 快速过滤" | 弱中性 |
| Warning | "更改未保存" | 琥珀 |
| Error | "邮箱格式不对" | 红 |
| Critical | "支付失败，未扣款" | 深红 + icon + 不可忽略 |

### 永远不写

```
✗ "Oops! Something went wrong"（毫无信息）
✗ "Sorry"（道歉无价值）
✗ "Please try again"（用户自然会试）
✗ 堆叠 error（5 个字段错给 5 个 toast）
```

---

## 5. 成功 / 完成

```
✗ "Success!"
✗ "Done!"
✓ "已发送邀请给 3 个成员"
✓ "项目已删除"   ← 同时给 Undo button
✓ "已保存"        ← toast，2 秒后消失
```

### Undo 优先于 confirm

破坏性操作（删除 / 归档）优先：
1. 直接执行
2. Toast 显示"已删除"+ "[撤销]" 按钮
3. 5-7 秒后才真正删

而不是：
- ❌ 弹 confirm modal "确定删除吗？"

confirm modal 只在**真的不可逆**时用（清空账号、永久删除）。

---

## 6. 表单 / 输入

### Placeholder

```
✗ Placeholder 当 label（无障碍灾难）
✗ Placeholder 重复 label（垃圾信息）
✓ Placeholder 给"格式样例"

例子：
  Label: 邮箱
  Placeholder: you@example.com
```

### Helper text

```
✗ "Please enter your password"（label 已经说了）
✓ "至少 8 位，包含字母和数字"
✓ "支持 PDF / DOCX / Markdown，单文件 ≤ 10MB"
```

### Optional vs Required

主流推荐：**标 Optional，不标 Required**（默认必填）。
反例：所有 label 后面都跟 `*`（视觉噪声）。

---

## 7. Onboarding（新手引导）

### 三类用户路径

```
1. Sign-up flow：< 3 步骤，每步 1 个目标
2. First-run experience：进入产品后给 1 个"赢"
3. Empty state：从空到有的引导
```

### 反模式

- 7 步 wizard 强制走完才能用
- Floating tour bubbles 一个接一个指
- 进站立刻弹 modal 让你选 use case + 公司规模 + role + …

### 推荐

- 把 wizard 拆成 form 一屏完
- Tour 改为"提示气泡"等用户主动点开
- 首屏给 1 个"赢"（一个 demo 模板 / 一个 sample 项目）

---

## 8. 微文案声音（Voice & Tone）

### Voice（始终一致）

| 属性 | 选择 |
|------|------|
| 形式 | 简单 vs 正式 → 我们选 **简单** |
| 距离 | "您" vs "你" → 视产品定 |
| 谦逊 | 自夸 vs 自谦 → **自谦但自信** |
| 幽默 | 有 vs 无 → 看场景，**默认无** |

### Tone（看场景调）

| 场景 | Tone |
|------|------|
| 成功 | 平静 + 信息 |
| 错误 | 简洁 + 解决方案 |
| Onboarding | 友善 + 推进 |
| Critical（支付失败） | 严肃 + 明确 |
| Easter egg | 偶有幽默（绝不在工作流里） |

---

## 9. 反模式速查

| 反模式 | 改 |
|--------|----|
| "Click here" | 用具体动词 |
| "Submit" | "保存更改" / "发送" / "创建账号" |
| "Oops! Something went wrong" | 具体描述 + 怎么修 |
| Placeholder 当 label | label 独立显示 |
| 所有 label 标 `*` | 改标 Optional |
| "暂无数据" | 4 要素空状态 |
| "Success!" | 具体说做了什么 |
| 单独 "OK" 按钮 | 改"知道了"或动词 |
| AI 套话："不得不说" "总之" "首先" | 删 |
| 营销自嗨："业内领先 / 革命性 / 颠覆性" | 改用具体数字或客户证言 |
| 长 modal 标题 + 一堆解释 | 标题 1 句，body 1 段 |
| "Please" 满天飞 | 中文版直接删；英文版只在请求时用 |

---

## 10. 中文文案小坑

```
✗ "您好，欢迎使用我们的产品" → 删客套，直接进主体
✗ "请您点击此处确认" → "确认"
✗ 句末加 "哦~" "啦" → 严肃产品禁
✗ "100% 安全" / "绝对" → 改"加密传输"等具体描述
✗ 长文末尾"如有疑问请联系我们" → 改"有问题？写信到 hi@…"
✗ "本产品" → "我们" 或具体产品名
✗ "用户" 作为指代 → "你"
```

### 标点

```
✗ 英文逗号 ,（中文应用 ，）
✗ 半角句号 .（中文应用 。）
✗ 中文里的 "..." → "……"
✓ 数字/英文混排前后加半角空格："已用 5 GB / 共 10 GB"
```

---

## 11. SOP

```
1. 写完一遍后，把文案大声读出来
2. 凡感觉"这是产品在说话"的，改成"人在说话"
3. 凡感觉"AI 写的"的，重写
4. 删一切"please / kindly / 您 / 请 / 哦 / 啦"
5. button：动词 + 名词
6. 错误：什么错 + 怎么修
7. 空状态：4 要素
8. 成功：具体 + Undo 选项
9. 标题：句首大写 / 中文一句话
10. 最后一遍：把所有 "Submit" 找出来 grep 替换
```
