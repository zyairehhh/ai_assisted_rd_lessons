# L01 讲师备注

> ⚠ 本文件含 bug 答案与评分要点，**不要**链接到学员可见入口（README、handout、faq、task）。仓库可见但靠约定不公开。

## 讲师目标

不要追求 bug 复杂。重点是让学员**第一次完整走通** Coding Agent 研发闭环——能读、能定范围、能验证、能写总结。bug 本身只是抓手。

本课用 SQLite-backed KVStore，3 个 bug 的共同根因是**SQL 查询漏 `WHERE` 过滤已过期行**——这是数据库岗位日常踩的真实坑，比纯 Python dict 版本更贴合"数据库部"身份。

预期学员先做 15–25 min 阅读 / 假设，再做 35–45 min 修改 + 总结。总时长 60–70 min。

## 建议讲法

1. 现场跑 `./validators/validate.sh`，让学员看到 5 条红
2. 演示**坏 prompt**："帮我修这 5 个测试"——观察 agent 可能：
   - 一次改 5 处不验证
   - 改 schema 加 `is_deleted` 列扩大范围
   - 在 Python 层做后过滤而不修 SQL（"能用就行"）
3. 演示**好 prompt**：四段式 + 先读后改三步法 + **要求 agent 先把每个方法的 SQL 列出来标注是否漏 WHERE**（这一步是本课新增亮点）
4. 强调白名单文件（store.py + persistence.py，不含 parser/cli/schema）
5. 现场写 `context.md` 与 `validation_report.md` 给学员看

## Bug 真相（练习答案）

### Bug 1（store.py，3 条 fail）：keys/__len__/__contains__ 的 SELECT 漏 WHERE

```python
# ❌ 当前
def keys(self) -> list[str]:
    rows = self._conn.execute("SELECT key FROM kv").fetchall()
    return [row[0] for row in rows]

def __len__(self) -> int:
    return self._conn.execute("SELECT COUNT(*) FROM kv").fetchone()[0]

def __contains__(self, key: str) -> bool:
    return self._conn.execute(
        "SELECT 1 FROM kv WHERE key = ?", (key,)
    ).fetchone() is not None
```

参考修复（最干净的 SQL-only 版本）：

```python
def keys(self) -> list[str]:
    rows = self._conn.execute(
        "SELECT key FROM kv WHERE expires_at IS NULL OR expires_at > ?",
        (time.time(),),
    ).fetchall()
    return [row[0] for row in rows]

def __len__(self) -> int:
    return self._conn.execute(
        "SELECT COUNT(*) FROM kv WHERE expires_at IS NULL OR expires_at > ?",
        (time.time(),),
    ).fetchone()[0]

def __contains__(self, key: str) -> bool:
    return self._conn.execute(
        "SELECT 1 FROM kv WHERE key = ? AND (expires_at IS NULL OR expires_at > ?)",
        (key, time.time()),
    ).fetchone() is not None
```

### Bug 2（store.py，1 条 fail）：delete() 不区分已过期行

```python
# ❌ 当前：只看 rowcount，删除已过期行也返回 True
def delete(self, key: str) -> bool:
    cur = self._conn.execute("DELETE FROM kv WHERE key = ?", (key,))
    return cur.rowcount > 0
```

参考修复（先 SELECT 判断再 DELETE）：

```python
def delete(self, key: str) -> bool:
    row = self._conn.execute(
        "SELECT expires_at FROM kv WHERE key = ?", (key,)
    ).fetchone()
    if row is None:
        return False
    expires_at = row[0]
    self._conn.execute("DELETE FROM kv WHERE key = ?", (key,))
    if expires_at is not None and time.time() >= expires_at:
        return False
    return True
```

也接受单 SQL 版（用 `RETURNING` 或 `WHERE ... AND (expires_at IS NULL OR ...)`），只要语义正确。

### Bug 3（persistence.py，1 条 fail）：dump 的 SELECT 漏 WHERE

