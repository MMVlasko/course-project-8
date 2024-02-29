from turtle import RawTurtle
import tkinter
from tkinter import ttk
import os.path

from graph import nonorient_euler
from orgraph import orient_euler
from visualisation import graph, center_window


class Stop:
    def __int__(self):
        self.stop = False


def main():
    def abort():
        err_label.configure(text='Отменено.', fg='orange')
        stop.stop = True

    def close():
        with open('dump.txt', 'w') as file:
            file.write(text.get(0.0, 'end'))
        window.quit()

    def build(mode=None):
        nonlocal canvas, euler_button, euler_speech, euler_entry
        if mode is None:
            euler_button.destroy()
            euler_speech.destroy()
            euler_entry.destroy()

        try:
            data = [list(map(int, i.split())) for i in text.get(0.0, 'end').split('\n') if i]

            if not all(len(i) == len(data[0]) for i in data):
                err_label.configure(text='Ошибка!', fg='red')
                state_label.configure(text='Введена не квадратная матрица!')
                return

            if any(data[i][i] for i in range(len(data))):
                err_label.configure(text='Ошибка!', fg='red')
                state_label.configure(text='Некорректный вид матрицы\nсмежности!')
                return

            tour, msg, vs = [], '', []
            start = end = info_tour = None

            for i in range(len(data)):
                for j in range(len(data)):
                    if data[i][j]:
                        vs.append((i + 1, j + 1))

            if all(tuple(reversed(i)) in vs for i in vs):
                msg += 'Введён неориентированный граф.\n\n'
                vs = list(set([tuple(sorted(i)) for i in vs]))
                can = all(not sum(i) % 2 for i in data)
                if not can:
                    if sum(sum(i) % 2 for i in data) == 2:
                        start, end = [i + 1 for i in range(len(data)) if sum(data[i]) % 2]
                        msg += f'В данном графе существует\nэйлеров путь из {start} в {end}.\n\n'
                        state = 'way'
                    else:
                        msg += 'Невозможно построить Эйлеров цикл в данном графе!'
                        state = 'fail'
                else:
                    state = 'cycle'
                if mode == 'cycle':
                    eu = int(euler_entry.get())
                    tour = nonorient_euler(vs, eu if eu <= len(data) else 1)
                elif mode == 'way':
                    vs = ([(end, start)] if (start, end) not in vs else []) + vs
                    tour = nonorient_euler(vs, start, warn=(start, end))
                    tour.pop(-1)

            else:
                msg += 'Введён ориентированный граф.\n\n'
                can = all(sum(data[i]) == sum(data[j][i] for j in range(len(data))) for i in range(len(data)))
                if not can:
                    if sum((sum(data[i]) != sum(data[j][i] for j in range(len(data)))) for i in range(len(data))) == 2:
                        print([sum(data[i]) + sum(data[j][i] for j in range(len(data))) % 2 for i in range(len(data))])
                        start, end = [i + 1 for i in range(len(data)) if (
                                sum(data[i]) + sum(data[j][i] for j in range(len(data)))) % 2]
                        msg += f'В данном графе существует\nэйлеров путь из {start} в {end}.\n\n'
                        state = 'way'
                    else:
                        state = 'fail'
                        msg += 'Невозможно построить Эйлеров\nцикл в данном орграфе!'
                else:
                    state = 'cycle'
                if mode == 'cycle':
                    eu = int(euler_entry.get())
                    tour = orient_euler(vs, eu if eu <= len(data) else 1)
                elif mode == 'way':
                    vs += [(end, start)] if ((end, start) not in vs and (start, end) not in vs) else []
                    tour = orient_euler(vs, start)
                    if tour[0] != tour[-2]:
                        tour.pop(-1)

            if mode is None:
                state_label.configure(text=f'{msg}{"Построить:" * (state != "fail")}')
                if state == 'cycle':
                    euler_button = ttk.Button(window, text='Эйлеров цикл', command=lambda: build(mode='cycle'))
                    euler_button.place(x=550, y=380)

                    euler_speech = tkinter.Label(text='Начать Эйлеров цикл\n\nс вершины              .', justify='left')
                    euler_speech.place(x=550, y=410)

                    euler_entry = tkinter.Entry(window, width=5)
                    euler_entry.place(x=620, y=437)
                    euler_entry.insert(0, '1')
                elif state == 'way':
                    euler_button = ttk.Button(window, text='Эйлеров путь', command=lambda: build(mode='way'))
                    euler_button.place(x=550, y=420)
            else:
                info_tour = tour.copy()
                tour = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]

            err_label.configure(text='Построение...', fg='black')
            canvas.destroy()
            canvas = tkinter.Canvas(master=window, width=500, height=600)
            canvas.place(x=20, y=20)
            draw = RawTurtle(canvas)
            draw.hideturtle()
            draw.speed(int(speed.get()))
            draw.penup()
            draw.left(90)
            draw.forward(230)
            draw.left(90)
            draw.forward(80)
            draw.left(180)
            draw.pendown()
            draw.pensize(3)
            stop.stop = False
            graph(data, base=draw, stop=stop, tour=tour, info_tour=info_tour)
            if not stop.stop:
                err_label.configure(text='Завершено.', fg='green')
        except ValueError:
            err_label.configure(text='Ошибка!', fg='red')
            state_label.configure(text='Введены не числовые значения!')
            return

    window = tkinter.Tk()
    center_window(window, 750, 640)
    window.title('Эйлеровы и Гамильтоновы пути (циклы)')
    window.protocol('WM_DELETE_WINDOW', close)

    euler_button = tkinter.Entry()
    euler_speech = tkinter.Entry()
    euler_entry = tkinter.Entry()

    canvas = tkinter.Canvas(master=window, width=500, height=600)
    canvas.place(x=20, y=20)

    text = tkinter.Text(width=22, height=10)
    text.place(x=550, y=90)
    stop = Stop()

    if os.path.exists('dump.txt'):
        with open('dump.txt') as f:
            text.insert(0.0, f.read())
    else:
        text.insert(0.0, '0 1\n1 0')

    ttk.Button(window, text='Анализ', command=build).place(x=550, y=280)
    ttk.Button(window, text='СТОП', command=abort).place(x=550, y=20)
    ttk.Button(window, text='Справка').place(x=655, y=20)

    err_label = tkinter.Label(window)
    err_label.place(x=640, y=280)

    state_label = tkinter.Label(window, justify='left')
    state_label.place(x=550, y=320)

    tkinter.Label(window, text='Скорость:').place(x=550, y=55)

    speed = tkinter.Entry(window, width=17)
    speed.place(x=625, y=55)
    speed.insert(0, '0')

    d = RawTurtle(canvas)
    d.hideturtle()
    d.write('GRAPH\'S VISUALISATION WELCOME YOU!', align='center')

    window.mainloop()


if __name__ == '__main__':
    main()
