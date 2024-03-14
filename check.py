def check_tour(tour, graph, orient):
    data = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]
    for i in data:
        if (i not in graph and orient) or (i not in graph and i not in graph and not orient) or data.count(i) == 2:
            return False
    return True
