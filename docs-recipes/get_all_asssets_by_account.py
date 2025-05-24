import subprocess

def get_assets_for_account(account_id):
    result = subprocess.run(
        ["iroha", "--config", "/root/client/client.toml", "assets", "list", "all"],
        capture_output=True,
        text=True,
        check=True
    )

    filtered_assets = []
    for line in result.stdout.splitlines():
        if account_id in line:
            filtered_assets.append(line.strip())

    print("\n".join(filtered_assets))
    return filtered_assets

get_assets_for_account("ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@wonderland")