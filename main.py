"""
Author : tharindra galahena (inf0_warri0r)
Project: artificial life simulation - greenies and blueies
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 29/08/2013
License:

     Copyright 2013 Tharindra Galahena

This is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
this. If not, see http://www.gnu.org/licenses/.

"""


import random
from Tkinter import *


class greeny:
    def __init__(self):
        self.env = list()
        self.env_tmp = list()
        for i in range(0, 100):
            tmp = list()
            tmp2 = list()
            for j in range(0, 100):
                tmp.append(0)
                tmp2.append(0)
            self.env.append(tmp)
            self.env_tmp.append(tmp2)

    def reproduct(self, p, q, bluey_env):

        lst = list()
        for y in range(q - 1, q + 2):
            for x in range(p - 1, p + 2):
                if x >= 0 and y >= 0 and x < 100 and y < 100:
                    if self.env[y][x] == 0 and bluey_env[y][x] == 0:
                        lst.append((x, y))

        if len(lst) > 0:
            n = random.randint(0, len(lst) - 1)
            self.env_tmp[lst[n][1]][lst[n][0]] = 1

    def grow(self, x, y):
        if self.env[y][x] > 0 and self.env[y][x] < 6:
            self.env_tmp[y][x] = self.env[y][x] + 1
        elif self.env[y][x] == 6:
            self.env_tmp[y][x] = self.env[y][x]

    def swap(self):
        for y in range(0, 100):
            for x in range(0, 100):
                self.env[y][x] = self.env_tmp[y][x]
                self.env_tmp[y][x] = 0

    def next_gen(self, bluey_env):
        for y in range(0, 100):
            for x in range(0, 100):
                self.grow(x, y)

        for y in range(0, 100):
            for x in range(0, 100):
                if self.env[y][x] > 0:
                    self.reproduct(x, y, bluey_env)

        self.swap()

    def reset(self):
        for y in range(0, 100):
            for x in range(0, 100):
                self.env[y][x] = 0
                self.env_tmp[y][x] = 0


class bluey:

    def __init__(self):
        self.env = list()
        self.env_tmp = list()
        for i in range(0, 100):
            tmp = list()
            tmp2 = list()
            for j in range(0, 100):
                tmp.append(0)
                tmp2.append(0)
            self.env.append(tmp)
            self.env_tmp.append(tmp2)

    def reproduct(self, p, q, greeny_env):

        lst = list()
        for y in range(q - 1, q + 2):
            for x in range(p - 1, p + 2):
                if x >= 0 and y >= 0 and x < 100 and y < 100:
                    if self.env[y][x] == 0 and greeny_env[y][x] > 0:
                        lst.append((x, y))

        if len(lst) > 0:
            n = random.randint(0, len(lst) - 1)
            self.env_tmp[lst[n][1]][lst[n][0]] = 1
            greeny_env[lst[n][1]][lst[n][0]] = 0
        self.env_tmp[q][p] = self.env[q][p]

    def feed(self, p, q, greeny_env):
        lst = list()
        for y in range(q - 1, q + 2):
            for x in range(p - 1, p + 2):
                if x >= 0 and y >= 0 and x < 100 and y < 100:
                    if greeny_env[y][x] > 2:
                        lst.append((x, y))

        if len(lst) > 0:
            n = random.randint(0, len(lst) - 1)
            self.env_tmp[lst[n][1]][lst[n][0]] = self.env[q][p]
            if self.env_tmp[lst[n][1]][lst[n][0]] < 6:
                self.env_tmp[lst[n][1]][lst[n][0]] = self.env[q][p] + 1
            self.env[q][p] = 0
            greeny_env[lst[n][1]][lst[n][0]] = 0
        else:
            if self.env[q][p] > 0:
                self.env_tmp[q][p] = self.env[q][p] - 1

    def swap(self):
        for y in range(0, 100):
            for x in range(0, 100):
                self.env[y][x] = self.env_tmp[y][x]
                self.env_tmp[y][x] = 0

    def next_gen(self, greeny_env):
        for y in range(0, 100):
            for x in range(0, 100):
                if self.env[y][x] > 0:
                    self.feed(x, y, greeny_env)

        self.swap()

        for y in range(0, 100):
            for x in range(0, 100):
                if self.env[y][x] > 0:
                    self.reproduct(x, y, greeny_env)

        self.swap()

    def reset(self):
        for y in range(0, 100):
            for x in range(0, 100):
                self.env[y][x] = 0
                self.env_tmp[y][x] = 0

################################### display ##################################

root = Tk()
root.title("Greenies and Blueies")

cw = 600
ch = 700

chart_1 = Canvas(root, width=cw, height=ch, background="black")
chart_1.grid(row=0, column=0)


ec = greeny()
an = bluey()

started = False
step_time = 50
reset = False
pause = False


def callback(event):
    global started
    x = int(event.x / 6)
    y = int(event.y / 6)
    if x < 100 and y < 100:
        started = True
        ec.env[y][x] = 1


def callback2(event):
    x = int(event.x / 6)
    y = int(event.y / 6)
    if x < 100 and y < 100:
        an.env[y][x] = 1


def speed(event):
    global step_time
    if event.keysym == "Up":
        if step_time > 0:
            step_time = step_time - 1
    elif event.keysym == "Down":
        step_time = step_time + 1


def reset_func(event):
    global reset
    reset = True


def pause_func(event):
    global pause
    if pause:
        pause = False
    else:
        pause = True

chart_1.bind("<Button-1>", callback)
chart_1.bind("<Button-3>", callback2)
chart_1.bind_all("<KeyPress-Up>", speed)
chart_1.bind_all("<KeyPress-Down>", speed)
chart_1.bind_all("<KeyPress-r>", reset_func)
chart_1.bind_all("<KeyPress-p>", pause_func)

steps = 0

while 1:

    if(started):
        steps = steps + 1

    for y in range(0, 100):
        for x in range(0, 100):
            if ec.env[y][x] > 0:
                chart_1.create_oval((x * 6 + 3) - ec.env[y][x] / 2,
                                    (y * 6 + 3) - ec.env[y][x] / 2,
                                    (x * 6 + 3) + ec.env[y][x] / 2,
                                    (y * 6 + 3) + ec.env[y][x] / 2,
                                    fill='green')
            if an.env[y][x] > 0:

                chart_1.create_oval((x * 6 + 3) - an.env[y][x] / 2,
                                    (y * 6 + 3) - an.env[y][x] / 2,
                                    (x * 6 + 3) + an.env[y][x] / 2,
                                    (y * 6 + 3) + an.env[y][x] / 2,
                                    fill='blue')

    chart_1.create_line(0, 600, 600, 600, fill="white")

    chart_1.create_text(100, 650,
        text="steps = " + str(steps) + " step time = " + str(step_time),
        fill='white')

    if not pause:
        ec.next_gen(an.env)
        an.next_gen(ec.env)

    if reset:
        ec.reset()
        an.reset()
        reset = False
        started = False
        steps = 0

    chart_1.update()
    chart_1.after(step_time)

    chart_1.delete(ALL)
root.mainloop()
