# CiteGuard

Source-bound citation auditing for GenLayer. CiteGuard checks whether each proposition in a document is supported by the public legal authorities attached to it. It records the fetched source URL, host, content digest, finding state, source indexes and pinpoint quote.

This is an advisory citation-verification tool. It is not legal advice, a court ruling, a legal certificate or a prediction of outcome.

## Why GenLayer

Citation support is semantic. A conventional contract cannot read an authority and decide whether its wording supports a proposition. CiteGuard makes that question bounded and auditable: validators independently fetch the same sources, hash normalized content, re-evaluate every proposition and accept only the same canonical result.

## Lifecycle

1. The creator submits jurisdiction, neutral context, two to eight propositions and at least two distinct allowlisted public authorities.
2. Any account may trigger the audit. Validators fetch all authorities and classify every proposition as `SUPPORTED`, `PARTIAL`, `UNSUPPORTED` or `UNAVAILABLE`.
3. The contract derives the overall status. The model cannot choose it.
4. A 48-hour appeal window starts after evaluation. Only the creator may attach one new authority and run one appeal.
5. After the deadline, anyone may finalize so an absent creator cannot stall the record.

## Trust and failure model

- URL parsing requires HTTPS, rejects credentials, fragments and local hosts, and only permits named public legal repositories.
- Query-string mirrors of the same host and path cannot occupy multiple source slots.
- Supported and partial findings require bounded source indexes and a pinpoint quote.
- Unavailable sources become an explicit failure rather than fabricated support.
- Validators compare the complete canonical result, including all findings and source receipts.
- Transaction timeout, cancellation and undetermined status never produce a success confirmation in the frontend.

## Originality

CiteGuard is not a generic rubric gate and not a compliance checklist. Its unit of work is a proposition-citation pair. Its consensus question is whether exact fetched authority text supports each proposition in the declared jurisdiction. The stored artifact is a source digest plus a pinpoint quote and citation mapping.

## Run locally

```text
gltest tests -v
genvm-lint contracts/contract.py
cd frontend
npm ci
npm test
npm run build
```

## Repository structure

```text
contracts/contract.py       Intelligent Contract
tests/test_contract.py      lifecycle and adversarial tests
frontend/src/main.jsx       live contract interface
frontend/src/transaction.js terminal-state polling
scripts/deploy.py           exact-source StudioNet deployment
scripts/verify_write.py     real post-deployment transaction
```

Deployment addresses and verified transactions are added after the reviewed source is deployed.
