from iroha2 import IrohaClient, KeyPair

client = IrohaClient("http://212.56.43.254:8080")
keypair = KeyPair.from_json("""
{
  "public_key": "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03",
  "private_key": "802620CCF31D85E3B32A4BEA59987CE0C78E3B8E2DB93881468AB2435FE45D5C9DCD53"
}
""")

query = {
    "find_transactions_by_account_id": {
        "account_id": "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"
    }
}

response = client.query(query, keypair)
print(response)
