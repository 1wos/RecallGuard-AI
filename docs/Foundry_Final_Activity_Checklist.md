# Foundry Final Activity Checklist

This checklist maps the final activity requirements to RecallGuard AI and keeps the build evidence easy to review.

## Exact Required Deliverables

### 1. Video

- Format: `.mp4` or `.mov`
- Length: maximum 3 minutes
- Must show:
  - Quick demo of the workflow
  - How collaboration with AI felt
  - What was hardest
  - What improved after testing, traces, or guardrails

### 2. Document

- Format: PDF or Word
- Must include:
  - Chosen use case
  - Agent roles
  - Key instruction snippets
  - Knowledge base setup
  - Tools enabled
  - Test cases and outcomes
  - Trace screenshots if possible
  - Guardrails configuration
  - Entra Agent ID governance notes

## Exact Build Requirements

| Requirement | RecallGuard AI Evidence |
|---|---|
| Design a multi-agent system in Microsoft Foundry | Foundry project `recallguard-ai` |
| Knowledge Agent | `RecallGuard Knowledge Agent` |
| Grounded enterprise knowledge source | Product safety SOP/checklist/recall policy indexed via File Search or Azure AI Search |
| Public or enterprise evidence dataset | Korea Data Portal KATS domestic recall CSV downloaded and normalized under `data/` |
| Task Agent | `RecallGuard Task Agent` |
| Tool-enabled action | Code Interpreter checks vendor CSV files |
| Workflow orchestration | Sequential workflow in Microsoft Foundry |
| Route to Knowledge Agent first | First workflow node invokes Knowledge Agent |
| Invoke Task Agent when needed | Final demo workflow is scoped to evidence-check requests, so the second workflow node invokes the Task Agent after grounding; a production visual workflow can add an explicit condition for non-file Q&A |
| Guardrails | Model deployments use `Microsoft.DefaultV2` RAI policy; agents and workflow add untrusted-content, grounded-answer, deterministic-tool, and HITL safeguards |
| Traces | Live Responses API artifacts show `workflow_action`, `file_search_call`, and `code_interpreter_call`; portal Trace screenshots remain recommended visual evidence |
| Identity governance | Entra Agent ID / agent identity notes |

## Requirement Coverage Terms

Use these exact terms in the report and video narration:

- Microsoft Foundry
- Foundry Agent Service
- Knowledge Agent
- Task Agent
- Sequential workflow
- Guardrails
- Prompt injection protection
- Jailbreak protection
- Grounded knowledge
- Knowledge base
- File Search
- Azure AI Search
- Code Interpreter
- Tool calling
- Preview
- Traces
- Observability
- Entra ID
- Agent ID
- Agent identity
- RBAC
- Least privilege
- Human-in-the-loop
- Evidence-based decision
- Public data
- Korea Data Portal
- KATS
- Test cases
- Success case
- Failure case
- Edge case

## Recommended Report Structure

The final report should include one table titled:

`Final Activity Requirement Mapping`

Each row should include:

- Requirement
- What I built
- Evidence screenshot or note
- Status: Complete / Partial / Blocked

## Minimum Submission-Safe Evidence

- Screenshot 1: Foundry project overview showing `recallguard-ai`
- Screenshot 2: Knowledge Agent setup with knowledge source
- Screenshot 3: Task Agent setup with Code Interpreter
- Screenshot 4: Sequential workflow visualizer
- Screenshot 5: Preview successful run
- Screenshot 6: Trace for successful run
- Screenshot 7: Trace or output for missing-field/prompt-injection edge case
- Screenshot 8: Guardrails configuration
- Screenshot 9: Entra Agent ID / identity / RBAC note

## Current Azure CLI Status

- Resource group created: `rg-recallguard-foundry-je`
- Foundry resource created: `recallguard-somi-20260513`
- Foundry project created: `recallguard-ai`
- Models deployed: `gpt-4o-mini`, `gpt-4o-mini-100`
- Deployment RAI policy: `Microsoft.DefaultV2` on both model deployments
- Earlier failed attempts:
  - `eastus`: blocked by subscription region policy
  - `koreacentral`: blocked by subscription region policy
  - `gpt-4.1-mini Standard`: failed because Standard quota was 0
- Resolved by:
  - using `japaneast`
  - using `gpt-4o-mini` with `GlobalStandard`
