from extensions import matchservice, lobbyservice
from util.vector import Vector2d

async def match_endpoints(parsedjson, websocket):
    if parsedjson['action'] == 'match_end_turn':
        await end_turn(parsedjson, websocket)
    elif parsedjson['action'] == 'match_roll_dice':
        await roll_dice(parsedjson, websocket)
    elif parsedjson['action'] == 'match_move':
        await move(parsedjson, websocket)
    elif parsedjson['action'] == 'match_get_hand':
        await get_hand(parsedjson, websocket)
    elif parsedjson['action'] == 'match_use_witch':
        await use_salem_witch(parsedjson, websocket)        
    elif parsedjson['action'] == 'match_accuse':
        await accuse(parsedjson, websocket)
    elif parsedjson['action'] == 'match_suspect':
        await suspect(parsedjson, websocket)
    elif parsedjson['action'] == 'match_question_res':
        await suspect_response(parsedjson, websocket)


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


async def get_hand(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
        player_name = parsedjson['player_name']
        player = matchservice.get_player_in_match(match, player_name)
        hand = match.get_hand(player_name)
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

    if websocket.client.host != player.socket.client.host:
        await websocket.client.socket.send_json(
            {'action': 'failed', 'info': "You are not ${player.nickname}"})

    for i in range(0, len(hand)):
        hand[i] = hand[i].to_dict()

    await player.socket.send_json({'action': 'get_hand', 'hand': hand})
    

async def use_salem_witch(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
        player_name = parsedjson['player_name']
        player = matchservice.get_player_in_match(match, player_name)
        card_type = parsedjson['card_type']
    
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return
    
    # Check if Salem Witch is in the player hand
    try:
        if match.player_has_witch(player_name):
            if card_type == "MONSTER":
                await player.socket.send_json({'action': 'mystery_card', 'card': match.mystery[0].to_dict()})
            elif card_type == "VICTIM":
                await player.socket.send_json({'action': 'mystery_card', 'card': match.mystery[1].to_dict()})
            elif card_type == "ROOM":
                await player.socket.send_json({'action': 'mystery_card', 'card': match.mystery[2].to_dict()})
            match.delete_witch(player_name)
        else:
            await player.socket.send_json({'action': 'failed', 'info': "You don't have the salem witch"})
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

async def accuse(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)

        # Fails if is not the turn of the requesting player
        if match.current_turn().socket != websocket:
            raise Exception ("It's not your turn")

        monster = parsedjson['monster']
        victim = parsedjson['victim']
        room = parsedjson['room']
        
        if(match.mystery[0].name == monster and match.mystery[1].name == victim and match.mystery[2].name == room):
            for player in match.players:
                await player.socket.send_json({'action': 'game_over', 'winner': match.current_turn().nickname})
            matchservice.delete_match(match)
            lobby = lobbyservice.get_lobby_by_name(match_name)
            lobbyservice.delete_lobby(lobby)

        else:
            for player in match.players:
                await player.socket.send_json({'action': 'player_deleted', 'loser': match.current_turn().nickname})
                match.players.remove(match.current_turn())

    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})


async def suspect(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
        player_name = parsedjson['player_name']
        player = matchservice.get_player_in_match(match, player_name)
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

    if match.current_turn().socket.client.host != websocket.client.host:
        websocket.send_json({'action': 'failed', 'info': "It's not your turn"})
        return

    if (str(match.board.get_player_square(player_name)) == 'None' or
        str(match.board.get_player_square(player_name)) == 'Regular' or
        str(match.board.get_player_square(player_name)) == 'Animal' or
        str(match.board.get_player_square(player_name)) == 'Trap'):
        await player.socket.send_json({'action': 'failed', 'info': 'You must be in a room to suspect'})
    room = str(match.board.get_player_square(player_name))
    if room != parsedjson['room']:
        await player.socket.send_json({'action': 'failed', 'info': f"You are not in ${parsedjson['room']}"})
        return

    monster = parsedjson['monster']
    victim = parsedjson['victim']

    for i in range(0, len(match.players)):
        if match.players[i] == player:
            player_turn = i

    await match.players[(player_turn+1)%len(match.players)].socket.send_json(
        {'action': 'question', 'monster': monster, 'victim': victim, 'room': room})


async def suspect_response(parsedjson, websocket):
    try:
        match_name = parsedjson['match_name']
        match = matchservice.get_match_by_name(match_name)
        player_name = parsedjson['player_name']
        player = matchservice.get_player_in_match(match, player_name)
        reply_to = parsedjson['reply_to']
        reply_to_player = matchservice.get_player_in_match(match, reply_to)
    except Exception as e:
        await websocket.send_json({'action': 'failed', 'info': str(e)})
        return

    for i in range(0, len(match.players)):
        if match.players[i] == player:
            player_turn = i
    
    if parsedjson['response'] == 'negative':
        if match.players[(player_turn+1)%len(match.players)] == reply_to_player:
            await reply_to_player.socket.send_json({'action': 'suspect_response', 'card': None})
        else:
            room = str(match.get_player_square(player_name))
            monster = parsedjson['monster']
            victim = parsedjson['victim']

            await match.players[(player_turn+1)%len(match.players)].socket.send_json(
                {'action': 'question', 'monster': monster, 'victim': victim, 'room': room})                
    elif parsedjson['response'] == 'affirmative':
        reply_card = parsedjson['reply_card']

        await reply_to_player.socket.send_json(
                {'action': 'suspect_response', 'card': reply_card})
