from typing import Optional, Dict, Tuple, Any
from directions import opposite_directions, directions, get_boost_dir
from speed import movement_points, real_movment_points, moves, stamina_costs, new_stamina
import numpy as np
tile_costs = {"water": 45, "road": 31, "trail": 40, "grass": 50,
              "forest": np.inf, "rockywater": np.inf, "start": 50, "win": 0}
deviation = {"water": 15, "trail": 25, "road": 40}
water_cost = 7


def get_goal(tiles) -> Tuple[int, int]:
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile["type"] == "win":
                return (x, y)


def is_impassable(tile_name: str) ->bool:
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


def amount_of_impassable(tileState, tile: Tuple[int, int]):
    y, x = tile
    count = 0
    count += 1 if tileState[y+1][x]["type"] == "forest" else 0
    count += 1 if tileState[y-1][x]["type"] == "forest" else 0
    count += 1 if tileState[y][x+1]["type"] == "forest" else 0
    count += 1 if tileState[y][x-1]["type"] == "forest" else 0
    return count


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
    player_position = (state["yourPlayer"]["xPos"],
                       state["yourPlayer"]["yPos"])
    stamina = state["yourPlayer"]["stamina"]
    tiles = state["tileInfo"]
    deviation_points = {"n": 0, "e": 0, "s": 0, "w": 0, }

    if movement_speed == "step":
        return get_position_in_direction(direction, player_position)

    current_movment_points = real_movment_points(stamina, movement_speed)
    while current_movment_points > 0:
        # check if inside forest, no good
        if is_impassable(state["tileInfo"][player_position[1]][player_position[0]]["type"]):
            break

        next_tile = get_tile_in_direction(tiles, direction, player_position)
        boost_tile = get_boost_dir(next_tile)

        tile_cost = 20 if is_impassable(
            next_tile["type"]) else tile_costs[next_tile["type"]]  # base cost
        if boost_tile != None:
            if boost_tile["direction"] == direction:
                tile_cost -= boost_tile["speed"]
            elif boost_tile["direction"] == opposite_directions[direction]:
                tile_cost += boost_tile["speed"]

        if current_movment_points > tile_cost:
            # "make virtual movement"
            player_position = get_position_in_direction(
                direction, player_position)
            current_movment_points -= tile_cost

            # sliding
            if boost_tile != None:
                if (boost_tile["direction"] != direction) or (boost_tile["direction"] != opposite_directions[direction]):
                    deviation_points[boost_tile["direction"]] += boost_tile["speed"]
                    deviation_points[opposite_directions[boost_tile["direction"]]] = min(deviation_points[opposite_directions[boost_tile["direction"]]] - boost_tile["speed"], 0)
                    for sliding_dir in directions:
                        if deviation_points[sliding_dir] >= deviation[next_tile["type"]]:
                            # make sliding
                            player_position = player_position = get_position_in_direction(
                                sliding_dir, player_position)
                            deviation_points[sliding_dir] -= deviation[next_tile["type"]]

        else:
            break

    return player_position


def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]


def is_around(tile_pos, player_pos, steps_from_path):
    return (abs(tile_pos[0]-player_pos[0]) + abs(tile_pos[1]-player_pos[1])) <= steps_from_path


all_pos = []
all_opt = []
opt_path = []


def get_next_best_move(path, state: Dict[str, Any]):
    stamina = state["yourPlayer"]["stamina"]
    stamina_threshold = 65
    steps_from_path = 1
    current_best = {"index": 0, "stamina_cost": np.inf,
                    "move": "step", "direction": ""}
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
                current_best = {
                    "index": np.inf, "stamina_cost": stamina_cost, "move": move, "direction": direction}
                break

            indices = find_indices(path, lambda tile: is_around(
                tile, position, steps_from_path))
            if len(indices) == 0:
                continue
            local_best = indices[-1]

            # sorts first on how long to go, then on stamina
            if local_best > current_best["index"]:
                current_best = {
                    "index": local_best, "stamina_cost": stamina_cost, "move": move, "direction": direction}
            elif (local_best == current_best["index"]) and (stamina_cost < current_best["stamina_cost"]):
                current_best = {
                    "index": local_best, "stamina_cost": stamina_cost, "move": move, "direction": direction}
    if position:
        all_pos.append(estimated_output_position(
            state, current_best["direction"], current_best["move"]))
    return current_best
