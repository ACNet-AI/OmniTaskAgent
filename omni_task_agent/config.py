"""
Configuration Module

Provides environment variable setup and configuration functionality
"""

import getpass
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


def setup_environment(interactive=False) -> Dict[str, str]:
    """Set up environment variables and load .env file

    First tries to load environment variables from .env file, then sets default values or gets them through interactive prompts.
    
    Args:
        interactive: Whether to prompt interactively for missing API keys, defaults to False
    
    Returns:
        Dictionary containing key environment variables and their values
    
    Examples:
        # Silent mode, use default values
        setup_environment()
        
        # Interactive mode, prompt for missing API keys
        setup_environment(interactive=True)
    """
    # Try to load .env file
    load_dotenv()
    
    # Set default environment variables
    if "PROJECT_ROOT" not in os.environ:
        os.environ["PROJECT_ROOT"] = str(Path(__file__).parent.parent)
    
    # Set API keys (may require interactive prompts)
    api_key_set = False
    
    # Check OpenAI API key first
    if "OPENAI_API_KEY" not in os.environ:
        if interactive:
            try:
                os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY: ")
                api_key_set = True
            except (KeyboardInterrupt, EOFError):
                print("\nOpenAI API key input cancelled")
    else:
        api_key_set = True
    
    # If no OpenAI API key, check Anthropic API key
    if not api_key_set and "ANTHROPIC_API_KEY" not in os.environ:
        if interactive:
            try:
                os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("ANTHROPIC_API_KEY: ")
                api_key_set = True
            except (KeyboardInterrupt, EOFError):
                print("\nAnthropic API key input cancelled")
    elif "ANTHROPIC_API_KEY" in os.environ:
        api_key_set = True
    
    # Set OpenAI API base URL (for third-party API services like WildCard)
    if "OPENAI_API_BASE" not in os.environ:
        # Default not set, use official OpenAI API
        # For third-party API, set in .env, e.g.:
        # OPENAI_API_BASE=https://api.gptsapi.net/v1
        pass
    
    # Other default configurations
    if "OMNI_TASK_API_URL" not in os.environ:
        os.environ["OMNI_TASK_API_URL"] = "http://localhost:8000"
    
    if "LLM_MODEL" not in os.environ:
        os.environ["LLM_MODEL"] = "gpt-4o"
    
    if "TEMPERATURE" not in os.environ:
        os.environ["TEMPERATURE"] = "0.2"
    
    if "MAX_TOKENS" not in os.environ:
        os.environ["MAX_TOKENS"] = "4000"
    
    # Return key environment variables
    return {
        "API_KEY_SET": str(api_key_set),
        "PROJECT_ROOT": os.environ["PROJECT_ROOT"],
        "OMNI_TASK_API_URL": os.environ["OMNI_TASK_API_URL"],
        "LLM_MODEL": os.environ["LLM_MODEL"],
        "OPENAI_API_BASE": os.environ.get("OPENAI_API_BASE", "default")
    } 