```python
# ❌ 当前
def dump(store: KVStore, path: str) -> None:
    rows = store._conn.execute(
        "SELECT key, value, expires_at FROM kv"
    ).fetchall()
    ...
```

参考修复（与 Bug 1 同构）：

```python
import time  # 模块顶部

def dump(store: KVStore, path: str) -> None:
    rows = store._conn.execute(
        "SELECT key, value, expires_at FROM kv "
        "WHERE expires_at IS NULL OR expires_at > ?",
        (time.time(),),
    ).fetchall()
    ...
```

## 预置失败测试（baseline 5 红）

| 测试 | 暴露的 Bug | 修复点 |
|---|---|---|
| `StoreExpirationViewTest::test_keys_excludes_expired` | 1 | store.py keys() SQL |
| `StoreExpirationViewTest::test_len_excludes_expired` | 1 | store.py __len__ SQL |
| `StoreExpirationViewTest::test_contains_returns_false_for_expired` | 1 | store.py __contains__ SQL |
| `StoreDeleteSemanticsTest::test_delete_on_expired_key_returns_false` | 2 | store.py delete() |
| `SnapshotTest::test_dump_excludes_expired_keys` | 3 | persistence.py dump() SQL |

修复后应有 39 条测试全绿，加上 1 条自主设计共 40 条。

## 自主设计测试（评分人工核查）

学员需新增**至少 1 条**测试。优秀候选：

- `test_expire_on_already_expired_key_returns_false` — `expire()` 已正确处理但无显式测试
- `test_overwrite_on_expired_key_clears_ttl` — 设计取舍点：覆写 expired key 是否清空 TTL（参考实现：是）
- `test_load_is_idempotent` — Snapshot.load 二次调用结果一致
- `test_keys_query_with_boundary_expires_at` — `expires_at == time.time()` 这一刻应判定为过期（`>=` vs `>`）

`context.md` 的"可沉淀内容"段应说明：为什么挑这个边界、它能/不能发现什么。

## 评分（除 validate.sh 通过外的人工部分）

### `context.md` — 满足以下 3 项即可通过

- [ ] 列出了提供给 agent 的具体文件清单
- [ ] 至少写了一条"刻意没有提供"的内容（说明取舍）
- [ ] 至少记录了一次 agent 错误判断 + 人工纠正

### `validation_report.md` — 满足以下 4 项即可通过

- [ ] 五段 heading 齐全（脚本已自动检查）
- [ ] Root Cause 引用了具体 SQL 字符串（哪条 SELECT/DELETE 缺哪段 WHERE）
- [ ] Changes 列出了所有改动的文件，没有意外文件
- [ ] Remaining Risks 不为空（哪怕写"未发现"也比空着好）

### Prompt 流程（讲师抽查会话历史）— 加分项

- [ ] 第一条 prompt 是否包含「背景 / 目标 / 约束 / 验收」四要素
- [ ] agent 改代码**之前**是否有"读 → 假设 → 计划"三段输出
- [ ] **是否要求 agent 先把每条 SQL 列出来标注是否漏 WHERE**（本课重点）
- [ ] 是否使用 plan mode 或等价机制
- [ ] 测试失败时是否先让 agent 解释根因再继续

## 红线（任一触发即不通过）

- 修改了任何已存在测试函数 / 弱化测试期望
- 修改了 `parser.py` 或 `cli.py`
- 修改了 `get()` / `ttl()`（task.md 已明确禁止）
- 修改了 kv 表 schema（字段、类型、主键）
- 用 `try/except` 吞异常让测试通过
- 在测试里 mock `time.time` 替代真实修复
- 修改了公开方法签名
- 引入了新的第三方依赖
- 没有任何自主设计的新测试

## 常见翻车点（巡场观察）

