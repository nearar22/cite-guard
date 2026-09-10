# CiteGuard

Source-bound citation auditing for GenLayer. CiteGuard checks whether each proposition in a document is supported by the public legal authorities attached to it. It records the fetched source URL, host, content digest, finding state, source indexes and pinpoint quote.

This is an advisory citation-verification tool. It is not legal advice, a court ruling, a legal certificate or a prediction of outcome.

## Why GenLayer

Citation support is semantic. A conventional contract cannot read an authority and decide whether its wording supports a proposition. CiteGuard makes that question bounded and auditable: the leader proposes a structured audit, while validators independently refetch every authority, verify its receipt, and judge every state, source index, and quote without requiring identical explanatory wording.

## Lifecycle

1. The creator submits jurisdiction, neutral context, two to eight propositions and at least two distinct allowlisted public authorities.
2. Any account may trigger the audit. Validators fetch all authorities and classify every proposition as `SUPPORTED`, `PARTIAL`, `UNSUPPORTED` or `UNAVAILABLE`.
3. The contract derives the overall status. The model cannot choose it.
4. A 48-hour appeal window starts after evaluation. Only the creator may attach one new authority and run one appeal.
5. After the deadline, anyone may finalize so an absent creator cannot stall the record.

## Trust and failure model

- URL parsing requires HTTPS, rejects credentials, fragments and local hosts, and only permits named public legal repositories.
- Query-string mirrors of the same host and path cannot occupy multiple source slots.
- Every nonempty pinpoint quote must occur in at least one referenced fetched source after harmless case, punctuation, and whitespace normalization.
- Supported and partial findings require bounded source indexes and a source-bound pinpoint quote.
- Unavailable sources become an explicit failure rather than fabricated support.
- Validators semantically verify the complete proposed result and exact receipts instead of comparing independently generated prose byte for byte.
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

## StudioNet deployment

- Public app: `https://cite-guard-a0z.pages.dev/`
- Contract: `0x2aFe8a0c960Ac2B8e874cF3500A5606f17c07A14`
- Deployment transaction: `0x0905743ecaccdbcb4ad6a564b7db4eac6c56f2810adac486dd1dca74b7322a39`
- Live matter transaction: `0x0693bb69aaa7b96fe78ff8d0a897da7255aa260093e5c508e5cfbcfab258f759`
- Live successful audit: `0xba9f881d051f5217df5a7065d6baef1111f4057b3bd0cd11eb80e021c5fb87f8`
- Live forged-quote rejection: `0xb6722188fb8dc72b8059689267a38a346b69e31386b9e723c1cea87d0848ee3f`
- Reviewed source commit: `1474df2c31acdd238aa94bfd814a31bd5ff4cffd`
- Contract SHA-256: `5235c09faf402b279223bb6782ea87034a96a47c94684940b55a650d9425f8f6`

The deployment is `FINALIZED` and its decoded source matches the reviewed repository source byte for byte. The successful audit stored two source-bound findings and two receipts. The rejected audit reached consensus with the expected contract rollback and did not mutate the matter.
