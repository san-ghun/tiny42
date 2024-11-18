"""Configuration settings for tiny42.

This module contains all configurable settings for tiny42 including:
- Workspace directory path
- Terminal colors for output
- Docker port publishing configuration
"""

import os
from typing import Optional

# Fill in the directory name that contains all your 42 projects
TINY42_WORKSPACE: str = os.path.join(os.environ['HOME'], 'Projects/42berlin')
TINY42_ECHO_ON_STARTUP: bool = True

# Terminal colors
TINY42_GREEN = '\033[0;32m'  # Used for success messages
TINY42_BLUE = '\033[0;36m'   # Used for instructions/guides
TINY42_RED = '\033[0;31m'    # Used for errors/warnings
TINY42_WHITE = '\033[0m'

# Docker port publishing configuration
# Set to True to enable port publishing
TINY42_PORT_PUBLISHING: bool = False
# Host port number (on your machine)
TINY42_PORT_PUBLISHING_HOST: int = 8080
# Container port number (inside Docker)
TINY42_PORT_PUBLISHING_CONTAINER: int = 8080

def get_port_mapping() -> Optional[str]:
    """Get Docker port mapping string if enabled.
    
    Returns:
        Optional[str]: Port mapping in format '-p HOST:CONTAINER' if enabled,
                      None if port publishing is disabled
    """
    if TINY42_PORT_PUBLISHING:
        return f'-p {TINY42_PORT_PUBLISHING_HOST}:{TINY42_PORT_PUBLISHING_CONTAINER}'
    return None