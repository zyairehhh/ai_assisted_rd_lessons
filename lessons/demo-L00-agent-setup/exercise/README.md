# L00 练习：环境检查与基础体验

## 背景

本练习用于确认你已经具备后续课程所需的最低工具环境，并完成一次基础 Coding Agent 体验。

## 任务目标

你需要完成：

1. 确认本机具备基础命令行工具。
2. 启动至少一种 Coding Agent。
3. 完成一次基础问答或代码阅读。
4. 下载或安装一个示例 skill，或记录失败原因。
5. 填写 `context.md` 和 `agent_setup_report.md`。

## 开始练习

复制上下文模板：

```bash
cp ../../../shared/templates/context.template.md context.md
```

阅读任务：

```bash
cat task.md
```

## 验证方式

运行：

```bash
./validators/validate.sh
```

验证脚本会检查：

- `python3` 和 `git` 是否可用。
- 是否存在 `context.md`。
- 是否存在 `agent_setup_report.md`。
- 报告中是否包含必要章节。

## 需要提交的产物

- `context.md`
- `agent_setup_report.md`

## 注意事项

不要在报告中写入 API key、token、内部地址或其他敏感信息。
