# 任务：修复代码中的 bug — Coding Agent 研发最小闭环

## 选择你的练习

三个练习**都要完成**，按 A → B → C 顺序做，难度递进：

| | A：KVStore | B：Mini SQL Parser | C：Mini Query Executor |
|---|---|---|---|
| 代码位置 | `src/kvstore/` | `src/minisql/` | `src/miniexec/` |
| Bug 类型 | SQL 漏 WHERE 过滤（同根因） | 词法 + 语法分析（不同根因） | 执行语义错误（NULL + 分页 + 聚合） |
| 失败测试 | 5 条（2 文件、3 class） | 5 条（2 文件、4 class） | 5 条（2 文件、3 class） |
| 可修改文件 | `store.py` + `persistence.py` | `lexer.py` + `parser.py` | `executor.py` + `evaluator.py` |
| 验证命令 | `./validators/validate_kvstore.sh` | `./validators/validate_minisql.sh` | `./validators/validate_miniexec.sh` |

---

## 练习 A 背景：KVStore

`src/kvstore/` 是一个 SQLite-backed 微型 KV 引擎：

- `store.py` — `KVStore` 类，单表 schema `kv(key, value, expires_at)`
- `persistence.py` — `Snapshot.dump` / `Snapshot.load`，导出/恢复为 JSON
- `parser.py` / `cli.py` — 命令解析与 REPL（**不在修改范围**）

`get()` / `ttl()` 实现了懒过期——读到过期行时清理。但**其它 SQL 查询路径没有在 WHERE 子句中过滤已过期行**，导致不同 API 看到不同的"key 集合"。

> 这是数据库工程师日常踩的真实坑：**SELECT 漏 WHERE 过滤软删除/已过期行**。

---

## 练习 B 背景：Mini SQL Parser

`src/minisql/` 是一个教学用迷你 SQL 解析器（SELECT / INSERT / UPDATE / DELETE）：

- `lexer.py` — `Lexer` 类，SQL 字符串 → Token 列表（词法分析）
- `parser.py` — `Parser` 类，Token 列表 → AST（语法分析）
- `ast_nodes.py` / `formatter.py` — AST 定义 + 格式化（**不在修改范围**）

数据流：`SQL 字符串` → `Lexer` → `[Token]` → `Parser` → `AST`

当前 `Lexer` 在处理**字符串字面量**时有两个 bug，`Parser` 在处理**括号分组条件**时有一个 bug。

> 这三个 bug 是数据库系统中常见的真实问题：tokenizer 不追踪引号状态（SQL 注入的经典根源）、类型混淆（ORM 框架常踩的坑）、递归下降解析器括号只剥一层（每个手写 parser 的必经之路）。

---

## 练习 C 背景：Mini Query Executor

`src/miniexec/` 是一个教学用内存查询执行器，对 `Table`（行列表）执行 SELECT / INSERT / UPDATE / DELETE 和聚合：

- `executor.py` — `Executor` 类，SELECT（投影、过滤、排序、分页）、INSERT / UPDATE / DELETE、聚合函数
- `evaluator.py` — `Evaluator` 类，评估 WHERE 条件（比较、IS NULL、AND/OR）
- `table.py` — `Table` 数据类（**不在修改范围**）

当前 `Executor` 在 **LIMIT+OFFSET 分页**和 **COUNT(column) 聚合**时有 bug，`Evaluator` 在 **NULL 比较语义**上有 bug。

> 三个 bug 对应数据库执行引擎的经典陷阱：OFFSET 偏移计算错误（分页 bug 是 StackOverflow 上 SQL 问题的前 10 名）、NULL 三值逻辑（每个数据库初学者都会踩）、COUNT(*) 和 COUNT(column) 的区别（SQL 标准中最常被误解的语义之一）。

---

## 复现

```bash
# 练习 A
./validators/validate_kvstore.sh

# 练习 B
./validators/validate_minisql.sh

# 练习 C
./validators/validate_miniexec.sh
```

baseline 应有 **5 条测试失败**。

---

## 你的任务

