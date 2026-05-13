const C = {
  primary: '#000000',
  dark: '#010120',
  darkSoft: '#313641',
  darkLine: '#26263a',
  canvas: '#ffffff',
  hairline: '#ebebeb',
  body: '#999999',
  ink: '#000000',
  orange: '#fc4c02',
  magenta: '#ef2cc1',
  periwinkle: '#bdbbff',
  mint: '#c8f6f9',
  green: '#d9f7e2',
  caution: '#fff4cc',
  red: '#ffe5e5',
};
const F = {
  display: 'Pretendard',
  mono: 'Pretendard',
};
export { C, F };

export function bg(slide, ctx, fill = C.canvas) {
  ctx.addShape(slide, { left: 0, top: 0, width: ctx.W, height: ctx.H, fill, line: ctx.line('#00000000', 0) });
}

export function text(slide, ctx, value, x, y, w, h, opts = {}) {
  return ctx.addText(slide, {
    text: value,
    left: x,
    top: y,
    width: w,
    height: h,
    fontSize: opts.size ?? 24,
    typeface: opts.face ?? F.display,
    color: opts.color ?? C.ink,
    bold: opts.bold ?? false,
    align: opts.align ?? 'left',
    valign: opts.valign ?? 'top',
    fill: opts.fill ?? '#00000000',
    line: opts.line ?? ctx.line('#00000000', 0),
    insets: opts.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
  });
}

export function mono(slide, ctx, value, x, y, w, h, opts = {}) {
  return text(slide, ctx, String(value).toUpperCase(), x, y, w, h, {
    size: opts.size ?? 12,
    face: F.mono,
    color: opts.color ?? C.body,
    bold: opts.bold ?? false,
    align: opts.align ?? 'left',
    fill: opts.fill,
    line: opts.line,
    insets: opts.insets,
  });
}

export function headline(slide, ctx, value, x, y, w, h, opts = {}) {
  return text(slide, ctx, value, x, y, w, h, {
    size: opts.size ?? 46,
    color: opts.color ?? C.ink,
    bold: false,
    face: F.display,
  });
}

export function body(slide, ctx, value, x, y, w, h, opts = {}) {
  return text(slide, ctx, value, x, y, w, h, {
    size: opts.size ?? 17,
    color: opts.color ?? C.body,
    face: F.display,
  });
}

export function pill(slide, ctx, value, x, y, w, h, opts = {}) {
  ctx.addShape(slide, { left: x, top: y, width: w, height: h, geometry: 'roundRect', fill: opts.fill ?? C.primary, line: ctx.line(opts.border ?? '#00000000', opts.border ? 1 : 0) });
  mono(slide, ctx, value, x, y + h / 2 - 8, w, 16, { size: opts.size ?? 13, color: opts.color ?? '#ffffff', align: 'center', bold: true });
}

export function card(slide, ctx, x, y, w, h, opts = {}) {
  ctx.addShape(slide, { left: x, top: y, width: w, height: h, geometry: opts.round ? 'roundRect' : 'rect', fill: opts.fill ?? C.canvas, line: ctx.line(opts.line ?? C.hairline, 1) });
}

export function header(slide, ctx, opts = {}) {
  const dark = opts.dark ?? false;
  mono(slide, ctx, opts.kicker ?? 'MICROSOFT FOUNDRY FINAL', 54, 32, 360, 18, { color: dark ? '#ffffff' : C.body, size: 11, bold: true });
  text(slide, ctx, 'RecallGuard AI', 1020, 30, 205, 22, { size: 18, color: dark ? '#ffffff' : C.ink });
}

export function footer(slide, ctx, index, opts = {}) {
  const dark = opts.dark ?? false;
  mono(slide, ctx, `SLIDE ${String(index).padStart(2, '0')} / GOVERNED MULTI-AGENT WORKFLOW`, 54, 672, 620, 16, { color: dark ? '#bdbbff' : C.body, size: 10 });
}

