from turtle import RawTurtle
from math import asin, degrees, cos, radians
import tkinter
from tkinter import ttk
import os.path


class Stop:
    def __int__(self):
        self.stop = False


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


def peak(n, bg='black', fg='white', out=0.0, inp=0.0, end='down', draw=1, base=None):
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
    base.right(180 - out)
    base.forward(20)

    if end == 'down':
        base.pendown()


def graph(data, base=None, stop=None):
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

        peak(item + 1, inp=inp if item else 0, end='up', out=0, draw=graphs[item], base=base)

        for pk in range(number):
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
                            pointer(base=base)
                            base.right(90)
                            peak(pk + 1, draw=graphs[pk], base=base)
                            base.penup()
                            base.forward(120 * abs(delta) + 40)

                        else:
                            if p():
                                base.pendown()
                            base.forward(120 * delta)
                            pointer(base=base)
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
                            pointer(base=base)
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
                            pointer(base=base)
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
                    pointer(base=base)
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
                    pointer(base=base)
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


def main():
    def abort():
        err_label.configure(text='Отменено.', fg='orange')
        stop.stop = True

    def close():
        with open('dump.txt', 'w') as file:
            file.write(text.get(0.0, 'end'))
        window.quit()

    def build():
        nonlocal canvas
        try:
            data = [list(map(int, i.split())) for i in text.get(0.0, 'end').split('\n') if i]
            err_label.configure(text='Построение...', fg='black')
            canvas.destroy()
            canvas = tkinter.Canvas(master=window, width=350, height=600)
            canvas.place(x=20, y=20)
            draw = RawTurtle(canvas)
            draw.hideturtle()
            draw.speed(int(speed.get()))
            draw.penup()
            draw.left(90)
            draw.forward(230)
            draw.left(90)
            draw.forward(70)
            draw.left(180)
            draw.pendown()
            draw.pensize(3)
            if any(len(data) != len(i) for i in data):
                err_label.configure(text='Ошибка!', fg='red')
                return
            stop.stop = False
            graph(data, base=draw, stop=stop)
            if not stop.stop:
                err_label.configure(text='Завершено.', fg='green')
        except ValueError:
            err_label.configure(text='Ошибка!', fg='red')
            return

    window = tkinter.Tk()
    center_window(window, 610, 640)
    window.title('Эйлеровы и Гамильтоновы пути (циклы)')
    window.protocol('WM_DELETE_WINDOW', close)

    canvas = tkinter.Canvas(master=window, width=350, height=600)
    canvas.place(x=20, y=20)

    text = tkinter.Text(width=22, height=10)
    text.place(x=400, y=20)
    stop = Stop()

    if os.path.exists('dump.txt'):
        with open('dump.txt') as f:
            text.insert(0.0, f.read())
    else:
        text.insert(0.0, '0 1\n1 0')

    ttk.Button(window, text='Построить', command=build).place(x=400, y=210)
    ttk.Button(window, text='СТОП', command=abort).place(x=400, y=310)
    ttk.Button(window, text='Справка').place(x=500, y=310)

    err_label = tkinter.Label(window)
    err_label.place(x=490, y=210)

    tkinter.Label(window, text='Скорость:').place(x=400, y=260)

    speed = tkinter.Entry(window, width=17)
    speed.place(x=470, y=260)
    speed.insert(0, '0')

    d = RawTurtle(canvas)
    d.hideturtle()
    d.write('GRAPH\'S VISUALISATION WELCOME YOU!', align='center')

    window.mainloop()


main()
