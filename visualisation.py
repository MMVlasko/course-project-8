from math import asin, degrees, cos, radians


def center_window(roots, x_width, height):
    x_window_height = height
    x_window_width = x_width

    screen_width = roots.winfo_screenwidth()
    screen_height = roots.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (x_window_width / 2))
    y_coordinate = int((screen_height / 2) - (x_window_height / 2))

    roots.geometry(f'{x_window_width}x{x_window_height}+{x_coordinate}+{y_coordinate}')


def pointer(col='black', base=None):
    base.pendown()
    base_col = base.pencolor()
    base.pencolor(col)
    base.begin_fill()
    base.left(150)
    base.forward(15)
    base.left(120)
    base.forward(15)
    base.left(120)
    base.forward(15)
    base.right(30)
    base.end_fill()
    base.pencolor(base_col)
    base.penup()


def peak(n, bg='black', fg='white', out=0.0, inp=0.0, end='down', draw=1, base=None, step=None):
    base.penup()
    if inp:
        base.forward(20)
        base.left(180 - inp)
        base.forward(20)
        base.left(90)
    if draw:
        base.pendown()
    base.color(bg)
    if draw:
        base.begin_fill()
    base.circle(20)
    if draw:
        base.end_fill()
    base.left(90)
    base.penup()
    base.forward(8)
    base.left(90)
    base.forward(4)
    base.color(fg)
    if draw:
        base.write(
            str(n),
            False,
            font=('Times New Roman', 17, 'bold')
        )
    base.color(bg)
    base.right(180)
    base.forward(4)
    base.left(90)
    base.forward(12)
    if step is not None:
        if step[0] == 'l':
            base.left(90)
            base.forward(25)
            base.right(90)
        else:
            base.right(90)
            base.forward(25)
            base.left(90)
        base.color('red')
        base.write(
            ', '.join(step[1]),
            False,
            font=('Times New Roman', 12, 'bold'),
            align='right' if step[0] == 'l' else 'left'
        )
        base.color(bg)
        if step[0] == 'r':
            base.left(90)
            base.forward(25)
            base.right(90)
        else:
            base.right(90)
            base.forward(25)
            base.left(90)

    base.right(180 - out)
    base.forward(20)

    if end == 'down':
        base.pendown()


