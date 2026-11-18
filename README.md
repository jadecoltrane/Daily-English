# Daily English｜可安装在自己 Claude 账户里的个性化英语学习系统

**每天一页英语课：学新表达、复习旧知识、在连续故事里练习开口，让答错的内容成为下一次练习。**

Daily English 是为 Claude Artifacts 设计的一套英语学习系统。用户使用**自己的 Claude 账户、自己的 AI 使用额度和自己的 Artifact 数据库**；不需要由作者托管英语学习网站，也不需要把学习数据交给作者。

> **仓库状态（2026-11）：公开的技术参考与项目说明，不是待售完整产品的下载页。** 当前仓库中的 `app/index.template.html`、`prompt/system-prompt.template.md`、`seed/`、`tools/build.py` 属于**早期模板**，与作者目前使用的 **V2 单文件 HTML** 不完全一致。不能把旧模板当作已经完成通用化的商业版本。本仓库暂不公开包含完整新版 System Prompt、脚本和界面的待售 HTML，也不包含任何真实学习记录。

## 能做什么

| 功能 | 体验 |
| --- | --- |
| 每日表达 | 按个人目标和水平学习少量实用表达 |
| Review Cards | 根据 got / fuzzy / miss 记录安排间隔复习 |
| Drills | 复练昨天的错误、换场景表达和主动输出 |
| 连续故事与接着聊 | 剧情根据用户的真实回答逐步推进 |
| Listening / Speaking | 听真实素材、复述和口语角色扮演 |
| 表达库 / 答疑本 | 持久保存表达、已掌握内容、易混淆用法 |
| 英语表达与思维训练 | 从真实输出中发现信息组织、搭配、句法和语气问题，而不是限制在固定十条 |

所有内容均以实际发布版本、Claude 账户能力及测试结果为准；本仓库现有旧模板尚未完成全部上述通用能力的验收。

## 产品采用什么架构？

```text
同一套通用 HTML（界面 + System Prompt + 出课脚本）
               │
        在用户自己的 Claude 中运行
               │
        读取该 Artifact 的数据库
         ┌─────┴──────────┐
         │                │
    新用户：无资料     已有用户：有资料
       → 初始化         → 继续学习
         │                │
         └──────┬─────────┘
                ▼
         独立的学习记录与复习进度
```

- **HTML 保存教学系统**：`snapData.cols.system.prompt.text` 保存出课 Prompt；`snapData.cols.system.tools.files` 保存出课脚本；同一页面还包含 AI 批改、故事互动等 Prompt。
- **Artifact 数据库保存学习者状态**：`story/state`（个人资料、目标、故事进度），`bank/phrases`、`bank/usage`、`bank/rules`、`days/YYYY-MM-DD`、`history/YYYY-MM-DD` 等。
- **个人数据不在出售的通用 HTML 中**。即使两个用户使用同样的页面代码，也必须分别建立并验证各自独立的 Artifact 和数据库。
- **新用户初始化**：只有未建立 `story/state` 的用户需要填写称呼、目标、水平、练习时长、偏好场景等；职业和项目经历均为选填。
- **已有用户继续学习**：更新原 Artifact 的 HTML 时必须保留数据库，不重新初始化，不提前结算复习。

作者已在自己的环境中确认：Claude 免费用户可以使用 HTML 创建独立 Artifact。这是**特定环境中的实际测试反馈**，不等于所有账户的 AI 调用、存储权限、跨天续学、安装步骤都已统一验收。是否能用，以购买者自己的 Claude 环境与产品说明为准。

技术细节见 [系统架构](docs/ARCHITECTURE.md) 和 [数据结构](docs/DATA_SCHEMA.md)。

## 为什么现在没有提供完整 HTML？

这是一个**公开仓库**。未来计划一次性交付完整版本，用户购买后可以自行修改自己的教学 Prompt；作者不提供代管 AI 服务，也不打算依靠强制订阅或远程授权来运行课程。

当前仓库保留早期研究模板，方便理解技术原理，但公开代码不代表最终交付物，也不代表所有旧模板功能已被修复。**请勿把旧模板打包冒充完整商业版。**

有关计划的安装、数据备份、升级和验收边界，参见 [用户使用指南（草案）](docs/USER_GUIDE.md)、[交付规范](docs/PRODUCT_DELIVERY.md) 及 [待验证问题](docs/KNOWN_ISSUES.md)。

## 日常使用方式（适用于完成安装的版本）

1. 用户在自己的 Claude 中创建 Artifact，并确认其数据库可以正常保存数据。
2. 第一次使用，根据页面/Claude 的引导初始化个人学习目标。数据库已有资料时跳过。
3. 在具有 Artifact 访问权限的 Claude 对话中发起「出今天的课」。Claude 读取**页面内的当前 System Prompt** 和**自己的数据库**，生成当天课程并写回数据库。
4. 打开自己的学习页面完成练习；第二天出课时根据已有答案和到期表达继续学习。

**每日出课不等于自动定时出课。** 是否能定时触发取决于 Claude 账户和额外配置，本项目不作统一承诺。

## 自由修改与数据备份

- 用户可以在自己的副本中修改 Prompt、课程主题、教学规则；修改不应直接覆盖 `story/state`、`bank`、`days` 和 `history`。
- HTML **不是**数据库备份。用户可以请有 Artifact 数据库访问权限的 Claude 只读导出全部集合、全部文档为 JSON，并将备份文件保存在 Claude 之外。
- 若要跨账号恢复，需在新的独立 Artifact 中写回数据并验证；**仅上传 JSON 不等于已经恢复成功**。
- 作者只计划提供必要的严重 Bug 修复，不承诺持续增加功能、自动更新、人工代管或保证所有 Claude 版本兼容。

## 仓库内仍保留的早期文件

| 路径 | 状态 |
| --- | --- |
| [`app/index.template.html`](app/index.template.html) | **旧版页面模板**；不是最新 `snapData` 成品 |
| [`prompt/system-prompt.template.md`](prompt/system-prompt.template.md) | **旧版独立 Prompt**；含车机设计求职默认情景 |
| [`config.example.json`](config.example.json) | 旧版构建配置示例，不是新版首次初始化 |
| [`tools/build.py`](tools/build.py) | 旧版 Python 占位符替换工具 |
| [`seed/`](seed/) | 旧版数据库初始结构参考，不可直接当作 V2 真实用户数据 |
| [`docs/KNOWN_ISSUES.md`](docs/KNOWN_ISSUES.md) | 历史审计，所述问题不等于已全部修复 |
| [`docs/example-day.json`](docs/example-day.json) | 示例课程数据 |
| [`docs/PRODUCT_DELIVERY.md`](docs/PRODUCT_DELIVERY.md) | 新版产品交付原则和验收清单 |
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | 准备给买家的操作说明（草案，非已验收功能） |

如需研究旧版模板，请注意：旧方案要求 `system/prompt` 数据库文档、`config.json` 和 Python 构建；**V2 的规则权威来源已改为 HTML 内的 `snapData`**。不要将这两种架构混用。

## 隐私、授权与声明

- 仓库不包含原作者的真实课程、答题记录、表达库和 Artifact 数据库备份。
- 请不要将个人备份 JSON、真实工作经历、访问令牌或包含私密内容的 HTML 提交到公开仓库。
- Daily English 是独立制作的第三方 Claude 学习工具，并非 Anthropic / Claude 官方产品；不包含 Claude 会员、无限使用额度或托管 AI 服务。
- **本仓库目前未附开源许可证**；公开可见不代表自动授予复制、修改、再分发或商业使用的许可。未来付费版的授权条款应在销售时单独明确。
