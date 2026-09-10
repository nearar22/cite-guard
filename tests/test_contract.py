import json

CONTRACT = "contracts/contract.py"
S1 = "https://www.law.cornell.edu/uscode/text/17/107"
S2 = "https://www.govinfo.gov/content/pkg/USCODE-2023-title17/html/USCODE-2023-title17-chap1-sec107.htm"
TEXT1 = "The fair use of a copyrighted work is not an infringement. Factors include the purpose and character of the use."
TEXT2 = "Factors include purpose nature amount and the effect of the use upon the potential market for the copyrighted work."

def create(c):
    return c.create_matter("Fair use citation check", "United States federal law", "Audit two propositions in a draft educational memorandum without deciding any dispute or predicting a court outcome.", ["Fair use analysis considers the purpose and character of the use.", "Fair use analysis considers market effect."], [S1, S2])
def mocks(vm, states=("SUPPORTED", "SUPPORTED")):
    vm.mock_web(S1, {"method":"GET","status":200,"body":TEXT1}); vm.mock_web(S2, {"method":"GET","status":200,"body":TEXT2})
    vm.mock_llm("CITEGUARD_PRODUCER", json.dumps({"findings":[{"index":0,"state":states[0],"source_indexes":[0],"pinpoint_quote":"purpose and character of the use"},{"index":1,"state":states[1],"source_indexes":[1],"pinpoint_quote":"effect of the use upon the potential market"}]})); vm.mock_llm("CITEGUARD_VALIDATOR", json.dumps({"valid":True,"explanation":"Equivalent support confirmed with different wording."}))

def test_rejects_untrusted_and_duplicate_authorities(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT)
    with direct_vm.expect_revert("Unsupported legal authority host"): c.create_matter("Matter title", "US federal", "A sufficiently detailed neutral context for citation verification only.", ["First sufficiently precise proposition.", "Second sufficiently precise proposition."], ["https://example.com/a", S1])
    with direct_vm.expect_revert("Duplicate authority identity"): c.create_matter("Matter title", "US federal", "A sufficiently detailed neutral context for citation verification only.", ["First sufficiently precise proposition.", "Second sufficiently precise proposition."], [S1, S1 + "?copy=1"])

def test_audit_binds_every_finding_quote_and_source_receipt(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT); mid = create(c); mocks(direct_vm); result = c.audit_citations(mid); direct_vm.clear_mocks()
    assert result["overall"] == "CITATION_READY" and len(result["findings"]) == 2 and len(result["source_receipts"]) == 2
    assert result["findings"][0]["source_indexes"] == [0] and len(result["source_receipts"][0]["sha256"]) == 64

def test_validator_tolerates_wording_but_rejects_wrong_semantics(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT); mid = create(c); mocks(direct_vm); c.audit_citations(mid); direct_vm.clear_mocks()
    direct_vm.mock_web(S1, {"method":"GET","status":200,"body":TEXT1}); direct_vm.mock_web(S2, {"method":"GET","status":200,"body":TEXT2}); direct_vm.mock_llm("CITEGUARD_VALIDATOR", json.dumps({"valid":True,"explanation":"Different harmless wording, same supported audit."}))
    assert direct_vm.run_validator() is True; direct_vm.clear_mocks()
    direct_vm.mock_web(S1, {"method":"GET","status":200,"body":TEXT1}); direct_vm.mock_web(S2, {"method":"GET","status":200,"body":TEXT2}); direct_vm.mock_llm("CITEGUARD_VALIDATOR", json.dumps({"valid":False,"explanation":"The proposed finding misstates the source."}))
    assert direct_vm.run_validator() is False; direct_vm.clear_mocks()

def test_overall_is_derived_not_trusted_from_llm(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT); mid = create(c); mocks(direct_vm, ("SUPPORTED", "UNSUPPORTED")); result = c.audit_citations(mid); direct_vm.clear_mocks()
    assert result["overall"] == "NOT_READY"

def test_malformed_attribution_is_rejected(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT); mid = create(c)
    direct_vm.mock_web(S1, {"method":"GET","status":200,"body":TEXT1}); direct_vm.mock_web(S2, {"method":"GET","status":200,"body":TEXT2})
    direct_vm.mock_llm("CITEGUARD_PRODUCER", json.dumps({"findings":[{"index":0,"state":"SUPPORTED","source_indexes":[99],"pinpoint_quote":"invented attribution"},{"index":1,"state":"SUPPORTED","source_indexes":[1],"pinpoint_quote":"effect of the use upon the potential market"}]}))
    with direct_vm.expect_revert("Source reference is out of range"): c.audit_citations(mid)

def test_forged_quote_with_valid_state_and_index_is_rejected(direct_vm, direct_deploy):
    c = direct_deploy(CONTRACT); mid = create(c)
    direct_vm.mock_web(S1, {"method":"GET","status":200,"body":TEXT1}); direct_vm.mock_web(S2, {"method":"GET","status":200,"body":TEXT2})
    direct_vm.mock_llm("CITEGUARD_PRODUCER", json.dumps({"findings":[{"index":0,"state":"SUPPORTED","source_indexes":[0],"pinpoint_quote":"a sentence that does not exist in the cited authority"},{"index":1,"state":"SUPPORTED","source_indexes":[1],"pinpoint_quote":"effect of the use upon the potential market"}]}))
    with direct_vm.expect_revert("Pinpoint quote is not present in a referenced source"): c.audit_citations(mid)

def test_appeal_is_creator_only_new_source_and_deadline_protected(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); direct_vm.sender = direct_alice; mid = create(c); mocks(direct_vm); c.audit_citations(mid); direct_vm.clear_mocks()
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("Only the creator may add"): c.add_appeal_authority(mid, "https://www.courtlistener.com/opinion/108713/campbell-v-acuff-rose-music-inc/")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("requires exactly one new authority"): c.appeal_audit(mid)
    c.add_appeal_authority(mid, "https://www.courtlistener.com/opinion/108713/campbell-v-acuff-rose-music-inc/")
    with direct_vm.expect_revert("Appeal authority limit reached"): c.add_appeal_authority(mid, "https://www.ecfr.gov/current/title-37")
    with direct_vm.expect_revert("elapsed appeal deadline"): c.finalize_matter(mid)

def test_permissionless_finalization_after_window(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy(CONTRACT); direct_vm.sender = direct_alice; mid = create(c); mocks(direct_vm); c.audit_citations(mid); direct_vm.clear_mocks()
    direct_vm.warp("2030-01-01T00:00:00Z"); direct_vm.sender = direct_bob; receipt = c.finalize_matter(mid)
    assert receipt["matter_id"] == mid and c.get_matter(mid)["phase"] == "FINAL"
