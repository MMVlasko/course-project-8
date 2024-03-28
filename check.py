def check_tour(tour, graph, orient, ham=False):
    data = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]

    for i in data:
        if (i not in graph and orient) or (i not in graph and i not in graph and not orient) or (ham and data.count(i) > 1 and tour[0] != tour[-1]):
            return False
    return True
