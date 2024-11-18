#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path
from typing import List, Union

def install_dorker() -> int:
    """Install Dorker to the user's system.
    
    This function:
    - Creates necessary directories in ~/.local/bin and ~/.config/dorker
    - Copies source files and Dockerfile to config directory
    - Makes the main dorker script executable
    - Adds ~/.local/bin to PATH in shell RC files if needed
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Get the absolute path of the installation directory
    install_dir: Path = Path(__file__).parent.absolute()
    
    # Define the target directories
    home: Path = Path.home()
    bin_dir: Path = home / '.local' / 'bin'
    config_dir: Path = home / '.config' / 'dorker'
    
    try:
        # Create necessary directories
        bin_dir.mkdir(parents=True, exist_ok=True)
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the source files to config directory
        src_dir: Path = install_dir / 'src'
        if src_dir.exists():
            shutil.copytree(src_dir, config_dir / 'src', dirs_exist_ok=True)
        
        # Copy Dockerfile
        dockerfile: Path = install_dir / 'src' / 'Dockerfile'
        if dockerfile.exists():
            shutil.copy2(dockerfile, config_dir / 'src' / 'Dockerfile')
        
        # Copy and make the main script executable
        dorker_script: Path = install_dir / 'dorker'
        if dorker_script.exists():
            shutil.copy2(dorker_script, bin_dir / 'dorker')
            os.chmod(bin_dir / 'dorker', 0o755)
        
        # Add the bin directory to PATH if it's not already there
        shell_rc_files: List[Path] = [
            home / '.zshrc',
            home / '.bashrc',
        ]
        
        path_export: str = f'\nexport PATH="$PATH:{bin_dir}"\n'
        
        for rc_file in shell_rc_files:
            if rc_file.exists():
                with open(rc_file, 'r') as f:
                    content: str = f.read()
                
                if str(bin_dir) not in content:
                    with open(rc_file, 'a') as f:
                        f.write(path_export)
        
        print(f"\033[0;32mDorker has been successfully installed!\033[0m")
        print(f"\033[0;36mPlease restart your terminal or run 'source ~/.zshrc' (or ~/.bashrc) to use dorker.\033[0m")
        
    except Exception as e:
        print(f"\033[0;31mError during installation: {str(e)}\033[0m")
        return 1
    
    return 0

def uninstall_dorker() -> int:
    """Remove Dorker from the user's system.
    
    This function:
    - Removes the dorker executable from ~/.local/bin
    - Removes the dorker config directory
    - Note: Does not remove PATH entries from shell RC files
    
    Returns:
        int: 0 for success, 1 for failure
    """
    home: Path = Path.home()
    bin_dir: Path = home / '.local' / 'bin'
    config_dir: Path = home / '.config' / 'dorker'
    
    try:
        # Remove the dorker executable
        dorker_script: Path = bin_dir / 'dorker'
        if dorker_script.exists():
            dorker_script.unlink()
        
        # Remove the config directory
        if config_dir.exists():
            shutil.rmtree(config_dir)
        
        print(f"\033[0;32mDorker has been successfully uninstalled!\033[0m")
        print(f"\033[0;36mNote: The PATH entry in your shell RC files was not removed. "
              f"You may want to remove it manually if no longer needed.\033[0m")
        
    except Exception as e:
        print(f"\033[0;31mError during uninstallation: {str(e)}\033[0m")
        return 1
    
    return 0

def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == '--uninstall':
        return uninstall_dorker()
    return install_dorker()

if __name__ == "__main__":
    sys.exit(main()) 