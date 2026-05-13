# RecallGuard AI Portfolio Product Strategy

RecallGuard AI should be evaluated as an agent product, not only as an assignment artifact. The core story is: **governed agents can support high-stakes compliance review when the workflow is grounded, deterministic where needed, auditable, and designed around human review.**

## Positioning

RecallGuard AI is a compliance evidence checker for marketplaces and procurement teams that need to prevent unsafe or recalled products from being listed, purchased, or approved.

The portfolio angle is strongest when the project is presented as a product case study:

- real user: compliance reviewer, marketplace operations analyst, procurement risk reviewer
- real pain: vendor submissions are incomplete, inconsistent, and hard to compare with recall/certification evidence
- agent value: agents reduce review time while preserving human accountability
- governance value: decisions are traceable, bounded, and reviewable

## Differentiation

Many agent demos stop at conversational Q&A. RecallGuard AI shows a more mature pattern:

| Capability | Why It Matters |
|---|---|
| Grounded Knowledge Agent | Prevents unsupported policy answers |
| Tool-using Task Agent | Performs concrete CSV evidence checks instead of guessing |
| Deterministic decision rules | Makes outcomes reproducible and auditable |
| Reviewer packet | Turns agent output into an operational compliance artifact |
| Evaluation harness | Shows how decision quality can be measured |
| Guardrails and HITL | Keeps risky actions under human control |
| Entra governance notes | Connects agent identity to ownership and access management |
| CopilotKit-ready UX | Shows a path from backend workflow to product-grade user experience |

## Portfolio Narrative

Use this short narrative in interviews or project summaries:

> I built RecallGuard AI to explore how governed multi-agent systems can support real compliance operations. The system uses Microsoft Foundry to separate grounded policy retrieval from deterministic task execution, then orchestrates both through a traceable workflow with guardrails and human-review escalation. I also built a local reviewer workspace so the workflow can be tested like a product: reviewers can upload vendor CSVs, inspect APPROVE/REVIEW/HOLD decisions, open reviewer packets, and use a copilot-style panel to understand the decision rationale.

## Roadmap to Production Quality

1. Replace local demo persistence with a small database for review sessions and audit history.
2. Add a React/Next.js frontend and integrate CopilotKit for in-app assistant UX.
3. Connect the Reviewer Copilot to Foundry workflow responses and trace IDs.
4. Expand the labeled evaluation harness from 25 rows to 100+ rows with borderline recall/certification cases.
5. Add reviewer feedback capture for false approvals, false holds, and missing evidence.
6. Add role-based views for reviewer, compliance owner, and admin.
7. Add CI that runs unit tests, decision-harness evaluation, and documentation link checks.
8. Add deployment notes for Azure Container Apps or App Service.

## What To Avoid

- Do not frame the project as only a class assignment.
- Do not overclaim that the local demo is the live Foundry portal.
- Do not present CopilotKit as the core agent backend; it is the future product UX layer.
- Do not hide deterministic logic behind agent language. The auditability is the strength.

