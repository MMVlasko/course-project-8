from turtle import RawTurtle
from tkinter import (
    Tk, Entry, Canvas,
    Text, Label, ttk, BooleanVar
)
import os.path

from graph import not_orient_euler
from orgraph import orient_euler
from visualisation import graph, center_window
from hamilton import hamilton_way


class Stop:
    stop = False


class Main:
    def __init__(self):
        self.window = Tk()
        center_window(self.window, 750, 680)
        self.window.title('Эйлеровы и Гамильтоновы пути (циклы)')
        self.window.protocol('WM_DELETE_WINDOW', self.close)

        self.euler_button = Entry()
        self.euler_speech = Entry()
        self.euler_entry = Entry()
        self.hamilton_button = Entry()

        self.canvas = Canvas(master=self.window, width=500, height=640)
        self.canvas.place(x=20, y=20)

        self.text = Text(width=22, height=10)
        self.text.place(x=550, y=90)
        self.stop = Stop()

        if os.path.exists('dump.txt'):
            with open('dump.txt') as f:
                self.text.insert(0.0, f.read())
        else:
            self.text.insert(0.0, '0 1\n1 0')

        self.var = BooleanVar()
        ttk.Checkbutton(self.window, text='Визуализировать при анализе', variable=self.var).place(x=550, y=265)

        ttk.Button(self.window, text='Анализ', command=self.build).place(x=550, y=300)
        ttk.Button(self.window, text='СТОП', command=self.abort).place(x=550, y=20)
        ttk.Button(self.window, text='Справка').place(x=655, y=20)

        self.err_label = Label(self.window)
        self.err_label.place(x=640, y=300)

        self.state_label = Label(self.window, justify='left')
        self.state_label.place(x=550, y=340)

        Label(self.window, text='Скорость:').place(x=550, y=55)

        self.speed = Entry(self.window, width=17)
        self.speed.place(x=625, y=55)
        self.speed.insert(0, '0')

        d = RawTurtle(self.canvas)
        d.hideturtle()
        d.write('GRAPH\'S VISUALISATION WELCOME YOU!', align='center')

    def build(self, mode=None):
        if mode is None:
            self.euler_button.destroy()
            self.euler_speech.destroy()
            self.euler_entry.destroy()
            self.hamilton_button.destroy()

        try:
            data = [list(map(int, i.split())) for i in self.text.get(0.0, 'end').split('\n') if i]

            if not all(len(i) == len(data[0]) for i in data):
                self.err_label.configure(text='Ошибка!', fg='red')
                self.state_label.configure(text='Введена не квадратная матрица!')
                return

            if any(data[i][i] for i in range(len(data))):
                self.err_label.configure(text='Ошибка!', fg='red')
                self.state_label.configure(text='Некорректный вид матрицы\nсмежности!')
                return

            tour, msg, vs, nor = [], '', [], False
            start = end = None

            for i in range(len(data)):
                for j in range(len(data)):
                    if data[i][j]:
                        vs.append((i + 1, j + 1))

            if all(tuple(reversed(i)) in vs for i in vs):
                msg += 'Введён неориентированный граф.\n\n'
                nor = True
                vs = list(set([tuple(sorted(i)) for i in vs]))
                can = all(not sum(i) % 2 for i in data) and all(sum(i) for i in data)
                if not can:
                    if sum(sum(i) % 2 for i in data) == 2:
                        start, end = [i + 1 for i in range(len(data)) if sum(data[i]) % 2]
                        msg += f'В данном графе существует\nЭйлеров путь из {start} в {end}.\n\n'
                        state = 'way'
                    else:
                        msg += 'Невозможно построить Эйлеров\nцикл в данном графе!'
                        state = 'fail'
                else:
                    state = 'cycle'

                if mode == 'cycle':
                    eu = int(self.euler_entry.get())
                    tour = not_orient_euler(vs, eu if eu <= len(data) else 1)
                elif mode == 'way':
                    vs = ([(end, start)] if (start, end) not in vs else []) + vs
                    tour = not_orient_euler(vs, start, warn=(start, end))
                    tour.pop(-1)
                elif mode == 'ham':
                    tour = hamilton_way(vs)

            else:
                msg += 'Введён ориентированный граф.\n\n'
                can = all(sum(data[i]) == sum(data[j][i] for j in range(len(data))) for i in range(len(data)))

                if not can:
                    if sum((sum(data[i]) != sum(data[j][i] for j in range(len(data)))) for i in range(len(data))) == 2 \
                            and all(any(data[i]) and any(data[j][i] for j in range(len(data))) for i in
                                    range(len(data))):
                        temp = [i + 1 for i in range(len(data)) if sum(data[i]) != sum(
                            data[j][i] for j in range(len(data)))]
                        start, end = temp if sum(data[temp[0] - 1]) else reversed(temp)
                        msg += f'В данном графе существует\nЭйлеров путь из {start} в {end}.\n\n'
                        state = 'way'
                    else:
                        state = 'fail'
                        msg += 'Невозможно построить Эйлеров\nцикл в данном орграфе!'
                else:
                    state = 'cycle'

                if mode == 'cycle':
                    eu = int(self.euler_entry.get())
                    tour = orient_euler(vs, eu if eu <= len(data) else 1)
                elif mode == 'way':
                    vs += [(end, start)] if ((end, start) not in vs and (start, end) not in vs) else []
                    tour = orient_euler(vs, start)
                    if tour[0] != tour[-2] and tour[-1] != end:
                        print(tour[-1])
                        tour.pop(-1)
                elif mode == 'ham':
                    tour = hamilton_way(vs)

            if mode is None:
                self.state_label.configure(text=f'{msg}{"Построить:" * (state != "fail")}')
                self.hamilton_button = ttk.Button(text='Гамильтонов путь', command=lambda: self.build(mode='ham'))
                if state == 'cycle':
                    self.euler_button = ttk.Button(self.window, text='Эйлеров цикл',
                                                   command=lambda: self.build(mode='cycle'))
                    self.euler_button.place(x=550, y=400)

                    self.euler_speech = Label(text='Начать Эйлеров цикл\n\nс вершины              .', justify='left')
                    self.euler_speech.place(x=550, y=430)

                    self.euler_entry = Entry(self.window, width=5)
                    self.euler_entry.place(x=620, y=457)
                    self.euler_entry.insert(0, '1')

                    self.hamilton_button.place(x=550, y=490)
                elif state == 'way':
                    self.euler_speech.destroy()
                    self.euler_entry.destroy()
                    self.euler_button = ttk.Button(self.window, text='Эйлеров путь',
                                                   command=lambda: self.build(mode='way'))
                    self.euler_button.place(x=550, y=440)
                    self.hamilton_button.place(x=550, y=480)
                else:
                    self.hamilton_button.place(x=550, y=430)

            self.err_label.configure(text='Построение...', fg='black')
            self.canvas.destroy()
            canvas = Canvas(master=self.window, width=500, height=640)
            canvas.place(x=20, y=20)
            draw = RawTurtle(canvas)
            draw.hideturtle()
            draw.speed(int(self.speed.get()))
            draw.penup()
            draw.left(90)
            if mode is not None:
                draw.forward(290)
                draw.write(
                    'Маршрут:',
                    False,
                    font=('Times New Roman', 14, 'bold'),
                    align='center'
                )
                draw.back(30)
                draw.write(
                    ' - '.join(map(str, tour)),
                    False,
                    font=('Times New Roman', 14, 'bold'),
                    align='center'
                )
                tour = [(tour[i], tour[i + 1]) for i in range(len(tour) - 1)]
                draw.back(70)
            else:
                draw.forward(190)
            draw.left(90)
            draw.forward(80)
            draw.left(180)
            draw.pendown()
            draw.pensize(3)
            self.stop.stop = False
            if mode is not None or self.var.get():
                graph(data, base=draw, stop=self.stop, tour=tour, nor=not nor)
            if not self.stop.stop:
                self.err_label.configure(text='Завершено.', fg='green')
        except ValueError:
            self.err_label.configure(text='Ошибка!', fg='red')
            self.state_label.configure(text='Введены не числовые значения!')
            return

    def abort(self):
        self.err_label.configure(text='Отменено.', fg='orange')
        self.stop.stop = True

    def close(self):
        with open('dump.txt', 'w') as file:
            file.write(self.text.get(0.0, 'end'))
        self.window.quit()


if __name__ == '__main__':
    app = Main()
    app.window.mainloop()
