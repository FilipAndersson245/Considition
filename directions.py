import numpy as np
from typing import Tuple, Dict, Any, Optional, List

_Position = Tuple[int, int]
directions: List[str] = ["n", "e", "s", "w"]
opposite_directions: Dict[str, str] = {"n": "s", "e": "w", "s": "e", "w": "e"}


def get_dir(current_position: _Position, destination: _Position) -> Optional[str]:
    """
    return string e, w, s ,n as string or False if the pos differ more then one.
    """
    diff = np.subtract(destination, current_position)
    if all(diff == [1, 0]):
        return "e"
    elif all(diff == [-1, 0]):
        return "w"
    elif all(diff == [0, 1]):
        return "s"
    elif all(diff == [0, -1]):
        return "n"
    else:
        return None


def tree_in_current_direction(state: Dict[str, Any], current_direction: str) -> bool:
    """
    Checks if a tree is in the current dirrection and return true if there is a tree
    """
    tiles = state["tileInfo"]
    current_player = state["yourPlayer"]
    current_y_pos = current_player["yPos"]
    current_x_pos = current_player["xPos"]

    active_tile = None

    if current_direction is "n":
        active_tile = tiles[current_y_pos-1][current_x_pos]
    elif current_direction is "e":
        active_tile = tiles[current_y_pos][current_x_pos+1]
    elif current_direction is "s":
        active_tile = tiles[current_y_pos+1][current_x_pos]
    else:
        active_tile = tiles[current_y_pos][current_x_pos-1]
    return active_tile['type'] == 'forest'


def tree_in_any_direction(state: Dict[str, Any]) -> bool:
    """
    Checks if a tree exists in any direction from the player checking clockwise from player position
    """
    for direction in directions:
        if tree_in_current_direction(state, direction):
            return True
    return False
