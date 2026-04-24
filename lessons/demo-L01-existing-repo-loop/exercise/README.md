# L01 练习：修复 MiniDB 中的 LIMIT bug

## 背景

本目录是一个小型已有代码仓，模拟数据库执行器中的查询处理逻辑。它支持非常有限的 SQL 子集：

```sql
SELECT * FROM employees;
SELECT * FROM employees WHERE age > 30;
SELECT * FROM employees WHERE dept = 'db' LIMIT 2;
```

当前代码中存在一个和 `LIMIT` 处理相关的 bug。

## 任务目标

请使用 Coding Agent 辅助完成：

1. 阅读任务和已有代码。
2. 运行测试，确认失败现象。
3. 定位 bug 根因。
4. 修复代码。
5. 必要时补充测试。
6. 运行验证脚本。
7. 填写 `context.md` 和 `validation_report.md`。

## 目录说明

```text
exercise/
├── README.md
├── task.md
├── src/
│   └── minidb/
├── tests/
├── expected-artifacts/
└── validators/
    └── validate.sh
```

## 开始练习

建议先运行初始验证，观察失败测试：

```bash
./validators/validate.sh
```

然后复制上下文和报告模板：

```bash
cp ../../../shared/templates/context.template.md context.md
cp expected-artifacts/validation_report.template.md validation_report.md
```

初始验证会因为预置 bug 失败。请不要先改测试绕过失败。

## 需要提交的产物

- `context.md`
- `validation_report.md`
- 修复后的源码
- 必要时补充的测试

## 约束

- 不要引入外部依赖。
- 不要删除已有测试。
- 不要修改验证脚本来绕过失败。
- 优先只修改 `src/minidb/` 中和 bug 相关的代码。
