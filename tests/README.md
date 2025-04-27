# Tests

Unit and integration tests for OmniTaskAgent using pytest.

## Structure

```
tests/
├── __init__.py     # Package marker
├── conftest.py     # Shared fixtures
├── test_agent.py   # Agent tests
├── test_cli.py     # CLI tests
├── test_config.py  # Config tests
└── test_integration.py  # Integration tests
```

## Usage

```bash
# Run all tests
pytest

# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run specific test file
pytest tests/test_config.py

# Generate coverage report
pytest --cov=omni_task_agent --cov-report=html
```

## Guidelines

1. Name test files as `test_*.py`
2. Use descriptive test names with `test_` prefix
3. Include docstrings for test purpose
4. Use `@pytest.mark.asyncio` for async tests
5. Use mocks to avoid external dependencies

## Fixtures

- `mock_env_vars`: Environment variables for testing 