export function gradientRibbon(slide, ctx, x, y, w, h, opts = {}) {
  const angle = opts.angle ?? -14;
  // One brand-chrome object, built as layered translucent bands to survive PPT export.
  ctx.addShape(slide, { left: x, top: y + h * 0.18, width: w, height: h * 0.32, geometry: 'roundRect', fill: C.orange, line: ctx.line('#00000000', 0) }).rotation = angle;
  ctx.addShape(slide, { left: x + w * 0.08, top: y + h * 0.34, width: w * 0.92, height: h * 0.32, geometry: 'roundRect', fill: C.magenta, line: ctx.line('#00000000', 0) }).rotation = angle;
  ctx.addShape(slide, { left: x + w * 0.18, top: y + h * 0.50, width: w * 0.82, height: h * 0.32, geometry: 'roundRect', fill: C.periwinkle, line: ctx.line('#00000000', 0) }).rotation = angle;
}

export function metricTile(slide, ctx, x, y, w, h, num, label, fill = C.mint) {
  card(slide, ctx, x, y, w, h, { fill, line: C.hairline, round: true });
  text(slide, ctx, num, x + 22, y + 22, w - 44, 42, { size: 38, color: C.ink });
  mono(slide, ctx, label, x + 24, y + h - 34, w - 48, 16, { size: 10.5, color: C.ink, bold: true });
}

export function table(slide, ctx, x, y, colWidths, rowH, headers, rows, opts = {}) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  card(slide, ctx, x, y, totalW, rowH * (rows.length + 1), { fill: C.canvas, line: C.hairline });
  let cx = x;
  headers.forEach((h, i) => {
    ctx.addShape(slide, { left: cx, top: y, width: colWidths[i], height: rowH, fill: opts.headerFill ?? C.hairline, line: ctx.line(C.hairline, 1) });
    mono(slide, ctx, h, cx + 12, y + 12, colWidths[i] - 24, rowH - 24, { size: opts.headerSize ?? 8.8, color: C.body, bold: true });
    cx += colWidths[i];
  });
  rows.forEach((row, r) => {
    cx = x;
    row.forEach((cell, i) => {
      const top = y + rowH * (r + 1);
      ctx.addShape(slide, { left: cx, top, width: colWidths[i], height: rowH, fill: C.canvas, line: ctx.line(C.hairline, 1) });
      const isMono = opts.monoCols?.includes(i);
      (isMono ? mono : text)(slide, ctx, cell, cx + 12, top + 10, colWidths[i] - 24, rowH - 24, { size: isMono ? (opts.monoSize ?? 8.8) : (opts.bodySize ?? 10.8), color: i === 0 ? C.ink : '#333333', bold: i === 0 });
      cx += colWidths[i];
    });
  });
}

export function node(slide, ctx, x, y, w, h, label, sub, opts = {}) {
  card(slide, ctx, x, y, w, h, { fill: opts.fill ?? C.canvas, line: opts.line ?? C.hairline, round: true });
  mono(slide, ctx, label, x + 16, y + 18, w - 32, 14, { size: 10, color: opts.labelColor ?? C.body, bold: true });
  text(slide, ctx, sub, x + 16, y + 42, w - 32, h - 54, { size: opts.size ?? 16, color: opts.textColor ?? C.ink });
}

export function arrow(slide, ctx, x, y, w, label, dark=false) {
  ctx.addShape(slide, { left: x, top: y + 8, width: w, height: 2, fill: dark ? '#ffffff' : C.ink, line: ctx.line('#00000000', 0) });
  text(slide, ctx, '>', x + w - 8, y - 1, 18, 18, { size: 16, color: dark ? '#ffffff' : C.ink, bold: false });
  if (label) mono(slide, ctx, label, x, y + 26, w, 14, { size: 8.6, color: dark ? '#bdbbff' : C.body, align: 'center' });
}
