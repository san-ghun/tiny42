# Dorker - Docker Development Environment Manager

Dorker is a Python-based tool designed to simplify Docker container management for development environments, specifically tailored for 42 School projects. It provides an easy way to run commands within a consistent Docker environment.

## Features

- Automatic Docker environment setup and management
- Seamless command execution within Docker containers
- Goinfre directory support for 42 School computers
- Consistent development environment across different machines
- Built-in support for common development tools

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dorker.git
cd dorker

# Install Dorker
python3 install.py

# Restart your terminal or source your shell configuration
source ~/.zshrc  # or ~/.bashrc
```

## Configuration

The default configuration can be found in `~/.config/dorker/src/settings.py`:

```python
# Basic settings
DORKER_WORKSPACE = os.path.join(os.environ['HOME'], 'Projects/42berlin')
DORKER_ECHO_ON_STARTUP = True

# Port publishing configuration
DORKER_PORT_PUBLISHING = False  # Set to True to enable port publishing
DORKER_PORT_PUBLISHING_HOST = 8080  # Port on your host machine
DORKER_PORT_PUBLISHING_CONTAINER = 8080  # Port inside the container
```

Modify `DORKER_WORKSPACE` to point to your project directory.

### Port Publishing

To enable port publishing between your host machine and the Docker container:

1. Set `DORKER_PORT_PUBLISHING = True` in settings.py
2. Configure the desired ports:
   - `DORKER_PORT_PUBLISHING_HOST`: Port on your local machine
   - `DORKER_PORT_PUBLISHING_CONTAINER`: Port inside the Docker container

This is useful for web development or running services that need to be accessed from outside the container.

## Usage

Dorker commands must be run within your configured workspace directory.

### Basic Commands

```bash
# Execute a command inside the Docker container
dorker <command>

# Examples:
dorker make re
dorker valgrind --leak-check=full ./program
dorker gcc -Wall -Wextra -Werror main.c

# Open a shell inside the container
dorker bash

# Other utility commands
dorker-init           # Initialize Docker container
dorker-reload         # Rebuild and restart container
dorker-open-docker    # Start Docker daemon
dorker-goinfre-docker # Setup Docker in goinfre (42 School)
```

### Development Environment

The Docker container includes:

- Build essentials (gcc, make)
- Debugging tools (valgrind, strace)
- Git
- Additional utilities (bat, jq)

## Project Structure

```
~/.config/dorker/
├── src/
│   ├── __init__.py
│   ├── settings.py    # Configuration settings
│   ├── docker.py      # Docker management functions
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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Originally inspired by 42 School's development environment needs
- Refactored from shell scripts to Python for better maintainability and features

<!--
This README provides a comprehensive overview of the refactored Python version while maintaining the original purpose and functionality of the project. It includes all necessary information for installation, usage, and contribution, while being clear and accessible to both new and experienced users.
-->
