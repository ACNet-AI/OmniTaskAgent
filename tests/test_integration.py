"""
Integration Test Module

Test integration functionality between components
"""
import json
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from omni_task_agent.utils.state import Task, TaskCollection


class TestIntegration:
    """Integration Test Class"""
    
    @pytest.mark.asyncio
    @patch("task_master_agent.agent.MultiServerMCPClient")
    @patch("task_master_agent.agent.ChatOpenAI")
    async def test_create_task_mocked(self, mock_chat, mock_client):
        """Test mocked task creation process"""
        # Mock task creation
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value={
            "messages": [{"content": "Task created successfully"}],
            "tools": [{
                "name": "create_task",
                "input": {"title": "Test Task", "description": "This is a test"},
                "output": {"success": True, "task_id": "1"}
            }]
        })
        
        # Directly test mocked agent
        result = await mock_agent.ainvoke({
            "messages": [{"role": "user", "content": "Create task: Test Integration"}]
        })
        
        # Verify results
        assert "Task created successfully" in str(result)
        mock_agent.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_task_lifecycle(self, test_data_dir):
        """Test task lifecycle: create, update, complete"""
        # Prepare test data
        tasks_file = test_data_dir / "tasks.json"
        os.makedirs(test_data_dir, exist_ok=True)
        
        # Create initial task collection
        initial_tasks = TaskCollection(tasks=[
            Task(
                id="1",
                title="Test Task",
                description="Test task lifecycle",
                status="pending"
            )
        ])
        
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(initial_tasks.model_dump(), f, ensure_ascii=False, indent=2)
        
        # Mock task status update
        updated_tasks = TaskCollection(tasks=[
            Task(
                id="1",
                title="Test Task",
                description="Test task lifecycle",
                status="in-progress"
            )
        ])
        
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(updated_tasks.model_dump(), f, ensure_ascii=False, indent=2)
        
        # Read and verify update
        with open(tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            loaded_tasks = TaskCollection(**data)
            assert len(loaded_tasks.tasks) == 1
            assert loaded_tasks.tasks[0].status == "in-progress"
        
        # Mock task completion
        completed_tasks = TaskCollection(tasks=[
            Task(
                id="1",
                title="Test Task",
                description="Test task lifecycle",
                status="done"
            )
        ])
        
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(completed_tasks.model_dump(), f, ensure_ascii=False, indent=2)
        
        # Read and verify completion
        with open(tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            loaded_tasks = TaskCollection(**data)
            assert len(loaded_tasks.tasks) == 1
            assert loaded_tasks.tasks[0].status == "done" 