本练习共 **8 步**，按课堂 PPT 顺序编排。前 5 步练习"怎么给 Agent 派活"，第 6 步执行修复，第 7 步练习上下文管理，第 8 步写总结。**每步写的 prompt 直接喂给 Agent 执行。**

---

### 步骤 1：生成并改写 AGENTS.md

> 对应 PPT：项目级配置约束（Slide 11-12）

让 Agent 为本项目生成 `AGENTS.md`，然后**你亲自审查和改写**。

**做法**：

1. 使用 `/init` 命令让 Agent 自动生成 `AGENTS.md` 草稿（它会阅读项目结构、README、代码后生成）
2. 按以下原则审查：
   - ✅ 应包含：Project 简介（一句话）、Commands（测试/验证命令）、Boundaries（红线）
   - ❌ 不用写：Agent 读代码就能推断的东西、语言标准约定、逐文件描述
3. 关键判断：**每写一行问自己"删掉这行 Agent 会犯错吗？"** 如果不会，就删掉
4. 改写后的 `AGENTS.md` 放在 `exercise/` 目录下

**参考结构（以练习 A 为例）**：

```markdown
# AGENTS.md
## Project
SQLite-backed KVStore — 教学用微型 KV 引擎，Python 3.10+，零第三方依赖。

## Commands
- Test all: `python3 -m unittest discover -s tests -v`
- Validate: `./validators/validate_kvstore.sh`

## Boundaries
- Do NOT modify kv table schema
- Do NOT modify get() / ttl() implementations
- Do NOT add third-party dependencies
```

**产出**：`exercise/AGENTS.md`

---

### 步骤 2：写一条五段式任务描述 prompt

> 对应 PPT：Prompt 怎么写 — 任务描述模板（Slide 8-9）

用五段式模板，为本次 bug 修复**自己写一条完整的 prompt**：

```
【背景】这段代码做什么、为什么要改它（1-3 句）
【上下文】读哪些文件、重点看什么（列出文件路径 + 阅读焦点）
【目标】这次改动要达成的可验证结果（1 句，只写一个目标）
【约束】哪些文件能改 / 不能改 / 不改的行为
【验收】跑哪条命令、看到什么算成功
```

**要求**：

- 【背景】练习 A 提到 schema 和 `get()` 的懒过期机制；练习 B 提到 lexer → parser → AST 的数据流；练习 C 提到 Executor 对 Table 做查询的流程
- 【上下文】列出具体文件路径和阅读焦点。练习 A 参考 `get()` 作为正确标杆；练习 B 参考 `formatter.py` 和 `ast_nodes.py` 理解正确数据结构；练习 C 参考 `table.py` 理解数据模型
- 【目标】只写一个，不要塞多个任务
- 【验收】用命令（`./validators/validate_*.sh`），不要只用文字描述
- 避免二义性词：优化 / 清理 / 重构

写完后喂给 Agent，**但先不要让它执行，要求它说出自己的理解**——观察 Agent 是否理解了任务。

**自查**：你的 prompt 是否超过 5 行？如果只有一句话（如"帮我修这 5 个测试"），回去看 PPT Slide 9 的反例对照。

---

### 步骤 3：用三层限制法写约束范围 prompt

> 对应 PPT：Prompt 怎么写 — 定范围约束（Slide 10）

在步骤 2 的基础上，细化约束段，单独写一条约束 prompt 喂给 Agent：

| 层级 | 说明 | 练习 A | 练习 B | 练习 C |
|---|---|---|---|---|
| **文件范围** | 只允许修改哪些文件 | `store.py` + `persistence.py` | `lexer.py` + `parser.py` | `executor.py` + `evaluator.py` |
| **接口边界** | 不改签名、不改数据模型 | 不改 `get()`/`ttl()`、不改 schema | 不改 `Token`、不改 AST 定义 | 不改 `Table` 类、不改公开 API |
| **行为边界** | 已有通过的测试继续通过 | CLI 不变、JSON schema 不变 | formatter 输出不变 | 已通过的聚合/排序测试不变 |

将约束作为补充指令喂给 Agent。

