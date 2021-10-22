from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import matchservice
from .match import Match

router = APIRouter()

@router.post('/end-turn')
def end_turn(name: str):
    match = matchservice.get_match_by_name(name)
    match.next_turn()
    return JSONResponse(content={'current turn': match._current_turn,
                                'current player': match.current_player()},
                        status_code=200)