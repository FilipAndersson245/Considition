from typing import Optional, Dict, Tuple, Any
from directions import opposite_directions
from speed import movement_points
tile_costs = {"water": 45, "road": 31, "trail": 40, "grass": 50}
deviation = {"water": 10, "trail": 25, "road": 40}
water_cost = 7


def rain_cost(tile: str) -> int:
    return tile_costs[tile] + water_cost


def can_i_afford_to_move(movment_points: int, tile_type: str) -> bool:
    """
    Checks if a move can be afforded.  
    Does not take stream/uphill into consideration
    """
    if tile_type in tile_costs:
        return True if movment_points-tile_costs[tile_type] > 0 else False
    else:
        print("Error ({}) is not a valid tyletype!".format(tile_type))


def foo(direction: str, tyle: str) -> str:
    if tyle == "water":
        return direction
    else:
        return opposite_directions[direction]


def get_tile_in_direction(tiles, direction, position) -> Optional[Dict[str, Any]]:
    if direction == 'n':
        return tiles[position[1]-1][position[0]]
    elif direction == 's':
        return tiles[position[1]+1][position[0]]
    elif direction == 'w':
        return tiles[position[1]][position[0]-1]
    elif direction == 'e':
        return tiles[position[1]+1][position[0]+1]
    else:
        return None


def get_position_in_direction(direction, position) -> Optional[Tuple[int, int]]:
    if direction == 'n':
        return (position[0], position[1]-1)
    elif direction == 's':
        return (position[0], position[1]+1)
    elif direction == 'w':
        return (position[0]-1, position[1])
    elif direction == 'e':
        return (position[0]+1, position[1])
    else:
        return None


def estimated_output_position(state: Dict[str, Any], direction: str, movement_speed: str):
    player_position = (state["yourPlayer"]["position"]
                       ["xPos"], state["yourPlayer"]["position"]["yPos"])
    stamina = state["yourPlayer"]["stamina"]
    tiles = state["tileInfo"]
    current_movment_points = movement_points[movement_speed]
    while current_movment_points > 0:
        next_tile = get_tile_in_direction(tiles, direction, player_position)
        if current_movment_points > tile_costs[next_tile["type"]]:
            # "make virtual movement"
            player_position = get_position_in_direction(
                direction, player_position)
            current_movment_points -= tile_costs[next_tile["type"]]
        else:
            break
    pass
