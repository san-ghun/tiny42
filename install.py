#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def install_dorker():
    # Get the absolute path of the installation directory
    install_dir = Path(__file__).parent.absolute()
    
    # Define the target directories
    home = Path.home()
    bin_dir = home / '.local' / 'bin'
    config_dir = home / '.config' / 'dorker'
    
    try:
        # Create necessary directories
        bin_dir.mkdir(parents=True, exist_ok=True)
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy the source files to config directory
        src_dir = install_dir / 'src'
        if src_dir.exists():
            shutil.copytree(src_dir, config_dir / 'src', dirs_exist_ok=True)
        
        # Copy Dockerfile
        dockerfile = install_dir / 'src' / 'Dockerfile'
        if dockerfile.exists():
            shutil.copy2(dockerfile, config_dir / 'src' / 'Dockerfile')
        
        # Copy and make the main script executable
        dorker_script = install_dir / 'dorker'
        if dorker_script.exists():
            shutil.copy2(dorker_script, bin_dir / 'dorker')
            os.chmod(bin_dir / 'dorker', 0o755)
        
        # Add the bin directory to PATH if it's not already there
        shell_rc_files = [
            home / '.zshrc',
            home / '.bashrc',
        ]
        
        path_export = f'\nexport PATH="$PATH:{bin_dir}"\n'
        
        for rc_file in shell_rc_files:
            if rc_file.exists():
                with open(rc_file, 'r') as f:
                    content = f.read()
                
                if str(bin_dir) not in content:
                    with open(rc_file, 'a') as f:
                        f.write(path_export)
        
        print(f"\033[0;32mDorker has been successfully installed!\033[0m")
        print(f"\033[0;36mPlease restart your terminal or run 'source ~/.zshrc' (or ~/.bashrc) to use dorker.\033[0m")
        
    except Exception as e:
        print(f"\033[0;31mError during installation: {str(e)}\033[0m")
        return 1
    
    return 0

def uninstall_dorker():
    home = Path.home()
    bin_dir = home / '.local' / 'bin'
    config_dir = home / '.config' / 'dorker'
    
    try:
        # Remove the dorker executable
        dorker_script = bin_dir / 'dorker'
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

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--uninstall':
        return uninstall_dorker()
    return install_dorker()

if __name__ == "__main__":
    sys.exit(main()) 