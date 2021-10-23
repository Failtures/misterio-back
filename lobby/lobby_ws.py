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
    while True: # Keeps socket alive
        data = await websocket.recv()
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
        lobbyservice.join_player(lobby, user)

        for user in lobby.players:
            await user.socket.send(json.dumps({'action': 'new_player', 'nickname': player, 'lobby': lobby.to_dict()}))
    except Exception as e:
        await websocket.send(json.dumps({'action': 'failed', 'info': e}))


async def start_match(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    player = parsedjson['player_name']
    lobbyname = parsedjson['lobby_name']
    try:
        lobby = lobbyservice.get_lobby_by_name(lobbyname)
        start_player = lobbyservice.get_player_in_lobby(lobby, player)
    except Exception as e:
        await websocket.send("{'error': " + str(e) + "}")

    if lobby.can_start(start_player):
        match = matchservice.create_new_match(lobby.name, lobby.players)
        for user in lobby.players:
            await user.socket.send(json.dumps({'action': 'match_started', 'match': match.to_dict()}))
    else:
        for user in lobby.players:
            await user.socket.send(json.dumps({'action': 'match_not_started'}))


# Must be done this way to not conflict with main thread
asyncio.get_event_loop().create_task(main())
