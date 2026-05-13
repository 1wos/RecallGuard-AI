import { C, bg, header, footer, mono, headline, body, card, text } from './shared.mjs';
export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'PROBLEM SURFACE' });
  mono(slide, ctx, 'WHY GOVERNANCE MATTERS', 58, 96, 360, 16, { size: 11, bold: true });
  headline(slide, ctx, 'A vendor CSV can carry more risk than it looks.', 56, 124, 700, 104, { size: 41 });
  body(slide, ctx, 'The workflow has to catch product risk, missing evidence, and adversarial content without inventing a compliance answer.', 58, 236, 720, 50, { size: 17, color: '#555555' });
  const items = [
    ['01', 'Recalled product slips through', 'A recalled model or importer match must create HOLD and trigger human review.', C.red],
    ['02', 'Certification evidence is incomplete', 'Missing model, manufacturer, or KC number should become REVIEW, not APPROVE.', C.caution],
    ['03', 'Vendor note attempts instruction override', 'Uploaded files are untrusted data; notes must not change agent policy.', C.mint],
  ];
  items.forEach((it, i) => {
    const x = 58 + i * 392;
    card(slide, ctx, x, 340, 348, 206, { fill: it[3], line: C.hairline, round: true });
    mono(slide, ctx, it[0], x + 24, 362, 50, 18, { size: 13, color: C.ink, bold: true });
    text(slide, ctx, it[1], x + 24, 396, 290, 56, { size: 23, color: C.ink });
    body(slide, ctx, it[2], x + 24, 466, 286, 54, { size: 14.5, color: '#222222' });
  });
  footer(slide, ctx, 2); return slide;
}
