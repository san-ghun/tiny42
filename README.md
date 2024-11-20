# tiny42 - Keep on coding with your portable 42

> Inspired from the [Dorker](https://github.com/Scarletsang/Dorker) by [Scarletsang](https://github.com/Scarletsang)

## Overview

`tiny42` is a Python-based tool that provides a consistent Docker environment for C/C++ development, particularly useful for 42 School projects. It allows developers to run Linux-specific tools (like valgrind and strace) on macOS through a seamless Docker interface.

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
git clone https://github.com/yourusername/tiny42.git
cd tiny42

# Install tiny42
python3 install.py

# Restart your terminal or source your configuration
source ~/.zshrc  # or ~/.bashrc
```

## Configuration

The configuration file is located at `~/.config/tiny42/src/settings.py`:

```python
# Workspace configuration
TINY42_WORKSPACE = os.path.join(os.environ['HOME'], 'Projects/42berlin')
TINY42_ECHO_ON_STARTUP = True

# Port forwarding settings
TINY42_PORT_PUBLISHING = False
TINY42_PORT_PUBLISHING_HOST = 8080
TINY42_PORT_PUBLISHING_CONTAINER = 8080
```

### Port Publishing

To enable port forwarding between your host machine and container:

1. Set `TINY42_PORT_PUBLISHING = True`
2. Configure ports:
   - `TINY42_PORT_PUBLISHING_HOST`: Host machine port
   - `TINY42_PORT_PUBLISHING_CONTAINER`: Container port

## Usage

### Basic Commands

```bash
# Execute commands in container
tiny42 [command] [args...]

# Examples
tiny42 make re
tiny42 valgrind --leak-check=full ./program
tiny42 gcc -Wall -Wextra -Werror main.c
tiny42 "cd ./webserv ; cat webserv.conf | grep location"

# Open shell in container
tiny42 bash

# Management commands
--init, -i             # Initialize the tiny42 container
--reload, -r           # Rebuild and restart the tiny42 container
--open-docker, -o      # Start Docker daemon if not running
--goinfre-docker, -g   # Setup Docker in goinfre directory (42 School specific)
--help, -h             # Show help message

# Examples with flags
tiny42 --init
tiny42 -r              # Short form for reload
```

### Development Environment

The container includes:

- Build tools (gcc, make)
- Debugging tools (valgrind, strace)
- Git
- Additional utilities (bat, jq)
- readline development libraries

> [!WARNING]
> Docker enables you to code and compile your results, but CANNOT display graphical projects, such as fract-ol, FdF, so_long, cub3d, miniRT.

## Project Structure

```
~/.config/tiny42/
├── src/
│   ├── __init__.py
│   ├── settings.py    # Configuration
│   ├── docker.py      # Docker operations
│   ├── tiny42.py      # Core functionality
│   └── Dockerfile     # Container definition
└── ...

~/.local/bin/
└── tiny42            # Main executable
```

## Uninstallation

```bash
# Move to the cloned directory
cd tiny42

# Execute install script with --uninstall flag
python3 install.py --uninstall
```

## Requirements

- Python 3.6+
- Docker
- Unix-like environment (macOS or Linux)

## Technical Details

The codebase consists of several key components:

1. Core functionality (referenced in `src/tiny42.py`):

```python
# 9:59:src/tiny42.py
def _check_environment() -> bool:
    """Check if we're in the correct workspace and Docker is running."""
    current_path: str = os.getcwd()

    if current_path == TINY42_WORKSPACE:
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
    """Run a command inside the tiny42 container."""
    if not args or args[0] in ['-h', '--help']:
        show_help()
        return

    current_path: str = os.getcwd()
    relative_path: str = os.path.relpath(current_path, TINY42_WORKSPACE)

    if not _check_environment():
        return

    command: str = ' '.join(args)
    subprocess.run(['docker', 'exec', '-it', 'tiny42', 'bash', '-c',
                   f"cd '/tiny42_workspace/{relative_path}' && {command}"])

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


def setup_goinfre_docker() -> None:
    """Setup Docker in goinfre directory."""
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

```

3. Settings management (referenced in `src/settings.py`):

```python
# 1:31:src/settings.py
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
    """
    Returns the port mapping string for Docker if port publishing is enabled.

    Returns:
        str: Port mapping in format '-p HOST:CONTAINER' or None if disabled
    """
    if TINY42_PORT_PUBLISHING:
        return f'-p {TINY42_PORT_PUBLISHING_HOST}:{TINY42_PORT_PUBLISHING_CONTAINER}'
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

- Started by forking the repository from [Dorker](https://github.com/Scarletsang/Dorker) by [Scarletsang](https://github.com/Scarletsang)
- Originally designed for 42 School's development environment needs
- Refactored from shell scripts to Python for improved maintainability
