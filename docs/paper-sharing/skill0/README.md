# SKILL0 论文分享材料

面向训练团队的 SKILL0 论文分享包。

## 交付物

- `slides/dist/SKILL0-paper-sharing.pptx`：可编辑 PowerPoint，28 页，包含 speaker notes。
- `slides/src/skill0_paper_sharing.js`：PptxGenJS 源码。
- `context.md`：本次材料制作上下文记录。

## 结构

1. Motivation：为什么 inference-time skill augmentation 有噪声、耗 token、难以真正内化。
2. Method：ICRL、dynamic curriculum、skill budget 退火、visual context compression 和 reward。
3. Evidence：主结果、token efficiency、training dynamics、ablation。
4. Related work：与 AgentEvolver、MemSkill、SkillRL 的区别。
5. Implications：训练团队如何从“经验增强”走向“经验内化”。

## 重新生成

```bash
cd docs/paper-sharing/skill0/slides
npm install
npm run build
```

## 验证记录

- `npm run build` 已通过。
- 生成脚本内包含 `warnIfSlideHasOverlaps` 和 `warnIfSlideElementsOutOfBounds`，当前构建无重叠/越界警告。
- 已用 macOS QuickLook 渲染封面缩略图做视觉检查。
- 尝试通过 Microsoft PowerPoint 自动导出 PDF，但 AppleScript 调用超时，未生成 PDF；因此未完成全页 PDF 渲染检查。
