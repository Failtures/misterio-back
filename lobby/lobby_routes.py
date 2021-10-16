from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import lobbyservice

router = APIRouter()


@router.get('/get-lobbies')
def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return JSONResponse(content={'lobbies': [lobby.to_dict() for lobby in lobbies]},
                        status_code=200)

@router.post('/create-lobby')
def create_lobby(name: str, host:str):
    lobbyservice.create_new_lobby(name, host)
    return ("Lobby created")

@router.put('/add-player')
def add_player(name:str, player:str):
    lobbyservice.add_player(name, player)
    return ("Player added")