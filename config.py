import os

from pydantic import BaseSettings


class Development(BaseSettings):
    ENDPOINT_CORS = os.getenv('ENDPOINT_CORS') or "*"
    WEBSOCKETS_PORT = os.getenv('WEBSOCKETS_PORT') or 8080
    WEBSOCKETS_IP = os.getenv('WEBSOCKETS_IP') or "0.0.0.0"


env = os.getenv('env') or 'dev'
env = env.lower()

if env.startswith('dev'):
    settings = Development()
