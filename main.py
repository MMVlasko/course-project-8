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
        if euler_button is not None and mode is None:
            euler_button.destroy()
            euler_speech.destroy()
            euler_entry.destroy()

        try:
            data = [list(map(int, i.split())) for i in text.get(0.0, 'end').split('\n') if i]
            if any(data[i][i] for i in range(len(data))):
                err_label.configure(text='Ошибка!', fg='red')
                state_label.configure(text='Некорректный вид матрицы\nсмежности!')
                return
            tour = []
            msg = ''
            vs = []
            for i in range(len(data)):
                for j in range(len(data)):
                    if data[i][j]:
                        vs.append((i + 1, j + 1))

            if all(tuple(reversed(i)) in vs for i in vs):
                msg += 'Введён неориентированный граф.\n'
                vs = list(set([tuple(sorted(i)) for i in vs]))
                can = all(not sum(i) % 2 for i in data)
                if not can:
                    msg += 'Невозможно построить Эйлеров цикл в данном графе!'
                if mode is not None:
                    eu = int(euler_entry.get())
                    tour = nonorient_euler(vs, eu if eu <= len(data) else 1)

            else:
                msg += 'Введён ориентированный граф.\n'
                can = all(sum(data[i]) == sum(data[j][i] for j in range(len(data))) for i in range(len(data)))
                if not can:
                    msg += 'Невозможно построить Эйлеров\nцикл в данном орграфе!'
                if mode is not None:
                    eu = int(euler_entry.get())
                    tour = orient_euler(vs, eu if eu <= len(data) else 1)
            if mode is None:
                state_label.configure(text=f'{msg}{"\nПостроить:" if len(msg) < 35 else ""}')
                if len(msg) < 35:
                    euler_button = ttk.Button(window, text='Эйлеров цикл', command=lambda: build(mode='cycle'))
                    euler_button.place(x=400, y=380)

                    euler_speech = tkinter.Label(text='Начать Эйлеров цикл\n\nс вершины              .', justify='left')
                    euler_speech.place(x=400, y=410)

                    euler_entry = tkinter.Entry(window, width=5)
                    euler_entry.place(x=470, y=437)
                    euler_entry.insert(0, '1')
            else:
                tour = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]

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
                state_label.configure(text='Введена не квадратная матрица!')
                return
            stop.stop = False
            graph(data, base=draw, stop=stop, tour=tour)
            if not stop.stop:
                err_label.configure(text='Завершено.', fg='green')
        except ValueError:
            err_label.configure(text='Ошибка!', fg='red')
            state_label.configure(text='Введены не числовые значения!')
            return

    window = tkinter.Tk()
    center_window(window, 610, 640)
    window.title('Эйлеровы и Гамильтоновы пути (циклы)')
    window.protocol('WM_DELETE_WINDOW', close)

    euler_button = None
    euler_speech = None
    euler_entry = None

    canvas = tkinter.Canvas(master=window, width=350, height=600)
    canvas.place(x=20, y=20)

    text = tkinter.Text(width=22, height=10)
    text.place(x=400, y=90)
    stop = Stop()

    if os.path.exists('dump.txt'):
        with open('dump.txt') as f:
            text.insert(0.0, f.read())
    else:
        text.insert(0.0, '0 1\n1 0')

    ttk.Button(window, text='Анализ', command=build).place(x=400, y=280)
    ttk.Button(window, text='СТОП', command=abort).place(x=400, y=20)
    ttk.Button(window, text='Справка').place(x=505, y=20)

    err_label = tkinter.Label(window)
    err_label.place(x=490, y=280)

    state_label = tkinter.Label(window, justify='left')
    state_label.place(x=400, y=320)

    tkinter.Label(window, text='Скорость:').place(x=400, y=55)

    speed = tkinter.Entry(window, width=17)
    speed.place(x=470, y=55)
    speed.insert(0, '0')

    d = RawTurtle(canvas)
    d.hideturtle()
    d.write('GRAPH\'S VISUALISATION WELCOME YOU!', align='center')

    window.mainloop()


if __name__ == '__main__':
    main()
