# L01 从已有代码仓开始：Coding Agent 研发最小闭环

本目录是示例课程材料，因此使用 `demo-L01-existing-repo-loop` 目录名。正式版本可由主讲人在 `lessons/L01-existing-repo-loop/` 下维护。

## 本课目标

本课是第一堂正式实战课。目标是让学员在一个已有代码仓中完成一次完整研发闭环：

1. 阅读任务和已有代码。
2. 让 Coding Agent 先分析再修改。
3. 定位一个明确 bug。
4. 补充或更新测试。
5. 修改代码。
6. 运行验证脚本。
7. 记录上下文、过程和结果。

## 为什么从已有代码仓开始

数据库研发日常多数工作不是从空项目写 demo，而是在已有代码库中理解、定位、修改和验证。因此本课从一个小型 MiniDB 训练仓开始，模拟真实研发中的 bugfix 流程。

## 课前准备

1. 完成 L00 的工具配置。
2. 阅读 `docs/handout.md`。
3. 进入 `exercise/` 完成任务。
4. 提交 `context.md` 和 `validation_report.md`。

## 课堂安排

| 环节 | 内容 |
|---|---|
| 15 分钟 | 讲解已有代码仓中的 agent 使用方式 |
| 20 分钟 | 演示错误用法：一句话让 AI 直接修 |
| 25 分钟 | 演示正确用法：读任务、读测试、定范围、修改、验证 |
| 25 分钟 | 讲解学员常见问题 |
| 15 分钟 | 总结上下文控制和验证要求 |

## 练习入口

```bash
cd lessons/demo-L01-existing-repo-loop/exercise
```

阅读：

```bash
cat README.md
cat task.md
```

运行验证：

```bash
./validators/validate.sh
```

初始状态下验证会失败，这是练习的一部分。学员需要修复代码并补充过程记录。

## 需要提交的产物

- `exercise/context.md`
- `exercise/validation_report.md`
- 修复后的代码
- 必要时补充的测试

## 通过标准

1. `./validators/validate.sh` 通过。
2. `context.md` 说明了提供给 agent 的上下文和限制范围。
3. `validation_report.md` 说明了失败现象、修复内容和验证结果。
4. 修改范围集中，没有无关重构。
