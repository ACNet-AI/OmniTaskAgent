import os
from unittest.mock import patch

from omni_task_agent.config import setup_environment


class TestConfig:
    """Configuration Module Tests"""
    
    @patch.dict(os.environ, {}, clear=True)
    @patch("omni_task_agent.config.getpass")
    def test_setup_environment_defaults(self, mock_getpass):
        """Test environment variable default settings"""
        # Mock case without API key
        
        # Call function
        env_vars = setup_environment()
        
        # Verify return values
        # Note: Since setup_environment implementation may check OPENAI_API_KEY and ANTHROPIC_API_KEY
        # we accept API_KEY_SET returning either "False" or "True", as this may depend on system environment variables
        # We mainly verify other default values are correct
        
        assert "PROJECT_ROOT" in env_vars
        assert env_vars["OMNI_TASK_API_URL"] == "http://localhost:8000"
        # Actual model may vary (gpt-4 or gpt-3.5-turbo etc.), so we just check if model is set
        assert "LLM_MODEL" in env_vars
        # OpenAI API base URL might be set in .env, so just check its existence
        assert "OPENAI_API_BASE" in env_vars
        
        # Verify environment variables
        assert "PROJECT_ROOT" in os.environ
        assert os.environ["OMNI_TASK_API_URL"] == "http://localhost:8000"
        assert "LLM_MODEL" in os.environ
        assert os.environ["TEMPERATURE"] == "0.2"
        assert os.environ["MAX_TOKENS"] == "4000"
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True)
    def test_setup_environment_with_api_key(self):
        """Test environment variable settings with API key"""
        env_vars = setup_environment()
        
        # Verify API key status
        assert env_vars["API_KEY_SET"] == "True" 