import requests
import json
from iroha2 import Client, KeyPair

class ClientWrapper:
    def __init__(self, client: Client):
        self.client = client
        self.api_url = client.api_url

    def query_raw(self, payload: dict):
        url = self.api_url + "/query"
        headers = { "Content-Type": "application/json" }
        print("[DEBUG] Sending raw query...")
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

# Initialize the real client
key_pair = KeyPair.from_json("""
{
    "public_key": "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03",
    "private_key": "802620CCF31D85E3B32A4BEA59987CE0C78E3B8E2DB93881468AB2435FE45D5C9DCD53"
}
""")

account_id = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"

client = Client.create(
    key_pair,
    account_id,
    "mad_hatter",
    "ilovetea",
    "http://212.56.43.254:8080/",
    "00000000-0000-0000-0000-000000000000"
)

wrapped = ClientWrapper(client)

# Now test a raw query
payload = {
    "find_transactions_by_account_id": {
        "account_id": account_id
    }
}

response = wrapped.query_raw(payload)
print("Response:", response)
