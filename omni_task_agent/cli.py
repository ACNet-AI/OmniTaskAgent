"""
OmniTask Command Line Interface

This module provides a command line interface for interacting with the OmniTask agent.
"""

import logging
import os
import asyncio

from langchain_core.messages import AIMessage, HumanMessage
from omni_task_agent.config import setup_environment
from omni_task_agent.agent import make_graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("omni_task_cli")


async def async_main():
    """Command line interface main function"""
    # Set up environment
    setup_environment()
    
    # Initialize chat history
    messages = []
    
    # Display welcome message
    print("\n=== OmniTask Command Line Interface ===")
    print("Welcome to OmniTask! Type 'exit' to end session, 'help' to see available commands.")
    
    # Create agent session - Create agent instance once and reuse throughout the session
    try:
        has_tools = True
        agent = None
        
        # Use an async context manager to ensure proper resource management
        async with make_graph() as agent_instance:
            # Save agent instance for later use
            agent = agent_instance
            
            # Display feature list
            print("You can perform the following common operations:")
            operations = ["Plan task workflow", "Show all tasks", "Update task content", 
                        "Execute specific task", "Break down complex tasks into subtasks"]
            for op in operations:
                print(f"- {op}")
            
            # Interactive loop
            while True:
                try:
                    user_input = input("\nUser: ")
                    
                    # Handle special commands
                    if user_input.lower() in ["exit", "quit"]:
                        print("Goodbye!")
                        break
                        
                    if user_input.lower() == "help":
                        print("\nAvailable commands:")
                        print("- help: Show this help message")
                        print("- exit/quit: Exit program")
                        print("- version: Show version information")
                        
                        if has_tools:
                            # Get tools list
                            tools = agent.tools
                            print("\nAvailable tools:")
                            for tool in tools:
                                name = getattr(tool, "name", str(tool))
                                desc = getattr(tool, "description", "No description")
                                print(f"- {name}: {desc}")
                        continue
                        
                    if user_input.lower() == "version":
                        print("\nVersion information:")
                        print("OmniTask CLI v0.1.0")
                        print(f"Working directory: {os.getcwd()}")
                        continue
                    
                    # Process user input
                    if has_tools:
                        # Add user message to history
                        messages.append(HumanMessage(content=user_input))
                        
                        # Call agent - Reuse the created instance
                        response = await agent.ainvoke({"messages": messages})
                        
                        # Process response
                        if "messages" in response and response["messages"]:
                            output = response["messages"][-1].content
                            print(f"Assistant: {output}")
                            messages.append(AIMessage(content=output))
                        else:
                            print("Assistant: Unable to generate valid response, please try again.")
                    else:
                        print("Assistant: Sorry, I cannot fully process your request due to missing required tools.")
                    
                except KeyboardInterrupt:
                    print("\nOperation cancelled. Type 'exit' to quit.")
                except Exception as e:
                    logger.error(f"Processing error: {str(e)}")
                    print(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"Error loading agent: {str(e)}")
        print(f"Error: Could not initialize agent - {str(e)}")
        has_tools = False


def main():
    """CLI entry point"""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print("\nProgram exited.")
    except Exception as e:
        logger.error(f"CLI error: {str(e)}")
        print(f"Program error: {str(e)}")


if __name__ == "__main__":
    main()