| 翻车形态 | 发生原因 | 现场怎么说 |
|---|---|---|
| Agent 一次改 5 处不分组 | prompt 没要求"先把每条 SQL 列出来" | handout 模块 1：任务描述里加"先按 SQL 列出来" |
| Bug 修在 Python 层（取出全表后再过滤） | agent 想"防止改 SQL 改出新问题" | 现场：演示在大表上的全表扫开销，引导回到 SQL 层 |
| Agent 加了 `is_deleted` 列 / 索引 | 学员让 agent "彻底解决" | 模块 2：约束没写"不允许改 schema" |
| Agent 把 SQL 写进字符串拼接（没用占位符） | 走捷径 | 红线：可能引入 SQL 注入；现场补一次"始终用 ? 占位符"教学 |
| Bug 1 修了但 Bug 2 漏掉 | `delete()` 看上去是写不是读，没意识到也属于"过期一致性" | 现场审 diff 时点出 |
| Bug 3 用了和 Bug 1 完全独立的实现 | 没复用 helper / 没意识到同根因 | 接受。但 review 时点出"这是设计冗余"，引出抽 helper 的取舍 |
| 测试是 mock 时间的 | 路径正确但偏离行为 | 接受，但提醒"集成测试 vs 单元测试"取舍 |
| 自主设计的测试是"换个 key 重做一遍 baseline" | 没理解边界的概念 | 引导：你的测试能发现什么 baseline 发现不了的？ |

## 时间表（90 min 课堂）

| 时段 | 内容 |
|---|---|
| 00:00–00:10 | 心智模型 + 闭环 5 阶段 |
| 00:10–00:25 | 错误用法演示（让 agent 一次改 5 处 SQL） |
| 00:25–00:50 | 正确用法演示（先列 SQL → 标注 WHERE → 分组修） |
| 00:50–01:05 | `context.md` 与 `validation_report.md` 写法演示 |
| 01:05–01:20 | 学员高频问题集中讲（自主测试设计、SQL 注入风险） |
| 01:20–01:30 | 总结 + 下节课预告 |

---

# 练习 B：Mini SQL Parser Bug 真相

> 以下是 `exercise/src/minisql/` 的答案。与 KVStore 为平行练习，学员二选一或分组做不同的。

## 讲师目标（同上）

重点是让学员**第一次完整走通** Coding Agent 研发闭环。SQL Parser 的 3 个 bug 分属不同类型（词法 × 2 + 语法 × 1），比 KVStore 的"同根因 SQL 漏 WHERE"更考验定位能力——学员需要分别找到 bug 在 lexer 和 parser 两个文件中。

## Bug 真相

### Bug T1（lexer.py `_split()`，影响 2 条 fail）：字符串内空格导致 token 被拆断

```python
# ❌ 当前：遇到空格无条件分割
if ch in " \t\n\r":
    if current:
        tokens.append(current)
        current = ""
    i += 1
    continue
```

参考修复（加 `in_quote` 状态追踪）：

```python
def _split(self, sql: str) -> List[str]:
    tokens: List[str] = []
    current = ""
    in_quote = False
    i = 0
    while i < len(sql):
        ch = sql[i]

        # 追踪引号状态
        if ch == "'":
            in_quote = not in_quote
            current += ch
            i += 1
            continue

        # 在引号内，所有字符直接追加
        if in_quote:
            current += ch
            i += 1
            continue

        # 以下为引号外的正常分割逻辑（保持不变）
        # ... 两字符运算符、单字符符号、空格 ...
```

### Bug T3（lexer.py `_classify()`，影响 1 条 fail）：纯数字字符串误判为 INTEGER

```python
# ❌ 当前
if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
    content = raw[1:-1]
    if content.isdigit():          # ← 这个分支是 bug
        return Token("INTEGER", int(content))
    return Token("STRING", content)
```

参考修复（删除 `isdigit` 分支）：

```python
if raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
    content = raw[1:-1]
    return Token("STRING", content)
```

### Bug N1（parser.py `_parse_primary_condition()`，影响 2 条 fail）：括号内只解析单个比较

```python
# ❌ 当前（第 234 行附近）
def _parse_primary_condition(self) -> Condition:
    if self._peek_symbol() == "(":
        self._advance()
        inner = self._parse_comparison()   # ← 只能处理 ident op val
        self._expect_symbol(")")
        return GroupedCondition(inner)
    return self._parse_comparison()
```

