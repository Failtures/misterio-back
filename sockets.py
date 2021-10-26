import asyncio
import json


from fastapi import APIRouter, WebSocket
from lobby.lobby_ws import lobby_endpoints
from matches.match_ws import match_endpoints

router = APIRouter()


@router.websocket('/ws')
async def endpoints(websocket:WebSocket):
    await websocket.accept()
    print(f'New connection from {websocket.client.host}')
    # Keeps socket alive
    while True:
        try:
            data = await websocket.receive_json()
        except Exception as e:
            print(f'{websocket.client.host} Socket crashed, reason: {e}')
            break
        parsedjson = data

        if parsedjson['action'].startswith('lobby'):
            await lobby_endpoints(parsedjson, websocket)
        elif parsedjson['action'].startswith('match'):
            await match_endpoints(parsedjson, websocket)
