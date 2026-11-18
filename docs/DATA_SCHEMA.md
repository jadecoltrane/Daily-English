# Daily English 数据结构与兼容性说明

**本文件描述目标 V2 的数据归属。** 早期 `seed/`、独立 Prompt 和构建工具已从公开仓库移除。最终字段以实际交付的 HTML、内嵌脚本及运行时数据库为准。

## 数据存放原则

| 位置 | 内容 | 规则 |
| --- | --- | --- |
| HTML：`snapData.cols.system.prompt.text` | 生成每日课程的完整 Prompt | V2 的权威规则，**不再写进数据库的 `system/prompt`** |
| HTML：`snapData.cols.system.tools.files` | `prepare.js`、`finalize.js`、`scheduler.js` | 出课准备、结算和校验 |
| HTML：`snapData.cols.system.appendix` / `followups` | 数据字段说明和课后问答规则 | 随 HTML 发布 |
| HTML：`snapData.cols.system.thinkingRules` | 初始英语思维规律参考 | 供新用户初始化参考；不是封闭批改标准 |
| 数据库：`story/state` | 称呼、目标、英语水平、场景偏好、真实经历、故事状态 | 仅数据库缺失时首次初始化，不能因升级覆盖 |
| 数据库：`bank/phrases` | `rows`、`mastered` | 表达及其间隔复习进度 |
| 数据库：`bank/usage` | `rows` | 答疑本 |
| 数据库：`bank/rules` | `rows: [{n,rule,ex}]` | 旧版兼容；已有用户不能自动清空 |
| 数据库：`days/YYYY-MM-DD` | 当天课程、回答、批改、完成标记 | 一天一文档 |
| 数据库：`history/YYYY-MM-DD` | 旧课归档 | 不等于完整数据备份 |

### 核心字段约定

- `bank/phrases.rows`：`{date, scene, chunk, zh, ex, level, due}`；`mastered` 为 `{chunk, zh, ex, mastered}`。
- `bank/usage.rows`：`{date, group, type, rule, myCase, ex, source, stage, due, lastRight, lastWrong}`。
- `story/state`：现有 V2 兼容字段含 `name`、`jade`（**历史字段名，不代表学习者必须是 Jade**）、`scenes`、`portfolio`、`company`、`characters`、`arc`、`episode`、`log`、`pending`、`nextHook`、`standing`、`drillLog`、`focusLog`、`usedClips` 等。重命名字段前必须逐一校验依赖脚本。
- `days/` 中页面写入的 `results`、`typed`、`answers`、`replies`、`adapted`、`thinkAns`、`thinkFb`、`quickAns`、`bossScore`、`done` 等，重出课时必须保留。
- 旧课只应在确认归档成功且策略允许后删除。完整备份需要导出**全部**集合/文档，不是最近七天页面列表。

### 更新规则

修改 Prompt 或 HTML 不意味着自动修改数据库。已有用户应继续读取原来的 `story/state` 与 `bank`；仅新用户空库时运行初始化。**不要让新用户的空初始化数据覆盖已有学习记录。**

复习次数和到期日期是学习状态，不应该在未作答时提前增加。AI 批改必须接受语境中自然的变体，不得因与示例答案不同而机械扣错。

### 与历史架构的区别

早期系统曾将完整规则写入数据库 `system/prompt`；这套文件已从当前公开分支删除。V2 的权威规则存放在 HTML 的 `snapData`，不得再要求用户额外初始化数据库中的 `system/prompt`。

参见 [架构](ARCHITECTURE.md) 与 [产品交付规范](PRODUCT_DELIVERY.md)。
