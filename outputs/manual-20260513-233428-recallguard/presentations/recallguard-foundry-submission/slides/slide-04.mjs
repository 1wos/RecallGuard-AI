import { C, bg, header, footer, mono, headline, body, node, arrow, card, text } from './shared.mjs';
export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx, C.dark); header(slide, ctx, { dark: true, kicker: 'SEQUENTIAL WORKFLOW' });
  mono(slide, ctx, 'ORCHESTRATION', 58, 90, 280, 18, { color: '#bdbbff', size: 11, bold: true });
  headline(slide, ctx, 'Ground first. Act second. Escalate when risk is real.', 56, 122, 720, 92, { color: '#ffffff', size: 42 });
  body(slide, ctx, 'The workflow intentionally separates policy grounding from file execution, then preserves a human gate for HOLD decisions.', 58, 218, 700, 46, { color: '#ffffff', size: 17 });
  node(slide, ctx, 64, 338, 172, 110, 'USER', 'Compliance associate uploads vendor CSV', { fill: C.darkSoft, line: C.darkLine, labelColor: '#bdbbff', textColor: '#ffffff', size: 15 });
  arrow(slide, ctx, 246, 383, 82, 'ASK', true);
  node(slide, ctx, 346, 338, 192, 110, 'KNOWLEDGE AGENT', 'Ground policy with File Search', { fill: C.darkSoft, line: C.darkLine, labelColor: '#bdbbff', textColor: '#ffffff', size: 15 });
  arrow(slide, ctx, 548, 383, 82, 'CRITERIA', true);
  node(slide, ctx, 648, 338, 192, 110, 'TASK AGENT', 'Run Code Interpreter checker', { fill: C.darkSoft, line: C.darkLine, labelColor: '#bdbbff', textColor: '#ffffff', size: 15 });
  arrow(slide, ctx, 850, 383, 82, 'DECIDE', true);
  node(slide, ctx, 950, 338, 192, 110, 'HITL', 'HOLD requires compliance review', { fill: C.darkSoft, line: C.darkLine, labelColor: '#bdbbff', textColor: '#ffffff', size: 15 });
  card(slide, ctx, 64, 512, 1078, 56, { fill: '#00000000', line: C.darkLine });
  mono(slide, ctx, 'OBSERVABILITY RAIL', 86, 530, 180, 14, { color: '#bdbbff', size: 10, bold: true });
  text(slide, ctx, 'Preview + Traces + Guardrails + Entra Agent ID governance sit across the full workflow.', 270, 524, 780, 28, { color: '#ffffff', size: 19 });
  footer(slide, ctx, 4, { dark: true }); return slide;
}
