"""
CLI Module Tests
"""
import pytest
from unittest.mock import patch, MagicMock

from omni_task_agent.cli import main, async_main


class TestCLI:
    """CLI Module Test Class"""
    
    @pytest.mark.asyncio
    @patch("omni_task_agent.cli.input", return_value="exit")
    @patch("omni_task_agent.cli.make_graph")
    @patch("omni_task_agent.cli.setup_environment")
    async def test_async_main_exit(self, mock_setup_env, mock_make_graph, mock_input):
        """Test CLI main function - Exit"""
        # Setup mocks
        mock_agent_context = MagicMock()
        mock_make_graph.return_value.__aenter__.return_value = mock_agent_context
        
        # Execute test
        await async_main()
        
        # Verify calls
        mock_setup_env.assert_called_once()
        mock_make_graph.assert_called()
    
    @pytest.mark.asyncio
    @patch("omni_task_agent.cli.input", side_effect=["help", "exit"])
    @patch("omni_task_agent.cli.make_graph")
    @patch("omni_task_agent.cli.setup_environment")
    async def test_async_main_help(self, mock_setup_env, mock_make_graph, mock_input):
        """Test CLI main function - Help command"""
        # Setup mocks
        mock_agent_context = MagicMock()
        mock_agent_context.tools = [MagicMock(name="tool1", description="Test Tool")]
        mock_make_graph.return_value.__aenter__.return_value = mock_agent_context
        
        # Execute test
        await async_main()
        
        # Verify calls
        mock_setup_env.assert_called_once()
        mock_make_graph.assert_called()
        assert mock_input.call_count == 2
    
    @pytest.mark.asyncio
    @patch("omni_task_agent.cli.input", side_effect=["version", "exit"])
    @patch("omni_task_agent.cli.make_graph")
    @patch("omni_task_agent.cli.setup_environment")
    async def test_async_main_version(self, mock_setup_env, mock_make_graph, mock_input):
        """Test CLI main function - Version command"""
        # Setup mocks
        mock_agent_context = MagicMock()
        mock_make_graph.return_value.__aenter__.return_value = mock_agent_context
        
        # Execute test
        await async_main()
        
        # Verify calls
        mock_setup_env.assert_called_once()
        assert mock_input.call_count == 2
    
    @patch("omni_task_agent.cli.asyncio.run")
    def test_main(self, mock_run):
        """Test main function"""
        main()
        mock_run.assert_called_once()


if __name__ == "__main__":
    pytest.main() 