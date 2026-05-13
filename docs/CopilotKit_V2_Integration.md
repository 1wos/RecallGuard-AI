# CopilotKit V2 Integration Notes

RecallGuard AI should keep Microsoft Foundry as the governed agent backend. CopilotKit is useful as a user-facing agent UX layer, not as a replacement for the Foundry Knowledge Agent, Task Agent, Sequential Workflow, traces, guardrails, or Entra governance.

## Current Implementation

The local demo now includes a lightweight **Reviewer Copilot** panel that mirrors the intended CopilotKit experience:

- explains the selected `APPROVE`, `REVIEW`, or `HOLD` decision
- summarizes missing fields and evidence count
- drafts a concise reviewer memo
- explains the guardrail and human-review path
- keeps decision logic deterministic and auditable

This is intentionally local and deterministic so the demo stays runnable without API keys or a React build pipeline.

## Target Product Architecture

| Layer | Responsibility |
|---|---|
| Microsoft Foundry Knowledge Agent | Ground policy and recall-response answers in indexed knowledge files |
| Microsoft Foundry Task Agent | Run `recallguard_checker.py` with Code Interpreter against vendor CSV input |
| Microsoft Foundry Sequential Workflow | Route reviewer requests from Knowledge Agent to Task Agent and preserve traces |
| RecallGuard API | Expose stable endpoints such as `/api/classify`, `/api/evaluation`, and reviewer-packet retrieval |
| CopilotKit frontend | Provide in-app chat, generative UI, shared state, and human-in-the-loop controls |

## Suggested CopilotKit Mapping

| RecallGuard UX | CopilotKit Concept |
|---|---|
| Current CSV text and selected product | Shared readable application state |
| `Run review` | Frontend action or backend tool call |
| `Inspect packet` | Generative UI card or structured tool result |
| `Reviewer memo` | Copilot action that drafts a human-review packet summary |
| HOLD/REVIEW approval path | Human-in-the-loop action requiring reviewer confirmation |
| Foundry trace ID and guardrail status | Persistent thread metadata shown inside the copilot panel |

## Implementation Plan

1. Keep the current Python checker and Foundry workflow unchanged as the source of truth.
2. Add a React or Next.js frontend only when the product needs live assistant UX.
3. Wrap the app with CopilotKit frontend components.
4. Connect CopilotKit actions to RecallGuard API endpoints.
5. Pass selected product, decision summary, reviewer packet, and guardrail status into the copilot as shared state.
6. Add approval actions for `HOLD` and `REVIEW` that require explicit reviewer confirmation before any downstream action.

## Why This Is V2

The final activity is graded primarily on Foundry agents, tool use, workflow orchestration, traces, guardrails, and Entra governance. Adding CopilotKit too early can distract from those requirements. The right sequencing is:

1. prove the governed Foundry workflow
2. prove deterministic classification and reviewer packets
3. polish the local reviewer workspace
4. add CopilotKit as a product-grade agent UX layer

