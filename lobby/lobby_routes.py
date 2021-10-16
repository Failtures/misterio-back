from fastapi import APIRouter
from extensions import lobbyservice

router = APIRouter()


@router.get('/get-lobbies')
def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return [{'lobbies': [lobby.to_dict() for lobby in lobbies]}]
