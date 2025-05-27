import iroha2

key_pair = iroha2.KeyPair.from_json("""
{
  "public_key": "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03",
  "private_key": "802620CCF31D85E3B32A4BEA59987CE0C78E3B8E2DB93881468AB2435FE45D5C9DCD53"
}
""")

account_id = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@wonderland"
web_login = "mad_hatter"
password = "ilovetea"
api_url = "http://212.56.43.254:8080/"
telemetry_url = "http://212.56.43.254:8180/"
chain_id = "00000000-0000-0000-0000-000000000000"

client = iroha2.Client.create(
            key_pair,
            account_id,
            web_login,
            password,
            api_url,
            chain_id)

domains = client.query_all_domains()

print("Listing all domains...")
for d in domains:
    print(" - ", d,)

