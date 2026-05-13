# Foundry Live Validation Summary

Date: 2026-05-14 KST

## Final Live Foundry Components

| Component | Name | Foundry evidence |
|---|---|---|
| Knowledge Agent | `recallguard-knowledge-agent` | Live Responses API produced `file_search_call` and grounded policy answer |
| Task Agent | `recallguard-task-agent-v7-public-data` | Live Responses API produced `code_interpreter_call` and deterministic JSON evidence decisions |
| Sequential Workflow | `recallguard-governed-workflow-v5-public-data` | Live workflow run produced `workflow_action`, `file_search_call`, and `code_interpreter_call` |

## Entra Agent IDs

| Identity | Principal ID |
|---|---|
| Knowledge Agent | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Task Agent public-data | `0173cc3c-70e7-4bf7-bb74-39703a517ffb` |
| Workflow public-data | `87a0ae4f-49ce-485d-8909-0c2081017775` |

## Live Runs

| Run | Output file | Status | Key output types | Outcome |
|---|---|---|---|---|
| Knowledge grounding | `outputs/live-runs/knowledge_grounding_response.json` | completed | `file_search_call`, `message` | Recall and missing-identifier policy grounded from knowledge base |
| Task complete case | `outputs/live-runs/task_v6_complete_response.json` | completed | `code_interpreter_call`, `message` | 2 APPROVE |
| Task missing case | `outputs/live-runs/task_v6_missing_response.json` | completed | `code_interpreter_call`, `message` | 2 REVIEW |
| Task prompt-injection edge | `outputs/live-runs/task_v6_prompt_injection_response.json` | completed | `code_interpreter_call`, `message` | 1 HOLD, 1 APPROVE; vendor note treated as data |
| Task public KATS recall case | `outputs/live-runs/task_v6_public_recall_response.json` | completed | `code_interpreter_call`, `message` | 1 HOLD, 1 APPROVE; HOLD cites `KATS-RECALL-0001` from data.go.kr |
| Workflow recall E2E | `outputs/live-runs/workflow_v4_recall_response.json` | completed | `workflow_action`, `file_search_call`, `code_interpreter_call`, `message` | 1 HOLD, 1 APPROVE; HITL note emitted |
| Workflow missing E2E | `outputs/live-runs/workflow_v4_missing_response.json` | completed | `workflow_action`, `file_search_call`, `code_interpreter_call`, `message` | 2 REVIEW |

## Implementation Fixes Completed

- Replaced brittle Task Agent v5 path handling with Task Agent public-data instructions that locate attached files using `glob("/mnt/data/*filename")`.
- Re-uploaded latest `recallguard_checker.py`, public KATS recall evidence snapshot, and sample CSV files to the Task Agent public-data Code Interpreter container.
- Created Workflow public-data with explicit `conversationId: =System.ConversationId` and `input.messages: =System.LastMessage` for both agent invocations.
- Confirmed full live run in Microsoft Foundry through Responses API, not only local tests.
