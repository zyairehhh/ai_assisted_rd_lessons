# L00 Coding Agent 安装配置与基础体验

## 本课目标

本课是正式实战课前的环境准备和基础体验课。学员完成后应能够：

1. 安装并打开至少一种 Coding Agent 工具，例如 opencode、Cursor 或 Codex。
2. 完成 LLM、API、Base URL、代理和默认模型配置。
3. 下载或安装一个示例 skill。
4. 体验问答、读代码、计划、编辑、测试、review 等常见交互模式。
5. 明确后续课程中 `context.md` 的记录要求。

## 适用对象

数据库研发、测试、资料工程、AI 工程相关人员。要求具备基础命令行和代码阅读能力。

## 课前准备

请在上课前完成：

1. 阅读 `docs/handout.md`。
2. 根据团队提供的账号和模型服务信息配置至少一种 Coding Agent。
3. 进入 `exercise/` 完成环境检查。
4. 提交 `context.md` 和 `agent_setup_report.md`。

## 课堂安排

| 环节 | 内容 |
|---|---|
| 10 分钟 | 课程目标、工具定位和安全边界 |
| 20 分钟 | opencode、Cursor、Codex 常见配置项说明 |
| 20 分钟 | 基础 prompt 和常见交互模式演示 |
| 20 分钟 | 下载和使用示例 skill |
| 20 分钟 | 常见配置问题答疑 |
| 10 分钟 | 后续课程练习规范说明 |

## 练习入口

```bash
cd lessons/L00-agent-setup/exercise
```

先阅读：

```bash
cat README.md
cat task.md
```

复制上下文模板：

```bash
cp ../../../shared/templates/context.template.md context.md
```

运行验证：

```bash
./validators/validate.sh
```

## 需要提交的产物

- `exercise/context.md`
- `exercise/agent_setup_report.md`

## 通过标准

1. 至少一种 Coding Agent 工具可以正常启动。
2. 能够通过配置的 LLM 完成一次基础问答。
3. 能够让 Coding Agent 阅读一个小文件并给出摘要。
4. 能够下载或安装一个示例 skill，或记录无法安装的原因。
5. `context.md` 和 `agent_setup_report.md` 内容完整。

## FAQ

常见问题见 `docs/faq.md`。
