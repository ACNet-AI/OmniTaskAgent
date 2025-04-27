"""
OmniTask Agent

This module implements a powerful multi-model task management system using LangGraph.
"""

import os
import logging
from contextlib import asynccontextmanager

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from omni_task_agent.config import setup_environment

# Setup logging and environment
logger = logging.getLogger(__name__)
setup_environment()

# Get configuration
model_name = os.environ.get("LLM_MODEL", "gpt-4o")
openai_base_url = os.environ.get("OPENAI_API_BASE")

# Define server configuration
def get_server_config():
    """Get server configuration"""
    project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
    
    # Find shrimp-task-manager executable path
    # 1. First try to find in project node_modules
    node_modules_path = os.path.join(project_root, "node_modules", "mcp-shrimp-task-manager", "dist", "index.js")
    
    # 2. If not found, try global npm path
    npx_path = "npx"
    
    if os.path.exists(node_modules_path):
        logger.info(f"Using locally installed shrimp-task-manager: {node_modules_path}")
        command = "node"
        args = [node_modules_path]
    else:
        logger.info("Using npx to run shrimp-task-manager")
        command = npx_path
        args = ["-y", "mcp-shrimp-task-manager"]
    
    # Prepare environment variables
    data_dir = os.path.join(project_root, "data")
    os.makedirs(os.path.abspath(data_dir), exist_ok=True)
    
    env = {
        "DATA_DIR": data_dir,
        "PATH": os.environ.get("PATH", ""),
        "ENABLE_THOUGHT_CHAIN": "true"
    }
    
    return {
        "shrimp-task-manager": {
            "transport": "stdio",
            "command": command,
            "args": args,
            "env": env,
            "encoding": "utf-8",                # Ensure UTF-8 encoding
            "encoding_error_handler": "replace" # Key modification: change strict to replace
        }
    }

# Create graph using asynccontextmanager
@asynccontextmanager
async def make_graph():
    """
    Create and provide agent graph following langgraph-api standard
    
    Usage:
    ```python
    async with make_graph() as agent:
        response = await agent.ainvoke({"messages": messages})
    ```
    """
    logger.info("Creating MCP client...")
    async with MultiServerMCPClient(get_server_config()) as client:
        logger.info("Getting tools list...")
        tools = client.get_tools()
        tool_count = len(tools) if tools else 0
        logger.info(f"Got {tool_count} tools")
        
        logger.info("Creating LLM...")
        # Create LLM directly in function
        llm_args = {"model": model_name}
        if openai_base_url:
            llm_args["openai_api_base"] = openai_base_url
        
        llm = ChatOpenAI(**llm_args)
        
        logger.info("Creating prompt template...")
        # Create prompt template directly in function
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Task Master Assistant, designed to help users create, manage, and analyze project tasks.

            You can perform the following operations:
            - Create Tasks: Create new tasks from scratch
            - List Tasks: View all current tasks
            - Update Tasks: Modify task details or status
            - Decompose Tasks: Break down large tasks into subtasks
            - Set Dependencies: Establish relationships between tasks
            - Analyze Projects: Analyze project complexity and task structure

            Based on the user's request, choose the most appropriate tool and provide clear, concise responses.
            Always prioritize helping users efficiently achieve their task management goals."""),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        logger.info("Creating agent...")
        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=prompt
        )
        
        yield agent
