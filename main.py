import sys
import threading

from lobby.lobby_routes import router as lobbyrouter
from matches.match_routes import router as matchrouter
from fastapi import FastAPI
from server import start_server

# Activates terminal colors for windows users
if sys.platform == 'win32':
    import os;os.system('color')

app = FastAPI()
app.include_router(lobbyrouter)
app.include_router(matchrouter)

server_thread = threading.Thread(target=start_server)
server_thread.start()
