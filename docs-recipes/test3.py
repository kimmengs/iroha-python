import asyncio
import websockets
import json

IROHA_WS_URL = "ws://localhost:8080"  # Update if your port differs
ACCOUNT_ID = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"

async def main():
    async with websockets.connect(IROHA_WS_URL) as ws:
        request = {
            "jsonrpc": "2.0",
            "id": "get_tx_by_account",
            "method": "find_transactions",
            "params": {
                "predicate": {
                    "Atom": {
                        "Value": {
                            "path": "payload.instructions.Instructions[0].Transfer.Asset.source",
                            "value": {
                                "Equals": {
                                    "Atom": f"khr##{ACCOUNT_ID}"
                                }
                            }
                        }
                    }
                },
                "limit": 20
            }
        }

        await ws.send(json.dumps(request))
        response = await ws.recv()
        parsed = json.loads(response)
        print(json.dumps(parsed, indent=2))

asyncio.run(main())
