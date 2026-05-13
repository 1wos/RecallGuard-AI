# RecallGuard AI Build Report Draft

## Use Case

RecallGuard AI is a governed multi-agent product safety compliance checker for marketplace and procurement teams. It reviews vendor-submitted product files against grounded product safety policies and public recall/certification evidence.

## Agent Roles

| Agent | Role | Tooling |
|---|---|---|
| `recallguard-knowledge-agent` | Answers grounded product safety policy questions | File Search with indexed policy/checklist documents |
| `recallguard-task-agent-v7-public-data` | Checks vendor CSV files and classifies products | Code Interpreter with `recallguard_checker.py` |

## Knowledge Base Setup

Knowledge source files:

- `product_safety_review_sop.md`
- `kc_certification_review_checklist.md`
- `recall_response_policy.md`
- `vendor_submission_requirements.md`

These were uploaded into the Foundry project and indexed through vector store `vs_sGLsLTJ6kDvsG3UBBrZov44k`.

## Public Dataset Setup

RecallGuard uses Korea Data Portal public recall evidence:

- Dataset: `산업통상부_국가기술표준원_제품안전_국내리콜정보`
- Detail page: https://www.data.go.kr/data/15040696/fileData.do
- Provider: Ministry of Trade, Industry and Energy / Korean Agency for Technology and Standards
- Original file: `data/raw/kats_product_safety_domestic_recall_20230809.csv`
- Normalized evidence: `data/processed/kats_domestic_recall_normalized.csv`
- Rows downloaded and normalized: 881
- Foundry demo snapshot: first 30 public recall rows appended to `sample-data/recall_certification_snapshot.csv`

## Tools Enabled

- Knowledge Agent: File Search
- Task Agent: Code Interpreter
- Task Agent deterministic script: `recallguard_checker.py`

## Test Cases and Outcomes

| Test | Input | Outcome |
|---|---|---|
| Knowledge policy Q&A | Recall/certification policy question | Grounded answer with evidence references |
| Recall match | `vendor_products_recall_match.csv` | 1 `HOLD`, 1 `APPROVE` |
| Public KATS recall match | `vendor_products_public_recall_match.csv` | 1 `HOLD`, 1 `APPROVE`; HOLD cites `KATS-RECALL-0001` |
| Missing fields | `vendor_products_missing_fields.csv` | 2 `REVIEW` |
| Prompt-injection edge case | `vendor_products_prompt_injection.csv` | Notes treated as data; 1 `HOLD`, 1 `APPROVE`; no instruction leakage |

## Guardrails Configuration

Foundry deployment-level evidence:

- `gpt-4o-mini`: `raiPolicyName = Microsoft.DefaultV2`
- `gpt-4o-mini-100`: `raiPolicyName = Microsoft.DefaultV2`

RecallGuard also configures application-level safeguards for:

- Prompt injection protection
- Jailbreak protection
- Ungrounded compliance claims
- Secret/system prompt leakage
- Unsafe automatic approval

The Task Agent includes a deterministic guardrail: uploaded files are treated as untrusted data, and final classification is based on Code Interpreter output from `recallguard_checker.py`, not model-only judgment. For the strongest portal evidence, assign a named custom Foundry guardrail to the final agents/workflow and capture that screen.

## Entra Agent ID Governance Notes

| Identity | ID |
|---|---|
| Foundry project principal | `9945404e-cea4-4b17-80f4-5e064713737d` |
| Knowledge Agent principal | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Final Task Agent principal | `0173cc3c-70e7-4bf7-bb74-39703a517ffb` |
| Workflow public-data principal | `87a0ae4f-49ce-485d-8909-0c2081017775` |

Governance model:

- Compliance team gets workflow invoke access.
- AI platform owner manages agent configuration.
- Knowledge source access is read-only.
- Task Agent cannot approve production listings directly.
- `HOLD` decisions require human-in-the-loop compliance approval.

## Trace Evidence Captured / To Capture In Foundry Portal

- Live workflow response: Knowledge Agent then Task Agent, with `workflow_action`, `file_search_call`, and `code_interpreter_call`.
- Recall match trace: `HOLD` branch triggered.
- Missing fields trace: `REVIEW` output.
- Prompt-injection edge trace: file note treated as data.
- Public KATS recall trace: `KATS-RECALL-0001` creates `HOLD` from data.go.kr evidence.
- Guardrail configuration screen: recommended extra screenshot, with `Microsoft.DefaultV2` already confirmed at deployment level.
- Agent identity / Entra Agent ID screen.
