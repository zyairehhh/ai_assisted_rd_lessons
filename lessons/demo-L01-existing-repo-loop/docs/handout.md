# L01 课前讲义：从已有代码仓开始 — Coding Agent 研发最小闭环

## 1. 本课要解决什么

本课训练最基础但最重要的研发闭环：

```text
读任务 → 读代码 → 定范围 → 改代码 → 跑测试 → 修失败 → 写总结
```

很多 AI 辅助研发失败，不是因为模型不会写代码，而是因为**任务边界、上下文和验证方式没有给清楚**。

本课通过 3 个练习（A：KVStore、B：Mini SQL Parser、C：Mini Query Executor），让你在已有代码仓上走完这个闭环 3 遍，逐步熟练。

## 2. 三个练习概览

| | A：KVStore | B：Mini SQL Parser | C：Mini Query Executor |
|---|---|---|---|
| 代码 | `src/kvstore/` | `src/minisql/` | `src/miniexec/` |
| Bug 类型 | SQL 漏 WHERE 过滤（同根因） | 词法 + 语法分析（不同根因） | 执行语义（NULL + 分页 + 聚合） |
| 失败测试 | 5 条 | 5 条 | 5 条 |
| 验证 | `validate_kvstore.sh` | `validate_minisql.sh` | `validate_miniexec.sh` |

## 3. 建议工作流（8 步）

### Step 1：生成 AGENTS.md

用 `/init` 生成草稿，然后**你亲自审查和改写**。原则：删掉 Agent 读代码就能推断的东西。

### Step 2：写五段式任务描述 prompt

```
【背景】【上下文】【目标】【约束】【验收】
```

写完先让 Agent 说出理解，不要直接让它改代码。

### Step 3：写三层约束 prompt

- **文件范围**：只允许改哪些文件
- **接口边界**：不改签名、不改数据模型
- **行为边界**：已有测试继续通过

### Step 4：让 Agent 先读代码

要求 Agent **只输出文字，不改代码**——列出 bug 在哪、为什么、怎么修。审查它是真读了还是在猜。

### Step 5：进入 Plan Mode

审计划看四件事：文件清单、有没有新抽象、改动大小、是否支持分步验证。

### Step 6：分步修复

每修完一组 bug 就跑测试。每个练习至少新增一条自主设计的边界测试。

### Step 7：管理上下文

修完一组 bug 后用 `/clear` 清空上下文再继续下一组。长会话用 `/compact` 压缩历史。

### Step 8：写总结

生成 `validation_report.md`（五段结构）和 `context.md`（上下文管理记录），然后**你自己改一遍**。

## 4. 本课常见误区

| 误区 | 问题 |
|---|---|
| 直接让 AI "帮我修这 5 个测试" | 一句话 prompt 导致范围失控 |
| 不看测试输出就让 Agent 继续改 | 不知道验证标准是什么 |
| 让 AI 改测试绕过失败 | 失去训练意义 |
| 不记录 Agent 的错误判断 | 无法复盘为什么做错 |
| 全改完再跑测试 | 出错后不知道哪步引入的 |
| Agent 说不清楚就让它继续改 | 读不懂就改不对 |

## 5. 本课产出

| 产物 | 说明 |
|---|---|
| 修复后的源码（A+B+C） | 三个练习各自的 buggy 文件 |
| 至少 3 条新测试 | 每个练习至少 1 条 |
| `validation_report.md` | 五段标准 heading |
| `context.md` | 上下文管理记录 |

## 6. 验证

```bash
./validators/validate_kvstore.sh
./validators/validate_minisql.sh
./validators/validate_miniexec.sh
```

三个全部通过才算完成。
