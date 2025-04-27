import os
from unittest.mock import patch

from omni_task_agent.agent import make_graph, get_server_config


class TestAgent:
    """Agent Module Tests"""
    
    @patch.dict(os.environ, {"PROJECT_ROOT": "/test/path"})
    @patch("os.path.exists", return_value=True)
    @patch("os.makedirs")  # Mock makedirs to avoid filesystem errors
    def test_get_server_config(self, mock_makedirs, mock_exists):
        """Test server configuration generation"""
        config = get_server_config()
        
        # Verify configuration structure
        assert "shrimp-task-manager" in config
        assert config["shrimp-task-manager"]["transport"] == "stdio"
        assert config["shrimp-task-manager"]["command"] == "node"
        assert "/test/path/node_modules/mcp-shrimp-task-manager/dist/index.js" in config["shrimp-task-manager"]["args"][0]
        
        # Verify environment variables
        env = config["shrimp-task-manager"]["env"]
        assert "DATA_DIR" in env
        assert "/test/path/data" in env["DATA_DIR"]
        assert env["ENABLE_THOUGHT_CHAIN"] == "true"
    
    @patch.dict(os.environ, {"PROJECT_ROOT": "/test/path"})
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")  # Mock makedirs to avoid filesystem errors
    def test_get_server_config_npx(self, mock_makedirs, mock_exists):
        """Test server configuration generation - npx mode"""
        config = get_server_config()
        
        # Verify npx usage
        assert config["shrimp-task-manager"]["command"] == "npx"
        assert config["shrimp-task-manager"]["args"] == ["-y", "mcp-shrimp-task-manager"]
    
    def test_make_graph_exists(self):
        """Test make_graph function existence"""
        assert callable(make_graph) 