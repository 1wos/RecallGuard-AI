import { C, bg, header, footer, mono, headline, body, card, text, arrow } from './shared.mjs';
export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'TASK AGENT HARDENING' });
  mono(slide, ctx, 'TOOL EXECUTION', 58, 80, 260, 18, { size: 11, bold: true });
  headline(slide, ctx, 'A false HOLD became the reason to stop trusting free-form classification.', 56, 110, 800, 108, { size: 39 });
  body(slide, ctx, 'The final Task Agent uses Code Interpreter plus recallguard_checker.py so row-level decisions are deterministic and evidence_type-aware.', 58, 226, 760, 50, { size: 17, color: '#555555' });
  card(slide, ctx, 66, 346, 286, 154, { fill: C.red, line: C.hairline, round: true });
  mono(slide, ctx, 'EARLY FAILURE', 88, 370, 180, 16, { color: C.ink, size: 10.5, bold: true });
  text(slide, ctx, 'Certification evidence was incorrectly treated as HOLD.', 88, 404, 230, 58, { size: 22, color: C.ink });
  arrow(slide, ctx, 376, 406, 92, 'TRACE', false);
  card(slide, ctx, 496, 346, 286, 154, { fill: C.caution, line: C.hairline, round: true });
  mono(slide, ctx, 'FIX', 518, 370, 120, 16, { color: C.ink, size: 10.5, bold: true });
  text(slide, ctx, 'Only evidence_type == recall can create HOLD.', 518, 404, 230, 58, { size: 22, color: C.ink });
  arrow(slide, ctx, 806, 406, 92, 'CODE', false);
  card(slide, ctx, 926, 346, 286, 154, { fill: C.mint, line: C.hairline, round: true });
  mono(slide, ctx, 'FINAL AGENT', 948, 370, 160, 16, { color: C.ink, size: 10.5, bold: true });
  text(slide, ctx, 'Task Agent v5 runs deterministic Python.', 948, 404, 230, 58, { size: 22, color: C.ink });
  footer(slide, ctx, 6); return slide;
}
