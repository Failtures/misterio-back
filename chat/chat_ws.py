from extensions import lobbyservice, matchservice
from datetime import datetime


async def chat_endpoints(parsedjson, websocket):
    if parsedjson['action'] == 'chat_lobby_send':
        await send_msg(parsedjson, websocket, "lobby")
    elif parsedjson['action'] == 'chat_match_send':
        await send_msg(parsedjson, websocket, "match")    


async def send_msg(parsedjson, websocket, place:str):
    try:
        now = datetime.now().strftime("%H:%M, %d/%m")
        player = parsedjson['player_name']
        msg = parsedjson['mesagge']

        message = str(now + " - " + player + ": " + msg)

        if place == "lobby":
            lobby = lobbyservice.get_lobby_by_name(parsedjson['chat_name'])
            lobby.chat.appendleft(message)

            for player in lobby.players:
                await player.socket.send_json({'action': 'new_message', 'message': message})

        elif place == "match":
            match = matchservice.get_match_by_name(parsedjson['chat_name'])
            match.chat.appendleft(message)

            for player in match.players:
                await player.socket.send_json({'action': 'new_message', 'message': message})

    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})