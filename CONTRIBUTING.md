# 贡献与合入规范

本文档规定课程材料、练习项目和共享模板的贡献方式。

## 一、基本原则

1. 所有课程材料必须通过 PR 合入。
2. 每节课至少提前 7 天合入主分支。
3. 每节课必须包含可执行练习和验证入口。
4. 练习必须能独立运行，不依赖其他课程的完成结果。
5. 不允许提交真实客户数据、密钥、内部凭证、敏感日志或完整标准答案。
6. 优先保证训练质量，不追求练习项目复杂度。

## 二、课程目录规范

每节课目录应位于 `lessons/` 下，命名格式：

```text
Lxx-short-topic
```

示例：

```text
lessons/L03-requirement-to-code/
```

每节课至少包含：

```text
README.md
lesson.yaml
slides/
docs/handout.md
docs/faq.md
exercise/README.md
exercise/task.md
exercise/validators/validate.sh
```

建议包含：

```text
slides/*.pptx
slides/*.pdf
docs/instructor-notes.md
exercise/src/
exercise/tests/
exercise/fixtures/
exercise/expected-artifacts/
archive/classroom-questions.md
```

## 三、课程 README 要求

课程 `README.md` 应说明：

- 课程名称和目标。
- 适用对象。
- 课前准备。
- 课堂流程。
- 练习入口。
- 验证方式。
- 需要提交的产物。
- 常见问题入口。

## 四、lesson.yaml 要求

`lesson.yaml` 用于机器检查和发布统计。建议字段：

```yaml
id: L03
title: "从需求到代码：AI 辅助实现一个小功能"
owner: "owner-name"
release_date: "2026-05-01"
estimated_prep_time: "2-4h"
difficulty: "medium"
has_slides: true
has_exercise: true
required_artifacts:
  - "exercise/context.md"
  - "exercise/validation_report.md"
validation:
  entrypoint: "exercise/validators/validate.sh"
```

模板见 [shared/templates/lesson.yaml.template](shared/templates/lesson.yaml.template)。

## 五、练习设计规范

练习应符合以下要求：

| 项目 | 要求 |
|---|---|
| 独立性 | 可以单独运行，不依赖前序课程完成结果 |
| 真实性 | 尽量来自数据库研发真实场景，例如代码修改、测试设计、问题定位 |
| 可验证性 | 必须提供本地验证脚本 |
| 时间控制 | 课前练习建议 2 到 4 小时内完成 |
| 难度控制 | 不应只靠一句 prompt 完成，必须包含阅读、判断、验证或纠错 |
| 上下文训练 | 必须要求学员维护 `context.md` |
| 答案隔离 | 不得在学员可见目录提交完整标准答案 |

## 六、验证脚本规范

每个练习必须提供统一入口：

```bash
cd lessons/Lxx-topic/exercise
./validators/validate.sh
```

验证脚本应尽量检查：

- 代码是否能构建。
- 测试是否能运行。
- 必要产物是否存在。
- 文档结构是否符合要求。
- 输出报告是否包含关键字段。
- 是否存在明显敏感信息。

验证脚本可以使用 Bash、Python 或项目本身的构建工具。脚本应尽量给出清晰错误信息，便于学员自行修复。

## 七、Slides 与文档规范

每节课建议同时提交：

- 可编辑源文件，例如 `.pptx`。
- 面向学员阅读的 PDF。
- `docs/handout.md`，用于课前阅读。
- `docs/faq.md`，用于沉淀课前和课堂问题。

材料应少讲概念，多给操作路径、错误案例和验证标准。

## 八、安全与合规

提交前必须检查：

- 不包含密钥、token、账号密码。
- 不包含真实客户数据。
- 不包含敏感内部地址。
- 日志和 DTS 内容已脱敏。
- 不包含不可公开的产品代码或私有实现细节。
- 不把标准答案放在学员可见目录。

详细要求见 [SECURITY.md](SECURITY.md)。

## 九、PR 合入要求

PR 至少需要一名课程 reviewer 和一名技术 reviewer 审核。

合入前必须满足：

- 目录结构符合规范。
- 本地验证脚本通过。
- 课程材料完整。
- 安全检查通过。
- 预计练习时间合理。
- PR 模板中的自检项已完成。

## 十、Review 关注点

Reviewer 应重点检查：

- 课程目标是否清晰。
- 练习是否真能训练对应能力。
- 是否存在“一句 prompt 就完成”的低价值练习。
- 验证脚本是否可运行。
- 学员是否能独立完成课前练习。
- 讲师是否提供了足够的 FAQ 和排障说明。
- 是否有敏感信息风险。

## 十一、发布节奏

建议节奏：

| 时间 | 动作 |
|---|---|
| T-14 天 | 讲师提交初稿 PR |
| T-10 天 | 完成第一轮 review |
| T-7 天 | 合入主分支并通知学员 |
| T-2 天 | 更新 FAQ |
| T 日 | 课堂讲解与答疑 |
| T+1 天 | 归档课堂问题 |
