def orient_euler(gr, start):
    stack, tour = [], []

    stack.append(start)
    while len(stack) > 0:
        v = stack[-1]
        degree = get_degree(v, gr)

        if not degree:
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
