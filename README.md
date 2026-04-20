# AI 辅助研发实战培训仓

本仓库用于归档数据库研发团队 AI 辅助研发培训材料，承载课程讲义、PPT、练习项目、自动化验证脚本、示例 rules、示例 skills 和知识库样例。

仓库定位不是产品代码仓，而是一个面向培训交付的 monorepo：

- 每节课一个目录，课程材料和实战练习放在一起。
- 每个练习尽量独立，不依赖上一节课的完成结果。
- 每节课都必须提供可执行的验证入口。
- 每次练习都要求学员记录上下文选择、约束和验证方式。
- 标准答案、隐藏测试和敏感材料不放在学员可见路径。

## 培训目标

学员完成培训后，应能够：

1. 安装、配置并使用常见 Coding Agent，例如 opencode、Cursor、Codex。
2. 在已有代码仓中完成读代码、改代码、跑测试、修复失败的研发闭环。
3. 面对陌生代码仓时，建立 AI 可用的项目工作台。
4. 从需求出发，借助 AI 完成可验收的代码变更。
5. 使用 AI 辅助代码检视、重构、测试设计和问题定位。
6. 将高频研发流程沉淀为 skill。
7. 将团队经验、DTS、测试经验和故障案例整理为知识库。

## 仓库结构

```text
ai-assisted-rd-training/
├── README.md
├── CONTRIBUTING.md
├── AGENTS.md
├── SECURITY.md
├── docs/
│   └── training-repo-design.md
├── lessons/
│   ├── README.md
│   ├── L00-agent-setup/
│   ├── L01-existing-repo-loop/
│   ├── L02-new-repo-workbench/
│   ├── L03-requirement-to-code/
│   ├── L04-review-refactor/
│   ├── L05-test-design/
│   ├── L06-debug-analysis/
│   ├── L07-build-skill/
│   ├── L08-build-knowledge-base/
│   └── L09-capstone/
├── shared/
│   ├── templates/
│   ├── example-skills/
│   ├── example-rules/
│   └── example-knowledge/
├── tools/
└── .github/
    └── pull_request_template.md
```

第一期培训采用“课程和练习放在一起”的结构。后续如果某个练习需要被多节课复用，再考虑抽取为公共 case 或共享练习项目。

## 课程目录约定

每节课目录建议包含：

```text
lessons/L03-requirement-to-code/
├── README.md
├── lesson.yaml
├── slides/
│   ├── L03-requirement-to-code.pptx
│   └── L03-requirement-to-code.pdf
├── docs/
│   ├── handout.md
│   ├── faq.md
│   └── instructor-notes.md
├── exercise/
│   ├── README.md
│   ├── task.md
│   ├── src/
│   ├── tests/
│   ├── fixtures/
│   ├── validators/
│   │   └── validate.sh
│   └── expected-artifacts/
└── archive/
    └── classroom-questions.md
```

## 学员使用方式

1. 进入对应课程目录，例如 `lessons/L03-requirement-to-code/`。
2. 阅读课程 `README.md` 和 `docs/handout.md`。
3. 浏览课程 PDF。
4. 进入 `exercise/` 完成练习。
5. 维护自己的 `context.md`，记录上下文选择和验证方法。
6. 运行 `exercise/validators/validate.sh`。
7. 带着问题参加课堂讲解和答疑。

## 讲师发布要求

每节课至少提前 7 天合入主分支，至少包含：

- 课程 `README.md`
- `lesson.yaml`
- 可阅读讲义或 handout
- PPT 或导出的 PDF
- 练习说明
- 自动化验证入口
- FAQ 初版
- 评分标准或验收标准

详细规范见 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [docs/training-repo-design.md](docs/training-repo-design.md)。

## 合入要求

所有课程材料和练习必须通过 PR 合入。PR 至少满足：

- 目录结构符合规范。
- 练习可以独立运行。
- 验证脚本可以本地执行。
- 不包含标准答案、密钥、真实客户数据或敏感内部信息。
- 课前练习预计耗时控制在 2 到 4 小时。
- 讲师已完成本地自检。

## 相关文档

- [仓库设计说明](docs/training-repo-design.md)
- [贡献与合入规范](CONTRIBUTING.md)
- [Coding Agent 行为规范](AGENTS.md)
- [安全与合规说明](SECURITY.md)
- [课程目录说明](lessons/README.md)
