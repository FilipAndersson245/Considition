import scipy as scipy
import numpy as np
import webbrowser
from os import system
from api import API
import random
import sys
import json
from colorama import Fore, Back, init, Style
from aStar import astar
init()

board = np.full((100, 100), np.inf)

# TODO : Insert your API-key here
_api_key = "3e555fd2-2d69-482f-b14c-e2fb503d66a5"
# Specify your API-key number of players per game),
# mapname, and number of waterstreams/elevations/powerups here
_api = API(_api_key, 1, "standardmap", 10, 10, 10)
directions = ["n", "e", "s", "w"]


def draw_map(game_state, path=False):
    tile_info = game_state["tileInfo"]
    for y, row in enumerate(tile_info):
        for x, col in enumerate(row):
            type = col["type"][:1]
            direction = col["waterstream"]["direction"] if "waterstream" in col else col[
                "elevation"]["direction"] if "elevation" in col else ' '
            direction = direction.replace('n', '↑').replace(
                'e', '→').replace('s', '↓').replace('w', '←') if type is "w" else direction.replace('n', '↓').replace(
                'e', '←').replace('s', '↑').replace('w', '→')

            if (game_state["yourPlayer"]["yPos"] is y) and (game_state["yourPlayer"]["xPos"] is x):
                print("☻", end='')

            elif path and (x, y) in path:
                print(Back.WHITE + direction, end='')

            elif type is 'f':
                print(Back.GREEN + direction, end='')
            elif type is 'w':
                print(Back.BLUE + direction, end='')
            elif type is 't':
                print(Back.RED + direction, end='')
            elif type is 'g':
                print(Back.YELLOW + direction, end='')
            elif type is "r":
                print(Back.BLACK + direction, end='')
            elif type is "s":
                print(Back.WHITE + "s", end='')
            else:
                print(Back.MAGENTA + " ", end='')
        print(Style.RESET_ALL)


def solution1(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
        prev_pos = (None, None)
        current_direction = "n"
        while not state["gameStatus"] == "done":
            turn = state["turn"]
            # if turn % 10 == 0:
            #     drawMap(state)

            # print("Turn: " + str(turn))
            # print("x: {}, y: {}".format(current_x_pos, current_y_pos))
            tiles = state["tileInfo"]

            if(tree_in_current_direction(state, current_direction)):
                current_direction = get_new_direction(current_direction, False)
            else:
                if not tree_in_any_direction(state):
                    current_direction = get_new_direction(
                        current_direction, True)

            prev_pos = (current_x_pos, current_y_pos)
            response = _api.make_move(game_id, current_direction, "fast")
            state = response["gameState"]
    else:
        print(initial_state["message"])


def map_to_board(state):
    for x, row in enumerate(state):
        for y, tile in enumerate(row):
            if tile["type"] != "forest":
                board[x][y] = 1


def get_dir(current_position, destination)->str:
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


def solution2(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
        path_index = 0
        map_to_board(tiles)
        # TODO: DETECT THESE AUTOMATICALLY IN THE FUTURE
        goal_point = (49, 92)

        # for row in board:
        #     for tile in row:
        #         if tile > 1:
        #             print("B", end='')
        #         else:
        #             print("1", end='')
        #     print("")

        path = astar(
            board, (current_x_pos, current_y_pos), goal_point)
        draw_map(state, path)
        while not state["gameStatus"] == "done":
            current_player = state["yourPlayer"]
            current_y_pos = current_player["yPos"]
            current_x_pos = current_player["xPos"]
            turn = state["turn"]

            tiles = state["tileInfo"]
            direction = get_dir(
                (current_x_pos, current_y_pos), path[path_index])
            path_index += 1
            if direction == None:
                path_index = 0
                path = astar(
                    board, (current_x_pos, current_y_pos), goal_point)
                direction = get_dir(
                    (current_x_pos, current_y_pos), path[path_index])

            response = _api.step(game_id, direction)
            state = response["gameState"]
    else:
        print(initial_state["message"])


def tree_in_any_direction(state) -> bool:
    for direction in directions:
        if tree_in_current_direction(state, direction):
            return True
    return False


def tree_in_current_direction(state, current_direction: str) -> bool:
    """Checks if a tree is in the current dirrection and return true if there is a tree"""

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


def get_new_direction(current_direction, clockwise: bool):
    index = directions.index(current_direction)
    if clockwise:
        return directions[(index+1) % 4]
    else:
        return directions[(index-1) % 4]


def main():
    system('cls')
    _api.end_previous_games_if_any()
    game_id = _api.init_game()
    _api.join_game(game_id)
    readied_game = _api.try_ready_for_game(game_id)
    print(game_id)
    if readied_game is not None:
        print("Joined and readied! Solving...")
        webbrowser.open(
            'http://www.theconsidition.se/ironmandebugvisualizer?gameId={}'.format(game_id), new=2)
        solution2(game_id)
    # game_state = _api.get_game(game_id)
    # drawMap(game_state)

    # Print map to json file.
    # file = open("map.json", "w")
    # file.write(json.dumps(mapDict))
    # file.close()


if __name__ == "__main__":
    main()
