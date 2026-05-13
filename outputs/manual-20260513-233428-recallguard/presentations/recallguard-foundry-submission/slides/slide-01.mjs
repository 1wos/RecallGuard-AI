import { C, bg, header, footer, mono, headline, body, pill, gradientRibbon, metricTile } from './shared.mjs';
export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx, C.dark); header(slide, ctx, { dark: true, kicker: 'FINAL ACTIVITY / MICROSOFT FOUNDRY' });
  gradientRibbon(slide, ctx, 710, 162, 430, 250);
  mono(slide, ctx, 'GOVERNED MULTI-AGENT WORKFLOW', 64, 138, 500, 20, { color: '#bdbbff', size: 11, bold: true });
  headline(slide, ctx, 'Product safety evidence checking, governed from prompt to identity.', 62, 178, 650, 178, { color: '#ffffff', size: 54 });
  body(slide, ctx, 'RecallGuard AI checks vendor product submissions against product safety policy, recall evidence, and KC certification records before marketplace listing.', 66, 384, 615, 70, { color: '#ffffff', size: 18 });
  pill(slide, ctx, 'KNOWLEDGE AGENT', 66, 496, 174, 40, { fill: C.mint, color: C.ink });
  pill(slide, ctx, 'TASK AGENT', 252, 496, 130, 40, { fill: '#ffffff', color: C.ink });
  pill(slide, ctx, 'TRACES + ENTRA ID', 394, 496, 190, 40, { fill: C.darkSoft, color: '#ffffff', border: C.darkLine });
  metricTile(slide, ctx, 784, 484, 132, 116, '2', 'AGENTS', C.mint);
  metricTile(slide, ctx, 928, 484, 132, 116, '4', 'TEST CASES', C.periwinkle);
  metricTile(slide, ctx, 1072, 484, 132, 116, '1', 'WORKFLOW', '#ffd6c2');
  footer(slide, ctx, 1, { dark: true });
  return slide;
}
