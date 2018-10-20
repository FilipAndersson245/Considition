movement_points = {"Fast": 210, "Medium": 150, "Slow": 100}
stamina_costs = {"Fast": 50, "Medium": 30, "Slow": 10, "Step": 15}


def stamina_regeneration(current_stamina: int)->int:
    return 15 if current_stamina < 65 else 20


def new_stamina(current_stamina: int, speed: str)->int:
    return current_stamina - stamina_costs[speed]


def real_movment_points(current_stamina: int, speed: str):
    if stamina_costs[speed] >= current_stamina:
        return movement_points[speed]
    else:
        return (current_stamina / stamina_costs[speed]) * movement_points[speed]
