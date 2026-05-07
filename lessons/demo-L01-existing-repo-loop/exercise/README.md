# L01 练习：Coding Agent 研发最小闭环 — 修复代码中的 bug

## 背景

本目录包含三个练习项目，**按 A → B → C 顺序全部完成**，难度递进。

### 练习 A：KVStore — SQL 过期一致性 bug

`src/kvstore/` 是一个 SQLite-backed 微型 KV 引擎。`get()` / `ttl()` 正确过滤了过期行，但**其它查询路径的 SQL 漏了 WHERE 过滤**。

> 数据库工程师日常踩的真实坑：**SELECT / DELETE 漏 WHERE 过滤已过期 / 软删除行**。

### 练习 B：Mini SQL Parser — 词法 + 语法分析 bug

`src/minisql/` 是一个教学用迷你 SQL 解析器。`Lexer` 在处理字符串字面量时有两个 bug，`Parser` 在处理括号分组条件时有一个 bug。

> tokenizer 不追踪引号状态、类型混淆、递归下降解析器括号只剥一层。

### 练习 C：Mini Query Executor — 执行语义 bug

`src/miniexec/` 是一个教学用内存查询执行器。`Executor` 在 LIMIT+OFFSET 分页和 COUNT(column) 聚合时有 bug，`Evaluator` 在 NULL 比较语义上有 bug。

> OFFSET 偏移计算错误、NULL 三值逻辑、COUNT(*) 与 COUNT(column) 的区别。

## 任务目标

完成本练习后，学员应能够：

1. 在已有代码仓中读懂跨多个文件的"行为不一致"类 bug
2. 用 Coding Agent 走完「读任务 → 读代码 → 定范围 → 改代码 → 跑测试 → 修失败 → 写总结」闭环
3. 从已有失败测试中识别 bug，并自主设计边界测试
4. 输出符合规范的 `context.md` 和 `validation_report.md`

## 目录说明

```text
exercise/
├── README.md
├── task.md                                # 任务说明（必读）
├── src/
│   ├── kvstore/                           # 练习 A
│   │   ├── store.py                       #   含 bug — 可修改
│   │   ├── persistence.py                 #   含 bug — 可修改
│   │   ├── parser.py                      #   ⚠ 不要修改
│   │   └── cli.py                         #   ⚠ 不要修改
│   ├── minisql/                           # 练习 B
│   │   ├── lexer.py                       #   含 bug — 可修改
│   │   ├── parser.py                      #   含 bug — 可修改
│   │   ├── ast_nodes.py                   #   ⚠ 不要修改
│   │   └── formatter.py                   #   ⚠ 不要修改
│   └── miniexec/                          # 练习 C
│       ├── executor.py                    #   含 bug — 可修改
│       ├── evaluator.py                   #   含 bug — 可修改
│       └── table.py                       #   ⚠ 不要修改
├── tests/
│   ├── test_store.py                      # 练习 A 测试
│   ├── test_persistence.py
│   ├── test_parser.py                     # kvstore parser 测试
│   ├── test_minisql_lexer.py              # 练习 B 测试
│   ├── test_minisql_parser.py
│   ├── test_minisql_formatter.py
│   ├── test_miniexec_executor.py          # 练习 C 测试
│   └── test_miniexec_evaluator.py
├── expected-artifacts/
│   └── validation_report.template.md
└── validators/
    ├── validate_kvstore.sh                # 练习 A 验证
    ├── validate_minisql.sh                # 练习 B 验证
    └── validate_miniexec.sh               # 练习 C 验证
```

Python 3.10+，零第三方依赖。

## 开始练习

1. 阅读 [`task.md`](task.md)
2. 查看初始失败（每个练习 baseline 都有 **5 条失败测试**）：

```bash
./validators/validate_kvstore.sh
./validators/validate_minisql.sh
./validators/validate_miniexec.sh
```

3. 按 task.md 的 8 步流程，依次完成 A → B → C

> 初始验证应失败——这是练习的一部分。**不要先改测试绕过失败。**

## 需要提交的产物

| 产物 | 说明 |
|---|---|
| 修复后的源码（A） | `store.py` + `persistence.py` |
| 修复后的源码（B） | `lexer.py` + `parser.py` |
| 修复后的源码（C） | `executor.py` + `evaluator.py` |
| 至少 1 条新测试 | 自主设计的边界测试 |
| `validation_report.md` | 五段标准 heading |
| `context.md` | 上下文管理记录 |

## 时间预算

预计 60–70 分钟。建议分配：

| 时段 | 内容 |
|---:|---|
| 5 min | 读任务、跑验证脚本、列 5 条失败 |
| 10 min | 读源码、定位 bug |
| 25 min | 分步修复（每修一组跑测试） |
| 10 min | 自主设计 1 条边界测试 |
| 15 min | 写 context.md + validation_report.md |

## 常见错误

| 现象 | 原因 |
|---|---|
| Agent 想改 schema / AST / Table 定义 | 缺约束——把约束粘到 prompt 里再来一次 |
| Agent 想"顺便"改不在范围的文件 | 同上 |
| 修了部分 bug 但仍漏一两条失败 | 用 `git diff` 过一遍所有改动，确认没遗漏 |
| `validate_*.sh` 报缺 heading | `validation_report.md` 没用模板 |
| 同一处反复修 ≥3 次还没绿 | `/clear` + 更好的 prompt 重来 |
