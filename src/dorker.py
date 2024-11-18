import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union
from .settings import *
from .docker import open_docker, setup_goinfre_docker
from .settings import get_port_mapping

def _check_environment() -> bool:
    """Check if we're in the correct workspace and Docker is running."""
    current_path: str = os.getcwd()
    
    if current_path == DORKER_WORKSPACE:
        print(f"{DORKER_RED}You are not inside the workspace specified.{DORKER_WHITE}")
        print(f"{DORKER_BLUE}Dorker can only be ran inside the specified workspace, "
              f"currently it is set to \"{DORKER_WORKSPACE}\".{DORKER_WHITE}")
        return False

    # Check if dorker container is running
    try:
        output: str = subprocess.check_output(['docker', 'ps'], text=True)
        if 'dorker' not in output:
            # Check if image exists
            images: str = subprocess.check_output(['docker', 'images'], text=True)
            if 'dorker' not in images:
                init_dorker()
            else:
                run_cmd: List[str] = ['docker', 'run', '-itd']
                port_mapping: Optional[str] = get_port_mapping()
                if port_mapping:
                    run_cmd.append(port_mapping)
                    
                run_cmd.extend([
                    '-v', f'{DORKER_WORKSPACE}:/dorker_workspace',
                    '--name=dorker', 'dorker'
                ])
                
                subprocess.run(run_cmd)
    except subprocess.CalledProcessError:
        return False
    
    return True

def run_dorker_command(args: List[str]) -> None:
    """Run a command inside the dorker container."""
    if not args or args[0] in ['-h', '--help']:
        show_help()
        return

    current_path: str = os.getcwd()
    relative_path: str = os.path.relpath(current_path, DORKER_WORKSPACE)
    
    if not _check_environment():
        return

    command: str = ' '.join(args)
    subprocess.run(['docker', 'exec', '-it', 'dorker', 'bash', '-c',
                   f"cd '/dorker_workspace/{relative_path}' && {command}"])

def init_dorker() -> None:
    """Initialize the dorker container."""
    response: str = input(f"{DORKER_RED}Dorker wants to know if you want to setup "
                    f"Docker inside goinfre. Do you want to setup Docker within "
                    f"goinfre? [y/N]{DORKER_WHITE}\n")
    
    if response.lower() == 'y':
        setup_goinfre_docker()

    open_docker()
    
    try:
        # Check if container exists
        output: str = subprocess.check_output(['docker', 'ps', '-a'], text=True)
        if 'dorker' in output:
            subprocess.run(['docker', 'start', 'dorker'])
        else:
            # Build and run new container
            dockerfile_path: Path = Path(__file__).parent / 'Dockerfile'
            subprocess.run(['chmod', '755', str(dockerfile_path)])
            subprocess.run(['docker', 'build', '.', '-t', 'dorker', 
                          '-f', str(dockerfile_path)])
            
            run_cmd: List[str] = ['docker', 'run', '-itd']
            port_mapping: Optional[str] = get_port_mapping()
            if port_mapping:
                run_cmd.append(port_mapping)
                
            run_cmd.extend([
                '-v', f'{DORKER_WORKSPACE}:/dorker_workspace',
                '--name=dorker', 'dorker'
            ])
            
            subprocess.run(run_cmd)
            
        print(f"{DORKER_GREEN}Dorker is running in {DORKER_WORKSPACE}{DORKER_WHITE}")
    except subprocess.CalledProcessError:
        print(f"{DORKER_RED}Failed to build the dorker image{DORKER_WHITE}")

def reload_dorker() -> None:
    """Rebuild and restart the dorker container."""
    open_docker()
    
    dockerfile_path: Path = Path(__file__).parent / 'Dockerfile'
    subprocess.run(['docker', 'build', '.', '-t', 'dorker', 
                   '-f', str(dockerfile_path)])
    subprocess.run(['docker', 'stop', 'dorker'])
    subprocess.run(['docker', 'rm', 'dorker'])
    
    run_cmd: List[str] = ['docker', 'run', '-itd']
    port_mapping: Optional[str] = get_port_mapping()
    if port_mapping:
        run_cmd.append(port_mapping)
        
    run_cmd.extend([
        '-v', f'{DORKER_WORKSPACE}:/dorker_workspace',
        '--name=dorker', 'dorker'
    ])
    
    subprocess.run(run_cmd)
    print(f"{DORKER_GREEN}Dorker is reloaded and restarted{DORKER_WHITE}")

def show_help() -> None:
    """Show help message."""
    print(f"{DORKER_BLUE}\nDorker is configured to run only inside {DORKER_WORKSPACE}")
    print("Change settings in src/settings.py")
    print("Change Dockerfile in src/Dockerfile\n")
    print("Available commands:\n")
    print("dorker <commands>        Execute any command inside the \"dorker\" container.")
    print("dorker-reload           Rebuild the dorker container.")
    print("dorker-init            Built and start the docker container called \"dorker\".")
    print("dorker-open-docker     Open docker from the command line.")
    print("dorker-goinfre-docker  Setup docker inside the goinfre directory.")
    
    if DORKER_PORT_PUBLISHING:
        print(f"\nPort Publishing: Host port {DORKER_PORT_PUBLISHING_HOST} -> "
              f"Container port {DORKER_PORT_PUBLISHING_CONTAINER}")
    print(f"{DORKER_WHITE}")