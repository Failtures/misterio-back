from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import lobbyservice

router = APIRouter()


@router.get('/get-lobbies')
def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return JSONResponse(content={'lobbies': [lobby.to_dict() for lobby in lobbies]},
                        status_code=200)
