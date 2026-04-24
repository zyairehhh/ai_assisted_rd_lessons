# 任务：修复 LIMIT 0 语义错误

## 问题描述

MiniDB 支持简单的 `SELECT` 查询和 `LIMIT` 子句。当前发现：

```sql
SELECT * FROM employees LIMIT 0;
```

预期应返回 0 行，但实际返回了所有行。

## 你的任务

1. 使用测试复现问题。
2. 阅读 `src/minidb/` 中的实现。
3. 找到 `LIMIT 0` 行为错误的原因。
4. 修复代码。
5. 确保已有测试和新增测试通过。
6. 填写 `context.md` 和 `validation_report.md`。

## 建议给 Coding Agent 的第一条指令

```text
请先不要修改代码。请阅读 README.md、task.md、src/minidb 和 tests，说明 LIMIT 0 失败可能和哪些文件有关，列出根因假设和验证计划。
```

## 验证命令

```bash
./validators/validate.sh
```

## validation_report.md 建议结构

```markdown
# Validation Report

## Initial Failure

## Root Cause

## Changes

## Validation

## Remaining Risks
```
