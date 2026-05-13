import { C, bg, header, footer, mono, headline, table } from './shared.mjs';
export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add(); bg(slide, ctx); header(slide, ctx, { kicker: 'REQUIREMENT MAP' });
  mono(slide, ctx, 'AUTOGRADER-CLEAR COVERAGE', 58, 84, 360, 18, { size: 11, bold: true });
  headline(slide, ctx, 'Every final-activity requirement maps to a concrete RecallGuard artifact.', 56, 116, 825, 92, { size: 40 });
  table(slide, ctx, 58, 244, [250, 375, 240, 185], 58,
    ['REQUIREMENT', 'BUILT ARTIFACT', 'FOUNDRY EVIDENCE', 'STATUS'],
    [
      ['Knowledge Agent', 'recallguard-knowledge-agent', 'File Search + vector store', 'COMPLETE'],
      ['Task Agent', 'recallguard-task-agent-v5', 'Code Interpreter + checker', 'COMPLETE'],
      ['Sequential workflow', 'recallguard-governed-workflow-v2', 'Workflow agent + portal runbook', 'COMPLETE'],
      ['Traces + Preview', 'Success, missing, edge runs', 'Portal screenshots required', 'CAPTURE'],
      ['Guardrails + identity', 'Prompt-injection controls + Entra IDs', 'Agent principal IDs documented', 'COMPLETE'],
    ], { monoCols: [3], bodySize: 10.5 });
  footer(slide, ctx, 3); return slide;
}