def graph(data, base=None, stop=None, tour=None):
    number = len(data)
    graphs = list(range(1, number + 1))
    memory = []

    def p():
        return {item, pk} not in memory

    for item in range(number):
        if stop.stop:
            return
        inp = None
        if item % 4 in (0, 2):
            inp = 180
        elif item % 4 == 1:
            inp = 270
        elif item % 4 == 3:
            inp = 90
        marks = [str(i + 1) for i in range(len(tour)) if tour[i][0] == item + 1]
        peak(item + 1, inp=inp if item else 0, end='up', out=0, draw=graphs[item], base=base,
             step=('l' if item % 4 in (0, 3) else 'r',
                   marks + ([str(len(tour) + 1)] if item + 1 == tour[-1][1] else []) if tour else []))

        for pk in range(number):

            color = ('black', 'red')[int((item + 1, pk + 1) in tour)]

            if stop.stop:
                return
            if data[item][pk]:
                place = (pk + 1) // 2 + (0 if pk % 2 else 1)
                now_place = (item + 1) // 2 + (0 if item % 2 else 1)
                delta = place - now_place

                if (item % 4 in (0, 3) and pk % 4 in (0, 3)) or (item % 4 in (1, 2) and pk % 4 in (1, 2)):
                    if abs(delta) == 1:
                        if delta < 0:
                            base.penup()
                            base.left(180)
                            base.forward(40)
                            if p():
                                base.pendown()
                            base.forward(120 * abs(delta))
                            pointer(base=base, col=color)
                            base.right(90)
                            peak(pk + 1, draw=graphs[pk], base=base)
                            base.penup()
                            base.forward(120 * abs(delta) + 40)

                        else:
                            if p():
                                base.pendown()
                            base.forward(120 * delta)
                            pointer(base=base, col=color)
                            peak(pk + 1, inp=180, out=180, draw=graphs[pk], base=base)
                            base.penup()
                            base.forward(120 * delta)
                            base.left(180)

                    else:
                        s_angle = (180 if delta > 0 else 0) - (1 if delta > 0 else -1) * 5 * abs(delta)
                        angle = 5 * abs(delta)
                        way = cos(radians(5 * abs(delta)))
                        base.penup()
                        base.left(180)
                        base.forward(20)

                        if item % 4 in (0, 3) and pk % 4 in (0, 3):
                            base.left(s_angle)
                            base.forward(20)
                            if p():
                                base.pendown()
                            base.forward(160 // way - 20)
                            base.right(angle) if delta < 0 else base.left(angle)
                            base.forward((abs(delta) - 2) * 160)
                            base.right(angle) if delta < 0 else base.left(angle)
                            base.forward(160 // way - 20)
                            pointer(base=base, col=color)
                            peak(pk + 1, inp=360 - s_angle, out=360 - s_angle, draw=graphs[pk],
                                 base=base)
                            base.penup()
                            base.forward(160 // way - 20)
                            base.left(angle) if delta < 0 else base.right(angle)
                            base.forward((abs(delta) - 2) * 160)
                            base.left(angle) if delta < 0 else base.right(angle)
                            base.forward(160 // way)
                            base.right(s_angle)

                        else:
                            base.right(s_angle)
                            base.forward(20)
                            if p():
                                base.pendown()
                            base.forward(160 // way - 20)
                            base.left(angle) if delta < 0 else base.right(angle)
                            base.forward((abs(delta) - 2) * 160)
                            base.left(angle) if delta < 0 else base.right(angle)
                            base.forward(160 // way - 20)
                            pointer(base=base, col=color)
                            peak(pk + 1, inp=s_angle, out=s_angle, draw=graphs[pk], base=base)
                            base.penup()
                            base.forward(160 // way - 20)
                            base.right(angle) if delta < 0 else base.left(angle)
                            base.forward((abs(delta) - 2) * 160)
                            base.right(angle) if delta < 0 else base.left(angle)
                            base.forward(160 // way)
                            base.left(s_angle)

                        base.forward(20)

                elif pk // 2 == item // 2:
                    base.penup()
                    base.left(180)
                    base.forward(20)
                    if item % 4 in (0, 3):
                        base.right(90)
                    else:
                        base.left(90)
                    base.forward(20)
                    if p():
                        base.pendown()
                    base.forward(120)
                    pointer(base=base, col=color)
                    if item % 4 in (0, 3):
                        peak(pk + 1, inp=270, out=270, draw=graphs[pk], base=base)
                    else:
                        peak(pk + 1, inp=90, out=90, draw=graphs[pk], base=base)
                    base.penup()
                    base.forward(140)
                    if item % 4 in (0, 3):
                        base.left(90)
                    else:
                        base.right(90)
                    base.forward(20)

                else:
                    angle = degrees(asin((abs(delta) * 190) / ((abs(delta) * 190) ** 2 + 190 ** 2) ** 0.5))
                    base.left(180)
                    base.forward(20)
                    if delta > 0 and item % 4 in (0, 3):
                        base.right(90 + angle)
                    elif delta > 0 and item % 4 in (1, 2):
                        base.left(90 + angle)
                    elif delta < 0 and item % 4 in (0, 3):
                        base.right(90 - angle)
                    elif delta < 0 and item % 4 in (1, 2):
                        base.left(90 - angle)
                    base.forward(20)
                    if p():
                        base.pendown()
                    base.forward(int(((abs(delta) * 160) ** 2 + 160 ** 2) ** 0.5 - 40))
                    pointer(base=base, col=color)
                    if delta > 0 and item % 4 in (0, 3):
                        peak(pk + 1, inp=270 - angle, out=270 - angle, draw=graphs[pk], base=base)
                    elif delta > 0 and item % 4 in (1, 2):
                        peak(pk + 1, inp=90 + angle, out=90 + angle, draw=graphs[pk], base=base)
                    elif delta < 0 and item % 4 in (0, 3):
                        peak(pk + 1, inp=270 + angle, out=270 + angle, draw=graphs[pk], base=base)
                    elif delta < 0 and item % 4 in (1, 2):
                        peak(pk + 1, inp=90 - angle, out=90 - angle, draw=graphs[pk], base=base)

                    base.penup()
                    base.forward(int(((abs(delta) * 160) ** 2 + 160 ** 2) ** 0.5 - 20))
                    if delta > 0 and item % 4 in (0, 3):
                        base.left(90 + angle)
                    elif delta > 0 and item % 4 in (1, 2):
                        base.right(90 + angle)
                    elif delta < 0 and item % 4 in (0, 3):
                        base.left(90 - angle)
                    elif delta < 0 and item % 4 in (1, 2):
                        base.right(90 - angle)
                    base.forward(20)
                memory.append({item, pk})
                graphs[pk] = 0

        base.right(180)
        base.forward(20)

        if item % 4 == 0:
            base.right(90)
        elif item % 4 in (1, 3):
            base.right(180)
        elif item % 4 == 2:
            base.left(90)

        base.forward(140)
        base.pendown()
        graphs[item] = 0
