import sys

from lobby.lobby_routes import router as lobbyrouter
from fastapi import FastAPI

# Activates terminal colors for windows users
if sys.platform == 'win32':
    import os;os.system('color')

app = FastAPI()
app.include_router(lobbyrouter)