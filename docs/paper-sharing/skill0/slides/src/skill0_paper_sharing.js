const pptxgen = require("pptxgenjs");
const { svgToDataUri } = require("./pptxgenjs_helpers/svg");
const {
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
} = require("./pptxgenjs_helpers/layout");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "AI Assisted R&D Training";
pptx.company = "Training Team";
pptx.subject = "SKILL0 paper sharing";
pptx.title = "SKILL0: In-Context Agentic Reinforcement Learning for Skill Internalization";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Microsoft YaHei",
  bodyFontFace: "Microsoft YaHei",
  lang: "zh-CN",
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";
pptx.margin = 0;

const W = 13.333;
const H = 7.5;

const C = {
  ink: "18212B",
  muted: "596677",
  faint: "EEF2F6",
  line: "D9E1EA",
  white: "FFFFFF",
  teal: "007A7A",
  teal2: "3CB7A5",
  coral: "E4572E",
  amber: "D89922",
  green: "2F7D4A",
  blue: "3867D6",
  violet: "6C4AB6",
  red: "B3261E",
  charcoal: "24313F",
  softTeal: "E7F5F2",
  softCoral: "FDECE6",
  softAmber: "FFF4D8",
  softBlue: "EAF0FF",
  softGreen: "EAF6EE",
};

const FONT = "Microsoft YaHei";
const BODY = { fontFace: FONT, color: C.ink, breakLine: false };

function addBg(slide, section = "SKILL0") {
  slide.background = { color: "FAFBFC" };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: H,
    fill: { color: "FAFBFC" },
    line: { color: "FAFBFC", transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: 0.12,
    fill: { color: C.teal },
    line: { color: C.teal, transparency: 100 },
  });
  slide.addText(section, {
    x: 0.52,
    y: 7.06,
    w: 4.2,
    h: 0.22,
    fontFace: FONT,
    fontSize: 7.5,
    color: "8C98A7",
    margin: 0,
    breakLine: false,
  });
}

function addTitle(slide, title, subtitle, section) {
  addBg(slide, section);
  slide.addText(title, {
    x: 0.62,
    y: 0.34,
    w: 9.8,
    h: 0.5,
    fontFace: FONT,
    fontSize: 25,
    bold: true,
    color: C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.64,
      y: 0.9,
      w: 11.3,
      h: 0.28,
      fontFace: FONT,
      fontSize: 10.5,
      color: C.muted,
      margin: 0,
      breakLine: false,
      fit: "shrink",
    });
  }
}

function addPage(slide, n) {
  slide.addText(String(n).padStart(2, "0"), {
    x: 12.25,
    y: 7.02,
    w: 0.55,
    h: 0.2,
    fontFace: "Aptos",
    fontSize: 8,
    color: "9AA6B5",
    align: "right",
    margin: 0,
  });
}

function pill(slide, text, x, y, w, color = C.teal, fill = C.softTeal) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 0.36,
    rectRadius: 0.08,
    fill: { color: fill },
    line: { color: fill, transparency: 100 },
  });
  slide.addText(text, {
    x: x + 0.12,
    y: y + 0.083,
    w: w - 0.24,
    h: 0.18,
    fontFace: FONT,
    fontSize: 8.6,
    bold: true,
    color,
    align: "center",
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
}

function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    fill: { color: opts.fill || C.white },
    line: { color: opts.line || C.line, transparency: opts.lineT || 0, width: 0.8 },
  });
}

function heading(slide, text, x, y, w, opts = {}) {
  slide.addText(text, {
    x,
    y,
    w,
    h: opts.h || 0.34,
    fontFace: FONT,
    fontSize: opts.size || 14.5,
    bold: true,
    color: opts.color || C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
}

function body(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    ...BODY,
    x,
    y,
    w,
    h,
    fontSize: opts.size || 11,
    color: opts.color || C.ink,
    bold: opts.bold || false,
    valign: opts.valign || "top",
    margin: opts.margin === undefined ? 0 : opts.margin,
    breakLine: false,
    fit: "shrink",
  });
}

function bullets(slide, items, x, y, w, opts = {}) {
  const size = opts.size || 10.5;
  const gap = opts.gap || 0.42;
  items.forEach((item, i) => {
    slide.addText(item, {
      x,
      y: y + i * gap,
      w,
      h: opts.lineH || 0.28,
      fontFace: FONT,
      fontSize: size,
      color: opts.color || C.ink,
      margin: 0,
      breakLine: false,
      fit: "shrink",
      bullet: { type: "bullet" },
      paraSpaceAfterPt: 0,
    });
  });
}

function numberBadge(slide, n, x, y, color = C.teal) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x,
    y,
    w: 0.34,
    h: 0.34,
    fill: { color },
    line: { color, transparency: 100 },
  });
  slide.addText(String(n), {
    x,
    y: y + 0.055,
    w: 0.34,
    h: 0.15,
    fontFace: "Aptos",
    fontSize: 8.5,
    bold: true,
    color: C.white,
    align: "center",
    margin: 0,
  });
}

function arrow(slide, x1, y1, x2, y2, color = C.teal) {
  slide.addShape(pptx.ShapeType.line, {
    x: x1,
    y: y1,
    w: x2 - x1,
    h: y2 - y1,
    line: { color, width: 1.4, beginArrowType: "none", endArrowType: "triangle" },
  });
}

