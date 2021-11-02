from extensions import matchservice
from util.vector import Vector2d


async def match_endpoints(parsedjson, websocket):
    if parsedjson['action'] == 'match_end_turn':
        await end_turn(parsedjson, websocket)
    elif parsedjson['action'] == 'match_roll_dice':
        await roll_dice(parsedjson, websocket)
    elif parsedjson['action'] == 'match_move':
        await move(parsedjson, websocket)


async def end_turn(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

    # Fails if is not the turn of the requesting player
    if match.current_turn().socket.client.host != websocket.client.host:
        await websocket.send_json({'action': 'failed', 'info': "It's not your turn"})
        return
    match.next_turn()

    for player in match.players:
        await player.socket.send_json({'action': 'turn_passed', 'current_turn': match.current_turn().nickname})


async def roll_dice(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
    except Exception as e:
        websocket.send_json({'action': 'failed', 'info': str(e)})
        return

    # Fails if is not the turn of the requesting player
    if match.current_turn().socket.client.host != websocket.client.host:
        websocket.send_json({'action': 'failed', 'info': "It's not your turn"})
        return
    dice = match.roll_dice()

    for player in match.players:
        await player.socket.send_json({'action': 'roll_dice', 'dice': dice})


async def move(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        position = Vector2d(int(parsedjson['pos_x']), int(parsedjson['pos_y']))
        match = matchservice.get_match_by_name(match_name)
        square = match.move(position)
        new_pos = match.board.get_player_position(match.current_turn().nickname)

        for player in match.players:
            await player.socket.send_json({'action': 'player_position',
                                            'pos_x': new_pos.x, 'pos_y': new_pos.y, 'square': str(square)})
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

