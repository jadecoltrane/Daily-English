# Daily English：V2 架构与旧模板区别

## 当前目标架构（V2）

```text
每个使用者自己的 Claude 账户
       │
       ├─ Artifact HTML（通用、可由用户自行修改）
       │    ├─ snapData.cols.system.prompt.text   出课 System Prompt
       │    ├─ snapData.cols.system.tools.files    出课/校验脚本
       │    ├─ snapData.cols.system.appendix       数据和手动兜底规则
       │    ├─ snapData.cols.system.followups      回答/追问规则
       │    ├─ snapData.cols.system.thinkingRules  初始参考规律
       │    └─ 页面 JS                          批改、Drills、故事互动
       │
       └─ 与该 Artifact 关联的数据库（个人数据）
            ├─ story/state                       个人档案、故事进度和配置
            ├─ bank/phrases                      表达、掌握状态、复习日期
            ├─ bank/usage                        答疑本
            ├─ bank/rules                        兼容旧版的参考规律数据
            ├─ days/YYYY-MM-DD                   课程、答案、批改
            └─ history/YYYY-MM-DD                历史归档
```

出课由 Claude 对话按页面内 Prompt 和数据库状态执行；HTML 本身不会在本地离线自动生成课程，网页内的部分 AI 互动仍依赖 Artifact 提供的 AI 能力。

### 课程如何延续

1. **第一次**：目标 Artifact 的 `story/state` 不存在，才走新用户初始化；不要求所有用户具备作品集、行业背景或求职经历。
2. **日常出课**：Claude 读取现有学习资料、到期表达和历史答题；执行复习结算，生成并写入 `days/当天`，页面渲染当天内容。
3. **页面学习**：用户答题后将结果写入当前 Artifact 的数据库。
4. **用户自己修改规则**：修改的是当前 Artifact 的 HTML / Prompt；数据仍保存在该 Artifact 自己的数据库里。
5. **少量严重 Bug 修复**：用户需要更新**原 Artifact 的 HTML**，而不是新建空数据库的 Artifact。升级须检查数据结构兼容、确认旧数据未被重置；不承诺自动推送更新。

### 表达库

「表达库」按钮、查看界面和空状态属于 HTML；真实表达和答疑记录在 `bank/phrases`、`bank/usage`。新用户最初为空；必须区分“加载中”“尚未初始化”“已初始化但无内容”“读取失败”，不能无限显示加载中。既有用户更新 HTML 后，应继续看到此前积累的数据。

### 英语表达与思维训练

教学原则为**开放式、情境化的表达训练**：关注句法、搭配、信息组织、语气、互动等，不应因为固定十条规律之外的错误就不批改，也不应把正确自然的不同说法误判为错。早期 `bank/rules` 中的编号规律是参考数据，为旧用户兼容而保留；不能强制覆盖或清空已有记录。

### 个人隐私与迁移

- 每个买家创建并维护自己的独立 Artifact；不共享原作者的 Artifact 数据。
- HTML 不等于学习数据的备份。使用具有权限的 Claude 数据库工具只读导出全部 `story`、`bank`、`days`、`history` 等实际存在的集合，保留文档 ID、日期、字段，下载到 Claude 之外。
- 数据恢复是单独的写回与核验操作；尚未完成的恢复不得宣称成功。

## GitHub 中的历史模板不是 V2

本仓库 `app/index.template.html` 和 `prompt/system-prompt.template.md` 是更早的**独立 Prompt 模板架构**：`system/prompt` 保存在数据库，`config.json` 通过 Python 注入学习者信息。此方案和 V2 的 `snapData` 方案不同；历史模板**未被自动迁移为通用商品**。

因此：不要同时告诉 Claude “从数据库的 system/prompt 出课”与“从页面 snapData 出课”。不同版本应以实际 HTML 为准。

## 验收边界

目前已有的用户实测反馈是：Claude 免费账户可以根据 HTML 创建自己的 Artifact。仍需单独验证新用户初始化、完整 AI 功能、跨天数据保留、复习正确性、不同 Artifact 的数据隔离，以及**更新原 Artifact 的 HTML 而不重置数据库**。静态源码审查不能替代这些端到端测试。

参见 [交付与测试清单](PRODUCT_DELIVERY.md)。
