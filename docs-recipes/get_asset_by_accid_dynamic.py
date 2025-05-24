import subprocess
import tempfile
import os

def list_assets_with_account(account_id, public_key, private_key, torii_url="http://127.0.0.1:8080"):
    # Create a temp file without auto-deletion
    tmp = tempfile.NamedTemporaryFile("w+", delete=False)
    config_path = tmp.name
    tmp.write(f"""
account_id = "{account_id}"
public_key = "{public_key}"
private_key = "{private_key}"
torii_url = "{torii_url}"
""")
    tmp.close()  # Important: close before subprocess uses it

    try:
        # Confirm content is really there
        print("Using config path:", config_path)
        with open(config_path) as f:
            print("== Config File Content ==")
            print(f.read())

        result = subprocess.run(
            ["iroha", "--config", config_path, "asset", "list", "all"],
            capture_output=True,
            text=True,
            check=True
        )
        print("== Asset list output ==")
        print(result.stdout)
        return result.stdout

    finally:
        os.remove(config_path)

# Example usage
list_assets_with_account(
    account_id="ed0120C1E00D1E555CA402EDDB26B04D3DD14829DB1EA1EC9A6D679EF336CEDCFC2F9C@hivefund",
    public_key="ed0120C1E00D1E555CA402EDDB26B04D3DD14829DB1EA1EC9A6D679EF336CEDCFC2F9C",
    private_key="802620F409DC65A0DFBCFBDF0B479C7318A17D30041D19EA99C4B0A26AE5A232CA18DE"
)