**自查**：三层都覆盖了吗？回想 PPT 翻车案例——Agent 改了 schema/AST 定义（缺接口边界）、改了测试（缺行为边界）、改了不该改的文件（缺文件范围）。

---

### 步骤 4：让 Agent 先读代码和文档

> 对应 PPT：先读后改（Slide 14-16）

写一条 prompt，要求 Agent **只输出文字，不改任何代码**：

**练习 A**：
1. 阅读 `store.py`、`persistence.py`、相关测试文件
2. 用 5 句话描述当前过期机制怎么工作
3. **把每个方法用的 SQL 列出来，逐条标注是否漏了 WHERE 过滤 `expires_at`**
4. 给出修复假设，指出怀疑的代码行
5. 给出修改计划：分几步、动哪个文件、改哪条 SQL

**练习 B**：
1. 阅读 `lexer.py`（注意 `_split` 和 `_classify`）、`parser.py`（注意 `_parse_primary_condition`）、相关测试文件
2. 用 5 句话描述 SQL → Token → AST 的数据流
3. **把 5 条失败测试列出来，逐条分析为什么失败、bug 在哪个方法的哪一行**
4. 给出修复假设，指出怀疑的代码行
5. 给出修改计划：分几步、动哪个文件、改哪个方法

**练习 C**：
1. 阅读 `executor.py`（注意 `_apply_limit` 和 `aggregate`）、`evaluator.py`（注意 `=` / `!=` 分支）、相关测试文件
2. 用 5 句话描述 Table → Evaluator → Executor 的协作方式
3. **把 5 条失败测试列出来，逐条分析为什么失败、bug 在哪个方法的哪一行**
4. 给出修复假设，指出怀疑的代码行
5. 给出修改计划：分几步、动哪个文件、改哪个方法

末尾加上："**我会 review 你的输出，确认后再让你动代码。**"

**审查 Agent 的输出**——判断它是真读了还是在猜：

| 真读了 ✅ | 在猜 ❌ |
|---|---|
| 引用具体函数名、SQL 片段 / 代码行号 | 教科书式泛泛描述，可以套用在任何项目 |
| "`SELECT key FROM kv` 缺少 WHERE 过滤" | "建议检查过期逻辑是否完善" |
| "`_split` 遇到空格无条件 append" | "可能存在字符串处理问题" |

**如果 Agent 说不清楚，说明它还没读懂，不要让它继续改。**

---

### 步骤 5：进入 Plan Mode 审计划

> 对应 PPT：Plan Mode — 系统级"只读锁"（Slide 15）

1. 进入 Plan Mode（`Shift+Tab` 或 `Tab`）
2. 让 Agent 基于前面的任务描述和约束，输出修复计划
3. **审计划看四件事**：
   - ☐ 文件清单只含授权文件？
   - ☐ 有没有冒出新 class / helper / 文件？
   - ☐ 每个改动点预估多大？（修 bug 应该是几行，不是几十行）
   - ☐ 改动顺序支持分步验证？（改一组跑一次，不是全改完再跑）
4. 确认后选择执行模式（Auto / Accept Edits / 手动审批）

**何时该用 Plan Mode**：修改 ≥2 个文件、方向不确定时。**何时不用**：改动一句话能描述清楚（修 typo、加 log）。

---

### 步骤 6：执行修复

按 Agent 的计划，**分步执行**修复。每修完一组 bug 就跑测试，不要全改完再跑。

#### 练习 A：修复 KVStore

##### 6A.1 修复 store.py 的过期一致性 SQL bug

`KVStore` 的 `get()` 和 `ttl()` 已经在 Python 层做了过期判断。但下面这些方法的 SQL 查询**完全没有过滤** `expires_at`：

| 方法 | 当前 SQL | 期望行为 |
|---|---|---|
| `keys()` | `SELECT key FROM kv` | 不返回已过期 key |
| `__len__` | `SELECT COUNT(*) FROM kv` | 不计入已过期 key |
| `__contains__` | `SELECT 1 FROM kv WHERE key = ?` | 对已过期 key 返回 False |
| `delete()` | `DELETE FROM kv WHERE key = ?` 然后看 rowcount | 已过期 key 视为不存在，应返回 False |

