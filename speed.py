movement_points = {"fast": 210, "medium": 150, "slow": 100}
stamina_costs = {"fast": 50, "medium": 30, "slow": 10, "step": 15}
moves = ["fast", "medium", "slow", "step"]


def stamina_regeneration(current_stamina: int, active_powerups)->int:
    additional = 0
    if "Energyboost" in active_powerups:
        if active_powerups["Energyboost"] > 0:
            additional = 10
    return (15 if current_stamina < 60 else 20) + additional


def get_stamina_cost(speed, active_powerups):
    multiplier = 1
    if "StaminaSale" in active_powerups:
        if active_powerups["StaminaSale"] > 0:
            multiplier = 0.6
    return multiplier*stamina_costs[speed]


def new_stamina(current_stamina: int, speed: str, active_powerups)->int:
    return max( (current_stamina - get_stamina_cost(speed, active_powerups)), 0)


def real_movment_points(current_stamina: int, speed: str, active_powerups):
    multiplier = 1
    if "Potion" in active_powerups:
        if active_powerups["Potion"] > 0:
            multiplier = 1.5
    if current_stamina >= get_stamina_cost(speed, active_powerups):
        return movement_points[speed] * multiplier
    else:
        return (current_stamina / get_stamina_cost(speed, active_powerups)) * (multiplier * movement_points[speed])
