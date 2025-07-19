import asyncio
import websockets
import json
import uuid

IROHA_RPC_URL = "ws://localhost:8080/websocket"  # update to match your node
TARGET_ACCOUNT = "ed0120CE7FA46C9DCE7EA4B125E2E36BDB63EA33073E7590AC92816AE1E861B7048B03@hivefund"

async def query_by_destination(account_id):
    async with websockets.connect(IROHA_RPC_URL) as ws:
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "find_transactions",
            "params": {
                "predicate": {
                    "Atom": {
                        "Value": {
                            "path": "payload.instructions.Instructions[0].Transfer.Asset.destination",
                            "value": {
                                "Equals": {
                                    "Atom": account_id
                                }
                            }
                        }
                    }
                }
            }
        }

        await ws.send(json.dumps(request))
        response = await ws.recv()
        result = json.loads(response)
        print(json.dumps(result, indent=2))

async def query_by_source(account_id):
    async with websockets.connect(IROHA_RPC_URL) as ws:
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "find_transactions",
            "params": {
                "predicate": {
                    "Atom": {
                        "Value": {
                            "path": "payload.instructions.Instructions[0].Transfer.Asset.source",
                            "value": {
                                "Equals": {
                                    "Atom": f"khr##{account_id}"
                                }
                            }
                        }
                    }
                }
            }
        }

        await ws.send(json.dumps(request))
        response = await ws.recv()
        result = json.loads(response)
        print(json.dumps(result, indent=2))

# Run both queries
async def main():
    print("=== Transfers where account is destination ===")
    await query_by_destination(TARGET_ACCOUNT)
    print("\n=== Transfers where account is source ===")
    await query_by_source(TARGET_ACCOUNT)

asyncio.run(main())
