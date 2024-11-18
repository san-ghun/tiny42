"""Configuration settings for Dorker.

This module contains all configurable settings for Dorker including:
- Workspace directory path
- Terminal colors for output
- Docker port publishing configuration
"""

import os
from typing import Optional

# Fill in the directory name that contains all your 42 projects
DORKER_WORKSPACE: str = os.path.join(os.environ['HOME'], 'Projects/42berlin')
DORKER_ECHO_ON_STARTUP: bool = True

# Terminal colors
DORKER_GREEN = '\033[0;32m'  # Used for success messages
DORKER_BLUE = '\033[0;36m'   # Used for instructions/guides
DORKER_RED = '\033[0;31m'    # Used for errors/warnings
DORKER_WHITE = '\033[0m'

# Docker port publishing configuration
# Set to True to enable port publishing
DORKER_PORT_PUBLISHING: bool = False
# Host port number (on your machine)
DORKER_PORT_PUBLISHING_HOST: int = 8080
# Container port number (inside Docker)
DORKER_PORT_PUBLISHING_CONTAINER: int = 8080

def get_port_mapping() -> Optional[str]:
    """Get Docker port mapping string if enabled.
    
    Returns:
        Optional[str]: Port mapping in format '-p HOST:CONTAINER' if enabled,
                      None if port publishing is disabled
    """
    if DORKER_PORT_PUBLISHING:
        return f'-p {DORKER_PORT_PUBLISHING_HOST}:{DORKER_PORT_PUBLISHING_CONTAINER}'
    return None