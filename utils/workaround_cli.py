import subprocess
import tempfile
import os
import json
import shutil
from decimal import Decimal
    
def write_iroha_config(path, domain, public_key, private_key, torii_url="http://127.0.0.1:8080/"):
    with open(path, "w") as f:
        f.write(f"""
chain = "00000000-0000-0000-0000-000000000000"
torii_url = "{torii_url}"

[account]
domain = "{domain}"
public_key = "{public_key}"
private_key = "{private_key}"

[basic_auth]
web_login = "mad_hatter"
password = "ilovetea"
""")
        
def create_wallet_with_kagami():
    result = subprocess.run(
        ["/root/.cargo/bin/kagami", "crypto"],
        capture_output=True,
        text=True,
        check=True
    )
    pub = None
    priv = None
    for line in result.stdout.splitlines():
        if line.startswith("Public key"):
            pub = line.split(":")[1].strip().strip('"')
        elif line.startswith("Private key"):
            priv = line.split(":")[1].strip().strip('"')
    if not pub or not priv:
        raise RuntimeError("Failed to parse kagami output:\n" + result.stdout)
    return pub, priv

def register_account_and_asset(public_key, domain, asset_names):
    account_id = f"{public_key}@{domain}"
    try:
       subprocess.run([
            "iroha",  "--config", "/root/client/client.toml", "account", "register", f"--id={account_id}"
        ], check=True)
    except subprocess.CalledProcessError as e:
        if "already exists" not in e.stderr:
            raise
    # Mint 0 units of asset to the new account
    asset_ids = []
    # Support multiple asset names separated by '|'
    for asset_name in asset_names.split("|"):
        asset_name = asset_name.strip()
        asset_id = f"{asset_name}##{account_id}"
        try:
            subprocess.run([
                "iroha", "--config", "/root/client/client.toml", "asset", "mint", f"--id={asset_id}", f"--quantity=0"
            ], check=True)
        except subprocess.CalledProcessError as e:
            if "already exists" not in e.stderr:
                raise
        asset_ids.append(asset_id)
    return account_id, asset_ids
def get_asset_balance(account_id, domain, public_key, private_key):
    """
    Returns the balance of asset_id for account_id using the Iroha CLI.
    """
    # Create temp config
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    config_path = tmp.name
    tmp.close()

    write_iroha_config(config_path, domain, public_key, private_key)
    try:
        result = subprocess.run(
            [
               "iroha","--config", config_path, "asset", "get", f"--id={account_id}",
            ],
            capture_output=True,
            text=True,
            check=True
        )
        # Parse balance from CLI output (assuming output is just the balance)
        output = result.stdout.strip()
        try:
            data = json.loads(output)
            balance = data.get("value", "0")
        except Exception:
            balance = 0
        return float(balance) / 100
    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        # Optionally, parse e.stderr for more details
        return 0
    finally:
        os.remove(config_path)
        
def list_assets_with_account(domain, public_key, private_key):
    import json

    # Create temp config
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    config_path = tmp.name
    tmp.close()

    write_iroha_config(config_path, domain, public_key, private_key)

    try:
        result = subprocess.run(
            ["iroha", "--config", config_path, "asset", "list", "all"],
            capture_output=True,
            text=True,
            check=True
        )

        assets_with_balance = []
        account_id = f"{public_key}@{domain}"

        for line in result.stdout.splitlines():
            line = line.strip().strip(",").strip('"')
            if account_id in line:
                asset_id = line
                # Get balance for this asset_id
                try:
                    balance_result = subprocess.run(
                        [
                            "iroha", "--config", config_path, "asset", "get", f"--id={asset_id}"
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    output = balance_result.stdout.strip()
                    try:
                        data = json.loads(output)
                        balance = int(data.get("value", 0))
                    except Exception:
                        balance = 0
                except Exception:
                    balance = 0

                assets_with_balance.append({
                    "asset_id": asset_id,
                    "balance": float(balance) / 100
                })

        return assets_with_balance

    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        return []
    finally:
        os.remove(config_path)
        
        
def list_all_assets(domain, public_key, private_key):
    # Create temp config
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    config_path = tmp.name
    tmp.close()

    write_iroha_config(config_path, domain, public_key, private_key)

    try:
        result = subprocess.run(
            ["iroha", "--config", config_path, "asset", "list", "all"],
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        return None
    finally:
        os.remove(config_path)
        
def transfer_asset(domain, public_key, private_key, asset_id, to_account_id, quantity):
    """
    Transfers a quantity of an asset to another account using the Iroha CLI.
    Returns only the transaction hash.
    """
    # Create temp config
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    config_path = tmp.name
    tmp.close()

    write_iroha_config(config_path, domain, public_key, private_key)

    try:
        result = subprocess.run(
            [
                "iroha",
                "--config", config_path,
                "asset", "transfer",
                f"--to={to_account_id}@{domain}",
                f"--id={asset_id}##{public_key}@{domain}",
                f"--quantity={int(Decimal(str(quantity)) * 100)}"

            ],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()

        # Extract hash from output
        hash_value = None
        lines = output.splitlines()

        for i, line in enumerate(lines):
            if line.strip() == "Hash:" and i + 1 < len(lines):
                hash_value = lines[i + 1].strip().strip('"')
                break

        return hash_value

    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        return None
    finally:
        os.remove(config_path)

# 🔐 Example usage (replace with real keys for each account)
# create_wallet_with_kagami()
# pub, priv = create_wallet_with_kagami()

# list_assets_with_account(
#     domain="hivefund",
#     public_key="ed0120C1E00D1E555CA402EDDB26B04D3DD14829DB1EA1EC9A6D679EF336CEDCFC2F9C",
#     private_key="802620F409DC65A0DFBCFBDF0B479C7318A17D30041D19EA99C4B0A26AE5A232CA18DE"
# )