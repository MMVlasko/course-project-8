from itertools import permutations


def recur_way(potential, way, graph, orient):
    if potential == way:
        return True
    elif (potential[-1], way[len(potential)]) in graph or (
            False if orient else (way[len(potential)], potential[-1]) in graph):
        return recur_way(way[:len(potential) + 1], way, graph, orient)
    else:
        return False


def hamilton_way(graph, orient):
    _set = sorted(list(set([i[0] for i in graph] + [i[1] for i in graph])))
    k = 0
    for i in permutations(_set):
        k += 1
        if recur_way([i[0]], i, graph, orient):
            return list(i)
