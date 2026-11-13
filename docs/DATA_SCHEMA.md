# 数据结构（均为数据库文档，"集合/文档 id"）

字段名被页面读取，改名会让页面失效。

## `system/prompt`
`{note, text}`：规则说明书全文（模板见 `prompt/`）。

## `bank/phrases`
`{note, rows: [{date, scene, chunk, zh, ex, level, due}], mastered: [{chunk, zh, ex, mastered}]}`
- `level` = 复习次数（0–3；4 = 移入 mastered），`due` = 下次复习（YYYY-MM-DD），新行放最前面。

## `bank/usage`（答疑本）
`{note, rows: [{date, group, type, rule, myCase, ex, source, stage, due, lastRight, lastWrong}]}`
- `stage`：`"1"`、`"1 对比"`、`"2"`、`"3"`；`due` 为日期或 `"已掌握"`。

## `bank/rules`
`{note, rows: [{n, rule, ex}]}`：英语思维规律，只读，批改时用编号引用。

## `story/state`
故事和出课的长期状态，种子见 `seed/story-state.json`。主要键：`episode`、`pending`、`log`、`nextHook`、`standing`、`portfolio`、`focusPool/focusLog`、`topicLog`、`drillLog`、`usedClips`、`listenLast`、`teacherNotes`（后来的纠正，优先于说明书）、`voiceBoiler`、`drillBoiler`、`weeklyTopic`。
- 注意：键名 `jade`（学习者简介）沿用原版命名，说明书里引用的就是这个键。

## `history/YYYY-MM-DD`（旧课的瘦身存档）
超过 7 天的 `days` 文档，在删除前先把**除 `lesson`、`cards` 以外的所有字段**（日期、场景、`results`、`typed`、`answers`、`done` 及其他页面写入的字段）写到这里，写成功后才删原文档。页面不读这个集合，永不自动删除。按原作者的真实数据估算，一份约 0.1–11 KB（对比整份 24–33 KB）。

## `days/YYYY-MM-DD`（每天一份）
出课时写入：`date, label, scene, cards[], lesson{…}, results{}, typed{}, answers{}, done{}`。
页面写入（重写当天文档时必须保留）：`results`（`got|fuzzy|miss`）、`typed`、`answers`、`replies`、`adapted`、`fhint`、`quickAns`、`thinkAns`、`thinkFb`、`bossScore`、`stalls`、`done`。
- `cards[]`：`{key, chunk, level, stage(gap|use|choice), prompt, hint, answer, example, why?}`；答疑本卡另有 `kind:"usage", step, form, rule, rows[], myCase`。
- `lesson` 包含：`chunks, quick, situation, story, dialogue, practice, fix, listen, talk, think, voice, paused`。
- 完整的字段示例：`docs/example-day.json`。
