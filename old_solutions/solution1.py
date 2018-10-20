from directions import (directions, get_dir, tree_in_any_direction,
                        tree_in_current_direction)

from api import API

_api_key = "3e555fd2-2d69-482f-b14c-e2fb503d66a5"

_api = API(_api_key, 1, "standardmap", 10, 10, 10)


def get_new_direction(current_direction, clockwise: bool):
    index = directions.index(current_direction)
    if clockwise:
        return directions[(index+1) % 4]
    else:
        return directions[(index-1) % 4]


def solution1(game_id):
    initial_state = _api.get_game(game_id)

    if(initial_state["success"] == True):
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
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
