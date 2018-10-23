movement_points = {"fast": 210, "medium": 150, "slow": 100}
stamina_costs = {"fast": 50, "medium": 30, "slow": 10, "step": 15}
moves = ["fast", "medium", "slow", "step"]


def stamina_regeneration(current_stamina: int)->int:
    return 15 if current_stamina < 60 else 20


def new_stamina(current_stamina: int, speed: str)->int:
    return max( (current_stamina - stamina_costs[speed]), 0)


def real_movment_points(current_stamina: int, speed: str):
    if current_stamina >= stamina_costs[speed]:
        return movement_points[speed]
    else:
        return (current_stamina / stamina_costs[speed]) * movement_points[speed]
