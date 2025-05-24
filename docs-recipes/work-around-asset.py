import subprocess

def list_assets_via_cli():
    try:
        result = subprocess.run(
            ["iroha", "--config", "/root/client/client.toml", "asset", "list", "all"],
            capture_output=True,
            text=True,
            check=True
        )
        print("CLI Output:")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error running Iroha CLI:", e.stderr)
        return None

if __name__ == "__main__":
    assets = list_assets_via_cli()