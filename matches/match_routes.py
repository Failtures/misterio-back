from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import matchservice

router = APIRouter()


@router.put('/end-turn')
async def end_turn(name: str):
    match = matchservice.get_match_by_name(name)
    match.next_turn()
    return JSONResponse(content={'current_turn': match._currentturn},
                        status_code=200)


@router.get('/roll-dice')
async def roll_dice(name: str):
    match = matchservice.get_match_by_name(name)
    return JSONResponse(content={'dice': match.roll_dice(),
                                'info': "Dice rolled"},
                        status_code=200)