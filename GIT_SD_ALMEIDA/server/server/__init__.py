import logging
import threading
from server.server_impl import Server

COMMAND_SIZE = 9
"""
INT_SIZE = 8
ADD_OP = "add      "
SYM_OP = "sym      "
BYE_OP = "bye      "
SUB_OP = "sub      "
STOP_SERVER_OP = "terminate"

PORT = 35000
SERVER_ADDRESS = "localhost"
"""
NAME_TAKEN = 2
MAP_OP = "map-     "
ADD_PLAYER_OP = "addplr-  "
INT_SIZE = 10
LOG_FILENAME = "math-server.log"
LOG_LEVEL = logging.DEBUG
nr_threads = 0
MAP_SETUP_OP = "stp_map- "
lock = threading.Lock()
MOVE_OP = "move-    "
MAP_SIZE = 10
GAME_FINISH_OP = "isfnd-   "
STOP_SERVER_OP = "terminate"
PORT = 47000
SERVER_ADDRESS = "localhost"
START_GAME_OP = "start-   "
GAME_WON_OP = "won-     "
GAME_LOST_OP = "lost-    "
HAS_PLAYER_OP = "player-   "
TURN_OP = "turn-    "
GAME_ONGOING = -1
GAME_WON = 1
GAME_LOST = 0
STATUS_OP = "status-   "
GAME_FULL = -1
PLAYER_NAME_SIZE = 20
MOVE_SIZE = 3
MAX_NUMBER_OF_CONCURRENT_CLIENTS = 2
ACCEPT_TIMEOUT = 1
PLAYER_EXISTS = -1
