import { C, bg, header, footer, mono, headline, body, pill, gradientRibbon, table } from './shared.mjs';
export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx, C.dark); header(slide, ctx, { dark: true, kicker: 'SUBMISSION PACKAGE' });
  gradientRibbon(slide, ctx, 780, 112, 360, 210, { angle: -18 });
  mono(slide, ctx, 'READY-TO-SUBMIT FILES', 58, 98, 300, 18, { color: '#bdbbff', size: 11, bold: true });
  headline(slide, ctx, 'Submit the video and report; keep the PPT as the editable source.', 56, 130, 700, 92, { color: '#ffffff', size: 42 });
  body(slide, ctx, 'The report is ATS-friendly, the deck is recording-ready, and the MP4 can be regenerated from slide previews and narration.', 58, 230, 650, 48, { color: '#ffffff', size: 18 });
  table(slide, ctx, 62, 342, [330, 420, 230], 58, ['FILE', 'PURPOSE', 'STATUS'], [
    ['RecallGuard_AI_Demo_Somi.mp4', 'Required video deliverable', 'READY'],
    ['RecallGuard_AI_Build_Report_Somi.pdf', 'Required document deliverable', 'READY'],
    ['RecallGuard_AI_Foundry_Deck_Somi.pptx', 'Editable video/source deck', 'READY'],
    ['RecallGuard_AI_PPT_Video_Script_Somi.md', 'Narration and capture guide', 'READY'],
  ], { headerFill: C.darkSoft, monoCols: [2], bodySize: 10.4 });
  pill(slide, ctx, 'MICROSOFT FOUNDRY', 64, 638, 194, 28, { fill: '#ffffff', color: C.ink, size: 10 });
  pill(slide, ctx, 'GUARDRAILS', 272, 638, 128, 28, { fill: C.mint, color: C.ink, size: 10 });
  pill(slide, ctx, 'ENTRA AGENT ID', 414, 638, 164, 28, { fill: C.darkSoft, color: '#ffffff', border: C.darkLine, size: 10 });
  footer(slide, ctx, 10, { dark: true }); return slide;
}
