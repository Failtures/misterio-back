from extensions import lobbyservice, matchservice
from users.network_user import NetworkUser


async def lobby_endpoints(parsedjson, websocket):
    if parsedjson['action'] == 'lobby_create':
        await create_lobby(parsedjson, websocket)
    elif parsedjson['action'] == 'lobby_join':
        await join_lobby(parsedjson, websocket)
    elif parsedjson['action'] == 'lobby_start_match':
        await start_match(parsedjson, websocket)


async def create_lobby(parsedjson, websocket):
    try:
        host = parsedjson['player_name']
        lobbyname = parsedjson['lobby_name']

        user = NetworkUser(host, websocket)
        lobby = lobbyservice.create_new_lobby(lobbyname, user)
        await user.socket.send_json({'action': 'new_lobby', 'lobby': lobby.to_dict()})
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})


async def join_lobby(parsedjson, websocket):
    try:
        player = parsedjson['player_name']
        lobbyname = parsedjson['lobby_name']

        user = NetworkUser(player, websocket)

        lobby = lobbyservice.get_lobby_by_name(lobbyname)

        lobbyservice.join_player(lobbyname, user)

        for lobbyplayer in lobby.players:
            if lobbyplayer.nickname == user.nickname:
                await user.socket.send_json({'action': 'joined_lobby', 'lobby': lobby.to_dict()})
            else:
                await lobbyplayer.socket.send_json({'action': 'new_player', 'player_name': player})

    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})


async def start_match(parsedjson, websocket):
    try:
        player = parsedjson['player_name']
        lobbyname = parsedjson['lobby_name']

        lobby = lobbyservice.get_lobby_by_name(lobbyname)
        start_player = lobbyservice.get_player_in_lobby(lobby, player)

        if lobby.can_start(start_player):
            match = matchservice.create_new_match(lobby.name, lobby.players)
            json_msg = {'action': 'match_started', 'match': match.to_dict()}
        else:
            json_msg = {'action': 'failed', 'info': "Match couldn't start, "
                                                    "check if there are enough players in the lobby"
                                                    " and that you are the creator of the lobby"}

        for user in lobby.players:
            await user.socket.send_json(json_msg)
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
