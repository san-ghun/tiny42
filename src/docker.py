"""Docker management utilities for tiny42.

This module handles Docker-specific operations like:
- Starting the Docker daemon
- Setting up Docker in goinfre (for 42 School)
- Managing Docker container lifecycle
"""
import os
import time
import subprocess
from typing import List
from .settings import *

def open_docker() -> None:
    """Start Docker daemon if not running.
    
    - Checks if Docker daemon is running
    - Launches Docker application if needed
    - Waits for Docker to be fully started
    """
    try:
        # Check if Docker is running
        subprocess.run(['docker', 'stats', '--no-stream'], 
                      capture_output=True, check=True)
        print(f"{TINY42_BLUE}Docker is already running{TINY42_WHITE}")
        return
    except subprocess.CalledProcessError:
        print(f"{TINY42_GREEN}Docker is starting up...{TINY42_WHITE}", end='', flush=True)
        
        # Open Docker app
        subprocess.run(['open', '-g', '-a', 'Docker'])
        
        # Wait for Docker to start
        while True:
            try:
                subprocess.run(['docker', 'stats', '--no-stream'], 
                             capture_output=True, check=True)
                break
            except subprocess.CalledProcessError:
                print(f"{TINY42_GREEN}.{TINY42_WHITE}", end='', flush=True)
                time.sleep(1)
        print()

def setup_goinfre_docker() -> None:
    """Configure Docker to use goinfre directory (42 School specific).
    
    - Creates Docker directories in /goinfre/<user>/docker
    - Sets up proper symlinks for Docker configuration
    - Handles existing installations and prompts for reset
    """
    user: str = os.environ['USER']
    docker_dest: str = f"/goinfre/{user}/docker"
    
    # Check if Docker is already in goinfre
    if os.path.exists(docker_dest):
        response: str = input(f"{TINY42_RED}Docker is already setup in {docker_dest}, "
                        f"do you want to reset it? [y/N]{TINY42_WHITE}\n")
        if response.lower() == 'y':
            subprocess.run(['rm', '-rf', 
                          f"{docker_dest}/com.docker.docker",
                          f"{docker_dest}/com.docker.helper",
                          f"{docker_dest}/.docker"])

    # Remove existing symlinks and directories
    paths_to_clean: List[str] = [
        "~/Library/Containers/com.docker.docker",
        "~/Library/Containers/com.docker.helper",
        "~/.docker"
    ]
    
    for path in paths_to_clean:
        expanded_path: str = os.path.expanduser(path)
        try:
            if os.path.islink(expanded_path):
                os.unlink(expanded_path)
            elif os.path.exists(expanded_path):
                subprocess.run(['rm', '-rf', expanded_path])
        except Exception:
            pass

    # Create destination directories
    os.makedirs(f"{docker_dest}/com.docker.docker", exist_ok=True)
    os.makedirs(f"{docker_dest}/com.docker.helper", exist_ok=True)
    os.makedirs(f"{docker_dest}/.docker", exist_ok=True)

    # Create symlinks
    links: List[tuple[str, str]] = [
        (f"{docker_dest}/com.docker.docker", "~/Library/Containers/com.docker.docker"),
        (f"{docker_dest}/com.docker.helper", "~/Library/Containers/com.docker.helper"),
        (f"{docker_dest}/.docker", "~/.docker")
    ]
    
    for src, dst in links:
        dst = os.path.expanduser(dst)
        os.symlink(src, dst)

    print(f"{TINY42_GREEN}docker is now set up in goinfre{TINY42_WHITE}") 