参考修复（一行改动）：

```python
        inner = self._parse_condition()    # ← 改为支持 AND/OR + 嵌套括号
```

## 预置失败测试（baseline 5 红）

| 测试 | 暴露的 Bug | 修复点 |
|---|---|---|
| `LexerStringTest::test_string_with_space` | T1 | lexer.py `_split()` |
| `LexerStringTest::test_digit_string_type` | T3 | lexer.py `_classify()` |
| `ParserConditionGroupTest::test_nested_parens` | N1 | parser.py `_parse_primary_condition()` |
| `ParserConditionGroupTest::test_compound_in_parens` | N1 | parser.py `_parse_primary_condition()` |
| `ParserInsertTest::test_insert_string_with_space` | T1 传播 | lexer.py `_split()`（同 T1） |

修复后应有 49 条测试全绿，加上 1 条自主设计共 50 条。

## 自主设计测试（评分人工核查）

学员需新增**至少 1 条**测试。优秀候选：

- `test_string_with_escaped_quote` — `'it''s'` 转义引号（修复 T1 后自然可测，但需 lexer 额外处理）
- `test_triple_nested_parens` — `(((a = 1)))` 三层嵌套（修复 N1 后递归自然支持）
- `test_string_and_integer_coexist` — `WHERE a = '123' AND b = 456`（同时验证 T1+T3 修复）
- `test_like_with_space` — `LIKE 'John %'`（T1 的变体）

## 红线（任一触发即不通过）

- 修改了任何已存在测试函数 / 弱化测试期望
- 修改了 `ast_nodes.py` 或 `formatter.py`
- 修改了 `Token` / `Lexer` / `Parser` 类的公开方法签名
- 用 `try/except` 吞异常让测试通过
- 引入了新的第三方依赖
- 没有任何自主设计的新测试

## 常见翻车点（巡场观察）

| 翻车形态 | 发生原因 | 现场怎么说 |
|---|---|---|
| Agent 一次性重写整个 `_split()` | prompt 没限定改动范围 | 引导：只需加 `in_quote` 状态变量，不要重写 |
| Agent 改了 `ast_nodes.py` 加新节点 | 缺接口边界约束 | 红线：AST 定义不在修改范围内 |
| Agent 在 `_classify` 里加了复杂的数字检测逻辑 | 没意识到直接删 `isdigit` 分支就行 | 引导：最简修复是 2 行，不是 20 行 |
| Agent 把 N1 修成在 `_parse_comparison` 里递归 | 没理解 condition vs comparison 的层次 | 画图：condition = primary (AND/OR primary)*，primary = `(` condition `)` |
| T1 修了但 parser 测试还红 | 忘了 `test_insert_string_with_space` 也依赖 lexer | 引导：先跑 lexer 测试，确认全绿后再跑 parser |

---

# 练习 C：Mini Query Executor Bug 真相

> 以下是 `exercise/src/miniexec/` 的答案。与 KVStore、Parser 为平行练习。

## 讲师目标（同上）

Mini Query Executor 的 3 个 bug 分属不同语义层面（分页、NULL 比较、聚合），是数据库执行引擎的经典陷阱。比 KVStore 的"同根因"更分散，比 Parser 的"结构 bug"更贴近 SQL 执行语义——适合对 SQL 标准有一定了解的学员。

## Bug 真相

### Bug E1（executor.py `_apply_limit`，影响 2 条 fail）：OFFSET+LIMIT 切片错误

```python
# ❌ 当前
def _apply_limit(rows, limit=None, offset=None):
    start = offset or 0
    if limit is not None:
        return rows[start:limit]     # BUG: limit 是"取几行"不是"到第几行"
    return rows[start:]
```

参考修复（改一个切片表达式）：

```python
        return rows[start:start + limit]
```

当 `offset=0` 时 `rows[0:limit]` 碰巧正确，所以 `test_limit_only` 通过。`offset > 0` 时切片终点错误。

### Bug E2（evaluator.py `evaluate`，影响 2 条 fail）：= 和 != 不处理 NULL

