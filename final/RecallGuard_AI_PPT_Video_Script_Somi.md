# RecallGuard AI PPT Demo Script

Target length: about 2 minutes 20 seconds. Required deliverables remain the MP4 video and PDF/DOCX build report; this PPT is the editable recording source.

## Slide 1 — Title

This is RecallGuard AI, a governed multi-agent compliance evidence checker built in Microsoft Foundry. The goal is simple: ground policy answers first, run file checks second, and preserve governance through traces, guardrails, and Entra Agent IDs.

## Slide 2 — Problem Surface

The scenario is vendor product safety review. A CSV can hide three risks: a recalled product, missing certification evidence, or a vendor note that tries to override instructions. A good system should never invent a compliance answer.

## Slide 3 — Requirement Map

I mapped each final-activity requirement to a concrete artifact: a Knowledge Agent, a Task Agent, a sequential workflow, trace evidence, guardrail configuration, and identity governance notes.

## Slide 4 — Workflow

The workflow is intentionally sequential. The user asks or uploads a file, the Knowledge Agent grounds the applicable policy, then the Task Agent runs a deterministic evidence check when action is required. HOLD decisions go to human review.

## Slide 5 — Knowledge Agent

The Knowledge Agent uses File Search over four policy documents: product safety SOP, KC certification checklist, recall response policy, and vendor submission requirements. Its instruction is strict: cite grounded evidence, list missing information, and say when the knowledge base is insufficient.

## Slide 6 — Task Agent

The Task Agent uses Code Interpreter and a deterministic Python checker. Testing exposed an early false HOLD, so I tightened the rule: only recall evidence can create HOLD. Certification evidence can support APPROVE or REVIEW, but not HOLD by itself.

## Slide 7 — Tests

The demo covers four cases: grounded Q&A, a recall match, missing fields, and prompt injection inside vendor notes. The expected output is clear and actionable: APPROVE, REVIEW, or HOLD with evidence IDs and recommended actions.

## Slide 8 — Governance

Governance sits across every layer. Prompt-injection content is treated only as data, missing identifiers force REVIEW, Foundry traces show the run path, and Entra Agent IDs document ownership and access management.

## Slide 9 — Recording Plan

For the final recording, I show Foundry first: the project, agents, workflow preview, test runs, traces, guardrails, and Agent ID screens. Then I briefly reflect on what improved after testing.

## Slide 10 — Submission Package

The final package includes the MP4 demo, the build report as PDF and DOCX, this editable PPT source, and the narration script. The report is written to be clear for both a human reviewer and an agent-based first pass.
