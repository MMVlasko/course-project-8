def not_orient_euler(graph, start, warn=(0, 0)):
    stack, tour = [], []
    stack.append(start)

    while len(stack) > 0:
        v = stack[-1]
        degree = get_degree(v, graph)

        if not degree:
            stack.pop()
            tour.append(v)
        else:
            index, edge = get_edge_and_index(v, graph, warn=warn)
            graph.pop(index)
            stack.append(edge[1] if v == edge[0] else edge[0])
    return tour


def get_degree(v, graph):
    degree = 0
    for (x, y) in graph:
        if v == x or v == y:
            degree += 1
    return degree


def get_edge_and_index(v, graph, warn):
    for i in range(len(graph)):
        if (v == graph[i][0] or v == graph[i][1]) and not (v == graph[i][0] and graph[i] == warn):
            return i, graph[i]
