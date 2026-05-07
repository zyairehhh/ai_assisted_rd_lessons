# L01 从已有代码仓开始：Coding Agent 研发最小闭环

本目录是示例课程材料，因此使用 `demo-L01-existing-repo-loop` 目录名。正式版本可由主讲人在 `lessons/L01-existing-repo-loop/` 下维护。

## 本课目标

本课是第一堂正式实战课。目标是让学员在一个已有代码仓中完成完整研发闭环：

1. 生成并改写 AGENTS.md（项目级配置）
2. 写五段式任务描述 prompt
3. 写三层约束 prompt
4. 让 Agent 先读代码再改（先读后改）
5. 进入 Plan Mode 审计划
6. 分步修复 bug、跑测试
7. 用 /clear 和 /compact 管理上下文
8. 生成 validation_report.md 和 context.md

## 为什么从已有代码仓开始

数据库研发日常多数工作不是从空项目写 demo，而是在已有代码库中理解、定位、修改和验证。因此本课包含三个递进练习，模拟真实研发中的 bugfix 流程：

| | A：KVStore | B：Mini SQL Parser | C：Mini Query Executor |
|---|---|---|---|
| 代码 | `src/kvstore/` | `src/minisql/` | `src/miniexec/` |
| Bug 类型 | SQL 漏 WHERE（同根因） | 词法 + 语法（不同根因） | 执行语义（NULL + 分页 + 聚合） |
| 失败测试 | 5 条 | 5 条 | 5 条 |

## 课前准备

1. 完成 L00 的工具配置
2. 阅读 `docs/handout.md`
3. 进入 `exercise/` 完成任务
4. 提交 `context.md` 和 `validation_report.md`

## 课堂安排

| 时段 | 内容 |
|---|---|
| 00:00–00:10 | 心智模型 + 闭环 5 阶段 |
| 00:10–00:25 | 错误用法演示（一句话让 AI 直接修） |
| 00:25–00:50 | 正确用法演示（先读后改 + 分步修 + 写约束） |
| 00:50–01:05 | context.md 与 validation_report.md 写法演示 |
| 01:05–01:20 | 学员高频问题集中讲 |
| 01:20–01:30 | 总结 + 下节课预告 |

## 练习入口

```bash
cd lessons/demo-L01-existing-repo-loop/exercise
cat task.md
```

验证：

```bash
./validators/validate_kvstore.sh
./validators/validate_minisql.sh
./validators/validate_miniexec.sh
```

初始状态下验证会失败（每个练习 5 条测试红），这是练习的一部分。

## 需要提交的产物

- `exercise/context.md`
- `exercise/validation_report.md`
- 修复后的代码（三个练习）
- 每个练习至少 1 条自主设计的测试

## 通过标准

1. 三个 `validate_*.sh` 全部通过
2. `context.md` 说明了提供给 Agent 的上下文、刻意未提供的内容、范围约束、Agent 错误判断记录
3. `validation_report.md` 含五段标准 heading，根因引用具体代码
4. 修改范围集中，没有无关重构
