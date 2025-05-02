import warnings
# from automcp.adapters.langgraph import create_langgraph_adapter  # Comment out original import
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

# Import LangGraph instance from omni_task_agent
from omni_task_agent.agent import make_graph
# Import our custom adapter implementation
from adapters import create_langgraph_async_adapter

# Create MCP server
mcp = FastMCP("OmniTask Agent MCP Server", log_level="DEBUG")

# Suppress warnings that might interfere with STDIO transport
warnings.filterwarnings("ignore")

# Define input schema to match omni_task_agent requirements
class InputSchema(BaseModel):
    prompt: str
    projectRoot: str = None
    file: str = None

name = "OmniTask Agent"
description = "A powerful multi-model task management system that can both integrate with various task management systems and help users choose and use the most suitable task management solution"

# Create LangGraph adapter
# Use make_graph as async context manager
# Note: This returns an async function, FastMCP supports registering async tool functions
mcp_langgraph_agent = create_langgraph_async_adapter(
    agent_instance=make_graph,  # Use make_graph async context manager from omni_task_agent.agent
    name="OmniTask_Agent",
    description=description,
    input_schema=InputSchema,
)

# Register async tool to FastMCP
# FastMCP supports registering async functions as tools, no sync conversion needed
mcp.add_tool(
    mcp_langgraph_agent,
    name=name,
    description=description
)

# Server entrypoints
def serve_sse():
    mcp.run(transport="sse")

def serve_stdio():
    # Redirect stderr to suppress warnings that bypass the filters
    import os
    import sys

    class NullWriter:
        def write(self, *args, **kwargs):
            pass
        def flush(self, *args, **kwargs):
            pass

    # Save the original stderr
    original_stderr = sys.stderr

    # Replace stderr with our null writer to prevent warnings from corrupting STDIO
    sys.stderr = NullWriter()

    # Set environment variable to ignore Python warnings
    os.environ["PYTHONWARNINGS"] = "ignore"

    try:
        mcp.run(transport="stdio")
    finally:
        # Restore stderr for normal operation
        sys.stderr = original_stderr

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "sse":
        serve_sse()
    else:
        serve_stdio()