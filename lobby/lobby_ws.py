import asyncio
import json
import websockets

from extensions import lobbyservice
from users.network_user import NetworkUser


async def main():
    # Runs on all ips available on the network
    async with websockets.serve(join_lobby, "0.0.0.0", 8080):
        await asyncio.Future()  # Run forever


async def join_lobby(websocket: websockets.WebSocketServerProtocol, path):
    while True:  # Keeps socket alive
        data = await websocket.recv()
        parsedjson = json.loads(data)

        if(parsedjson['action'] == 'join_lobby'):
            nickname = parsedjson['nickname']
            lobbyname = parsedjson['lobby_name']

            user = NetworkUser(nickname, websocket)

            try:
                lobbyservice.join_player(lobbyname, user)
                lobby = lobbyservice.get_lobby_by_name(lobbyname)

                for user in lobby.players:
                    await user.socket.send(json.dumps({'action': 'new_player_lobby', 'nickname': nickname}))

            except Exception as e:
                await websocket.send("{'error': " + str(e) + "}")


# Must be done this way to not conflict with main thread
asyncio.get_event_loop().create_task(main())
