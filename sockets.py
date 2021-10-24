import asyncio
import json
import websockets

from lobby.lobby_ws import lobby_endpoints, create_lobby
from matches.match_ws import match_endpoints

async def main_socket():
    # Runs on all ips available on the network
    async with websockets.serve(endpoints, "0.0.0.0", 8080):
        await asyncio.Future()  # Run forever


async def endpoints(websocket: websockets.WebSocketServerProtocol, path):
    print(f'New connection from {websocket.remote_address}')
    # Keeps socket alive
    while True:
        try:
            data = await websocket.recv()
        except websockets.exceptions.ConnectionClosedOK as e:
            # Recovers from closing sockets
            print(f'{websocket.remote_address} Closing ws connection: {e}')
            break
        except Exception as e:
            print(f'{websocket.remote_address} Socket crashed, reason: {e}')
            break
        parsedjson = json.loads(data)

        if parsedjson['action'].startswith('lobby'):
            await lobby_endpoints(parsedjson, websocket, path)
        elif parsedjson['action'].startswith('match'):
            await match_endpoints(parsedjson, websocket, path)
                    

# Must be done this way to not conflict with main thread
asyncio.get_event_loop().create_task(main_socket())
