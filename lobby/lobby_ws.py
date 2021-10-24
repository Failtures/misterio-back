import asyncio
import json
import websockets

from extensions import lobbyservice, matchservice
from users.network_user import NetworkUser


async def main():
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

        if parsedjson['action'] == 'create_lobby':
            await create_lobby(parsedjson, websocket, path)
        elif parsedjson['action'] == 'join_lobby':
            await join_lobby(parsedjson, websocket, path)
        elif parsedjson['action'] == 'start_match':
            await start_match(parsedjson, websocket, path)
            

async def create_lobby(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    host = parsedjson['host_name']
    lobbyname = parsedjson['lobby_name']

    user = NetworkUser(host, websocket)
    
    try:
        lobby = lobbyservice.create_new_lobby(lobbyname, user)
        await user.socket.send(json.dumps({'action': 'new_lobby', 'lobby': lobby.to_dict()}))
    except Exception as e:
        await websocket.send(json.dumps({'action': 'failed', 'info': e}))


async def join_lobby(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    player = parsedjson['player_name']
    lobbyname = parsedjson['lobby_name']

    user = NetworkUser(player, websocket)

    try:
        lobby = lobbyservice.get_lobby_by_name(lobbyname)

        for lobbyplayer in lobby.players:
            await lobbyplayer.socket.send(json.dumps({'action': 'new_player', 'nickname': player}))

        lobbyservice.join_player(lobbyname, user)
        await user.socket.send(json.dumps({'action': 'joined_lobby', 'lobby': lobby.to_dict()}))
    except Exception as e:
        await websocket.send(json.dumps({'action': 'failed', 'info': str(e)}))


async def start_match(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    player = parsedjson['player_name']
    lobbyname = parsedjson['lobby_name']

    try:
        lobby = lobbyservice.get_lobby_by_name(lobbyname)
        start_player = lobbyservice.get_player_in_lobby(lobby, player)

        if lobby.can_start(start_player):
            match = matchservice.create_new_match(lobby.name, lobby.players)
            json_msg = json.dumps({'action': 'match_started', 'match': match.to_dict()})
        else:
            json_msg = json.dumps({'action': 'match_not_started'})

        for user in lobby.players:
            await user.socket.send(json_msg)
    except Exception as e:
        await websocket.send(json.dumps({'action': 'failed', 'info': str(e)}))


# Must be done this way to not conflict with main thread
asyncio.get_event_loop().create_task(main())
