# 课程目录说明

`lessons/` 存放所有课程材料。第一期培训采用“一节课一个目录”的方式组织，slides、讲义、练习项目和验证脚本都放在同一个课程目录中。

## 课程列表

| 课次 | 建议目录名 | 课程名 |
|---:|---|---|
| 0 | `L00-agent-setup` | Coding Agent 安装配置与基础体验 |
| 1 | `L01-existing-repo-loop` | 从已有代码仓开始：Coding Agent 研发最小闭环 |
| 2 | `L02-new-repo-workbench` | 接手陌生代码仓：建立 AI 可用的项目工作台 |
| 3 | `L03-requirement-to-code` | 从需求到代码：AI 辅助实现一个小功能 |
| 4 | `L04-review-refactor` | AI 辅助代码检视与重构 |
| 5 | `L05-test-design` | AI 辅助测试设计与测试代码生成 |
| 6 | `L06-debug-analysis` | AI 辅助问题定位：日志、编译、压测与并发异常 |
| 7 | `L07-build-skill` | 构建 Skill：把高频研发流程固化下来 |
| 8 | `L08-build-knowledge-base` | 构建知识库：让 AI 用上团队经验和历史案例 |
| 9 | `L09-capstone` | Capstone：真实场景综合实战 |

## 单课目录结构

```text
Lxx-topic/
├── README.md
├── lesson.yaml
├── slides/
│   ├── Lxx-topic.pptx
│   └── Lxx-topic.pdf
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
│   ├── expected-artifacts/
│   └── validators/
│       └── validate.sh
└── archive/
    └── classroom-questions.md
```

## README.md 建议内容

每节课的 `README.md` 应包含：

- 本课目标。
- 适用对象。
- 课前准备。
- 课堂安排。
- 练习入口。
- 验证命令。
- 需要提交的产物。
- FAQ 入口。

## exercise/README.md 建议内容

练习目录的 `README.md` 应包含：

- 练习背景。
- 任务目标。
- 目录说明。
- 运行方式。
- 验证方式。
- 交付物清单。
- 常见错误。

## 验证入口

每节课练习建议统一提供：

```bash
cd lessons/Lxx-topic/exercise
./validators/validate.sh
```

## 上下文记录

每节课练习都建议要求学员提交 `context.md`。模板见：

```text
shared/templates/context.template.md
```
