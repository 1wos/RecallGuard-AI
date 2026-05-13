import { C, bg, header, footer, mono, headline, body, table, metricTile } from './shared.mjs';
export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'TEST CASES' });
  mono(slide, ctx, 'EVIDENCE MATRIX', 58, 82, 250, 18, { size: 11, bold: true });
  headline(slide, ctx, 'The demo covers the happy path, missing evidence, recall risk, and prompt injection.', 56, 112, 760, 108, { size: 38 });
  body(slide, ctx, 'These outcomes are intentionally submission-friendly: every result maps to a Foundry final-activity requirement.', 58, 236, 760, 42, { size: 17, color: '#555555' });
  metricTile(slide, ctx, 904, 130, 116, 110, '1', 'HOLD', C.red);
  metricTile(slide, ctx, 1032, 130, 116, 110, '2', 'REVIEW', C.caution);
  table(slide, ctx, 58, 310, [220, 300, 220, 300], 58, ['TEST', 'INPUT', 'OBSERVED OUTCOME', 'WHY IT MATTERS'], [
    ['Knowledge Q&A', 'Policy question', 'Grounded answer', 'Covers Knowledge Agent requirement'],
    ['Recall match', 'vendor_products_recall_match.csv', '1 HOLD / 1 APPROVE', 'Proves risk triage + HITL trigger'],
    ['Missing fields', 'vendor_products_missing_fields.csv', '2 REVIEW', 'Prevents unsafe approval'],
    ['Prompt injection edge', 'vendor_products_prompt_injection.csv', '1 HOLD / 1 APPROVE', 'Treats notes as untrusted data'],
  ], { bodySize: 10.5 });
  footer(slide, ctx, 7); return slide;
}
