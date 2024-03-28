from check import check_tour


def orient_euler(gr, start):
    tour = _orient_euler(gr.copy(), start)
    if not check_tour(tour, gr.copy()[:-1], True):
        tour = special_euler(gr[:-1], start)
    if not check_tour(tour, gr.copy(), True):
        tour = special_euler(gr, start, last=True)[:-1]
    return tour


def _orient_euler(gr, start):
    stack, tour = [start], []

    while len(stack) > 0:
        v = stack[-1]

        if not get_degree(v, gr):
            stack.pop()
            tour.append(v)

        else:
            index, edge = get_edge_and_index(v, gr, False)
            gr.pop(index)
            stack.append(edge[1])

    return list(reversed(tour))


def special_euler(gr, start, last=False):
    stack, tour = [start], []

    while len(stack):
        v = stack[-1]

        if get_degree(v, gr):
            ind = get_edge_and_index(v, gr.copy(), True, last=last)[0]
            stack.append(gr[ind][1])
            gr.pop(ind)

        else:
            tour.append(stack[-1])
            stack.pop(-1)

    return list(reversed(tour))


def get_degree(v, gr):
    degree = 0
    for (x, y) in gr:
        if v == x:
            degree += 1

    return degree


def get_edge_and_index(v, gr, spec, last=False):
    for i in range(len(gr)):
        if v == gr[i][0] and (gr[i] != gr[-1] or spec):
            if last:
                temp = gr.copy()
                if (gr[i][1], v) in temp and (v, gr[i][1]) not in temp:
                    temp.remove((gr[i][1], v))
                if get_degree(gr[i][1], temp):
                    return i, gr[i]

            else:
                if spec:
                    temp = gr.copy()
                    if (gr[i][1], v) in temp and (v, gr[i][1]) not in temp:
                        temp.remove((gr[i][1], v))
                    if get_degree(gr[i][1], temp):
                        return i, gr[i]

                else:
                    return i, gr[i]

    return len(gr) - 1, gr[-1]
