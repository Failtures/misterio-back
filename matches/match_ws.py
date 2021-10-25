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
    match.next_turn()

    for player in match.players:
        await player.socket.send(json.dumps({'action': 'turn_passed', 'current_turn': match._currentturn}))


async def roll_dice(parsedjson, websocket: websockets.WebSocketServerProtocol, path):
    match_name = parsedjson['match_name']
    match = matchservice.get_match_by_name(match_name)
    dice = match.roll_dice()

    for player in match.players:
        await player.socket.send(json.dumps({'action': 'roll_dice', 'dice': dice}))
