from typing import Optional, Dict, Tuple, Any
from directions import opposite_directions, directions
from speed import movement_points, real_movment_points, moves, stamina_costs, new_stamina
import numpy as np
tile_costs = {"water": 45, "road": 31, "trail": 40, "grass": 50, "forest": np.inf, "rockywater": np.inf, "start": 50, "win": 0}
deviation = {"water": 15, "trail": 25, "road": 40}
water_cost = 7


def is_impassable(tile_name):
    return tile_costs[tile_name] == np.inf


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
        return tiles[position[1]][position[0]+1]
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
    player_position = (state["yourPlayer"]["xPos"], state["yourPlayer"]["yPos"])
    stamina = state["yourPlayer"]["stamina"]
    tiles = state["tileInfo"]

    if movement_speed == "step":
        return get_position_in_direction(direction, player_position)
    
    current_movment_points = real_movment_points(stamina, movement_speed)
    while current_movment_points > 0:
        if is_impassable(state["tileInfo"][player_position[1]][player_position[0]]["type"]):
            break
        next_tile = get_tile_in_direction(tiles, direction, player_position)
        tile_type_cost = 20 if is_impassable(next_tile["type"]) else tile_costs[next_tile["type"]]
        if current_movment_points > tile_type_cost:
            # "make virtual movement"
            player_position = get_position_in_direction(
                direction, player_position)
            current_movment_points -= tile_type_cost
        else:
            break

    return player_position


def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]


def is_around(tile_pos, player_pos, steps_from_path):
    return (abs(tile_pos[0]-player_pos[0]) + abs(tile_pos[1]-player_pos[1])) <= steps_from_path

all_pos = []

def get_next_best_move(path, state: Dict[str, Any]):
    stamina = state["yourPlayer"]["stamina"]
    stamina_threshold = 50
    steps_from_path = 1
    current_best = {"index": 0, "stamina_cost": np.inf, "move": "step", "direction": ""}
    position = None
    for move in moves:
        if new_stamina(stamina, move) < stamina_threshold:
            continue
        stamina_cost = stamina_costs[move]
        for direction in directions:
            position = estimated_output_position(state, direction, move)

            if is_impassable(state["tileInfo"][position[1]][position[0]]["type"]):
                continue

            if position == path[-1]:
                current_best = {"index": np.inf, "stamina_cost": stamina_cost, "move": move, "direction": direction}
                break

            indices = find_indices(path, lambda tile: is_around(tile, position, steps_from_path))
            if len(indices) == 0:
                continue
            local_best = indices[-1]

            if local_best > current_best["index"]:
                current_best = {"index": local_best, "stamina_cost": stamina_cost, "move": move, "direction": direction}
            elif (local_best == current_best["index"]) and (stamina_cost < current_best["stamina_cost"]):
                current_best = {"index": local_best, "stamina_cost": stamina_cost, "move": move, "direction": direction}
    if position:
        all_pos.append(estimated_output_position(state, current_best["direction"], current_best["move"]))
    return current_best

            
                    