import { C, bg, header, footer, mono, headline, body, card, text, arrow } from './shared.mjs';
export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'VIDEO STORYBOARD' });
  mono(slide, ctx, '3-MINUTE DEMO SCRIPT', 58, 82, 280, 18, { size: 11, bold: true });
  headline(slide, ctx, 'The recording should prove Foundry usage before it explains the idea.', 56, 112, 860, 92, { size: 40 });
  body(slide, ctx, 'Use this slide as the video run-of-show. Replace the placeholder segments with actual portal Preview, Trace, Guardrails, and Agent ID screens.', 58, 206, 790, 48, { size: 18, color: '#555555' });
  const steps = [
    ['0:00', 'Project', 'Show recallguard-ai project and scenario'],
    ['0:25', 'Agents', 'Show Knowledge Agent and Task Agent v5'],
    ['0:55', 'Workflow', 'Show sequential workflow Preview'],
    ['1:40', 'Tests', 'Show recall + missing + edge outcomes'],
    ['2:25', 'Traces', 'Show Trace and guardrail configuration'],
    ['2:50', 'Reflection', 'What improved after testing'],
  ];
  steps.forEach((s, i) => {
    const x = 60 + (i % 3) * 382; const y = 320 + Math.floor(i / 3) * 144;
    card(slide, ctx, x, y, 330, 104, { fill: i === 2 ? C.mint : C.canvas, line: C.hairline, round: true });
    mono(slide, ctx, s[0], x + 18, y + 18, 80, 16, { size: 11, color: C.ink, bold: true });
    text(slide, ctx, s[1], x + 105, y + 14, 190, 26, { size: 23, color: C.ink });
    body(slide, ctx, s[2], x + 18, y + 52, 280, 35, { size: 14, color: '#555555' });
    if (i < 5 && i % 3 !== 2) arrow(slide, ctx, x + 334, y + 38, 34, '', false);
  });
  footer(slide, ctx, 9); return slide;
}
