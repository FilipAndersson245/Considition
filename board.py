import matplotlib.pyplot as plt
import numpy as np
from typing import Set, Tuple
from tiles import tile_costs
import networkx as nx
from os import sys
from directions import get_dir, get_boost_value, get_elevation_stream_direction, opposite_directions
board: np.ndarray = np.full((100, 100), np.inf)

# debuging


def get_board():
    """
    Get current board
    """
    return board


def map_to_board_first(state):
    """
    Update board with a given state
    """
    for x, row in enumerate(state):
        for y, tile in enumerate(row):
            tile_type = tile["type"]
            if tile_type != "forest":
                board[x][y] = (tile_costs[tile_type] /
                               100) if tile_type in tile_costs else 1
    return board


def direction_we_are_moving(u, v):
    pass


def place_tile_types_in_board_state(state):
    """
    Update board with a given state
    """
    board_of_types = np.ndarray((100, 100), dtype=object)
    for x, row in enumerate(state["tileInfo"]):
        for y, tile in enumerate(row):
            tile_type = tile.get("type")
            board_of_types[x][y] = tile["type"]

    return board_of_types


def map_to_board_optimization(state):
    pass


# # TODO Include elevation/streams
# def generate_graph(state):
#     grid = place_tile_types_in_board_state(state)
#     F = nx.grid_2d_graph(100, 100)
#     G = nx.Graph()
#     for (u, v) in F.edges():
#         if grid[u[0], u[1]] == "forest" and grid[v[0], v[1]] == "forest":
#             continue
#         elif grid[v[0], v[1]] == "forest":
#             continue
#         elif grid[v[0], v[1]] != "forest":
#             tile_type_cost = tile_costs[grid[v[0], v[1]]]
#             G.add_edge(u, v, weight=tile_type_cost)
#     return G

def add_neighbours(tiles, G, own: Tuple[int, int]):
    neighbours = np.array([None, None, None, None], None)
    own_tile = tiles[own[1]][own[0]]["type"]
    if(own_tile == "forest" or len(G.edges(own)) == 4):
        return neighbours
    else:
        neighbours[0] = other = (own[0]+1, own[1])
        create_connection(G, own, other, tiles)

        neighbours[1] = other = (own[0], own[1]+1)
        create_connection(G, own, other, tiles)

        neighbours[2] = other = (own[0]-1, own[1])
        create_connection(G, own, other, tiles)

        neighbours[3] = other = (own[0], own[1]-1)
        create_connection(G, own, other, tiles)
    return neighbours


def create_connection(G, own, other, tiles):
    if not G.has_edge(own, other):
        moving_direction = get_dir(own, other)
        boost = get_boost_value(moving_direction, tiles[other[1]][other[0]])
        tile_cost = (tile_costs[tiles[other[1]][other[0]]["type"]] + boost)

        current_tile_push = get_elevation_stream_direction(
            tiles[other[1]][other[0]])
        if current_tile_push is not None:
            if moving_direction == current_tile_push:
                tile_cost -= 5
            elif moving_direction != opposite_directions[current_tile_push]:
                tile_cost += 5
        if tile_cost < 0:
            tile_cost = 1
        G.add_edge(own, other, weight=(tile_cost))


def generate_graph(state, currentPos: Tuple[int, int]):
    G = nx.Graph()
    G.add_node(currentPos)
    added_nodes = [currentPos]
    while added_nodes:
        neighbours = add_neighbours(state["tileInfo"], G, added_nodes.pop(-1))

        for val in neighbours:
            if val != None:
                added_nodes.append(val)
    return G


def astar_shortest_path(state, start: Tuple[int, int], finish: Tuple[int, int]):
    graph = generate_graph(state, start)

    # nx.draw(graph, with_labels=True)

    # plt.show()

    shortest_path = nx.astar_path(graph, start, finish)
    return shortest_path
