import subprocess
import tempfile
import os
import json
import shutil
    
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
    # if not shutil.which("kagami"):
    #     raise RuntimeError("kagami CLI not found in PATH.")
    result = subprocess.run(
        ["/root/.cargo/bin/kagami", "crypto", "generate-keypair", "--output-format", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    keypair = json.loads(result.stdout)
    return keypair["public_key"], keypair["private_key"]

def register_account_and_asset(public_key, domain, asset_name):
    account_id = f"{public_key}@{domain}"
    try:
       subprocess.run([
            "iroha",  "--config", "/root/client/client.toml", "account", "register", f"--id={account_id}"
        ], check=True)
    except subprocess.CalledProcessError as e:
        if "already exists" not in e.stderr:
            raise
    # Mint 0 units of asset to the new account
    asset_id = f"{asset_name}##{account_id}"
    try:
        subprocess.run([
            "iroha", "--config", "/root/client/client.toml", "asset", "mint", f"--id={asset_id}", f"--quantity=0"
        ], check=True)
    except subprocess.CalledProcessError as e:
        if "already exists" not in e.stderr:
            raise
    return account_id, asset_id

def list_assets_with_account(domain, public_key, private_key):
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
        
        filtered_assets = []
        for line in result.stdout.splitlines():
            if f"{public_key}@{domain}" in line:
                filtered_assets.append(line.strip())

        print("\n".join(filtered_assets))
        return filtered_assets
        # return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        return None
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

# 🔐 Example usage (replace with real keys for each account)
create_wallet_with_kagami()
# pub, priv = create_wallet_with_kagami()

list_assets_with_account(
    domain="hivefund",
    public_key="ed0120C1E00D1E555CA402EDDB26B04D3DD14829DB1EA1EC9A6D679EF336CEDCFC2F9C",
    private_key="802620F409DC65A0DFBCFBDF0B479C7318A17D30041D19EA99C4B0A26AE5A232CA18DE"
)