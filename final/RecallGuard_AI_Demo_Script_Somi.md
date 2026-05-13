# RecallGuard AI Demo Script

## Slide 1: Use case

This is RecallGuard AI, a governed multi-agent product safety compliance checker built in Microsoft Foundry. It helps marketplace and procurement teams review vendor product submissions against safety policy and recall evidence.

## Slide 2: Knowledge Agent

The Knowledge Agent answers only from grounded knowledge sources. It uses File Search over the product safety SOP, KC certification checklist, recall response policy, and vendor submission requirements.

## Slide 3: Task Agent

The Task Agent performs the concrete action. It uses Code Interpreter and a deterministic checker script to inspect vendor CSV files and compare them with recall and certification evidence.

## Slide 4: Sequential Workflow

The sequential workflow grounds the review policy first, then invokes the Task Agent when evidence checking is required. Any HOLD decision requires human compliance review before listing.

## Slide 5: Successful and failure tests

I tested a recall match case, a missing-field case, and a prompt-injection edge case. The final system produced one hold and one approval for the recall batch, two reviews for missing identifiers, and safe handling of vendor notes as data.

## Slide 6: Trace-driven improvement

The hardest part was validating that agent outputs were actually safe. Testing exposed a false hold classification, so I improved the design with deterministic code and stricter evidence handling.

## Slide 7: Guardrails and identity

The governance layer includes prompt-injection protection, untrusted-file handling, Entra Agent ID notes, RBAC ownership, and least-privilege access. The agent does not directly approve production listings.

## Slide 8: Reflection

Collaboration with AI felt like having a fast implementation partner. But the most valuable part was review: traces and tests helped reveal failure modes and improve the workflow with guardrails, deterministic tools, and identity governance.
