from typing import Optional, Dict, Tuple, Any
from directions import opposite_directions, directions, get_boost_dir
from speed import movement_points, real_movment_points, moves, stamina_costs, new_stamina, stamina_regeneration
import numpy as np
import heapq

tile_costs = {"water": 45, "road": 31, "trail": 40, "grass": 50,
              "forest": np.inf, "rockywater": np.inf, "start": 50, "win": 0}
deviation = {"water": 15, "trail": 25, "road": 40}
weather_cost = 7


def get_goal(tiles) -> Tuple[int, int]:
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile["type"] == "win":
                return (x, y)


def is_impassable(tile_name: str) ->bool:
    return tile_costs[tile_name] == np.inf


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


def estimated_output_position(state: Dict[str, Any], position, stamina, direction: str, movement_speed: str):
    player_position = position
    stamina = state["yourPlayer"]["stamina"]
    tiles = state["tileInfo"]
    deviation_points = {"n": 0, "e": 0, "s": 0, "w": 0, }
    number_of_weather_tiles = 0

    if movement_speed == "step":
        return get_position_in_direction(direction, player_position), weather_cost if "weather" in get_tile_in_direction(tiles, direction, player_position) else 0

    current_movment_points = real_movment_points(stamina, movement_speed)
    while current_movment_points > 0:
        # check if inside forest, no good
        if is_impassable(state["tileInfo"][player_position[1]][player_position[0]]["type"]):
            break

        next_tile = get_tile_in_direction(tiles, direction, player_position)
        boost_tile = get_boost_dir(next_tile)
        if "weather" in next_tile:
            number_of_weather_tiles += 1


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
    return player_position, number_of_weather_tiles


def find_indices(lst, condition):
    return [i for i, elem in enumerate(lst) if condition(elem)]


def is_around(tile_pos, player_pos, steps_from_path):
    return (abs(tile_pos[0]-player_pos[0]) + abs(tile_pos[1]-player_pos[1])) <= steps_from_path


all_pos = []
all_opt = []
opt_path = []


def get_next_best_move(path, state: Dict[str, Any]):
    stamina = state["yourPlayer"]["stamina"]
    player_position = (state["yourPlayer"]["xPos"],
                       state["yourPlayer"]["yPos"])
    stamina_threshold = 65
    steps_from_path = 1
    current_best = {"index": 0, "stamina_cost": np.inf,
                    "move": "step", "direction": ""}
    position = None
    weather_tiles = 0
    for move in moves:
        if new_stamina(stamina, move) < stamina_threshold:
            continue
        stamina_cost = stamina_costs[move]
        for direction in directions:
            position, weather_tiles = estimated_output_position(state, player_position, stamina, direction, move)
            stamina_cost += weather_tiles*weather_cost

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
        all_pos.append(estimated_output_position(state, player_position, stamina, current_best["direction"], current_best["move"])[0])
    return current_best


class P_move:
    def __init__(self, index, direction, move, position, stamina, previous_moves):
        self.index = index
        self.direction = direction
        self.move = move
        self.position = position
        self.stamina = stamina
        self.previous_moves = previous_moves

def get_all_best_moves(path, state: Dict[str, Any]):
    goal_point = path[-1]
    radius = 3
    moves_tree = []
    stamina_threshold = 65
    best_move_set = P_move(np.inf, None, None, None, None, None)
    stamina = state["yourPlayer"]["stamina"]
    player_position = (state["yourPlayer"]["xPos"], state["yourPlayer"]["yPos"])
    



    for move in moves:
        for direction in directions:
            position, weather_tiles = estimated_output_position(state, player_position, stamina, direction, move)
            if is_impassable(state["tileInfo"][position[1]][position[0]]["type"]):
                continue
            if not any([is_around(pos, position, radius) for pos in path]):
                continue
            current_stamina = stamina - (stamina_costs[move] + (weather_tiles * weather_cost))
            current_stamina += stamina_regeneration(current_stamina)
            moves_tree.append( 
                P_move(
                    0, 
                    direction,
                    move,
                    position,
                    current_stamina,
                    []
                ) 
            )
    
    while moves_tree != []:
        current_branch = moves_tree.pop()

        if current_branch.position == goal_point:
            if current_branch.index < best_move_set.index:
                best_move_set = current_branch
                print(best_move_set.index)
            continue
        
        for move in moves:
            if new_stamina(current_branch.stamina, move) < stamina_threshold:
                acc_moves = current_branch.previous_moves
                acc_moves.append(current_branch)
                current_stamina = current_branch.stamina
                current_stamina += stamina_regeneration(current_stamina) + 15
                moves_tree.append( 
                    P_move(
                        current_branch.index+1, 
                        "",
                        "rest",
                        current_branch.position,
                        current_stamina,
                        acc_moves
                    )
                )
                continue
            for direction in directions:
                position, weather_tiles = estimated_output_position(state, current_branch.position, current_branch.stamina, direction, move)
                if is_impassable(state["tileInfo"][position[1]][position[0]]["type"]):
                    continue
                if position in map(lambda p_move: p_move.position, current_branch.previous_moves[:-1]):
                    continue
                if not any([is_around(pos, position, radius) for pos in path]):
                    continue

                acc_moves = current_branch.previous_moves
                acc_moves.append(current_branch)
                current_stamina = current_branch.stamina - (stamina_costs[move] + (weather_tiles * weather_cost))
                current_stamina += stamina_regeneration(current_stamina)

                moves_tree.append( 
                    P_move(
                        current_branch.index+1, 
                        direction,
                        move,
                        position,
                        current_stamina,
                        acc_moves
                    )
                )
    return_moves = best_move_set.previous_moves
    return_moves.append(best_move_set)
    return best_move_set