function smallLabel(slide, text, x, y, w, color = C.muted) {
  slide.addText(text, {
    x,
    y,
    w,
    h: 0.18,
    fontFace: FONT,
    fontSize: 7.8,
    color,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
}

function sectionSlide(n, eyebrow, title, sub, accents = [C.teal, C.coral, C.amber]) {
  const slide = pptx.addSlide();
  slide.background = { color: C.charcoal };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: H,
    fill: { color: C.charcoal },
    line: { color: C.charcoal, transparency: 100 },
  });
  accents.forEach((color, i) => {
    slide.addShape(pptx.ShapeType.rect, {
      x: 0.62 + i * 0.28,
      y: 1.12,
      w: 0.16,
      h: 0.88,
      fill: { color },
      line: { color, transparency: 100 },
    });
  });
  slide.addText(eyebrow, {
    x: 1.42,
    y: 1.08,
    w: 5.8,
    h: 0.24,
    fontFace: "Aptos",
    fontSize: 9,
    bold: true,
    color: "AFC1D4",
    charSpace: 1.2,
    margin: 0,
    breakLine: false,
  });
  slide.addText(title, {
    x: 1.4,
    y: 1.55,
    w: 9.8,
    h: 0.82,
    fontFace: FONT,
    fontSize: 32,
    bold: true,
    color: C.white,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addText(sub, {
    x: 1.43,
    y: 2.58,
    w: 8.7,
    h: 0.42,
    fontFace: FONT,
    fontSize: 13.5,
    color: "DCE6F1",
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addText(String(n).padStart(2, "0"), {
    x: 11.2,
    y: 5.58,
    w: 1.35,
    h: 0.56,
    fontFace: "Aptos Display",
    fontSize: 35,
    bold: true,
    color: "5B6B7B",
    align: "right",
    margin: 0,
  });
  slide.addNotes(`过渡页：${title}。提醒听众这一部分关注 ${sub}`);
  return slide;
}

function flowBox(slide, text, x, y, w, h, fill, line, opts = {}) {
  card(slide, x, y, w, h, { fill, line: line || fill });
  slide.addText(text, {
    x: x + 0.16,
    y: y + 0.16,
    w: w - 0.32,
    h: h - 0.28,
    fontFace: FONT,
    fontSize: opts.size || 11,
    bold: opts.bold !== false,
    color: opts.color || C.ink,
    align: opts.align || "center",
    valign: "mid",
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
}

function hBarChart(slide, rows, x, y, w, h, maxValue, opts = {}) {
  const labelW = opts.labelW || 1.75;
  const valueW = opts.valueW || 0.72;
  const barW = w - labelW - valueW - 0.24;
  const rowH = h / rows.length;
  rows.forEach((r, i) => {
    const yy = y + i * rowH;
    body(slide, r.label, x, yy + 0.12, labelW, 0.22, {
      size: opts.labelSize || 8.4,
      color: C.muted,
    });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: x + labelW,
      y: yy + 0.12,
      w: barW,
      h: 0.22,
      rectRadius: 0.04,
      fill: { color: "E7ECF2" },
      line: { color: "E7ECF2", transparency: 100 },
    });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: x + labelW,
      y: yy + 0.12,
      w: Math.max(0.04, (r.value / maxValue) * barW),
      h: 0.22,
      rectRadius: 0.04,
      fill: { color: r.color || opts.color || C.teal },
      line: { color: r.color || opts.color || C.teal, transparency: 100 },
    });
    slide.addText(r.display || String(r.value), {
      x: x + labelW + barW + 0.12,
      y: yy + 0.095,
      w: valueW,
      h: 0.18,
      fontFace: "Aptos",
      fontSize: 8.8,
      bold: true,
      color: C.ink,
      margin: 0,
      breakLine: false,
      fit: "shrink",
    });
  });
}

function miniAxisChart(slide, x, y, w, h) {
  slide.addShape(pptx.ShapeType.line, { x, y: y + h, w, h: 0, line: { color: C.line, width: 1 } });
  slide.addShape(pptx.ShapeType.line, { x, y, w: 0, h, line: { color: C.line, width: 1 } });
  const lineA = [
    [x + 0.2, y + h - 1.1],
    [x + 1.15, y + h - 1.75],
    [x + 2.35, y + h - 1.95],
    [x + 3.65, y + h - 2.08],
    [x + w - 0.2, y + h - 2.18],
  ];
  const lineB = [
    [x + 0.2, y + h - 0.34],
    [x + 1.15, y + h - 0.72],
    [x + 2.35, y + h - 1.18],
    [x + 3.65, y + h - 1.72],
    [x + w - 0.38, y + h - 1.9],
  ];
  drawPolyline(slide, lineA, C.teal, 2.2);
  drawPolyline(slide, lineB, C.coral, 2.2);
  body(slide, "with skill", x + w - 1.16, y + 0.46, 0.9, 0.18, { size: 7.8, color: C.teal, bold: true });
  body(slide, "w/o skill", x + w - 1.14, y + 0.92, 0.9, 0.18, { size: 7.8, color: C.coral, bold: true });
  smallLabel(slide, "training step", x + w - 1.12, y + h + 0.1, 1.0);
  smallLabel(slide, "success", x - 0.05, y - 0.25, 0.8);
}

function drawPolyline(slide, points, color, width = 1.8) {
  for (let i = 0; i < points.length - 1; i++) {
    const [x1, y1] = points[i];
    const [x2, y2] = points[i + 1];
    slide.addShape(pptx.ShapeType.line, {
      x: x1,
      y: y1,
      w: x2 - x1,
      h: y2 - y1,
      line: { color, width },
    });
  }
  points.forEach(([px, py]) => {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px - 0.045,
      y: py - 0.045,
      w: 0.09,
      h: 0.09,
      fill: { color },
      line: { color, transparency: 100 },
    });
  });
}

function addQuote(slide, text, x, y, w, h, accent = C.teal) {
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w: 0.06,
    h,
    fill: { color: accent },
    line: { color: accent, transparency: 100 },
  });
  body(slide, text, x + 0.22, y + 0.04, w - 0.22, h - 0.08, {
    size: 16,
    bold: true,
    color: C.ink,
  });
}

function svgIcon(kind, color) {
  const common = `fill="none" stroke="#${color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"`;
  const paths = {
    search: `<circle cx="21" cy="21" r="10" ${common}/><path d="M29 29 L38 38" ${common}/>`,
    token: `<path d="M12 16 h26 v16 H12z" ${common}/><path d="M16 21 h9 M16 27 h14 M31 21 h3" ${common}/>`,
    brain: `<path d="M22 12 c-5 0-8 4-8 8 0 2 1 4 3 5-1 4 2 8 6 8 2 0 4-1 5-3 1 2 3 3 5 3 4 0 7-4 6-8 2-1 3-3 3-5 0-4-3-8-8-8-2 0-4 1-6 3-2-2-4-3-6-3z" ${common}/><path d="M28 15 v15 M20 22 h16" ${common}/>`,
    compass: `<circle cx="25" cy="25" r="16" ${common}/><path d="M30 20 l-4 11-6 3 4-11z" ${common}/>`,
  };
  return svgToDataUri(`<svg viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">${paths[kind] || paths.brain}</svg>`);
}

const slides = [];
function push(slide, n) {
  addPage(slide, n);
  slides.push(slide);
  return slide;
}

