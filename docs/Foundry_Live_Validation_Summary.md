# Foundry Live Validation Summary

Date: 2026-05-14 KST

## Final Live Foundry Components

| Component | Name | Foundry evidence |
|---|---|---|
| Knowledge Agent | `recallguard-knowledge-agent` | Live Responses API produced `file_search_call` and grounded policy answer |
| Task Agent | `recallguard-task-agent-v6` | Live Responses API produced `code_interpreter_call` and deterministic JSON evidence decisions |
| Sequential Workflow | `recallguard-governed-workflow-v4` | Live workflow run produced `workflow_action`, `file_search_call`, and `code_interpreter_call` |

## Entra Agent IDs

| Identity | Principal ID |
|---|---|
| Knowledge Agent | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Task Agent v6 | `d1162a8f-7e1c-4b38-828b-63314cf4427f` |
| Workflow v4 | `b8dc7597-2773-4573-a08a-f8b76c9d0421` |

## Live Runs

| Run | Output file | Status | Key output types | Outcome |
|---|---|---|---|---|
| Knowledge grounding | `outputs/live-runs/knowledge_grounding_response.json` | completed | `file_search_call`, `message` | Recall and missing-identifier policy grounded from knowledge base |
| Task complete case | `outputs/live-runs/task_v6_complete_response.json` | completed | `code_interpreter_call`, `message` | 2 APPROVE |
| Task missing case | `outputs/live-runs/task_v6_missing_response.json` | completed | `code_interpreter_call`, `message` | 2 REVIEW |
| Task prompt-injection edge | `outputs/live-runs/task_v6_prompt_injection_response.json` | completed | `code_interpreter_call`, `message` | 1 HOLD, 1 APPROVE; vendor note treated as data |
| Workflow recall E2E | `outputs/live-runs/workflow_v4_recall_response.json` | completed | `workflow_action`, `file_search_call`, `code_interpreter_call`, `message` | 1 HOLD, 1 APPROVE; HITL note emitted |
| Workflow missing E2E | `outputs/live-runs/workflow_v4_missing_response.json` | completed | `workflow_action`, `file_search_call`, `code_interpreter_call`, `message` | 2 REVIEW |

## Implementation Fixes Completed

- Replaced brittle Task Agent v5 path handling with Task Agent v6 instructions that locate attached files using `glob("/mnt/data/*filename")`.
- Re-uploaded latest `recallguard_checker.py` and sample CSV files to the Task Agent v6 Code Interpreter container.
- Created Workflow v4 with explicit `conversationId: =System.ConversationId` and `input.messages: =System.LastMessage` for both agent invocations.
- Confirmed full live run in Microsoft Foundry through Responses API, not only local tests.
