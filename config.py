import os

from pydantic import BaseSettings


class Development(BaseSettings):
    ENDPOINT_CORS = os.getenv('ENDPOINT_CORS') or "*"
    TIMEOUT = 45


class Test(BaseSettings):
    ENDPOINT_CORS = os.getenv('ENDPOINT_CORS') or "*"
    TIMEOUT = 1


env = os.getenv('env') or 'dev'
env = env.lower()

if env.startswith('dev'):
    settings = Development()
elif env.startswith('test'):
    settings = Test()


# Dynamically return settings
def getSettings():
    return settings
