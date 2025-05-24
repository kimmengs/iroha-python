from iroha2 import Client, KeyPair, Instruction, AccountId, AssetId, AssetDefinitionId, NewAssetDefinition, Mintable
from iroha2.crypto import PrivateKey

# ---------- CONFIG ----------
node_url = "http://127.0.0.1:8080/"

# Authority (creator) account details
creator_id = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@wonderland"
creator_private_key_hex = "802620CCF31D85E3B32A4BEA59987CE0C78E3B8E2DB93881468AB2435FE45D5C9DCD53"

# New wallet details (generated using `iroha key generate`)
new_wallet_pubkey = "ed0120C1E00D1E555CA402EDDB26B04D3DD14829DB1EA1EC9A6D679EF336CEDCFC2F9C"
new_account_id = f"{new_wallet_pubkey}@hivefund"

# ---------- CREATE CLIENT ----------
creator_private_key = PrivateKey.from_hex(creator_private_key_hex)
creator_keypair = KeyPair.from_private_key(creator_private_key)
client = Client(node_url, creator_keypair)

# ---------- INSTRUCTIONS ----------

# 1. Register the new account
account_id_obj = AccountId.from_str(new_account_id)
instr_register_account = Instruction.Register(account=account_id_obj)

# 2. Register asset definition (only needed once — comment out after first run)
asset_def_id = AssetDefinitionId.from_str("usd#hivefund")
instr_register_asset_def = Instruction.Register(asset_definition=NewAssetDefinition(
    id=asset_def_id,
    mintable=Mintable.INFINITELY,
))

# 3. Mint 0 USD to the new account
asset_id_obj = AssetId.from_str(f"usd#hivefund#{new_account_id}")
instr_mint_zero = Instruction.Mint(
    object="0",
    destination=asset_id_obj
)

# ---------- BUILD & SUBMIT ----------
tx = client.build_transaction([
    instr_register_account,
    instr_register_asset_def,  # ⚠️ Comment this out if already registered
    instr_mint_zero
])
client.submit_transaction_blocking(tx)

# ---------- OUTPUT ----------
print("✅ Successfully created new wallet/account:")
print("  🧾 Account ID:", new_account_id)
print("  🔑 Public Key:", new_wallet_pubkey)