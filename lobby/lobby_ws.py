import json
import websockets

from extensions import lobbyservice, matchservice
from users.network_user import NetworkUser


async def lobby_endpoints(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    if parsedjson['action'] == 'lobby_create':
        await create_lobby(parsedjson, websocket, path)
    elif parsedjson['action'] == 'lobby_join':
        await join_lobby(parsedjson, websocket, path)
    elif parsedjson['action'] == 'lobby_start_match':
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
