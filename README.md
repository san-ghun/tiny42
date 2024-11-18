# Dorker - Docker Development Environment Manager

## Overview

Dorker is a Python-based tool that provides a consistent Docker environment for C/C++ development, particularly useful for 42 School projects. It allows developers to run Linux-specific tools (like valgrind and strace) on macOS through a seamless Docker interface.

## Key Features

- Automatic Docker environment management
- Seamless command execution within containers
- Port forwarding support for web development
- Goinfre directory support for 42 School computers
- Built-in development tools (gcc, valgrind, strace, etc.)
- Workspace isolation and consistency

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dorker.git
cd dorker

# Install Dorker
python3 install.py

# Restart your terminal or source your configuration
source ~/.zshrc  # or ~/.bashrc
```

## Configuration

The configuration file is located at `~/.config/dorker/src/settings.py`:

```python
# Workspace configuration
DORKER_WORKSPACE = os.path.join(os.environ['HOME'], 'Projects/42berlin')
DORKER_ECHO_ON_STARTUP = True

# Port forwarding settings
DORKER_PORT_PUBLISHING = False
DORKER_PORT_PUBLISHING_HOST = 8080
DORKER_PORT_PUBLISHING_CONTAINER = 8080
```

### Port Publishing

To enable port forwarding between your host machine and container:

1. Set `DORKER_PORT_PUBLISHING = True`
2. Configure ports:
   - `DORKER_PORT_PUBLISHING_HOST`: Host machine port
   - `DORKER_PORT_PUBLISHING_CONTAINER`: Container port

## Usage

### Basic Commands

```bash
# Execute commands in container
dorker <command>

# Examples
dorker make re
dorker valgrind --leak-check=full ./program
dorker gcc -Wall -Wextra -Werror main.c

# Open shell in container
dorker bash

# Management commands
dorker-init           # Initialize container
dorker-reload         # Rebuild container
dorker-open-docker    # Start Docker daemon
dorker-goinfre-docker # Setup Docker in goinfre (42 School)
```

### Development Environment

The container includes:

- Build tools (gcc, make)
- Debugging tools (valgrind, strace)
- Git
- Additional utilities (bat, jq)
- readline development libraries

## Project Structure

```
~/.config/dorker/
├── src/
│   ├── __init__.py
│   ├── settings.py    # Configuration
│   ├── docker.py      # Docker operations
│   ├── dorker.py      # Core functionality
│   └── Dockerfile     # Container definition
└── ...

~/.local/bin/
└── dorker            # Main executable
```

## Uninstallation

```bash
python3 install.py --uninstall
```

## Requirements

- Python 3.6+
- Docker
- Unix-like environment (macOS or Linux)

## Technical Details

The codebase consists of several key components:

1. Core functionality (referenced in `src/dorker.py`):

```python
# 9:59:src/dorker.py
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

```

2. Docker management (referenced in `src/docker.py`):

```python
# 7:79:src/docker.py
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

```

3. Settings management (referenced in `src/settings.py`):

```python
# 1:31:src/settings.py
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
    """
    Returns the port mapping string for Docker if port publishing is enabled.

    Returns:
        str: Port mapping in format '-p HOST:CONTAINER' or None if disabled
    """
    if DORKER_PORT_PUBLISHING:
        return f'-p {DORKER_PORT_PUBLISHING_HOST}:{DORKER_PORT_PUBLISHING_CONTAINER}'
    return None
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Originally designed for 42 School's development environment needs
- Refactored from shell scripts to Python for improved maintainability
- Community contributions and feedback
