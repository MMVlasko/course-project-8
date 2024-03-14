def hamilton_way(graph, orient):
    _set = sorted(list(set([i[0] for i in graph] + [i[1] for i in graph])))
    for i in _set:
        temp = graph.copy()
        level = 1
        tour = [i]
        while True:
            if _set == sorted(tour):
                return tour
            elif level == len(_set):
                level -= 1
                if (tour[-2], tour[-1]) in temp:
                    temp.remove((tour[-2], tour[-1]))
                if (tour[-1], tour[-2]) in temp and not orient:
                    temp.remove((tour[-1], tour[-2]))
                tour.pop(-1)
            for j in temp:
                if (j[0] == tour[-1] and j[1] not in tour) or (j[1] == tour[-1] and j[0] not in tour and not orient):
                    tour += [j[1] if j[0] == tour[-1] else j[0]]
                    level += 1
                    break
            else:
                if tour == [i]:
                    break
                level -= 1
                if (tour[-2], tour[-1]) in temp:
                    temp.remove((tour[-2], tour[-1]))
                if (tour[-1], tour[-2]) in temp and not orient:
                    temp.remove((tour[-1], tour[-2]))
                tour.pop(-1)
