import os

# Fill in the directory name that contains all your 42 projects
DORKER_WORKSPACE = os.path.join(os.environ['HOME'], 'Projects/42berlin')
DORKER_ECHO_ON_STARTUP = True

# Terminal colors
DORKER_GREEN = '\033[0;32m'  # Used for success messages
DORKER_BLUE = '\033[0;36m'   # Used for instructions/guides
DORKER_RED = '\033[0;31m'    # Used for errors/warnings
DORKER_WHITE = '\033[0m' 