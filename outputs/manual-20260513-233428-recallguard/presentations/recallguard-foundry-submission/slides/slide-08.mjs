import { C, bg, header, footer, mono, headline, body, table, card, text } from './shared.mjs';
export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx, C.dark); header(slide, ctx, { dark: true, kicker: 'GOVERNANCE' });
  mono(slide, ctx, 'GUARDRAILS + IDENTITY', 58, 84, 300, 18, { color: '#bdbbff', size: 11, bold: true });
  headline(slide, ctx, 'The workflow is governed at the prompt, tool, trace, and identity layers.', 56, 116, 840, 92, { color: '#ffffff', size: 40 });
  body(slide, ctx, 'Foundry guardrails cover prompt injection and safety. Agent instructions and deterministic code add application-level controls.', 58, 214, 760, 46, { color: '#ffffff', size: 17 });
  table(slide, ctx, 60, 304, [235, 360, 355], 58, ['CONTROL', 'IMPLEMENTATION', 'EVIDENCE'], [
    ['Prompt injection', 'Vendor notes treated only as data', 'Edge case output saved'],
    ['Ungrounded answers', 'Knowledge Agent cites connected sources', 'File Search/vector store'],
    ['Unsafe approval', 'Missing identifiers => REVIEW', 'Checker policy'],
    ['Identity governance', 'Agent principal IDs documented', 'Entra Agent ID notes'],
  ], { headerFill: C.darkSoft, bodySize: 10.4 });
  card(slide, ctx, 1000, 304, 184, 226, { fill: C.darkSoft, line: C.darkLine, round: true });
  mono(slide, ctx, 'KEY IDS', 1020, 328, 80, 14, { color: '#bdbbff', size: 10, bold: true });
  text(slide, ctx, 'Knowledge\n934a3b63...\n\nTask v5\n0883e31b...\n\nWorkflow\n10ac3c72...', 1020, 362, 144, 140, { color: '#ffffff', size: 14 });
  footer(slide, ctx, 8, { dark: true }); return slide;
}
