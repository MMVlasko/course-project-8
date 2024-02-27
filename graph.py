def nonorient_euler(gr, start):
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
            stack.append(edge[1] if v == edge[0] else edge[0])
    return tour


def get_degree(v, gr):
    degree = 0
    for (x, y) in gr:
        if v == x or v == y:
            degree += 1
    return degree


def get_edge_and_index(v, gr):
    for i in range(len(gr)):
        if v == gr[i][0] or v == gr[i][1]:
            return i, gr[i]


if __name__ == '__main__':
    graph = [(0, 1), (1, 5), (5, 0)]

    print((nonorient_euler(graph, 5)))