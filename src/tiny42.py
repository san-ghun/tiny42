"""Core functionality for tiny42.

This module provides the main functionality for:
- Running commands inside Docker containers
- Managing container lifecycle
- Initializing and reloading containers
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union
from .settings import *
from .docker import open_docker, setup_goinfre_docker
from .settings import get_port_mapping

def _check_environment() -> bool:
    """Verify the execution environment is valid.
    
    Checks:
    - Current directory is within configured workspace
    - Docker is running
    - tiny42 container exists and is running
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    current_path: str = os.getcwd()
    
    # Check if current path is within workspace
    if not current_path.startswith(TINY42_WORKSPACE):
        print(f"{TINY42_RED}You are not inside the workspace specified.{TINY42_WHITE}")
        print(f"{TINY42_BLUE}tiny42 can only be ran inside the specified workspace, "
              f"currently it is set to \"{TINY42_WORKSPACE}\".{TINY42_WHITE}")
        return False
    
    # Check if tiny42 container is running
    try:
        output: str = subprocess.check_output(['docker', 'ps'], text=True)
        if 'tiny42' not in output:
            # Check if image exists
            images: str = subprocess.check_output(['docker', 'images'], text=True)
            if 'tiny42' not in images:
                init_tiny42()
            else:
                run_cmd: List[str] = ['docker', 'run', '-itd']
                port_mapping: Optional[str] = get_port_mapping()
                if port_mapping:
                    run_cmd.append(port_mapping)
                    
                run_cmd.extend([
                    '-v', f'{TINY42_WORKSPACE}:/tiny42_workspace',
                    '--name=tiny42', 'tiny42'
                ])
                
                subprocess.run(run_cmd)
    except subprocess.CalledProcessError:
        return False
    
    return True

def run_tiny42_command(args: List[str]) -> None:
    """Execute a command inside the tiny42 container.
    
    Args:
        args: List of command arguments to execute
        
    The command is executed in the same relative path inside the container
    as the current working directory is to TINY42_WORKSPACE.
    
    Special cases:
        - Empty args list: shows help message
        - First arg is -h or --help: shows help message
    """
    if not args or args[0] in ("--help", "-h"):
        show_help()
        return

    if not _check_environment():
        return

    current_path: str = os.getcwd()
    relative_path: str = os.path.relpath(current_path, TINY42_WORKSPACE)
    
    command: str = ' '.join(args)
    subprocess.run(['docker', 'exec', '-it', 'tiny42', 'bash', '-c',
                   f"cd '/tiny42_workspace/{relative_path}' && {command}"])

def init_tiny42() -> None:
    """Initialize the tiny42 container environment.
    
    - Prompts for goinfre setup if needed
    - Ensures Docker is running
    - Builds container image if needed
    - Creates and starts container with proper volume mounts
    """
    response: str = input(f"{TINY42_RED}tiny42 wants to know if you want to setup "
                    f"Docker inside goinfre. Do you want to setup Docker within "
                    f"goinfre? [y/N]{TINY42_WHITE}\n")
    
    if response.lower() == 'y':
        setup_goinfre_docker()

    open_docker()
    
    try:
        # Check if container exists
        output: str = subprocess.check_output(['docker', 'ps', '-a'], text=True)
        if 'tiny42' in output:
            subprocess.run(['docker', 'start', 'tiny42'])
        else:
            # Build and run new container
            dockerfile_path: Path = Path(__file__).parent / 'Dockerfile'
            subprocess.run(['chmod', '755', str(dockerfile_path)])
            subprocess.run(['docker', 'build', '.', '-t', 'tiny42', 
                          '-f', str(dockerfile_path)])
            
            run_cmd: List[str] = ['docker', 'run', '-itd']
            port_mapping: Optional[str] = get_port_mapping()
            if port_mapping:
                run_cmd.append(port_mapping)
                
            run_cmd.extend([
                '-v', f'{TINY42_WORKSPACE}:/tiny42_workspace',
                '--name=tiny42', 'tiny42'
            ])
            
            subprocess.run(run_cmd)
            
        print(f"{TINY42_GREEN}tiny42 is running in {TINY42_WORKSPACE}{TINY42_WHITE}")
    except subprocess.CalledProcessError:
        print(f"{TINY42_RED}Failed to build the tiny42 image{TINY42_WHITE}")

def reload_tiny42() -> None:
    """Rebuild and restart the tiny42 container.
    
    - Rebuilds the container image
    - Stops and removes existing container
    - Creates new container with updated image
    - Maintains same volume mounts and port mappings
    """
    open_docker()
    
    dockerfile_path: Path = Path(__file__).parent / 'Dockerfile'
    subprocess.run(['docker', 'build', '.', '-t', 'tiny42', 
                   '-f', str(dockerfile_path)])
    subprocess.run(['docker', 'stop', 'tiny42'])
    subprocess.run(['docker', 'rm', 'tiny42'])
    
    run_cmd: List[str] = ['docker', 'run', '-itd']
    port_mapping: Optional[str] = get_port_mapping()
    if port_mapping:
        run_cmd.append(port_mapping)
        
    run_cmd.extend([
        '-v', f'{TINY42_WORKSPACE}:/tiny42_workspace',
        '--name=tiny42', 'tiny42'
    ])
    
    subprocess.run(run_cmd)
    print(f"{TINY42_GREEN}tiny42 is reloaded and restarted{TINY42_WHITE}")

def show_help() -> None:
    """Show help message with available commands and configuration info."""
    print(f"{TINY42_BLUE}\ntiny42 - A Docker-based development environment manager")
    print(f"\nKeep coding with your portable 42")
    print(f"\nConfiguration:")
    print(f"  Workspace: {TINY42_WORKSPACE}")
    print("  Settings: ~/.config/tiny42/src/settings.py")
    print("  Dockerfile: ~/.config/tiny42/src/Dockerfile")
    
    print("\nUsage:")
    print("  tiny42 [command] [args...]")
    
    print("\nCommands:")
    print("  tiny42 <command>       Execute command inside the tiny42 container")
    print("  --init, -i             Initialize the tiny42 container")
    print("  --reload, -r           Rebuild and restart the tiny42 container")
    print("  --open-docker, -o      Start Docker daemon if not running")
    print("  --goinfre-docker, -g   Setup Docker in goinfre directory (42 School specific)")
    print("  --help, -h             Show this help message")
    
    if TINY42_PORT_PUBLISHING:
        print(f"\nPort Publishing:")
        print(f"  Host port {TINY42_PORT_PUBLISHING_HOST} -> Container port {TINY42_PORT_PUBLISHING_CONTAINER}")
    
    print(f"{TINY42_WHITE}")
