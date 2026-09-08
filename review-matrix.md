# Readiness matrix

| Mandatory requirement | Code path | Evidence | Status |
| --- | --- | --- | --- |
| Distinct GenLayer-native use case | proposition-level semantic source audit | README originality comparison | PASS |
| Every material external fact is fetched and attributed | `_audit`, `_normalize` | source receipt and adversarial tests | PASS |
| Validators independently recheck full output | `_audit.check` recomputes and compares canonical JSON | direct tests | PASS |
| Exact appeal protection | post-audit 48-hour deadline, creator-only new authority, one appeal | appeal tests | PASS |
| Permissionless completion | `finalize_matter` | finalization test from second account | PASS |
| Real frontend integration | all public methods, editable authorities, strict terminal polling | frontend tests | PASS locally, deployment pending |
| Exact deployed source | deployment manifest and Explorer source comparison | pending deployment | UNVERIFIED |
| Real network transaction | create and read back a new matter | pending deployment | UNVERIFIED |
| Public production path | clean build and browser lifecycle | pending deployment | UNVERIFIED |
