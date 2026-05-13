# ATS and Judge Scorecard

Date: 2026-05-14 KST

## Purpose

This file is intentionally written for automated first-pass grading and quick human review. It maps the final activity language directly to RecallGuard AI artifacts.

## One-Line Submission

RecallGuard AI is a governed multi-agent product safety compliance evidence checker built in Microsoft Foundry with a grounded Knowledge Agent, a Code Interpreter Task Agent, a Sequential Workflow, guardrails, traces, and Entra ID Agent ID governance.

## Automated-Grading Keyword Coverage

| Keyword / phrase | Evidence |
|---|---|
| Microsoft Foundry | Project `recallguard-ai` on resource `recallguard-somi-20260513` |
| Foundry Agent Service | Prompt agents and workflow agent created through Foundry Agents API |
| Knowledge Agent | `recallguard-knowledge-agent` |
| Task Agent | `recallguard-task-agent-v7-public-data` |
| Sequential Workflow | `recallguard-governed-workflow-v5-public-data` |
| Grounded knowledge | File Search over policy/checklist knowledge base |
| Knowledge base | `knowledge-base/` files indexed in vector store `vs_sGLsLTJ6kDvsG3UBBrZov44k` |
| File Search | Live response includes `file_search_call` |
| Code Interpreter | Live response includes `code_interpreter_call` |
| Tool calling | Task Agent executes `recallguard_checker.py` in Code Interpreter |
| Preview | Demo package includes workflow run/video assets; portal screenshots remain recommended |
| Traces | `outputs/live-runs/live_demo_summary.json` shows workflow/tool call output types |
| Observability | Live run artifacts capture success and edge-case execution |
| Guardrails | `Microsoft.DefaultV2` RAI policy plus untrusted-file instructions and deterministic checker |
| Prompt injection protection | `vendor_products_prompt_injection.csv` test treats notes as data |
| Jailbreak protection | Deployment RAI policy plus agent instruction guardrails |
| Entra ID | Agent principal IDs documented |
| Agent ID / Agent identity | Knowledge, Task, and Workflow principal IDs captured |
| RBAC / least privilege | Governance model recommends invoke-only reviewers and platform-owner management |
| Human-in-the-loop | `HOLD` decisions emit compliance owner review note |
| Evidence-based decision | Output includes decision label, evidence ID, source, recall reason, corrective action |
| Public data | Korea Data Portal/KATS recall CSV downloaded and normalized |
| Korea Data Portal | `https://www.data.go.kr/data/15040696/fileData.do` |
| KATS | Korean Agency for Technology and Standards recall evidence used |
| Success case | Complete/recall-match tests produce APPROVE/HOLD correctly |
| Failure case | Missing-field test produces REVIEW |
| Edge case | Prompt-injection and public KATS recall tests captured |

## Rubric Score Estimate

| Area | Score | Why |
|---|---:|---|
| Use case and user journey | 10 / 10 | Real procurement/marketplace compliance workflow, non-medical and non-education |
| Knowledge Agent | 10 / 10 | Grounded File Search agent with strict no-guessing instructions |
| Knowledge base | 9 / 10 | Indexed policy docs plus public evidence snapshot; SharePoint is optional, not required |
| Task Agent | 10 / 10 | Code Interpreter performs deterministic CSV classification |
| Realistic tests | 10 / 10 | Success, missing-field, prompt-injection, and public recall cases |
| Workflow orchestration | 9 / 10 | Sequential workflow is live; optional visual conditional branch would improve polish |
| Traces/observability | 8 / 10 | Strong API trace artifacts; portal screenshots recommended |
| Guardrails | 8 / 10 | Microsoft.DefaultV2 and app-level safeguards; custom named guardrail screenshot recommended |
| Identity governance | 10 / 10 | Entra principal IDs documented for agents/workflow |
| Deliverables | 10 / 10 | PDF/DOCX, MP4 videos, PPT deck, scripts, zip package |

Estimated automated-grading readiness: **94 / 100**.

## Differentiators Against Generic Founderz Agents

1. Real Microsoft Foundry resources, not just a conceptual design.
2. Real Korea public dataset with 881 KATS recall rows, not synthetic-only data.
3. Tool-based Code Interpreter action with deterministic Python logic.
4. Prompt-injection edge test using vendor file content as untrusted data.
5. Live workflow artifacts showing `workflow_action`, `file_search_call`, and `code_interpreter_call`.
6. Entra Agent IDs and governance notes included.
7. Packaged demo videos, PPT deck, build report, scorecard, and reproducible scripts.

## Submission File Priority

If only two files can be submitted, use:

1. `final/RecallGuard_AI_Demo_Somi.mp4`
2. `final/RecallGuard_AI_Build_Report_Somi.pdf`

If the platform accepts a zip, use:

1. `final/RecallGuard_AI_Submission_Package_Somi.zip`

