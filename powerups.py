instant_powerups = {"RemoveClouds": 0, "RestoreStamina": 0, "InvertStreams": 0}
duration_powerups = {
    "Shoes", 10,
    "Flippers", 10,
    "Cycletire", 10,
    "Umbrella", 25,
    "Energyboost", 10,
    "Potion", 10,
    "Helmet", 25,
    "StaminaSale", 10,
    "Spikeshoes", 10,
    "Cyclops", 10,
    "BicycleHandlebar", 10,
}
powerup_terrain = {
    "Flippers": "water",
    "Shoes": "trail",
    "Cycletire": "road"
}
terrain_powerups = {
    "water": "Flippers",
    "trail": "Shoes",
    "road": "Cycletire"
}
drop_list = [
    "BicycleHandlebar",
    "Spikeshoes",
    "Cyclops"
]
cool_powerups = [
    "Energyboost",
    "Potion",
    "StaminaSale"
]

powerup_bag = []
powerups_active = []


def get_powerup(tile):
    if "powerup" in tile:
        return tile["powerup"]["name"]
    else:
        return None

def get_powerup_terrain(powerup):
    return powerup_terrain[powerup] if powerup in powerup_terrain else None

def update_powerups_value():
    pass

def calculate_powerups(previous_powerups, new_powerups):
    return (previous_powerups + new_powerups)[:3]

def map_active_powerups(active_powerups):
    obj = {}
    for powerup in active_powerups:
        obj[powerup["name"]] = powerup["duration"]
    return obj