```python
# ❌ 当前：Python None == None → True，但 SQL NULL = NULL → NULL（falsy）
if op == "=":
    return row_val == value
if op == "!=":
    return row_val != value
```

注意：`<`、`>`、`<=`、`>=` 已经有 None 守卫（因为 Python 3 会 TypeError），只有 `=` 和 `!=` 漏了——开发者修了会崩的但忘了不会崩的。

参考修复（在 `=` / `!=` 前加 None 守卫）：

```python
        # 在 = / != 前加：
        if row_val is None or value is None:
            return False

        if op == "=":
            return row_val == value
        if op == "!=":
            return row_val != value
```

### Bug E3（executor.py `aggregate`，影响 1 条 fail）：COUNT(column) 不跳过 NULL

```python
# ❌ 当前
if func == "COUNT":
    if column is None or column == "*":
        return len(rows)
    return len(rows)  # BUG: 和 COUNT(*) 一样，没过滤 NULL
```

参考修复（COUNT(column) 过滤 None）：

```python
    return sum(1 for r in rows if r.get(column) is not None)
```

## 预置失败测试（baseline 5 红）

| 测试 | 暴露的 Bug | 修复点 |
|---|---|---|
| `ExecutorLimitOffsetTest::test_limit_with_offset` | E1 | executor.py `_apply_limit()` |
| `ExecutorLimitOffsetTest::test_offset_past_limit_value` | E1 | executor.py `_apply_limit()` |
| `EvaluatorNullTest::test_equal_null_not_matched` | E2 | evaluator.py `evaluate()` |
| `EvaluatorNullTest::test_not_equal_skips_null_rows` | E2 | evaluator.py `evaluate()` |
| `ExecutorAggregateTest::test_count_column_skips_nulls` | E3 | executor.py `aggregate()` |

修复后应有 50 条测试全绿，加上 1 条自主设计共 51 条。

## 自主设计测试（评分人工核查）

学员需新增**至少 1 条**测试。优秀候选：

- `test_not_equal_null_also_not_matched` — `WHERE col != NULL` 也不应匹配（与 `= NULL` 对称，验证修复的完整性）
- `test_limit_larger_than_rows` — LIMIT 超过行数时不报错（边界）
- `test_count_column_all_null` — 所有行该列都是 NULL，COUNT(column) 应返回 0
- `test_update_where_null_no_match` — `UPDATE ... WHERE status = NULL` 不应更新任何行（E2 通过 executor 传播）

## 红线（任一触发即不通过）

- 修改了任何已存在测试函数 / 弱化测试期望
- 修改了 `table.py`
- 修改了 `Table` / `Executor` / `Evaluator` 类的公开方法签名
- 用 `try/except` 吞异常让测试通过
- 引入了新的第三方依赖
- 没有任何自主设计的新测试

## 常见翻车点（巡场观察）

| 翻车形态 | 发生原因 | 现场怎么说 |
|---|---|---|
| Agent 把 `_apply_limit` 整个重写成复杂逻辑 | prompt 没指出"改一行切片" | 引导：只是 `rows[start:limit]` → `rows[start:start+limit]` |
| Agent 给所有运算符都加 None 守卫（包括 IS/IS NOT）| 没理解 IS NULL 本来就是测 NULL 的 | 引导：IS NULL 正确，只有 = != 需要修 |
| Agent 改了 Table 类加 NULL 处理 | 缺接口边界约束 | 红线：Table 是数据模型，不在修改范围 |
| E2 修了但 Agent 没意识到这也影响 executor 的 WHERE | 没跑完整测试 | 引导：evaluator 是 executor 的依赖，修 evaluator 也会修 executor 的行为 |
| COUNT(column) 修成过滤 None 后，SUM/AVG 也想改 | SUM/AVG 本来就正确过滤了 | 引导：先读代码确认哪些已经正确 |

## 课后归档

把课堂高频问题记到 `archive/classroom-questions.md`，下一期开课前更新到 `docs/faq.md`。
