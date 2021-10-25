import json
import websockets

from extensions import matchservice


async def match_endpoints(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    if parsedjson['action'] == 'match_end_turn':
        await end_turn(parsedjson, websocket, path)
    elif parsedjson['action'] == 'match_roll_dice':
        await roll_dice(parsedjson, websocket, path)


async def end_turn(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    match_name = parsedjson['match_name']
    match = matchservice.get_match_by_name(match_name)
    # Fails if is not the turn of the requesting player
    if match.current_turn().socket.remote_address != websocket.remote_address:
        websocket.send(json.dumps({'action': 'failed', 'info': "It's not your turn"}))
        return
    match.next_turn()

    for player in match.players:
        await player.socket.send(json.dumps({'action': 'turn_passed', 'current_turn': match.current_turn().nickname}))


async def roll_dice(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    match_name = parsedjson['match_name']
    match = matchservice.get_match_by_name(match_name)
    # Fails if is not the turn of the requesting player
    if match.current_turn().socket.remote_address != websocket.remote_address:
        websocket.send(json.dumps({'action': 'failed', 'info': "It's not your turn"}))
        return
    dice = match.roll_dice()

    for player in match.players:
        await player.socket.send(json.dumps({'action': 'roll_dice', 'dice': dice}))
