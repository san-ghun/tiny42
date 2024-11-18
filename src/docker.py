import os
import time
import subprocess
from typing import List
from .settings import *

def open_docker() -> None:
    """Open Docker application and wait for it to start."""
    try:
        # Check if Docker is running
        subprocess.run(['docker', 'stats', '--no-stream'], 
                      capture_output=True, check=True)
        print(f"{DORKER_BLUE}Docker is already running{DORKER_WHITE}")
        return
    except subprocess.CalledProcessError:
        print(f"{DORKER_GREEN}Docker is starting up...{DORKER_WHITE}", end='', flush=True)
        
        # Open Docker app
        subprocess.run(['open', '-g', '-a', 'Docker'])
        
        # Wait for Docker to start
        while True:
            try:
                subprocess.run(['docker', 'stats', '--no-stream'], 
                             capture_output=True, check=True)
                break
            except subprocess.CalledProcessError:
                print(f"{DORKER_GREEN}.{DORKER_WHITE}", end='', flush=True)
                time.sleep(1)
        print()

def setup_goinfre_docker() -> None:
    """Setup Docker in goinfre directory."""
    user: str = os.environ['USER']
    docker_dest: str = f"/goinfre/{user}/docker"
    
    # Check if Docker is already in goinfre
    if os.path.exists(docker_dest):
        response: str = input(f"{DORKER_RED}Docker is already setup in {docker_dest}, "
                        f"do you want to reset it? [y/N]{DORKER_WHITE}\n")
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

    print(f"{DORKER_GREEN}docker is now set up in goinfre{DORKER_WHITE}") 