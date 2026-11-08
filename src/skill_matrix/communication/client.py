import asyncio
import websockets
import json
import sys

async def listen_notifications(user_id: int):
    uri = f"ws://127.0.0.1:8001/ws/{user_id}"
    print(f"[*] Connecting to Notification Service as user ID={user_id}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"[+] Successfully connected to the notification server. Waiting for events...\n")
            while True:
                response = await websocket.recv()
                data = json.loads(response)
                print("=" * 50)
                print("NEW NOTIFICATION IN REAL-TIME:")
                print(f"Project ID:  {data.get('project_id')}")
                print(f"Message:   {data.get('message')}")
                print("=" * 50 + "\n")
    except ConnectionRefusedError:
        print("[!] Error: Notification Service is not available. Please check if it is running.")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    user_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    asyncio.run(listen_notifications(user_id))