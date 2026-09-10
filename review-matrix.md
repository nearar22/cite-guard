# Readiness matrix

| Mandatory requirement | Code path | Evidence | Status |
| --- | --- | --- | --- |
| Distinct GenLayer-native use case | proposition-level semantic source audit | README originality comparison | PASS |
| Every pinpoint quote is bound to a referenced fetched source | `_normalize`, `_quote_text` | forged quote with valid verdict and index is rejected | PASS |
| Every material external fact is fetched and attributed | `_audit`, `_normalize` | source receipt and out-of-range attribution tests | PASS |
| Consensus tolerates harmless wording differences | `_audit.check` refetches sources and semantically verifies the proposal | direct validator accepts wording variation and rejects wrong semantics | PASS |
| Exact appeal protection | post-audit 48-hour deadline, creator-only new authority, one appeal | appeal tests | PASS |
| Permissionless completion | `finalize_matter` | finalization test from second account | PASS |
| Real frontend integration | corrected address, source-grounded defaults, all public methods, creator and source-limit UI, rollback-aware polling | 10 frontend tests and production build | PASS |
| Exact deployed source | deployment manifest and Explorer source comparison | commit `1474df2`, deployment `0x090574...2a39`, byte-for-byte match | PASS |
| Real network transaction | create, audit, and read back source-bound findings | `0x0693bb...f759`, `0xba9f88...87f8`, `scripts/live_verification.json` | PASS |
| Public production read path | production site loads the corrected deployed address and latest matter | verified `matter-2`, `APPEAL`, `CITATION_READY`, two bound quotes, and two receipts | PASS |
| Public production wallet write path | create from the public site with fresh browser inputs | not executed with a browser wallet | UNVERIFIED |
| Live delayed finalization | finalize the deployed matter after its 48-hour deadline | local lifecycle passes, StudioNet deadline has not elapsed | UNVERIFIED |
