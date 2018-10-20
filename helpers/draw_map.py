from colorama import Fore, Back, init, Style
init()


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