// 1
{
  const slide = pptx.addSlide();
  slide.background = { color: C.charcoal };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: H,
    fill: { color: C.charcoal },
    line: { color: C.charcoal, transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.16, h: H, fill: { color: C.teal }, line: { transparency: 100 } });
  slide.addShape(pptx.ShapeType.rect, { x: 0.16, y: 0, w: 0.08, h: H, fill: { color: C.coral }, line: { transparency: 100 } });
  slide.addText("SKILL0", {
    x: 0.86,
    y: 1.02,
    w: 6.2,
    h: 0.9,
    fontFace: "Aptos Display",
    fontSize: 49,
    bold: true,
    color: C.white,
    margin: 0,
    breakLine: false,
  });
  slide.addText("In-Context Agentic RL · Skill Internalization", {
    x: 0.91,
    y: 2.06,
    w: 7.0,
    h: 0.38,
    fontFace: FONT,
    fontSize: 16,
    color: "DDE8F3",
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.92,
    y: 3.18,
    w: 0.08,
    h: 1.1,
    fill: { color: C.amber },
    line: { color: C.amber, transparency: 100 },
  });
  slide.addText("Skills at training,\nzero at inference.", {
    x: 1.16,
    y: 3.25,
    w: 5.9,
    h: 0.82,
    fontFace: FONT,
    fontSize: 22,
    bold: true,
    color: C.white,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  pill(slide, "训练团队论文分享", 0.92, 5.18, 1.62, C.white, "466072");
  pill(slide, "Agentic RL", 2.74, 5.18, 1.2, C.white, "466072");
  pill(slide, "Skill Internalization", 4.13, 5.18, 1.74, C.white, "466072");
  flowBox(slide, "训练时借助 skill", 8.24, 1.42, 2.5, 0.88, "324456", "4D6174", { color: C.white });
  flowBox(slide, "逐步减少暴露", 8.52, 3.02, 2.5, 0.88, "324456", "4D6174", { color: C.white });
  flowBox(slide, "推理时 0 skill", 8.8, 4.62, 2.5, 0.88, C.teal, C.teal, { color: C.white });
  arrow(slide, 9.48, 2.38, 9.74, 2.93, C.amber);
  arrow(slide, 9.76, 3.98, 10.02, 4.53, C.amber);
  slide.addNotes("开场先给一句话主张：不是更会检索 skill，而是训练时用 skill、推理时不带 skill。随后提示听众，这个问题和训练团队关心的经验池、RL、内化经验直接相关。");
  push(slide, 1);
}

// 2
{
  const slide = pptx.addSlide();
  addTitle(slide, "今天讲清楚 4 件事", "目标不是逐段复述论文，而是抽出可迁移的训练设计", "Talk map");
  const items = [
    ["问题", "为什么 inference-time skill augmentation 会遇到瓶颈", C.coral, C.softCoral],
    ["方法", "ICRL、动态 curriculum、视觉上下文压缩如何配合", C.teal, C.softTeal],
    ["证据", "主结果、token efficiency、training dynamics 和 ablation", C.blue, C.softBlue],
    ["启发", "如何迁移到经验池 + RL + 内化经验的研究路线", C.green, C.softGreen],
  ];
  items.forEach((it, i) => {
    const y = 1.58 + i * 1.18;
    card(slide, 0.78, y, 11.65, 0.78, { fill: it[3], line: it[3] });
    numberBadge(slide, i + 1, 1.06, y + 0.22, it[2]);
    heading(slide, it[0], 1.58, y + 0.19, 1.4, { size: 14, color: it[2] });
    body(slide, it[1], 3.0, y + 0.22, 8.3, 0.25, { size: 12.2, color: C.ink });
  });
  slide.addNotes("给出路线图。提醒大家后半段会把 SKILL0 和 AgentEvolver、SkillRL、MemSkill 放在一个坐标系里看。");
  push(slide, 2);
}

sectionSlide(3, "PART 1", "Motivation", "为什么“运行时找 skill”不是终点");

// 4
{
  const slide = pptx.addSlide();
  addTitle(slide, "现有范式：inference-time skill augmentation", "每一步检索相关 skill，把 skill 文本塞进 prompt，辅助 agent 做当前决策", "Motivation");
  flowBox(slide, "任务 I\n环境 observation", 0.82, 2.08, 1.8, 0.9, C.white, C.line);
  flowBox(slide, "skill bank\n检索 top-k", 3.18, 1.42, 1.76, 0.9, C.softBlue, C.blue);
  flowBox(slide, "prompt\nhistory + skills", 5.54, 2.08, 2.05, 0.9, C.softAmber, C.amber);
  flowBox(slide, "policy\n下一步 action", 8.22, 2.08, 1.8, 0.9, C.softTeal, C.teal);
  flowBox(slide, "环境反馈\n下一轮继续", 10.58, 2.08, 1.8, 0.9, C.white, C.line);
  arrow(slide, 2.62, 2.53, 5.42, 2.53, C.muted);
  arrow(slide, 4.94, 1.87, 5.5, 2.25, C.blue);
  arrow(slide, 7.62, 2.53, 8.14, 2.53, C.muted);
  arrow(slide, 10.04, 2.53, 10.5, 2.53, C.muted);
  card(slide, 1.02, 4.22, 10.95, 1.28, { fill: C.white });
  heading(slide, "它有效，但能力还在 context 里", 1.38, 4.48, 4.2, { size: 17, color: C.ink });
  body(slide, "SKILL0 的切入点：既然每次推理都要带说明书，模型到底有没有真正学会？", 5.84, 4.52, 5.54, 0.42, { size: 13, color: C.muted });
  slide.addNotes("这一页先建立共同语言：大多数 skill 方法是在推理时检索和注入 skill。它像给模型随身带说明书，短期有效，但推理成本和依赖都留着。");
  push(slide, 4);
}

// 5
{
  const slide = pptx.addSlide();
  addTitle(slide, "三个根本限制", "SKILL0 把问题从“如何检索 skill”改写成“如何摆脱 skill”", "Motivation");
  const cols = [
    ["search", "retrieval noise", "不相关或误导性的 guidance 被注入上下文，影响当前 step 决策。", C.coral, C.softCoral],
    ["token", "token overhead", "skill 内容在多轮交互中反复占用上下文预算，扩展性差。", C.amber, C.softAmber],
    ["brain", "not internalized", "模型只是照着 prompt 执行，能力仍在上下文中，而不在参数里。", C.teal, C.softTeal],
  ];
  cols.forEach((c, i) => {
    const x = 0.78 + i * 4.1;
    card(slide, x, 1.62, 3.55, 3.72, { fill: c[4], line: c[4] });
    slide.addImage({ data: svgIcon(c[0], c[3]), x: x + 0.28, y: 1.92, w: 0.72, h: 0.72 });
    heading(slide, c[1], x + 0.32, 2.88, 2.75, { size: 15, color: c[3] });
    body(slide, c[2], x + 0.34, 3.52, 2.74, 0.88, { size: 11.2, color: C.ink });
  });
  addQuote(slide, "关键问题：能不能把 skill 直接内化到模型参数中？", 1.02, 6.0, 10.6, 0.58, C.teal);
  slide.addNotes("三个限制逐个讲：噪声、成本、没有学进去。这里可以停一下，问听众：我们自己的经验池方法有没有同样问题。");
  push(slide, 5);
}

// 6
{
  const slide = pptx.addSlide();
  addTitle(slide, "SKILL0 的主张", "训练时借助 skill，推理时完全无 skill，实现 zero-shot autonomous behavior", "Motivation");
  card(slide, 0.95, 1.7, 5.15, 3.85, { fill: C.white });
  heading(slide, "不是优化 retrieval", 1.34, 2.06, 4.1, { size: 18, color: C.coral });
  bullets(slide, [
    "不再把 skill bank 当成推理期外挂",
    "不把 top-k 检索质量作为核心目标",
    "不希望模型长期依赖外部说明书",
  ], 1.46, 2.84, 3.95, { size: 11, gap: 0.5 });
  card(slide, 7.15, 1.7, 5.15, 3.85, { fill: C.softTeal, line: C.softTeal });
  heading(slide, "而是优化 internalization", 7.54, 2.06, 4.2, { size: 18, color: C.teal });
  bullets(slide, [
    "训练 rollout 阶段提供 structured guidance",
    "训练后期逐步撤掉 active skills",
    "最终 policy 参数自己执行复杂行为",
  ], 7.66, 2.84, 3.95, { size: 11, gap: 0.5 });
  arrow(slide, 6.25, 3.62, 6.93, 3.62, C.amber);
  body(slide, "研究重点迁移", 6.16, 3.08, 0.8, 0.22, { size: 8.2, color: C.amber, bold: true });
  slide.addNotes("这一页讲论文的范式转移。skill 不再是推理期依赖，而是训练脚手架。");
  push(slide, 6);
}

sectionSlide(7, "PART 2", "Method", "ICRL + dynamic curriculum + visual compression");

// 8
{
  const slide = pptx.addSlide();
  addTitle(slide, "整体框架：三块组件服务一个终点", "对应论文 Figure 2：先组织 skill，再用 skill 训练，最后逐步去 skill", "Method");
  const ys = 2.04;
  const xs = [0.8, 3.92, 7.04, 10.16];
  const labels = [
    ["1", "Relevance-Driven\nSkill Grouping", "训练前把 skill file 和验证子任务对齐", C.blue, C.softBlue],
    ["2", "In-Context\nReinforcement Learning", "rollout 时给 skill，让 RL 学迁移", C.teal, C.softTeal],
    ["3", "Dynamic\nCurriculum", "按 helpfulness 保留当前仍有用的 skill", C.amber, C.softAmber],
    ["4", "Zero-Skill\nInference", "部署时不再检索、不再注入 skill", C.green, C.softGreen],
  ];
  labels.forEach((l, i) => {
    card(slide, xs[i], ys, 2.35, 2.52, { fill: l[4], line: l[4] });
    numberBadge(slide, l[0], xs[i] + 0.23, ys + 0.22, l[3]);
    heading(slide, l[1], xs[i] + 0.26, ys + 0.78, 1.82, { size: 13.3, color: l[3], h: 0.55 });
    body(slide, l[2], xs[i] + 0.26, ys + 1.62, 1.8, 0.46, { size: 9.3, color: C.ink });
    if (i < labels.length - 1) arrow(slide, xs[i] + 2.38, ys + 1.26, xs[i + 1] - 0.16, ys + 1.26, C.muted);
  });
  addQuote(slide, "skill internalization 不是 reward 单点实现，而是训练流程把外部 scaffold 慢慢拿掉。", 1.0, 5.7, 10.9, 0.62, C.teal);
  slide.addNotes("把方法的三件套串起来讲。强调终点是 zero-skill inference，而不是更聪明的 retrieval。");
  push(slide, 8);
}

// 9
{
  const slide = pptx.addSlide();
  addTitle(slide, "Agent loop 与 skill library", "把 agent 自动化建模为序列决策，skill bank 用分层 Markdown 管理", "Method");
  flowBox(slide, "Instruction I", 0.82, 1.7, 1.62, 0.62, C.white, C.line);
  flowBox(slide, "Observation o_t", 0.82, 2.62, 1.62, 0.62, C.white, C.line);
  flowBox(slide, "History h_t", 0.82, 3.54, 1.62, 0.62, C.white, C.line);
  flowBox(slide, "Active Skills S", 3.18, 2.35, 1.88, 1.12, C.softTeal, C.teal);
  flowBox(slide, "Policy\nπθ(a_t | I, h_t)", 6.08, 2.35, 2.18, 1.12, C.softBlue, C.blue);
  flowBox(slide, "Action a_t", 9.25, 1.78, 1.62, 0.62, C.white, C.line);
  flowBox(slide, "Env feedback", 9.25, 3.38, 1.62, 0.62, C.white, C.line);
  arrow(slide, 2.48, 2.03, 3.08, 2.66, C.muted);
  arrow(slide, 2.48, 2.93, 3.08, 2.89, C.muted);
  arrow(slide, 2.48, 3.85, 3.08, 3.17, C.muted);
  arrow(slide, 5.08, 2.9, 5.98, 2.9, C.teal);
  arrow(slide, 8.28, 2.9, 9.12, 2.11, C.blue);
  arrow(slide, 10.04, 2.45, 10.04, 3.25, C.muted);
  card(slide, 1.1, 5.22, 4.6, 0.78, { fill: C.softAmber, line: C.softAmber });
  heading(slide, "General skills", 1.42, 5.42, 1.4, { size: 12, color: C.amber });
  body(slide, "exploration / goal-tracking / common strategy", 2.88, 5.45, 2.2, 0.2, { size: 8.5, color: C.ink });
  card(slide, 6.18, 5.22, 4.6, 0.78, { fill: C.softCoral, line: C.softCoral });
  heading(slide, "Task-specific skills", 6.48, 5.42, 1.95, { size: 12, color: C.coral });
  body(slide, "action sequence / preconditions / task category", 8.48, 5.45, 2.05, 0.2, { size: 8.5, color: C.ink });
  smallLabel(slide, "skills/{task_name}/{skill_category}.md", 4.7, 6.34, 3.8, C.muted);
  slide.addNotes("解释 skill library 的层次：通用 skill 和任务专属 skill。这里不需要展开每个 markdown，只讲它们是训练时 scaffold。");
  push(slide, 9);
}

// 10
{
  const slide = pptx.addSlide();
  addTitle(slide, "Context rendering：把长文本压成视觉上下文", "history 与 skills 不直接长文本拼接，而是渲染成 RGB 图像再编码", "Method");
  flowBox(slide, "interaction\nhistory h_t", 0.9, 2.0, 1.8, 0.9, C.white, C.line);
  flowBox(slide, "selected\nskills S", 0.9, 3.18, 1.8, 0.9, C.softTeal, C.teal);
  flowBox(slide, "Render\nRGB context", 3.55, 2.44, 2.1, 1.14, C.softAmber, C.amber);
  flowBox(slide, "Vision Encoder\nV_t = Enc(h_t,S;c_t)", 6.55, 2.44, 2.42, 1.14, C.softBlue, C.blue);
  flowBox(slide, "Policy outputs\n(a_t, c_t)", 9.92, 2.44, 1.98, 1.14, C.softCoral, C.coral);
  arrow(slide, 2.76, 2.45, 3.42, 2.8, C.muted);
  arrow(slide, 2.76, 3.63, 3.42, 3.08, C.muted);
  arrow(slide, 5.68, 3.01, 6.42, 3.01, C.amber);
  arrow(slide, 9.0, 3.01, 9.82, 3.01, C.blue);
  card(slide, 1.25, 5.18, 10.58, 0.82, { fill: C.white });
  body(slide, "关键：压缩比 c_t 不是固定超参，而是 policy 每一步一起生成；模型同时决定“做什么”和“上下文压缩到什么程度”。", 1.62, 5.42, 9.75, 0.28, { size: 12.2, color: C.ink });
  slide.addNotes("讲视觉上下文压缩时要避免让听众误以为只是工程优化。这里的 interesting point 是压缩比也由 policy 决定，并被 reward 引导。");
  push(slide, 10);
}

// 11
{
  const slide = pptx.addSlide();
  addTitle(slide, "ICRL：训练目标是“从依赖上下文到依赖参数”", "rollout 阶段提供 skill guidance，但 inference 全部撤掉", "Method");
  const phases = [
    ["early training", "full / high skill exposure", "先让模型能学到复杂 multi-step behavior", C.blue, C.softBlue],
    ["mid training", "reduced active skill set", "让 policy 开始承担更多决策负担", C.amber, C.softAmber],
    ["late training", "S = empty set", "直接优化无 skill 条件下的执行能力", C.green, C.softGreen],
  ];
  phases.forEach((p, i) => {
    const x = 0.84 + i * 4.05;
    card(slide, x, 1.72, 3.45, 2.58, { fill: p[4], line: p[4] });
    smallLabel(slide, p[0], x + 0.28, 1.98, 1.6, p[3]);
    heading(slide, p[1], x + 0.28, 2.44, 2.7, { size: 15, color: p[3], h: 0.5 });
    body(slide, p[2], x + 0.3, 3.32, 2.64, 0.43, { size: 10.2, color: C.ink });
    if (i < phases.length - 1) arrow(slide, x + 3.48, 3.0, x + 3.94, 3.0, C.muted);
  });
  addQuote(slide, "RL 不只是学任务，而是在学迁移：follow external skills → execute from internalized policy。", 1.0, 5.38, 10.9, 0.7, C.teal);
  slide.addNotes("这里给一个训练课程中的类比：先带着示范做题，再逐步撤掉提示，最后闭卷完成。");
  push(slide, 11);
}

// 12
{
  const slide = pptx.addSlide();
  addTitle(slide, "Dynamic curriculum：用 helpfulness 决定保留哪些 skill", "固定 schedule 要么删太快，要么删太慢；SKILL0 做在线评估", "Method");
  card(slide, 0.9, 1.64, 5.25, 3.64, { fill: C.white });
  heading(slide, "helpfulness 定义", 1.28, 2.0, 2.1, { size: 16, color: C.teal });
  slide.addText("Δ_k = Acc_k^{w/skill} - Acc_k^{w/o skill}", {
    x: 1.3,
    y: 2.72,
    w: 4.25,
    h: 0.42,
    fontFace: "Cambria Math",
    fontSize: 19,
    color: C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  body(slide, "若 Δ_k > 0，说明当前 policy 仍然能从该 skill 受益，暂时保留；否则剔除。", 1.32, 3.55, 4.15, 0.62, { size: 11.5, color: C.ink });
  card(slide, 7.08, 1.64, 4.98, 3.64, { fill: C.softAmber, line: C.softAmber });
  heading(slide, "Filter / Rank / Select", 7.44, 2.0, 3.3, { size: 16, color: C.amber });
  bullets(slide, [
    "Filter：只保留 Δ_k > 0",
    "Rank：按 helpfulness 降序",
    "Select：取 top-M^(s) skill files",
  ], 7.62, 2.78, 3.66, { size: 11.5, gap: 0.56 });
  addQuote(slide, "skill 不是机械删除，而是“当前 policy 仍然需要它时才保留”。", 1.06, 6.03, 10.6, 0.55, C.amber);
  slide.addNotes("重点讲 helpfulness 的含义：同一个 skill 对不同训练阶段的 policy 价值会变，所以 curriculum 要跟着 policy 变。");
  push(slide, 12);
}

// 13
{
  const slide = pptx.addSlide();
  addTitle(slide, "Skill budget 逐阶段下降", "训练被切成 stages，skill budget 从 N 线性退火到 0", "Method");
  slide.addText("|S^(s)| ≤ M^(s) = ceil(N · (N_S - s) / (N_S - 1))", {
    x: 1.04,
    y: 1.58,
    w: 10.7,
    h: 0.42,
    fontFace: "Cambria Math",
    fontSize: 18,
    color: C.ink,
    margin: 0,
    align: "center",
    breakLine: false,
    fit: "shrink",
  });
  const stageX = [1.15, 4.75, 8.35];
  const rows = [
    ["Stage 1", "高预算", "ALFWorld: 6\nSearch-QA: 5", C.blue, C.softBlue],
    ["Stage 2", "中预算", "ALFWorld: 3\nSearch-QA: 3", C.amber, C.softAmber],
    ["Stage 3", "零预算", "S = ∅", C.green, C.softGreen],
  ];
  rows.forEach((r, i) => {
    card(slide, stageX[i], 2.75, 2.7, 2.08, { fill: r[4], line: r[4] });
    smallLabel(slide, r[0], stageX[i] + 0.26, 3.06, 1.2, r[3]);
    heading(slide, r[1], stageX[i] + 0.26, 3.42, 1.8, { size: 17, color: r[3] });
    body(slide, r[2], stageX[i] + 0.28, 4.05, 1.95, 0.4, { size: 11, color: C.ink });
    if (i < 2) arrow(slide, stageX[i] + 2.75, 3.79, stageX[i + 1] - 0.16, 3.79, C.muted);
  });
  body(slide, "最后一个 stage 必须让 S 为空：这一步把“推理时不带 skill”直接纳入训练条件。", 1.42, 5.82, 9.75, 0.32, { size: 12.2, color: C.muted, bold: true });
  slide.addNotes("这一页讲 budget 退火。把默认预算数字念出来即可，不需要在公式上停太久。");
  push(slide, 13);
}

// 14
{
  const slide = pptx.addSlide();
  addTitle(slide, "Reward：任务成功 + 压缩效率", "composite reward 只在任务成功时奖励更高 compression ratio", "Method");
  card(slide, 0.92, 1.62, 5.4, 3.72, { fill: C.white });
  heading(slide, "Composite reward", 1.28, 1.98, 2.9, { size: 16, color: C.teal });
  slide.addText("r_t^comp = ln(c_t),  if success\nr_t^comp = 0,      otherwise", {
    x: 1.34,
    y: 2.72,
    w: 4.36,
    h: 0.78,
    fontFace: "Cambria Math",
    fontSize: 17,
    color: C.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addText("r̃_t = r_t + λ · r_t^comp", {
    x: 1.36,
    y: 4.06,
    w: 3.9,
    h: 0.34,
    fontFace: "Cambria Math",
    fontSize: 18,
    bold: true,
    color: C.coral,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  card(slide, 7.05, 1.62, 4.98, 3.72, { fill: C.softBlue, line: C.softBlue });
  heading(slide, "它推动两件事", 7.42, 1.98, 2.7, { size: 16, color: C.blue });
  bullets(slide, [
    "task-solving behavior：先做对任务",
    "context efficiency：成功后更省上下文",
    "internalization 仍主要来自 ICRL + curriculum",
  ], 7.62, 2.82, 3.58, { size: 11.2, gap: 0.54 });
  slide.addNotes("注意讲清楚边界：reward 主要鼓励任务和压缩，不是单靠 reward 内化 skill；内化来自训练过程中持续去 skill。");
  push(slide, 14);
}

sectionSlide(15, "PART 3", "Evidence", "结果是否支撑“skill 已内化”");

// 16
{
  const slide = pptx.addSlide();
  addTitle(slide, "实验设置：两个 agentic benchmark", "ALFWorld 检验多步行动，Search-QA 检验检索问答与泛化", "Experiments");
  card(slide, 0.84, 1.62, 5.58, 3.8, { fill: C.softTeal, line: C.softTeal });
  heading(slide, "ALFWorld", 1.18, 1.96, 2.0, { size: 18, color: C.teal });
  bullets(slide, [
    "3827 个文本环境 household tasks",
    "Pick / Look / Clean / Heat / Cool / Pick2",
    "batch 16 tasks，每个 prompt 8 rollouts",
    "max prompt length 3072",
  ], 1.34, 2.72, 4.28, { size: 10.8, gap: 0.46 });
  card(slide, 6.92, 1.62, 5.58, 3.8, { fill: C.softBlue, line: C.softBlue });
  heading(slide, "Search-based QA", 7.26, 1.96, 2.8, { size: 18, color: C.blue });
  bullets(slide, [
    "NQ / TriviaQA / PopQA / HotpotQA / 2Wiki / MuSiQue / Bamboogle",
    "训练来自 NQ 与 HotpotQA，其余做 OOD",
    "batch 128 tasks，retriever 使用 E5",
    "max prompt length 4096",
  ], 7.42, 2.72, 4.34, { size: 10.3, gap: 0.46 });
  pill(slide, "Backbone: Qwen2.5-(VL)-3B/7B-Instruct", 3.82, 6.02, 3.7, C.ink, C.white);
  pill(slide, "180 steps / 4 × H800 / N_S = 3", 7.82, 6.02, 2.9, C.ink, C.white);
  slide.addNotes("快速过实验设置。这里不需要展开所有数据集，核心是说明覆盖了环境行动和搜索问答两类 agentic 任务。");
  push(slide, 16);
}

// 17
{
  const slide = pptx.addSlide();
  addTitle(slide, "主结果：不带 inference skill 仍然有竞争力", "Table 1 中，SKILL0 显著优于标准 RL baseline，也能与 skill-augmented 方法竞争", "Results");
  card(slide, 0.88, 1.55, 5.52, 4.45, { fill: C.white });
  heading(slide, "ALFWorld success rate", 1.2, 1.9, 2.8, { size: 15.5, color: C.teal });
  hBarChart(slide, [
    { label: "AgentOCR 3B", value: 78.2, display: "78.2", color: "AAB4C0" },
    { label: "SKILL0 3B", value: 87.9, display: "87.9", color: C.teal },
    { label: "SKILL0 7B", value: 89.8, display: "89.8", color: C.green },
  ], 1.15, 2.62, 4.55, 1.52, 100, { labelW: 1.48 });
  body(slide, "3B 相比 AgentOCR：+9.7", 1.2, 4.84, 3.1, 0.26, { size: 12, color: C.teal, bold: true });
  card(slide, 6.9, 1.55, 5.52, 4.45, { fill: C.white });
  heading(slide, "Search-QA accuracy", 7.22, 1.9, 2.6, { size: 15.5, color: C.blue });
  hBarChart(slide, [
    { label: "AgentOCR 3B", value: 34.2, display: "34.2", color: "AAB4C0" },
    { label: "SKILL0 3B", value: 40.8, display: "40.8", color: C.blue },
    { label: "SKILL0 7B", value: 44.4, display: "44.4", color: C.green },
  ], 7.17, 2.62, 4.55, 1.52, 50, { labelW: 1.48 });
  body(slide, "3B 相比 AgentOCR：+6.6", 7.22, 4.84, 3.1, 0.26, { size: 12, color: C.blue, bold: true });
  addQuote(slide, "关键不是分数最高，而是在不依赖 inference-time skill prompting 的条件下达到这些分数。", 1.1, 6.25, 10.9, 0.48, C.teal);
  slide.addNotes("解释数字时强调条件：zero-skill inference。AgentOCR 的数值由论文报告的提升量反推，用作对比锚点。");
  push(slide, 17);
}

// 18
{
  const slide = pptx.addSlide();
  addTitle(slide, "Token efficiency：上下文成本低约 5 倍以上", "3B setting 下，每 step 平均 context 成本显著低于 SkillRL", "Results");
  card(slide, 1.0, 1.52, 10.95, 4.66, { fill: C.white });
  heading(slide, "Tokens / step (k)", 1.38, 1.86, 2.3, { size: 15, color: C.ink });
  hBarChart(slide, [
    { label: "SkillRL ALFWorld", value: 2.21, display: "2.21k", color: "AAB4C0" },
    { label: "SKILL0 ALFWorld", value: 0.38, display: "0.38k", color: C.teal },
    { label: "SkillRL Search-QA", value: 0.87, display: "0.87k", color: "AAB4C0" },
    { label: "SKILL0 Search-QA", value: 0.18, display: "0.18k", color: C.blue },
  ], 1.44, 2.64, 8.72, 2.25, 2.4, { labelW: 2.15, valueW: 0.8, labelSize: 9.5 });
  card(slide, 10.62, 2.5, 1.12, 1.2, { fill: C.softTeal, line: C.softTeal });
  slide.addText("≈5x", {
    x: 10.73,
    y: 2.75,
    w: 0.72,
    h: 0.36,
    fontFace: "Aptos Display",
    fontSize: 24,
    bold: true,
    color: C.teal,
    margin: 0,
    align: "center",
  });
  body(slide, "更低上下文开销", 10.68, 3.28, 0.92, 0.18, { size: 7.6, color: C.teal, bold: true });
  addQuote(slide, "对训练团队的含义：如果经验/skill 不能内化，规模越大越容易被上下文预算卡住。", 1.08, 6.5, 10.7, 0.42, C.blue);
  slide.addNotes("把 token efficiency 讲成工程收益，而不只是论文指标。低 token 也意味着更可部署。");
  push(slide, 18);
}

// 19
{
  const slide = pptx.addSlide();
  addTitle(slide, "Training dynamics：早期借助 skill，后期无 skill 追上", "论文趋势显示 skill knowledge 正在从 context 转移到参数中", "Results");
  card(slide, 0.95, 1.52, 6.0, 4.35, { fill: C.white });
  heading(slide, "验证曲线的读法", 1.32, 1.88, 2.4, { size: 15.5, color: C.ink });
  miniAxisChart(slide, 1.48, 2.7, 4.6, 2.28);
  card(slide, 7.45, 1.52, 4.8, 4.35, { fill: C.softAmber, line: C.softAmber });
  heading(slide, "三点观察", 7.82, 1.88, 1.8, { size: 15.5, color: C.amber });
  bullets(slide, [
    "with skill：早期收敛更快",
    "without skill：早期较弱，后期逐渐追上",
    "SKILL0 未早早 plateau，后期仍持续提升",
  ], 8.02, 2.72, 3.42, { size: 10.8, gap: 0.56 });
  smallLabel(slide, "schematic summary of paper-reported trend", 1.5, 5.42, 3.2, C.muted);
  slide.addNotes("这页不要把示意曲线当精确数值。重点讲现象：如果无 skill 的验证后期追上，说明模型不只是依赖提示词。");
  push(slide, 19);
}

// 20
{
  const slide = pptx.addSlide();
  addTitle(slide, "Ablation 1：固定 skill budget 会出问题", "渐进式 budget 退火效果最好，full skill set 反而导致撤掉后崩塌", "Ablation");
  card(slide, 0.96, 1.62, 5.15, 3.9, { fill: C.softCoral, line: C.softCoral });
  heading(slide, "固定 full skill set", 1.32, 2.0, 3.1, { size: 16, color: C.coral });
  body(slide, "早期 guidance 强，但 policy 容易长期依赖外部 skill。", 1.38, 2.76, 3.95, 0.48, { size: 11.2, color: C.ink });
  slide.addText("去掉 skill 后：-12.3", {
    x: 1.38,
    y: 4.22,
    w: 3.2,
    h: 0.34,
    fontFace: FONT,
    fontSize: 19,
    bold: true,
    color: C.coral,
    margin: 0,
  });
  card(slide, 7.12, 1.62, 5.15, 3.9, { fill: C.softGreen, line: C.softGreen });
  heading(slide, "渐进式 budget 退火", 7.48, 2.0, 3.4, { size: 16, color: C.green });
  body(slide, "先利用 skill 降低探索难度，再逐步把负担交回 policy。", 7.54, 2.76, 3.95, 0.48, { size: 11.2, color: C.ink });
  slide.addText("无 skill 反而高：+1.6", {
    x: 7.54,
    y: 4.22,
    w: 3.2,
    h: 0.34,
    fontFace: FONT,
    fontSize: 19,
    bold: true,
    color: C.green,
    margin: 0,
  });
  slide.addNotes("解释两个失败模式：full skill 依赖太强；低预算限制早期探索。SKILL0 折中，但不是简单折中，而是动态选择。");
  push(slide, 20);
}

// 21
{
  const slide = pptx.addSlide();
  addTitle(slide, "Ablation 2：Filter / Rank / Select 缺一不可", "不是 skill 越多越好，关键是保留真正 helpful 的 skill", "Ablation");
  card(slide, 0.95, 1.5, 6.2, 4.6, { fill: C.white });
  heading(slide, "ALFWorld w/o skill performance", 1.3, 1.86, 3.4, { size: 15.5, color: C.ink });
  hBarChart(slide, [
    { label: "Complete", value: 87.9, display: "87.9", color: C.teal },
    { label: "w/o Filter", value: 78.9, display: "78.9", color: C.amber },
    { label: "w/o Rank", value: 62.9, display: "62.9", color: C.coral },
  ], 1.32, 2.72, 4.9, 1.55, 100, { labelW: 1.35 });
  card(slide, 7.58, 1.5, 4.45, 4.6, { fill: C.softBlue, line: C.softBlue });
  heading(slide, "为什么 Rank 很重要？", 7.94, 1.88, 3.1, { size: 15.5, color: C.blue });
  body(slide, "有些 skill 虽然仍有正收益，但收益很小；预算下降时，如果不排序，可能把真正关键的 skill 挤掉。", 7.98, 2.7, 3.2, 0.9, { size: 11.2, color: C.ink });
  body(slide, "结论：curriculum 的价值在于“随 policy 改变而选择”。", 7.98, 4.42, 3.22, 0.42, { size: 12, color: C.blue, bold: true });
  slide.addNotes("强调 ablation 支撑论文核心：不是撤 skill 这个动作本身，而是 helpfulness-driven 撤 skill。");
  push(slide, 21);
}

sectionSlide(22, "PART 4", "Related Work", "AgentEvolver / MemSkill / SkillRL 放进同一张图");

// 23
{
  const slide = pptx.addSlide();
  addTitle(slide, "AgentEvolver self-navigating vs SKILL0", "两者都用外部经验，但一个解决探索，一个追求内化", "Related work");
  card(slide, 0.82, 1.5, 5.65, 4.5, { fill: C.softAmber, line: C.softAmber });
  heading(slide, "AgentEvolver", 1.2, 1.9, 2.2, { size: 18, color: C.amber });
  bullets(slide, [
    "experience 是 rollout-time navigation signal",
    "离线从成功/失败轨迹构造 experience pool",
    "在线检索 top-k experience 注入 prompt",
    "experience stripping 避免训练时记住提示词",
    "selective boosting 提升正优势样本权重",
  ], 1.38, 2.74, 4.22, { size: 10.2, gap: 0.43 });
  card(slide, 6.9, 1.5, 5.65, 4.5, { fill: C.softTeal, line: C.softTeal });
  heading(slide, "SKILL0", 7.28, 1.9, 1.6, { size: 18, color: C.teal });
  bullets(slide, [
    "skill 是 training-time scaffold",
    "核心目标是把 skill 内化进 policy 参数",
    "动态 curriculum 逐步减少 skill 暴露",
    "终点是 zero-skill inference",
    "不强调继续扩充 skill bank",
  ], 7.46, 2.74, 4.22, { size: 10.2, gap: 0.43 });
  body(slide, "一句话：AgentEvolver 给 agent 一张导航地图；SKILL0 先看说明书学，最后不带说明书也会做。", 1.18, 6.35, 10.75, 0.28, { size: 12.2, color: C.ink, bold: true });
  slide.addNotes("这里用比喻帮助听众记住差异。也提醒 AgentEvolver 有 stripping 机制，所以不是简单 prompt 记忆。");
  push(slide, 23);
}

// 24
{
  const slide = pptx.addSlide();
  addTitle(slide, "MemSkill / SkillRL / SKILL0：分别学进了什么？", "三篇都和 skill 有关，但 skill 的对象不同", "Related work");
  const x0 = 0.55;
  const widths = [2.02, 3.08, 3.08, 3.08];
  const headers = ["维度", "MemSkill", "SkillRL", "SKILL0"];
  let x = x0;
  headers.forEach((h, i) => {
    card(slide, x, 1.42, widths[i], 0.55, { fill: i === 0 ? C.charcoal : C.teal, line: i === 0 ? C.charcoal : C.teal });
    body(slide, h, x + 0.08, 1.6, widths[i] - 0.16, 0.18, { size: 9.5, color: C.white, bold: true });
    x += widths[i] + 0.07;
  });
  const table = [
    ["解决问题", "如何构造/维护 memory", "如何把轨迹蒸馏成 reusable skills", "如何把 skills 内化到参数"],
    ["skill 对象", "memory operation", "task-solving strategy", "task-solving strategy"],
    ["skill bank", "持续演化", "持续演化", "动态筛减，不强调扩充"],
    ["推理依赖", "依赖 skill bank", "依赖 skill retrieval", "目标是 zero skill inference"],
    ["主命题", "教 agent 怎么记", "教 agent 借助手册做题", "教 agent 最后不用手册也会做"],
  ];
  table.forEach((row, r) => {
    x = x0;
    row.forEach((cell, c) => {
      const fill = r % 2 === 0 ? "FFFFFF" : "F5F7FA";
      card(slide, x, 2.05 + r * 0.78, widths[c], 0.68, { fill, line: "E5EBF2" });
      body(slide, cell, x + 0.08, 2.2 + r * 0.78, widths[c] - 0.16, 0.32, {
        size: c === 0 ? 8.2 : 8.1,
        color: c === 0 ? C.muted : C.ink,
        bold: c === 0,
      });
      x += widths[c] + 0.07;
    });
  });
  slide.addNotes("这页是相关工作对比的主表。不要逐格念，重点讲最后一行的三个比喻，帮助定位 SKILL0 的独特性。");
  push(slide, 24);
}

// 25
{
  const slide = pptx.addSlide();
  addTitle(slide, "对训练团队的启发：从“经验增强”走向“经验内化”", "SKILL0 给了一个可迁移的两段式研究路线", "Implications");
  flowBox(slide, "阶段 A\n提升 rollout 质量", 0.98, 1.88, 2.3, 1.15, C.softBlue, C.blue);
  flowBox(slide, "经验池 / skill bank\n检索或导航", 3.82, 1.88, 2.3, 1.15, C.softAmber, C.amber);
  flowBox(slide, "阶段 B\n逐步减少暴露", 6.66, 1.88, 2.3, 1.15, C.softTeal, C.teal);
  flowBox(slide, "部署\nzero skill / low retrieval", 9.5, 1.88, 2.3, 1.15, C.softGreen, C.green);
  arrow(slide, 3.3, 2.46, 3.72, 2.46, C.muted);
  arrow(slide, 6.14, 2.46, 6.56, 2.46, C.muted);
  arrow(slide, 8.98, 2.46, 9.4, 2.46, C.muted);
  card(slide, 1.04, 4.16, 3.28, 1.58, { fill: C.white });
  heading(slide, "训练设计", 1.32, 4.46, 1.5, { size: 13.5, color: C.teal });
  body(slide, "把“去经验/去 skill”变成训练条件，而不是上线前的临时裁剪。", 1.34, 5.02, 2.35, 0.45, { size: 10.2, color: C.ink });
  card(slide, 5.02, 4.16, 3.28, 1.58, { fill: C.white });
  heading(slide, "评估设计", 5.3, 4.46, 1.5, { size: 13.5, color: C.blue });
  body(slide, "每个 skill/experience 要有对应验证子集，才能估计 helpfulness。", 5.32, 5.02, 2.35, 0.45, { size: 10.2, color: C.ink });
  card(slide, 9.0, 4.16, 3.28, 1.58, { fill: C.white });
  heading(slide, "部署设计", 9.28, 4.46, 1.5, { size: 13.5, color: C.green });
  body(slide, "上线目标可以从 full retrieval 降到 low retrieval，甚至 zero retrieval。", 9.3, 5.02, 2.35, 0.45, { size: 10.2, color: C.ink });
  slide.addNotes("这一页落到团队研究：经验池先用于提升 rollout，之后用 curriculum 逐步减少经验暴露，逼 policy 接管能力。");
  push(slide, 25);
}

// 26
{
  const slide = pptx.addSlide();
  addTitle(slide, "落地时要追问的 5 个问题", "这些问题决定 SKILL0 思路能不能迁移到我们的任务", "Implications");
  const qs = [
    ["1", "经验/skill 的粒度是什么？", "file、rule、trajectory summary，还是 action template？"],
    ["2", "如何构造验证子任务？", "没有可分解验证集，就很难做 helpfulness-driven filtering。"],
    ["3", "去 skill 的最终目标是什么？", "zero retrieval、low retrieval，还是只去掉长文本？"],
    ["4", "怎样避免 false internalization？", "需要无 skill 验证、OOD 验证和消融，而不是只看训练 reward。"],
    ["5", "压缩效率是否值得联合优化？", "如果部署成本敏感，可以把 context cost 纳入 reward。"],
  ];
  qs.forEach((q, i) => {
    const y = 1.36 + i * 1.0;
    numberBadge(slide, q[0], 0.9, y + 0.14, [C.teal, C.blue, C.amber, C.coral, C.green][i]);
    heading(slide, q[1], 1.38, y + 0.1, 3.6, { size: 13.4, color: C.ink });
    body(slide, q[2], 5.18, y + 0.13, 6.6, 0.28, { size: 10.6, color: C.muted });
    slide.addShape(pptx.ShapeType.line, { x: 0.9, y: y + 0.78, w: 11.15, h: 0, line: { color: "E7ECF2", width: 0.8 } });
  });
  slide.addNotes("这一页适合作为讨论前的 checklist。可以邀请训练团队针对自己的任务逐项回答。");
  push(slide, 26);
}

// 27
{
  const slide = pptx.addSlide();
  addTitle(slide, "总结 takeaway", "SKILL0 的价值在于明确提出并验证 skill internalization 训练目标", "Takeaway");
  const takes = [
    ["1", "核心贡献不是更强 retrieval", "而是 training with skills, inference with zero skills。", C.teal, C.softTeal],
    ["2", "方法论很清晰", "ICRL + helpfulness-driven curriculum + visual context compression。", C.blue, C.softBlue],
    ["3", "实验支撑“脚手架可以撤掉”", "早期 skill 帮助探索，后期撤掉后仍能保持甚至提升表现。", C.green, C.softGreen],
    ["4", "最值得迁移的是训练范式", "先用经验提升 rollout，再逐步减少经验暴露，把经验写进参数。", C.amber, C.softAmber],
  ];
  takes.forEach((t, i) => {
    const x = i % 2 === 0 ? 0.9 : 6.75;
    const y = i < 2 ? 1.58 : 4.0;
    card(slide, x, y, 5.25, 1.56, { fill: t[4], line: t[4] });
    numberBadge(slide, t[0], x + 0.26, y + 0.24, t[3]);
    heading(slide, t[1], x + 0.78, y + 0.23, 3.75, { size: 13.4, color: t[3] });
    body(slide, t[2], x + 0.8, y + 0.88, 3.75, 0.34, { size: 10.5, color: C.ink });
  });
  slide.addNotes("用四句话收束。如果时间不足，可以直接用这一页做最后总结。");
  push(slide, 27);
}

// 28
{
  const slide = pptx.addSlide();
  slide.background = { color: C.charcoal };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: W,
    h: H,
    fill: { color: C.charcoal },
    line: { color: C.charcoal, transparency: 100 },
  });
  slide.addText("最后一句话", {
    x: 0.95,
    y: 1.08,
    w: 3.2,
    h: 0.36,
    fontFace: FONT,
    fontSize: 17,
    bold: true,
    color: C.amber,
    margin: 0,
  });
  slide.addText("SkillRL 在教模型“怎么更好地借助手册做题”；\nMemSkill 在教模型“怎么写和维护手册”；\nSKILL0 在教模型“先看手册学，最后不带手册也会做”。", {
    x: 0.95,
    y: 2.05,
    w: 10.9,
    h: 1.76,
    fontFace: FONT,
    fontSize: 24,
    bold: true,
    color: C.white,
    margin: 0,
    breakLine: false,
    fit: "shrink",
    valign: "mid",
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.98,
    y: 5.16,
    w: 3.72,
    h: 0.08,
    fill: { color: C.teal },
    line: { transparency: 100 },
  });
  body(slide, "Q&A / discussion", 0.98, 5.45, 3.0, 0.28, { size: 13, color: "DDE8F3", bold: true });
  slide.addNotes("收尾时直接念这句话，然后进入讨论。");
  push(slide, 28);
}

for (const slide of slides) {
  warnIfSlideHasOverlaps(slide, pptx, {
    ignoreLines: true,
    ignoreDecorativeShapes: true,
    muteContainment: true,
  });
  warnIfSlideElementsOutOfBounds(slide, pptx);
}

pptx.writeFile({ fileName: "dist/SKILL0-paper-sharing.pptx" });