要求：
- 让上面四个方法对已过期行的处理与 `get()` / `ttl()` 一致
- **不允许修改 `get()` / `ttl()`**（它们是已知正确的参考实现）
- **不允许改 schema**

> **提示**：最自然的修复是把 `WHERE expires_at IS NULL OR expires_at > ?` 子句加进对应 SQL，并绑定 `time.time()` 参数。

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_store -v
```

##### 6A.2 修复 persistence.py 的 snapshot SQL 一致性

`Snapshot.dump()` 当前 SQL `SELECT key, value, expires_at FROM kv` 也漏了 WHERE 过滤。

要求：让 `Snapshot.dump()` 只持久化未过期的行。**不允许调整 JSON schema**。

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_persistence -v
```

##### 6A.3 至少新增一条自主设计的测试

预置的 5 条失败测试不覆盖所有边界。请新增**至少一条**测试，覆盖以下任一类（自选）：

- `expire(key, ex)` 在 key 已过期但尚未清理时的返回值
- `Snapshot.load()` 重复执行的幂等性
- `set()` 在已过期 key 上覆写时 TTL 的清空行为
- SQL 层边界（如 `expires_at = time.time()` 这一刻的判定）

---

#### 练习 B：修复 Mini SQL Parser

##### 6B.1 修复 lexer.py 的字符串处理 bug

`Lexer` 的 `_split()` 和 `_classify()` 各有一个 bug：

| 方法 | 当前行为 | 期望行为 |
|---|---|---|
| `_split()` | 遇到空格无条件分割，`'John Doe'` → `"'John"` + `"Doe'"` | 在引号内的空格不应分割 |
| `_classify()` | `'123'` 判定为 `Token('INTEGER', 123)` | `'123'` 应为 `Token('STRING', '123')` |

要求：
- `_split()` 需要追踪当前是否在单引号内，在引号内不对空格和符号做分割
- `_classify()` 需要删除或修改错误的 `isdigit()` 判断分支
- **不允许修改 `Token` 的字段定义**
- **不允许改 `ast_nodes.py`**

> **提示**：`_split()` 最自然的修复是加一个 `in_quote: bool` 状态变量，遇到 `'` 时翻转状态，在 `in_quote == True` 时跳过所有分割逻辑。

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_minisql_lexer -v
```

##### 6B.2 修复 parser.py 的括号递归 bug

`Parser._parse_primary_condition()` 在处理括号分组时，括号内调用 `_parse_comparison()` — 只能处理单个比较，应调用 `_parse_condition()` — 支持 AND/OR 和嵌套括号。

要求：
- 把 `_parse_primary_condition()` 中括号分支里的函数调用从 `_parse_comparison()` 改为 `_parse_condition()`
- **一行改动**，不需要更多

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_minisql_parser -v
```

##### 6B.3 至少新增一条自主设计的测试

预置的 5 条失败测试不覆盖所有边界。请新增**至少一条**测试，覆盖以下任一类（自选）：

- 字符串内含单引号的转义（如 `'it''s'`）
- 三层嵌套括号 `(((a = 1)))`
- `WHERE a = '123' AND b = 456` — 字符串 `'123'` 与整数 `456` 共存
- `LIKE` 模式中带空格（如 `LIKE 'John %'`）

---

#### 练习 C：修复 Mini Query Executor

##### 6C.1 修复 evaluator.py 的 NULL 比较语义 bug

`Evaluator.evaluate()` 在处理 `=` 和 `!=` 运算符时没有对 NULL 做特殊处理：

| 表达式 | Python 行为 | SQL 正确语义 |
|---|---|---|
| `None == None` | `True` | `NULL = NULL` → NULL（falsy） |
| `None != 'active'` | `True` | `NULL != 'active'` → NULL（falsy） |

注意：`<`、`>`、`<=`、`>=` 已经正确处理了 NULL（因为 Python 3 会 TypeError），只有 `=` 和 `!=` 漏了。

要求：
- 在 `=` 和 `!=` 的比较逻辑前增加 NULL 守卫——如果任一操作数为 None，直接返回 False
- **不允许修改 `IS` / `IS NOT` 的逻辑**（它们是正确的）
- **不允许修改 `table.py`**

