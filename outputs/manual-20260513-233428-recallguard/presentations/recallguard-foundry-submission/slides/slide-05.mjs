import { C, bg, header, footer, mono, headline, body, card, text, table } from './shared.mjs';
export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'KNOWLEDGE AGENT' });
  mono(slide, ctx, 'GROUNDED Q&A', 58, 82, 240, 18, { size: 11, bold: true });
  headline(slide, ctx, 'The policy answer is allowed to say “I do not know.”', 56, 112, 670, 104, { size: 39 });
  body(slide, ctx, 'The Knowledge Agent uses indexed policy files and must cite evidence or surface missing information instead of guessing.', 58, 226, 660, 50, { size: 17, color: '#555555' });
  card(slide, ctx, 760, 92, 370, 184, { fill: C.hairline, line: C.hairline, round: true });
  mono(slide, ctx, 'INSTRUCTION SNIPPET', 786, 116, 220, 16, { size: 10.5, color: C.ink, bold: true });
  text(slide, ctx, 'Answer only using connected knowledge sources. Do not guess. List evidence, missing information, and next compliance action.', 786, 148, 310, 88, { size: 17, color: C.ink });
  table(slide, ctx, 58, 340, [310, 640], 54, ['KNOWLEDGE SOURCE', 'ROLE IN ANSWERING'], [
    ['product_safety_review_sop.md', 'Decision labels and conservative approval rule'],
    ['kc_certification_review_checklist.md', 'Required vendor fields and evidence strength'],
    ['recall_response_policy.md', 'Recall match handling and human review rule'],
    ['vendor_submission_requirements.md', 'Untrusted content and required submission fields'],
  ], { bodySize: 10.5 });
  footer(slide, ctx, 5); return slide;
}
