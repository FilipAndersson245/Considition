tile_costs = {"water": 45, "road": 31, "trail": 40, "grass": 50}


def can_i_afford_to_move(movment_points: int, tile_type: str)->bool:
    """
    Checks if a move can be afforded.  
    Does not take stream/uphill into consideration
    """
    if tile_type in tile_costs:
        return True if movment_points-tile_costs[tile_type] > 0 else False
    else:
        print("Error ({}) is not a valid tyletype!".format(tile_type))
