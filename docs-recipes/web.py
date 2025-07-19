import websockets
import asyncio

async def test_ws():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        print("✅ WebSocket connected!")

asyncio.run(test_ws())