> **提示**：最自然的修复是在 `=` / `!=` 分支前加一行：`if row_val is None or value is None: return False`

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_miniexec_evaluator -v
```

##### 6C.2 修复 executor.py 的 OFFSET+LIMIT 和 COUNT(column) bug

`Executor` 有两个 bug：

**LIMIT+OFFSET 分页错误**（`_apply_limit` 方法）：

| 当前代码 | 正确代码 |
|---|---|
| `rows[start:limit]` | `rows[start:start + limit]` |

当 `OFFSET > 0` 时，切片终点错误——`LIMIT 2 OFFSET 3` 变成 `rows[3:2]`（空）而非 `rows[3:5]`（2 行）。

**COUNT(column) 不跳过 NULL**（`aggregate` 方法）：

| 当前行为 | SQL 正确语义 |
|---|---|
| `COUNT(score)` 计入所有行 | `COUNT(score)` 只计 score 非 NULL 的行 |

> **提示**：`_apply_limit` 改一个切片表达式；`aggregate` 的 COUNT 分支加一行过滤 None。

修完后跑测试：
```bash
PYTHONPATH=src python3 -m unittest tests.test_miniexec_executor -v
```

##### 6C.3 至少新增一条自主设计的测试

预置的 5 条失败测试不覆盖所有边界。请新增**至少一条**测试，覆盖以下任一类（自选）：

- `WHERE col != NULL` 也不应匹配任何行（与 `= NULL` 对称）
- `LIMIT` 大于行数时的行为（不应报错）
- `COUNT(column)` 当所有行该列都是 NULL 时应返回 0
- `UPDATE ... WHERE status = NULL` 不应更新任何行（E2 通过 executor 传播）

---

#### 通用要求

这条自主设计的测试**当前应该是绿的**（验证修复后的行为，不用于触发失败）。把"为什么挑这条"写进 `context.md`。

#### 测试红了怎么办

测试红了，**第一件事不是改代码**，是让 Agent 解释：

```
这条测试为什么失败？是测试期望错了，还是实现错了？
给我两种可能性的论据，再告诉我你倾向哪一种。
```

**停止信号**（任一出现，立刻停下）：
- 同一处反复修了 ≥3 次还没绿
- diff 越来越大（10 行 → 100 行）
- Agent 开始吞异常让测试过
- Agent 修改了明确禁止的文件

停下后：不要在污染的 context 里硬拧 → `/clear` + 更好的 prompt 重来。

---

### 步骤 7：使用 /clear 和 /compact 管理上下文

> 对应 PPT：Context Window 管理（Slide 19）

在步骤 6 执行修复的过程中，实践以下操作：

| 命令 | 何时用 | 作用 |
|---|---|---|
| `/clear` | 修完一组 bug 切到下一组时 | 清空上下文，避免"厨房水池式会话" |
| `/compact` | 长会话中 Agent 开始"遗忘"早期指令 | 压缩历史，保留关键信息 |

**建议流程（以练习 A 为例）**：

```
Bug 1（store.py: keys/__len__/__contains__）→ 跑测试 → /clear
→ 重新喂 AGENTS.md + 任务 prompt → Bug 2（store.py: delete）→ 跑测试 → /clear
→ 重新喂 AGENTS.md + 任务 prompt → Bug 3（persistence.py: dump）→ 跑测试
```

> 每次 `/clear` 后上下文已清空，需要重新把任务描述和约束喂给 Agent。这就是为什么步骤 2 和 3 写好的 prompt 很重要——它们是可复用的。

在 `context.md` 中记录你何时用了这些命令、为什么用、效果如何。

---

### 步骤 8：生成 validation_report.md 和 context.md

> 对应 PPT：写总结（Slide 20）

测试全绿后，闭环还没结束。让 Agent 生成两份总结文档，**然后你自己改一遍**。

#### validation_report.md

让 Agent 按以下五段结构生成草稿（参见 `expected-artifacts/validation_report.template.md`）：

| 段落 | 写什么 | 示例 |
|---|---|---|
| Initial Failure | 初始失败命令与摘要 | `validate_*.sh` 输出 5 FAILED |
| Root Cause | 根因，**引用具体代码** | 具体哪个方法、哪条 SQL/代码行有什么问题 |
| Changes | 改了哪些文件、哪段逻辑 | 列出修改的方法 |
| Validation | 最终验证命令与结果 | 全部测试通过 |
| Remaining Risks | 未覆盖场景或潜在风险 | 边界条件、未处理的情况 |

Prompt：

```
基于本次会话的所有改动，按 validation_report.template.md 的五段结构
生成草稿，每段不超过 5 行，不夸张表达功能。
```

#### context.md

记录你如何管理 Agent 的上下文：

| 板块 | 内容 |
|---|---|
| 提供给 Agent 的材料清单 | 列出具体喂了哪些文件 |
| **刻意没提供的内容** | 比如没给 cli.py / formatter.py（比"给了什么"更有训练价值）|
| 范围约束 | 哪些文件能改、哪些不能 |
| 验证方式 | 用了什么命令验证 |
| Agent 的错误判断与人工纠正 | 至少记录一次 agent 错了你纠了 |
| /clear 和 /compact 使用记录 | 何时用、为什么用、效果如何 |
| 自主设计的测试 | 选了哪条边界测试、为什么选它 |

**最后你自己改一遍** — 不写总结的人，会越用 Agent 越糊涂。

---

## 产物

| 产物 | 说明 |
|---|---|
| 修复后的源文件（A） | `store.py` + `persistence.py` |
| 修复后的源文件（B） | `lexer.py` + `parser.py` |
| 修复后的源文件（C） | `executor.py` + `evaluator.py` |
| 至少 1 条新测试 | 步骤 6.3 |
| `validation_report.md` | 步骤 8，含五段标准 heading |
| `context.md` | 步骤 8，含上下文管理记录 |

步骤 1-5、7 的产出（AGENTS.md、prompt、Plan Mode 计划等）不要求提交，但建议保留用于课堂讨论。

## 验证命令

三个都要通过：

```bash
./validators/validate_kvstore.sh
./validators/validate_minisql.sh
./validators/validate_miniexec.sh
```

## 约束

### 练习 A：KVStore

- ✅ 可修改：`src/kvstore/store.py` / `src/kvstore/persistence.py`
- ✅ 可新增：`tests/` 中的新测试函数（不限测试文件）
- ❌ 不允许：修改任何已有测试函数 / 修改 `parser.py` / 修改 `cli.py`
- ❌ 不允许：修改 `kv` 表 schema（字段名、类型、主键）
- ❌ 不允许：新增第三方依赖（仅允许 stdlib `sqlite3`）
- ❌ 不允许：修改 `KVStore` / `Snapshot` 公开方法的签名
- ❌ 不允许：修改 `get()` / `ttl()` 的实现
- ❌ 不允许：用 `try/except` 吞异常或 mock 时间来绕过失败

### 练习 B：Mini SQL Parser

- ✅ 可修改：`src/minisql/lexer.py` / `src/minisql/parser.py`
- ✅ 可新增：`tests/` 中的新测试函数（不限测试文件）
- ❌ 不允许：修改任何已有测试函数 / 修改 `ast_nodes.py` / 修改 `formatter.py`
- ❌ 不允许：修改 `Token` / `Lexer` / `Parser` 类的公开方法签名
- ❌ 不允许：新增第三方依赖（仅允许 stdlib）
- ❌ 不允许：用 `try/except` 吞异常或 mock 来绕过失败

### 练习 C：Mini Query Executor

- ✅ 可修改：`src/miniexec/executor.py` / `src/miniexec/evaluator.py`
- ✅ 可新增：`tests/` 中的新测试函数（不限测试文件）
- ❌ 不允许：修改任何已有测试函数 / 修改 `table.py`
- ❌ 不允许：修改 `Table` / `Executor` / `Evaluator` 类的公开方法签名
- ❌ 不允许：新增第三方依赖（仅允许 stdlib）
- ❌ 不允许：用 `try/except` 吞异常或 mock 来绕过失败
