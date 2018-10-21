import json
import random
import sys
import webbrowser
from os import system
import time

import numpy as np
import scipy as scipy

from a_star import astar
from api import API
from directions import (directions, get_dir, tree_in_any_direction,
                        tree_in_current_direction)
from helpers.draw_map import draw_map
from board import map_to_board_first, get_board, astar_shortest_path
from tiles import get_next_best_move, get_goal


_api_key = "3e555fd2-2d69-482f-b14c-e2fb503d66a5"

_api = API(_api_key, 1, "standardmap", 10, 10, 10)


def solution2(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
        path_index = 0
        map_to_board_first(tiles)
        # TODO: DETECT THESE AUTOMATICALLY IN THE FUTURE
        goal_point = get_goal(tiles)

        # for row in get_board():
        #     for tile in row:
        #         print(str(tile)[:1], end='')
        #     print("")

        path = astar(
            get_board(), (current_x_pos, current_y_pos), goal_point)
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
                    get_board(), (current_x_pos, current_y_pos), goal_point)
                direction = get_dir(
                    (current_x_pos, current_y_pos), path[path_index])

            response = _api.step(game_id, direction)
            state = response["gameState"]
    else:
        print(initial_state["message"])


def solution3(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        turn = state["turn"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_position = (current_player["xPos"], current_player["yPos"])
        path_index = 0
        map_to_board_first(tiles)
        # TODO: DETECT THESE AUTOMATICALLY IN THE FUTURE
        goal_point = get_goal(tiles)

        path = astar_shortest_path(state, current_position, goal_point)
        draw_map(state, path)
        while (not state["gameStatus"] == "done") and (current_position != goal_point):
            current_player = state["yourPlayer"]
            current_position = (current_player["xPos"], current_player["yPos"])
            turn = state["turn"]

            tiles = state["tileInfo"]
            direction = get_dir(
                current_position, path[path_index])
            path_index += 1
            if direction == None:
                path_index = 0
                # path = astar_shortest_path(state, current_position, goal_point)
                direction = get_dir(
                    current_position, path[path_index])

            next_move = get_next_best_move(path, state)

            if next_move["direction"] == "":
                response = _api.rest(game_id)
            elif next_move["move"] == "step":
                response = _api.step(game_id, next_move["direction"]) 
            else:
                response = _api.make_move(game_id, next_move["direction"], next_move["move"])
            print(current_position)

            print("Stamina: " + str(current_player["stamina"]))
            state = response["gameState"]
            #time.sleep(2)
            # weird hard check when game won't stop
            if ("message" in response) and (response["message"] == "Game has finished"):
                break
        draw_map(state, path)
        print("Turns: "+str(turn))
    else:
        print(initial_state["message"])


def main():
    system('cls')
    _api.end_previous_games_if_any()
    game_id = _api.init_game()
    _api.join_game(game_id)
    readied_game = _api.try_ready_for_game(game_id)
    print(game_id)
    if readied_game is not None:
        print("Joined and readied! Solving...")
        # webbrowser.open(
        #    'http://www.theconsidition.se/ironmandebugvisualizer?gameId={}'.format(game_id), new = 2)
        solution3(game_id)
    # game_state = _api.get_game(game_id)
    # drawMap(game_state)


if __name__ == "__main__":
    main()
