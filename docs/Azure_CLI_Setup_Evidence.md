# Azure CLI Setup Evidence

## Environment

- Azure CLI version: `2.85.0`
- Default subscription: `Azure for Students`
- Tenant: `한양대학교`
- Signed-in user: `wosom@m365.hanyang.ac.kr`

## Commands Used

```bash
az group create \
  --name rg-recallguard-foundry-je \
  --location japaneast \
  --tags project=RecallGuardAI activity=FoundryFinal owner=Somi purpose=governed-multi-agent-demo
```

```bash
az cognitiveservices account create \
  --name recallguard-somi-20260513 \
  --resource-group rg-recallguard-foundry-je \
  --kind AIServices \
  --sku S0 \
  --location japaneast \
  --allow-project-management \
  --custom-domain recallguard-somi-20260513 \
  --tags project=RecallGuardAI activity=FoundryFinal owner=Somi
```

```bash
az cognitiveservices account project create \
  --name recallguard-somi-20260513 \
  --resource-group rg-recallguard-foundry-je \
  --project-name recallguard-ai \
  --display-name "RecallGuard AI" \
  --description "Governed multi-agent product safety compliance checker for Microsoft Foundry final activity" \
  --location japaneast \
  --assign-identity
```

```bash
az cognitiveservices account deployment create \
  --name recallguard-somi-20260513 \
  --resource-group rg-recallguard-foundry-je \
  --deployment-name gpt-4o-mini \
  --model-name gpt-4o-mini \
  --model-version "2024-07-18" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name GlobalStandard
```

## Created Resources

| Resource | Value |
|---|---|
| Resource group | `rg-recallguard-foundry-je` |
| Foundry resource | `recallguard-somi-20260513` |
| Foundry project | `recallguard-ai` |
| Project endpoint | `https://recallguard-somi-20260513.services.ai.azure.com/api/projects/recallguard-ai` |
| Foundry resource principal ID | `208e2c79-a96f-4c50-919d-5091a2fa3c5d` |
| Project principal ID | `9945404e-cea4-4b17-80f4-5e064713737d` |
| Model deployment | `gpt-4o-mini` |
| Model version | `2024-07-18` |
| Model SKU | `GlobalStandard` |
| Provisioning state | `Succeeded` |

## Created Agents

| Agent | Foundry ID | Model | Tooling | Instance principal ID |
|---|---|---|---|---|
| Knowledge Agent | `recallguard-knowledge-agent` | `gpt-4o-mini` | File Search + vector store | `934a3b63-408b-416f-b7cf-e3a410e0cf06` |
| Final Task Agent | `recallguard-task-agent-v7-public-data` | `gpt-4o-mini-100` | Code Interpreter + deterministic checker script | `0173cc3c-70e7-4bf7-bb74-39703a517ffb` |
| Sequential Workflow | `recallguard-governed-workflow-v5-public-data` | Workflow Agent | Knowledge Agent then Task Agent | `87a0ae4f-49ce-485d-8909-0c2081017775` |

## Additional Demo Deployment

The initial deployment used `gpt-4o-mini` with capacity 10. Code Interpreter tests hit rate limits during repeated calls, so a second deployment was created:

```bash
az cognitiveservices account deployment create \
  --name recallguard-somi-20260513 \
  --resource-group rg-recallguard-foundry-je \
  --deployment-name gpt-4o-mini-100 \
  --model-name gpt-4o-mini \
  --model-version "2024-07-18" \
  --model-format OpenAI \
  --sku-capacity 100 \
  --sku-name GlobalStandard
```

This deployment should be used for the final Task Agent demo.

## Issues Encountered and Fixes

| Issue | Cause | Fix |
|---|---|---|
| `eastus` resource creation blocked | Subscription region policy | Switched to `japaneast` |
| `koreacentral` resource creation blocked | Subscription region policy | Switched to `japaneast` |
| `gpt-4.1-mini Standard` deployment failed | Standard quota was 0 | Used `gpt-4o-mini GlobalStandard` |
| Task Agent v1/v2 over-classified certification evidence as `HOLD` | LLM post-processing was too loose | Added deterministic `recallguard_checker.py` and created `recallguard-task-agent-v7-public-data` |
| Repeated Code Interpreter calls hit rate limit | Initial capacity was 10k TPM | Created `gpt-4o-mini-100` deployment |
| Entra bearer token could create agents after RBAC propagation but could not upload files | File/vector store API accepted API key in this environment | Used API key for file/vector store setup and Entra bearer token for agent creation; document production recommendation to use managed identity/RBAC where available |

## Next Portal Evidence to Capture

- Open https://ai.azure.com
- Select project `RecallGuard AI`
- Confirm model deployment `gpt-4o-mini`
- Create two agents
- Build Sequential workflow
- Capture Preview, Traces, Guardrails, and Agent Identity screens
