# Install

---------------------------

- ```python -m pip install -r requirements.txt```

# Run

---------------------------

- ```python -m uvicorn main:app```

# Tests

---------------------------

- ```python -m unittest discover tests/```

# Notes for developers

---------------------------

- All tests using the FastAPI test client should extend the TestCaseFastAPI class

# Websockets protocol

---------------------------

Lobby:
``` {'name': str, 'host': str, 'current_players': int, 'players': [str] }```

Error:
```{'action': 'failed', 'info': str}```

## Lobby endpoint

### lobby_join
Takes: ```{'action': 'lobby_join', 'player_name': String, 
'lobby_name': String}```

Returns:
```'action': 'joined_lobby', 'lobby': Lobby }```

### lobby_create
Takes: ```{'action': 'lobby_create', 'host_name': str, 'lobby_name': str}```

Returns:
```{'action': 'new_lobby', 'lobby': Lobby}```


### Start match
Needs implementation


## Match endpoint
<small>Might have changed</small>

Takes:
```{'action': 'match_roll_dice'}```

Returns:
```{'action': 'roll_dice', 'dice': int}```



