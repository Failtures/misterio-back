# Install

- ```python -m pip install -r requirements.txt```

# Run
- ```python -m uvicorn main:app```

# Tests
- ```python -m unittest discover tests/```

# Notes for developers
- All tests using the FastAPI test client should extend the TestCaseFastAPI class
