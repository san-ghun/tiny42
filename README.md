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
> *Docker* enables you to code and compile your results.   
> But it **CANNOT** display graphical projects, such as *fract-ol*, *FdF*, *so_long*, *cub3d*, *miniRT*.

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
2. Docker management (referenced in `src/docker.py`):
3. Settings management (referenced in `src/settings.py`):

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

## Backstory

I am a student of 42Berlin. I love the space and people. However, my biggest concern was the commute from my place to the cluster, which takes a total of 4 hours a day. On top of that, my working hours are irregular, so being at the 42Berlin cluster was and still is diffcult for me. 

I installed Ubuntu on my machines but it wasn't smooth and didn't fit with my daily usage. Since I rely heavily on `gdb` and `valgrind` in my projects, I needed a solution to improve my setup. 

Then I found the [Dorker](https://github.com/Scarletsang/Dorker) by [Scarletsang](https://github.com/Scarletsang) (big thanks!) and used it for a while. I didn't have any problems using it by myself, but I did have some difficulties when collaborating on the `webserv` project with my peers. 

So I forked the Dorker repository and started converting Bash scripts into Python3 code, and here we are. It still needs a lot of improvements and bug fixes. But I am really enjoying the process.

I hope `tiny42` will help my peers who are experiencing the same issues as me.
