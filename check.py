def check_tour(tour, graph):
    for i in range(1, len(tour)):
        if (tour[i - 1], tour) not in graph:
            return False
    return True
