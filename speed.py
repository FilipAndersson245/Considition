speed_points = {"Fast": 210, "Medium": 150, "Slow": 100}
speed_costs = {"Fast": 50, "Medium": 30, "Slow": 10, "Step": 15}


def stamina_regeneration(current_stamina: int)->int:
    return 15 if current_stamina < 65 else 20
