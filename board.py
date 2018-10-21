import numpy as np
from typing import Set
from tiles import tile_costs

board: np.ndarray = np.full((100, 100), np.inf)


def get_board():
    """
    Get current board
    """
    return board


def map_to_board_first(tiles):
    """
    Update board with a given state
    """
    for x, row in enumerate(tiles):
        for y, tile in enumerate(row):
            tile_type = tile["type"]
            if tile_type != "forest":
                board[x][y] = (tile_costs[tile_type] /
                               100) if tile_type in tile_costs else 1
    return board


def map_to_board_optimization(state):
    pass
