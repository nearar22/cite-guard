import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
import patch_status; patch_status.apply()
from gl import make_client, read_view

TERMINAL = {"ACCEPTED", "FINALIZED", "UNDETERMINED", "CANCELED"}
def wait(client, tx):
    for _ in range(160):
        item = client.get_transaction(transaction_hash=tx); status = str(item.get("status_name") or item.get("status")); print(status, flush=True)
        if status in TERMINAL:
            if status not in {"ACCEPTED", "FINALIZED"}: raise RuntimeError("Transaction ended " + status)
            return status
        time.sleep(8)
    raise TimeoutError("Transaction did not reach a successful terminal status")

def main():
    root = os.path.dirname(os.path.dirname(__file__)); address = json.load(open(os.path.join(root, "deployment.json")))["address"]; client, account = make_client()
    args = ["Fair use citation check", "United States federal law", "Audit two propositions in a draft educational memorandum without deciding any dispute or predicting a court outcome.", ["Fair use analysis considers the purpose and character of the use.", "Fair use analysis considers market effect."], ["https://www.law.cornell.edu/uscode/text/17/107", "https://www.govinfo.gov/content/pkg/USCODE-2023-title17/html/USCODE-2023-title17-chap1-sec107.htm"]]
    tx = client.write_contract(address=address, function_name="create_matter", args=args, value=0); print("tx", tx, flush=True); status = wait(client, tx)
    matter = read_view(client, account, address, "get_matter", ["matter-1"]); out = {"transaction": tx, "status": status, "matter": {"id": matter.get("id"), "phase": matter.get("phase"), "source_count": len(matter.get("sources", [])), "proposition_count": len(matter.get("propositions", []))}}
    with open(os.path.join(root, "scripts", "live_verification.json"), "w", encoding="utf-8") as handle: json.dump(out, handle, indent=2)
    print(json.dumps(out, indent=2))
if __name__ == "__main__": main()
