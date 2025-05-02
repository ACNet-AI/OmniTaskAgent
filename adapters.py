"""Custom adapter module for supporting async context manager LangGraph adapters"""

import textwrap
import logging
from typing import Callable, Type, AsyncContextManager
from pydantic import BaseModel

# Setup logging
logger = logging.getLogger(__name__)

def create_langgraph_async_adapter(
    agent_instance: AsyncContextManager,
    name: str,
    description: str,
    input_schema: Type[BaseModel],
) -> Callable:
    """
    Create a LangGraph adapter that supports async context managers
    
    Args:
        agent_instance: Async context manager, like make_graph
        name: Tool name
        description: Tool description
        input_schema: Pydantic model for input data
        
    Returns:
        Adapted async function that can be called by MCP server
    """
    
    # Get input schema fields
    schema_fields = input_schema.model_fields

    # Create parameter string
    params_str = ", ".join(
        f"{field_name}: {getattr(field_info.annotation, '__name__', 'Any')}"
        for field_name, field_info in schema_fields.items()
    )

    # Create function body that directly returns async function
    body_str = textwrap.dedent(f"""
    async def run_agent({params_str}):
        inputs = input_schema({', '.join(f'{name}={name}' for name in schema_fields)})
        logger.info(f"Received request with projectRoot: {{inputs.projectRoot}}")
        logger.info(f"File parameter: {{inputs.file if hasattr(inputs, 'file') else None}}")
        
        async with agent_instance(inputs.projectRoot) as agent:
            logger.info(f"Invoking agent with prompt: {{inputs.prompt[:50]}}...")
            result = await agent.ainvoke({{"messages": [{{"role": "user", "content": inputs.prompt}}]}})
            logger.info("Agent invocation completed")
        return result
    """)

    # Create namespace
    namespace = {
        "input_schema": input_schema,
        "agent_instance": agent_instance,
        "logger": logger
    }

    # Execute function definition
    exec(body_str, namespace)

    # Get created function
    run_agent = namespace["run_agent"]

    # Add function metadata
    run_agent.__name__ = name
    run_agent.__doc__ = description

    return run_agent 