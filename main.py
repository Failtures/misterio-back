import sys

from lobby.lobby_routes import router as lobbyrouter
# from matches.match_routes import router as matchrouter
from fastapi import FastAPI
from sockets import main_socket

# Activates terminal colors for windows users
if sys.platform == 'win32':
    import os;os.system('color')

app = FastAPI()
app.include_router(lobbyrouter)
# app.include_router(matchrouter)
