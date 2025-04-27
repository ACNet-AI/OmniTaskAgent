#!/usr/bin/env python
"""
OmniTaskAgent Basic Usage Example

This example demonstrates how to use OmniTaskAgent to create and manage tasks
"""

import asyncio
import os
import logging
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from omni_task_agent.agent import make_graph
from omni_task_agent.config import setup_environment

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_example():
    """Run example"""
    try:
        # Load environment variables
        load_dotenv()
        setup_environment()
        
        # Print configuration information
        print("=== Configuration Information ===")
        print(f"Project root directory: {os.environ.get('PROJECT_ROOT')}")
        print(f"Using model: {os.environ.get('LLM_MODEL')}")
        print(f"API base URL: {os.environ.get('OPENAI_API_BASE', 'default')}")
        print()
        
        # Create agent
        print("=== Creating Agent ===")
        
        # Create and use agent with exception handling
        try:
            async with make_graph() as agent:
                # Create a simple task
                print("\n=== Create Task Example ===")
                create_task_response = await agent.ainvoke({
                    "messages": [
                        HumanMessage(content="Create a new task: Implement user registration with form validation")
                    ]
                })
                print_response(create_task_response)
                
                # List all tasks
                print("\n=== List Tasks Example ===")
                list_tasks_response = await agent.ainvoke({
                    "messages": [
                        HumanMessage(content="List all tasks")
                    ]
                })
                print_response(list_tasks_response)
                
        except UnicodeEncodeError as e:
            logger.error(f"Character encoding error: {e}")
            print("Encoding error: Possible due to API input or output containing non-ASCII characters")
        except Exception as e:
            logger.error(f"Error calling agent: {e}")
            print(f"Error: {e}")
            
    except Exception as e:
        logger.error(f"Error running example: {e}")
        print(f"Error: {e}")


def print_response(response):
    """Print agent response"""
    try:
        if "messages" in response and response["messages"]:
            # Print AI messages
            for message in response["messages"]:
                if "content" in message:
                    print(f"AI: {message['content']}")
        
        # Print tool calls
        if "tools" in response and response["tools"]:
            print("\nTool Calls:")
            for tool in response["tools"]:
                print(f"- Tool: {tool.get('name', 'Unknown')}")
                if "input" in tool:
                    print(f"   Input: {tool['input']}")
                if "output" in tool:
                    print(f"   Output: {tool['output']}")
        print("-" * 50)
    except Exception as e:
        logger.error(f"Error printing response: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(run_example())