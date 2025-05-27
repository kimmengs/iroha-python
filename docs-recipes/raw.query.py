import requests
import json
from iroha2 import Client, KeyPair

class PatchedClient(Client):
    def query_raw(self, raw_query_dict):
        url = self.api_url + "/query"
        headers = { "Content-Type": "application/json" }
        print("[DEBUG] Sending raw query:", json.dumps(raw_query_dict, indent=2))
        res = requests.post(url, headers=headers, json=raw_query_dict)
        return res.json()

# Use your keys and client setup
key_pair = KeyPair.from_json("""
{
   "public_key": "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03",
  "private_key": "802620CCF31D85E3B32A4BEA59987CE0C78E3B8E2DB93881468AB2435FE45D5C9DCD53"
}
""")
account_id = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"
client = PatchedClient.create(
    key_pair,
    account_id,
    "mad_hatter",
    "ilovetea",
    "http://212.56.43.254:8080/",
    "00000000-0000-0000-0000-000000000000"
)

# Send raw JSON query (won’t be signed!)
payload = {
    "find_transactions_by_account_id": {
        "account_id": account_id
    }
}
response = client.query_raw(payload)
print(response)
