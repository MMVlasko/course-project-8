from itertools import permutations


def recur_way(potential, way, graph):
    if potential == way:
        return True
    elif (potential[-1], way[len(potential)]) in graph:
        return recur_way(way[:len(potential) + 1], way, graph)
    else:
        return False


def hamilton_way(graph):
    _set = sorted(list(set([i[0] for i in graph] + [i[1] for i in graph])))
    k = 0
    for i in permutations(_set):
        k += 1
        if recur_way([i[0]], i, graph):
            print(k)
            return list(i)
