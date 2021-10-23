import asyncio
import json
import websockets

from extensions import matchservice
from matches.match import Match

async def main():
    # Runs on all ips available on the network
    async with websockets.serve(endpoints, "0.0.0.0", 8081):
        await asyncio.Future()  # Run forever   


async def endpoints(websocket: websockets.WebSocketServerProtocol, path):
    while True: # Keeps socket alive
        data = await websocket.recv()
        parsedjson = json.loads(data)

        if parsedjson['action'] == 'end_turn':
            await end_turn(parsedjson, websocket, path)
        elif parsedjson['action'] == 'roll_dice':
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

    for player in match.players:
        await player.socket.send(json.dumps({'action': 'roll_dice', 'dice': match.roll_dice()}))


# Must be done this way to not conflict with main thread
asyncio.get_event_loop().create_task(main())
