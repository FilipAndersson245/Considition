import json
import random
import sys
import webbrowser
from os import system
import time

import numpy as np

from a_star import astar
from api import API
from directions import (directions, get_dir, tree_in_any_direction,
                        tree_in_current_direction)
from helpers.draw_map import draw_map
from board import map_to_board_first, get_board, astar_shortest_path
from tiles import get_next_best_move, get_goal, all_pos, get_all_best_moves, P_move, is_around, get_n_best_moves
from pprint import pprint
from powerups import *

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
    offs = 0

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        turn = state["turn"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_position = (current_player["xPos"], current_player["yPos"])
        path_index = 0
        map_to_board_first(tiles)
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
                # Create new path everytime devienting from standard path this will incresse time calculating
                # path = astar_shortest_path(state, current_position, goal_point)
                direction = get_dir(
                    current_position, path[path_index])

            next_move = get_next_best_move(path, state)

            print(current_position)

            if next_move["direction"] == "":
                response = _api.rest(game_id)
            elif next_move["move"] == "step":
                response = _api.step(game_id, next_move["direction"])
            else:
                response = _api.make_move(
                    game_id, next_move["direction"], next_move["move"])

            print("Stamina: " + str(current_player["stamina"]))
            state = response["gameState"]
            # time.sleep(2)

            current_player = state["yourPlayer"]
            current_position = (current_player["xPos"], current_player["yPos"])
            print("Position: "+str(current_position))
            print("Predicted: "+str(all_pos[-1]))
            off = abs(current_position[0] - all_pos[-1][0]) + \
                abs(current_position[1] - all_pos[-1][1])
            offs += off
            print("Off by: "+str(off))
            print()

            # weird hard check when game won't stop
            if ("message" in response) and (response["message"] == "Game has finished"):
                break
        draw_map(state, path)
        print("Turns: "+str(turn))
        print("Predicted: "+str(len(all_pos)))
        print("MisPredicts: "+str(offs))
        print("Game-id: "+game_id)
    else:
        print(initial_state["message"])


def solution4(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        turn = state["turn"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_position = (current_player["xPos"], current_player["yPos"])
        path_index = 0
        map_to_board_first(tiles)
        goal_point = (16, 75)

        path = astar_shortest_path(state, current_position, goal_point)
        draw_map(state, path)

        best_move = get_all_best_moves(path, state)
        moves = best_move.previous_moves
        print(best_move.index)

        while moves != []:
            next_move = moves.pop(0)
            if next_move.direction == "":
                response = _api.rest(game_id)
            elif next_move.move == "step":
                response = _api.step(game_id, next_move.direction)
            else:
                pprint(vars(next_move))
                response = _api.make_move(
                    game_id, next_move.direction, next_move.move)

        print("Turns: "+str(turn))
        print("Predicted: "+str(len(all_pos)))
    else:
        print(initial_state["message"])


def solution5(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        turn = state["turn"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_position = (current_player["xPos"], current_player["yPos"])
        path_index = 0
        map_to_board_first(tiles)
        goal_point = get_goal(tiles)
        stamina = current_player["stamina"]

        path = astar_shortest_path(state, current_position, goal_point)
        # draw_map(state, path)

        while (not is_around(goal_point, current_position, 1)):
            powerups = current_player["powerupInventory"]
            active_powerups = map_active_powerups(
                current_player["activePowerups"])
            tile = state["tileInfo"][current_position[1]][current_position[0]]
            current_player = state["yourPlayer"]
            stamina = current_player["stamina"]

            if len(powerups) == 3:
                response = None
                if powerups[2] in drop_list:
                    response = _api.drop_powerup(game_id, powerups[2])
                else:
                    response = _api.use_powerup(game_id, powerups[2])
                state = response["gameState"]
                current_player = state["yourPlayer"]
                stamina = current_player["stamina"]
                powerups = current_player["powerupInventory"]
            else:
                for powerup in powerups:
                    if powerup in cool_powerups and stamina < 60:
                        response = _api.use_powerup(game_id, powerup)
                        state = response["gameState"]
                        current_player = state["yourPlayer"]
                        stamina = current_player["stamina"]
                        powerups = current_player["powerupInventory"]
                        break
                for powerup in powerups:
                    if get_powerup_terrain(powerup) == tile["type"] and powerup not in active_powerups:
                        response = _api.use_powerup(game_id, powerup)
                        state = response["gameState"]
                        current_player = state["yourPlayer"]
                        stamina = current_player["stamina"]
                        powerups = current_player["powerupInventory"]
                        break

            moves = get_n_best_moves(3, path, state)
            for next_move in moves:
                turn += 1
                all_pos.append(next_move.position)
                if next_move.direction == "":
                    response = _api.rest(game_id)
                elif next_move.move == "step":
                    response = _api.step(game_id, next_move.direction)
                else:
                    response = _api.make_move(
                        game_id, next_move.direction, next_move.move)
            state = response["gameState"]
            current_player = state["yourPlayer"]
            stamina = current_player["stamina"]
            current_position = (current_player["xPos"], current_player["yPos"])
            path = astar_shortest_path(state, current_position, goal_point)
        # draw_map(state, path)

        # Hack to go to finnish line!
        print("This should happen max 1 time" + str(path))
        if len(path) == 2:
            direction = get_dir(current_position, path[1])
            response = _api.step(game_id, direction)
            state = response["gameState"]
            print("THE GAME STATE IS:" + str(state["gameStatus"]))
            current_player = state["yourPlayer"]
            current_position = (current_player["xPos"], current_player["yPos"])
            path = astar_shortest_path(state, current_position, goal_point)
        print("Turns: " + str(state["turn"]))
        return state["turn"]
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

        return (game_id, solution5(game_id))

    # game_state = _api.get_game(game_id)
    # drawMap(game_state)


if __name__ == "__main__":
    turns_result = []
    avg = 0
    for i in range(3):
        turns_result.append(main())
        # webbrowser.open(
        #     'http://www.theconsidition.se/ironmandebugvisualizer?gameId={}'.format(turns_result[i][0]), new=2)
    for i in range(4):
        print("Turns for round {}: {}".format(
            turns_result[i][0], str(turns_result[i][1])))
        avg += turns_result[i][1]
    print("avg: " + str(avg/4))
