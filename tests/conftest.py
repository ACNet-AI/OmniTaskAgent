"""
Test Configuration Module

Provides test fixtures and shared resources
"""
import os
import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Return test data directory path"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "test_data"
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


@pytest.fixture
def sample_task_json():
    """Return a sample task JSON"""
    return {
        "id": "1",
        "title": "Test Task",
        "description": "This is a task for testing",
        "status": "pending",
        "priority": "medium",
        "dependencies": [],
        "details": "Implement test functionality",
        "test_strategy": "Unit testing",
        "subtasks": [
            {
                "id": "1.1",
                "title": "Subtask 1",
                "description": "First subtask",
                "status": "pending",
                "dependencies": []
            },
            {
                "id": "1.2",
                "title": "Subtask 2",
                "description": "Second subtask",
                "status": "pending",
                "dependencies": ["1.1"]
            }
        ]
    }


@pytest.fixture
def mock_env_vars():
    """Set up test environment variables"""
    original_environ = os.environ.copy()
    
    # Set test environment variables
    os.environ["OPENAI_API_KEY"] = "test-api-key"
    os.environ["PROJECT_ROOT"] = "/test/project/path"
    os.environ["LLM_MODEL"] = "test-model"
    
    yield
    
    # Restore original environment variables
    os.environ.clear()
    os.environ.update(original_environ) 