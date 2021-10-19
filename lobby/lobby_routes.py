from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import lobbyservice
from users.user import User

router = APIRouter()


@router.get('/get-lobbies')
def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return JSONResponse(content={'lobbies': [lobby.to_dict() for lobby in lobbies]},
                        status_code=200)

@router.post('/create-lobby')
def create_lobby(name: str, host:str):
    #When you create your lobby, you have to provide your user name 
    host_user = User(host)
    lobbyservice.create_new_lobby(name, host_user)
    return JSONResponse(content={'lobby': lobbyservice.get_lobby_by_name(name).to_dict(),
                                'info': "Lobby was created"},
                                status_code=200)

@router.put('/join-player')
def join_player(name:str, player:str):
    try:
        lobbyservice.join_player(name, player)
        return JSONResponse(content={'lobby': lobbyservice.get_lobby_by_name(name).to_dict(),
                                    'info': "Player added"},
                            status_code=200)
    except Exception:
        return JSONResponse(content={'lobby': lobbyservice.get_lobby_by_name(name).to_dict(),
                                    'info': "The lobby is full or the player is already in the lobby"},
                            status_code=502)
