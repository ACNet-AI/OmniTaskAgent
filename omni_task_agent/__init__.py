"""
OmniTaskAgent

A powerful multi-model task management system that can both integrate with various task management systems 
and help users choose and use the most suitable task management solution.
"""

import os
import sys
from pathlib import Path

from omni_task_agent.config import setup_environment
from omni_task_agent.agent import make_graph

__version__ = "0.1.0"
__author__ = "OmniTaskAgent Team"

# Export API
__all__ = [
    "make_graph",    # Async context manager for creating agent graph
    "setup_environment",  # Environment configuration tool
]

# Ensure current directory is in path
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

# Add project root directory to path
project_root = Path(__file__).parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

if __name__ == "__main__":
    # Run command line interface
    from omni_task_agent.cli import main
    main()
