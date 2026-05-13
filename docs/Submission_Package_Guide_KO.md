# RecallGuard AI 제출 패키지 가이드

## 최종 제출물

제출물은 보통 아래 2개로 준비하면 가장 안전합니다.

| 제출물 | 형식 | 권장 파일명 |
|---|---|---|
| 데모 영상 | `.mp4` 또는 `.mov`, 최대 3분 | `RecallGuard_AI_Demo_Somi.mp4` |
| 빌드 리포트 | `.pdf` 또는 `.docx` | `RecallGuard_AI_Build_Report_Somi.pdf` |

추가로 플랫폼이 여러 파일 업로드를 허용하면 아래 파일도 첨부 후보입니다.

- `RecallGuard_AI_PRD.pdf`
- `Azure_CLI_Setup_Evidence.pdf`
- `Foundry_Portal_Runbook.pdf`

하지만 필수는 **영상 1개 + 보고서 1개**로 보는 것이 맞습니다.

## 보고서에 반드시 들어가야 하는 내용

과제 문구 기준 필수 항목:

1. Chosen use case
2. Agent roles
3. Key instruction snippets
4. Knowledge base setup
5. Tools enabled
6. Test cases + outcomes
7. Trace screenshots
8. Guardrails configuration
9. Entra Agent ID governance notes

자동채점/ATS를 고려해 아래 제목을 그대로 쓰는 것을 권장합니다.

- Use Case
- Microsoft Foundry Architecture
- Knowledge Agent
- Task Agent
- Sequential Workflow
- Knowledge Base Setup
- Tools Enabled
- Test Cases and Outcomes
- Preview and Traces
- Guardrails Configuration
- Entra Agent ID Governance
- Reflection

## 3분 영상 구성

### 0:00-0:20 — Use Case

화면:

- Foundry project overview 또는 PRD 첫 페이지

말:

```text
This is RecallGuard AI, a governed multi-agent product safety compliance checker built in Microsoft Foundry. It helps marketplace and procurement teams review vendor product submissions against product safety policies and recall/certification evidence.
```

### 0:20-0:50 — Knowledge Agent

화면:

- `recallguard-knowledge-agent`
- File Search / knowledge source 설정
- 정책 질문 테스트 응답

말:

```text
The Knowledge Agent answers only from grounded knowledge sources. I connected product safety SOP, KC certification checklist, recall response policy, and vendor submission requirements. If evidence is missing, the agent must say so instead of guessing.
```

### 0:50-1:30 — Task Agent

화면:

- `recallguard-task-agent-v6`
- Code Interpreter enabled
- `recallguard_checker.py`
- CSV test output

말:

```text
The Task Agent performs the concrete action. It uses Code Interpreter and a deterministic checker script to inspect vendor CSV files. This avoids hallucinated classification and ensures that only recall evidence can create a HOLD decision.
```

### 1:30-2:00 — Sequential Workflow

화면:

- Visual workflow 또는 workflow agent
- Knowledge Agent first, Task Agent second
- Preview run

말:

```text
The workflow routes the request to the Knowledge Agent first, then invokes the Task Agent when a product file or evidence check is required. HOLD decisions require human compliance review before any listing action.
```

### 2:00-2:30 — Traces and Guardrails

화면:

- Trace view
- Guardrails configuration
- prompt-injection / edge case result

말:

```text
I reviewed traces for a successful run and an edge case. The main improvement from testing was replacing loose LLM classification with deterministic code. Guardrails and instructions also treat vendor notes as untrusted data to reduce prompt-injection risk.
```

### 2:30-3:00 — Reflection

화면:

- Entra Agent ID / identity screen
- final output summary

말:

```text
Collaboration with AI felt like having a fast reviewer and implementation partner, but the hardest part was validating that agent outputs were actually safe. Traces exposed a false HOLD classification, and after that I improved the design with deterministic tool execution, clearer guardrails, and identity governance through Entra Agent IDs.
```

## 영상에서 꼭 보여줄 화면

최소 화면 6개:

1. Foundry project: `recallguard-ai`
2. Knowledge Agent: `recallguard-knowledge-agent`
3. Task Agent: `recallguard-task-agent-v6`
4. Sequential workflow / workflow agent
5. Preview output
6. Trace + Guardrails + Entra Agent ID

## 보고서 첫 페이지 문구

아래 문구를 첫 페이지나 Executive Summary에 넣으면 자동채점에 유리합니다.

```text
RecallGuard AI is a governed multi-agent workflow built in Microsoft Foundry. It includes a Knowledge Agent grounded in product safety policy documents, a Task Agent using Code Interpreter for vendor CSV evidence checks, and a Sequential Workflow with guardrails, traces, and Entra Agent ID governance.
```

## 제출 전 최종 체크

- [ ] 영상 길이가 3분 이하인지 확인
- [ ] 영상에서 Microsoft Foundry 화면이 보이는지 확인
- [ ] Knowledge Agent와 Task Agent 이름이 보이는지 확인
- [ ] Workflow Preview 또는 workflow run이 보이는지 확인
- [ ] Trace 화면이 최소 1개 이상 보이는지 확인
- [ ] Guardrails 화면이 보이는지 확인
- [ ] Entra Agent ID 또는 agent identity 정보가 보고서에 들어갔는지 확인
- [ ] 보고서에 test cases + outcomes 표가 있는지 확인
- [ ] 보고서에 "Microsoft Foundry", "Knowledge Agent", "Task Agent", "Sequential Workflow", "Guardrails", "Traces", "Entra ID" 키워드가 들어갔는지 확인
