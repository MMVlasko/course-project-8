def find_eulerian_tour(gr, start):
    stack = []
    tour = []

    stack.append(start)
    while len(stack) > 0:
        v = stack[-1]

        degree = get_degree(v, gr)

        if degree == 0:
            stack.pop()
            tour.append(v)
        else:
            index, edge = get_edge_and_index(v, gr)
            gr.pop(index)
            stack.append(edge[1])
    return list(reversed(tour))


def get_degree(v, gr):
    degree = 0
    for (x, y) in gr:
        if v == x:
            degree += 1

    return degree


def get_edge_and_index(v, gr):
    for i in range(len(gr)):
        if v == gr[i][0]:
            return i, gr[i]


graph = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 2), (2, 6), (6, 0)]

print((find_eulerian_tour(graph, 4)))