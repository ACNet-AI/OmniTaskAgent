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
    
    # Create agent session
    try:
        # Test agent creation
        has_tools = True
        async with make_graph() as agent:
            # We just test if we can create it, no further operations needed
            pass
    except Exception as e:
        logger.error(f"Error loading agent: {str(e)}")
        has_tools = False
    
    # Initialize chat history
    messages = []
    
    # Display welcome message
    print("\n=== OmniTask Command Line Interface ===")
    print("Welcome to OmniTask! Type 'exit' to end session, 'help' to see available commands.")
    
    if has_tools:
        print("You can perform the following common operations:")
        operations = ["Plan task workflow", "Show all tasks", "Update task content", 
                      "Execute specific task", "Break down complex tasks into subtasks"]
        for op in operations:
            print(f"- {op}")
    else:
        print("Warning: Failed to load agent, functionality may be limited")
    
    # Interactive loop
    try:
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
                        # Dynamically get tool list
                        async with make_graph() as agent:
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
                    
                    # Call agent
                    async with make_graph() as agent:
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
    finally:
        # No need to explicitly clean up resources
        pass


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