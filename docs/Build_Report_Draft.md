# RecallGuard AI Build Report Draft

## Use Case

RecallGuard AI is a governed multi-agent product safety compliance checker for marketplace and procurement teams. It reviews vendor-submitted product files against grounded product safety policies and public recall/certification evidence.

## Agent Roles

| Agent | Role | Tooling |
|---|---|---|
| `recallguard-knowledge-agent` | Answers grounded product safety policy questions | File Search with indexed policy/checklist documents |
| `recallguard-task-agent-v5` | Checks vendor CSV files and classifies products | Code Interpreter with `recallguard_checker.py` |

## Knowledge Base Setup

Knowledge source files:

- `product_safety_review_sop.md`
- `kc_certification_review_checklist.md`
- `recall_response_policy.md`
- `vendor_submission_requirements.md`

These were uploaded into the Foundry project and indexed through vector store `vs_sGLsLTJ6kDvsG3UBBrZov44k`.

## Tools Enabled

- Knowledge Agent: File Search
- Task Agent: Code Interpreter
- Task Agent deterministic script: `recallguard_checker.py`

## Test Cases and Outcomes

| Test | Input | Outcome |
|---|---|---|
| Knowledge policy Q&A | Recall/certification policy question | Grounded answer with evidence references |
| Recall match | `vendor_products_recall_match.csv` | 1 `HOLD`, 1 `APPROVE` |
| Missing fields | `vendor_products_missing_fields.csv` | 2 `REVIEW` |
| Prompt-injection edge case | `vendor_products_prompt_injection.csv` | Notes treated as data; 1 `HOLD`, 1 `APPROVE`; no instruction leakage |

## Guardrails Configuration

The workflow should configure guardrails for:

- Prompt injection protection
- Jailbreak protection
- Ungrounded compliance claims
- Secret/system prompt leakage
- Unsafe automatic approval

The Task Agent also includes an application-level guardrail: uploaded files are treated as untrusted data, and final classification is based on deterministic Code Interpreter output.

## Entra Agent ID Governance Notes

| Identity | ID |
|---|---|
| Foundry project principal | `9945404e-cea4-4b17-80f4-5e064713737d` |
| Knowledge Agent principal | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Final Task Agent principal | `0883e31b-d2aa-416f-9a5b-01638e011aaf` |
| Workflow v2 principal | `10ac3c72-43e8-4872-8859-0f0d06f55550` |

Governance model:

- Compliance team gets workflow invoke access.
- AI platform owner manages agent configuration.
- Knowledge source access is read-only.
- Task Agent cannot approve production listings directly.
- `HOLD` decisions require human-in-the-loop compliance approval.

## Trace Evidence To Capture In Foundry Portal

- Successful workflow Preview: Knowledge Agent then Task Agent.
- Recall match trace: `HOLD` branch triggered.
- Missing fields trace: `REVIEW` output.
- Prompt-injection edge trace: file note treated as data.
- Guardrail configuration screen.
- Agent identity / Entra Agent ID screen.
