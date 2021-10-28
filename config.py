import os

from pydantic import BaseSettings


class Development(BaseSettings):
    ENDPOINT_CORS = os.getenv('ENDPOINT_CORS') or "*"


env = os.getenv('env') or 'dev'
env = env.lower()

if env.startswith('dev'):
    settings = Development()
