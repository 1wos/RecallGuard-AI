# Foundry Expert Audit

Date: 2026-05-14 KST

## Verdict

RecallGuard AI is genuinely built in Microsoft Foundry and is ready for the final activity submission. The core activity asks are implemented with live Foundry resources:

- Knowledge Agent: `recallguard-knowledge-agent`
- Task Agent: `recallguard-task-agent-v7-public-data`
- Workflow Agent: `recallguard-governed-workflow-v5-public-data`
- Project endpoint: `https://recallguard-somi-20260513.services.ai.azure.com/api/projects/recallguard-ai`
- Model deployments: `gpt-4o-mini`, `gpt-4o-mini-100`

The system is strong because it has real File Search, Code Interpreter, workflow orchestration, live Responses API evidence, Entra Agent IDs, and a real Korea Data Portal/KATS public dataset. The remaining risk is mostly evidence polish: named custom guardrail screenshots and portal Trace screenshots would make it harder for a human reviewer to question the governance layer.

## Build Alignment Review

| Activity area | Evidence | Assessment |
|---|---|---|
| Scenario and user journey | RecallGuard marketplace/procurement product safety review, documented in PRD/report | Complete |
| Knowledge Agent | `recallguard-knowledge-agent` is active and uses File Search | Complete |
| Grounded knowledge base | Vector store `vs_sGLsLTJ6kDvsG3UBBrZov44k` with policy/checklist files | Complete |
| Knowledge test questions | `outputs/live-runs/knowledge_grounding_response.json` includes `file_search_call` | Complete |
| Task Agent | `recallguard-task-agent-v7-public-data` is active | Complete |
| Tool-based action | Code Interpreter plus `recallguard_checker.py` parses CSV and applies deterministic evidence rules | Complete |
| Realistic tests | Complete, missing-field, prompt-injection, and public KATS recall cases captured under `outputs/live-runs/` | Complete |
| Sequential workflow | `recallguard-governed-workflow-v5-public-data` invokes Knowledge Agent first and Task Agent second | Complete for evidence-check workflow |
| Traces/observability | Live output types show `workflow_action`, `file_search_call`, and `code_interpreter_call` | Strong API evidence; portal screenshots recommended |
| Guardrails | `Microsoft.DefaultV2` RAI policy is assigned to both model deployments; agent instructions and checker script handle untrusted vendor content | Complete for MVP; custom named guardrail screenshot recommended |
| Identity governance | Agent principal IDs documented for Knowledge, Task, and Workflow agents | Complete |
| Required deliverables | PDF/DOCX report, MP4 demos, PPT deck, package zip under `final/` | Complete |

## Live Foundry Evidence Checked

### Agent identities

| Component | Principal ID |
|---|---|
| Knowledge Agent | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Task Agent | `0173cc3c-70e7-4bf7-bb74-39703a517ffb` |
| Workflow Agent | `87a0ae4f-49ce-485d-8909-0c2081017775` |

### Tool evidence

| Agent | Tool evidence |
|---|---|
| Knowledge Agent | `file_search` with vector store `vs_sGLsLTJ6kDvsG3UBBrZov44k` |
| Task Agent | `code_interpreter` with seven uploaded files |
| Workflow Agent | Workflow definition invokes Knowledge Agent, then Task Agent |

### Guardrail evidence

| Deployment | RAI policy |
|---|---|
| `gpt-4o-mini` | `Microsoft.DefaultV2` |
| `gpt-4o-mini-100` | `Microsoft.DefaultV2` |

The default policy is not the same as a visibly named custom guardrail. For the strongest final submission, capture the Guardrails page showing default/custom assignment, or create a named guardrail such as `RecallGuard-Compliance-Guardrail` and assign it to the final agents/model deployments.

## What a Microsoft Foundry Expert Would Improve

1. Add a named custom guardrail in the portal with prompt attack, indirect attack, harmful content, PII/protected material where available, and output safety controls. Capture the assignment screen.
2. Capture two portal Traces screenshots: one success path and one missing-field or prompt-injection edge path.
3. Add an explicit conditional branch in a visual workflow for non-file policy Q&A versus file evidence checks. The current workflow is correct for evidence-check demo prompts, but a conditional branch would look more mature.
4. Convert the HITL note into a native approval/queue step if the portal workflow supports it in the environment.
5. For production, replace CLI API-key automation with managed identity/RBAC-only automation.

## Submission Recommendation

Submit the current package if the deadline is close. If there is another 20-30 minutes, the highest-impact improvement is to add portal screenshots for:

- Agents list showing Knowledge/Task/Workflow agents
- Knowledge Agent File Search setup
- Task Agent Code Interpreter setup
- Workflow Preview/Trace
- Guardrails assignment
- Agent identity / Entra principal IDs

## References

- Microsoft Foundry Agent Service overview: https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- Microsoft Foundry guardrails setup: https://learn.microsoft.com/en-us/azure/foundry/guardrails/how-to-create-guardrails
- Microsoft Foundry guardrails overview: https://learn.microsoft.com/en-us/azure/foundry/guardrails/guardrails-overview
- Microsoft Foundry File Search tool: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search
- Microsoft Foundry Code Interpreter tool: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/code-interpreter
