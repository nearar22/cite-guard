import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import patch_status; patch_status.apply()
from gl import make_client, read_view

TERMINAL = {"ACCEPTED", "FINALIZED", "UNDETERMINED", "CANCELED"}
SUCCESS = {"ACCEPTED", "FINALIZED"}
def execution(item):
    receipts = ((item.get("consensus_data") or {}).get("leader_receipt") or [])
    for receipt in receipts:
        result = receipt.get("result") or {}
        if receipt.get("execution_result") == "SUCCESS" and result.get("status") == "return": return "SUCCESS", ""
        if result.get("status") == "rollback": return "ROLLBACK", str(result.get("payload") or "")
    return "UNKNOWN", ""

def wait(client, tx):
    for _ in range(160):
        item = client.get_transaction(transaction_hash=tx); status = str(item.get("status_name") or item.get("status")); print(status, flush=True)
        if status in TERMINAL:
            if status not in SUCCESS: raise RuntimeError("Transaction ended " + status)
            result, message = execution(item)
            if result != "SUCCESS": raise RuntimeError("Contract execution was " + result + ": " + message)
            return {"consensus": status, "execution": result}
        time.sleep(8)
    raise TimeoutError("Transaction did not reach a successful terminal status")

def write(client, address, name, args):
    tx = client.write_contract(address=address, function_name=name, args=args, value=0); print(name, tx, flush=True)
    return tx, wait(client, tx)

def main():
    root = os.path.dirname(os.path.dirname(__file__)); address = json.load(open(os.path.join(root, "deployment.json")))["address"]; client, account = make_client()
    args = ["Fair use citation check", "United States federal law", "Audit two statutory propositions in a draft educational memorandum without deciding any dispute or predicting a court outcome.", ["The purpose and character of the use includes whether the use is commercial or for nonprofit educational purposes.", "The analysis considers the effect of the use upon the potential market for or value of the copyrighted work."], ["https://www.law.cornell.edu/uscode/text/17/107", "https://www.govinfo.gov/content/pkg/USCODE-2023-title17/html/USCODE-2023-title17-chap1-sec107.htm"]]
    create_tx, create_status = write(client, address, "create_matter", args)
    stats = read_view(client, account, address, "get_stats"); matter_id = "matter-" + str(stats["matters"])
    audit_tx, audit_status = write(client, address, "audit_citations", [matter_id])
    matter = read_view(client, account, address, "get_matter", [matter_id]); result = matter.get("result") or {}; findings = result.get("findings") or []
    out = {"contract": address, "transactions": {"create": {"hash": create_tx, "status": create_status}, "audit": {"hash": audit_tx, "status": audit_status}}, "matter": {"id": matter.get("id"), "phase": matter.get("phase"), "overall": result.get("overall"), "source_count": len(matter.get("sources", [])), "receipt_count": len(result.get("source_receipts") or []), "proposition_count": len(matter.get("propositions", [])), "finding_count": len(findings), "quotes": [x.get("pinpoint_quote") for x in findings]}}
    with open(os.path.join(root, "scripts", "live_verification.json"), "w", encoding="utf-8") as handle: json.dump(out, handle, indent=2)
    print(json.dumps(out, indent=2))
if __name__ == "__main__": main()
