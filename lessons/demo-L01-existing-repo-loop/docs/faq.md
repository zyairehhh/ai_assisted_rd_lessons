# L01 FAQ

## Q1: 初始验证失败是不是环境问题？

不是。每个练习的初始状态故意包含 bug，验证脚本失败是预期现象（每个练习 5 条测试失败）。你需要阅读失败信息并修复代码。

## Q2: 可以修改测试吗？

可以**新增**测试（步骤 6.3 要求至少加一条），但**不能删除或修改**已有测试。不要通过改测试来绕过 bug。

## Q3: 三个练习可以用同一个 AGENTS.md 吗？

可以。AGENTS.md 是项目级的，三个练习共用一个 `exercise/AGENTS.md`。但 Boundaries 段需要覆盖所有三个练习的红线。

## Q4: 三个练习的 context.md 和 validation_report.md 分开写还是合并？

合并写一份即可。在 Root Cause 段分别列出三个练习的根因，Changes 段分别列出改了哪些文件。

## Q5: 如果 Agent 判断错了怎么办？

在 `context.md` 中记录错误判断、你的纠正方式和依据。这是本课训练的重要部分——"Agent 的错误判断与人工纠正"是 context.md 的必填板块。

## Q6: 每个练习的验证命令是什么？

```bash
./validators/validate_kvstore.sh     # 练习 A
./validators/validate_minisql.sh     # 练习 B
./validators/validate_miniexec.sh    # 练习 C
```

## Q7: validation_report.md 需要哪五段？

```
## Initial Failure
## Root Cause
## Changes
## Validation
## Remaining Risks
```

验证脚本会检查这五个 heading 是否存在。

## Q8: 同一处改了 3 次还没绿怎么办？

这是停止信号。不要在污染的 context 里硬拧——用 `/clear` 清空上下文，写一条更好的 prompt 重来。
