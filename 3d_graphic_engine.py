import os

import tkinter as tk
from tkinter import filedialog

from math import radians, cos, sin, sqrt
from statistics import mean
import random


def settings():
    global color_canvas, color_bg, color_fg, color_buttons, color_faces, font
    color_canvas = '#131623'
    color_bg = '#060915'
    color_fg = 'lightgrey'
    color_buttons = '#222734'
    font = ('Helvetica', '10') 
    
    global canvas_size, coef, origin
    canvas_size = 500
    coef = 360 / canvas_size
    origin = canvas_size // 2
    
    global light_source
    light_source = (0, 0, -1)


class Object:

    def __init__(self, verticies, faces, scale=250):
        self.verticies = [list(sub) for sub in verticies]
        self.verticies_original = verticies
        self.faces = faces
        self.scale = scale
        self.color = (224, 17, 95)
        self.color = (0, 100, 255)
        self.color_faces = []
        
        for i, face in enumerate(self.faces):
            self.color_faces.append(random_color())
        self.update()


    def rotate(self, s=0, t=0):
        δ, θ = radians(s), radians(t)
        
        temp_verticies = []
        for x, y, z in self.verticies:
            x, y, z = rot_x(-θ, x, y, z)
            x, y, z = rot_y(-δ, x, y, z)
            temp_verticies.append([x, y, z])
        
        self.verticies = temp_verticies
        self.update()


    def update(self):
        canvas.delete('all')

        for i in sort_faces(self.faces, self.verticies):
            c = [x*self.scale//2 + origin for y in self.faces[i] for x in self.verticies[y][:2]]
            j1, j2, j3 = self.faces[i][:3]
            li = light_intensity(self.verticies[j1], self.verticies[j2], self.verticies[j3])
            if li < 0: li = 0
            color = '#%02x%02x%02x' % (int(self.color[0]*li), int(self.color[1]*li), int(self.color[2]*li))
            canvas.create_polygon(c, outline=color, fill=color)


    def reset(self):
        self.verticies = self.verticies_original
        self.scale = 250
        self.update()


    def scaling(self, evt):
        self.scale -= evt.delta // 30
        self.update()
    
    
    def move_x(self, x):
        for vertex in self.verticies:
            vertex[0] += int(x)//15
        self.update()
    
    
    def move_y(self, y):
        for vertex in self.verticies:
            vertex[1] += int(y)//15
        self.update()


def rot_x(θ, x, y, z):
    return x, y*cos(θ) - z*sin(θ), y*sin(θ) + z*cos(θ)


def rot_y(δ, x, y, z):
    return x*cos(δ) + z*sin(δ), y, -x*sin(δ) + z*cos(δ)


def sort_faces(faces, verticies):
    dic = {}
    for i, face in enumerate(faces):
        z_min = mean([verticies[j][2] for j in face])
        dic[i] = z_min
    res = [key for key, _ in sorted(dic.items(), key = lambda ele: ele[1], reverse=True)]
    return res


def light_intensity(p1, p2, p3):
    l1 = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    l2 = (p2[0] - p3[0], p2[1] - p3[1], p2[2] - p3[2])
    
    normal = [
        l1[1]*l2[2] - l1[2]*l2[1],
        l1[2]*l2[0] - l1[0]*l2[2],
        l1[0]*l2[1] - l1[1]*l2[0]
        ]
    normal = normalise(normal)
    
    # light_source = normalise(light_source)
    
    return normal[0]*light_source[0] + normal[1]*light_source[1] + normal[2]*light_source[2] # DotProduct


def normalise(vector):
    l = sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
    if l == 0: return vector
    for i in range(len(vector)): vector[i] /= l
    return vector


def random_color():
    color = '#'
    for _ in range(6): color += random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'], 1)[0]
    return color


def press(evt):
    global x, y
    x, y = evt.x, evt.y


def drag(evt):
    global x, y
    if x != evt.x: delta_x = evt.x - x
    else: delta_x = 0
    if y != evt.y: delta_y = y - evt.y
    else: delta_y = 0
    x, y = evt.x, evt.y
    obj_selected.rotate(delta_x*coef, delta_y*coef)


def select_object(obj):
    global obj_selected
    obj_selected = obj
    menu_buttons[1]['command'] = obj.reset
    canvas.bind('<MouseWheel>', obj.scaling)
    


def load_file(path=None):
    if path: file = open(path)
    else: file = filedialog.askopenfile(title="Select save file", filetypes=(("Save files", '*.obj'), ("all files", '*.*')))
    if file is None: return
    
    verticies, faces = [], []
    for line in file.readlines():
        if line[0] == 'v':
            line = line.split(' ')
            verticies.append([float(v) for v in line[1::]])
        elif line[0] == 'f':
            line = line.split(' ')
            faces.append([int(i)-1 for i in line[1::]])
        elif line[0] == 'o':
            name = line[2::]
    select_object(Object(verticies, faces))
    
    file.close()


def gui():
    global root, canvas
    root = tk.Tk()
    root.title("Cube")
    root.configure(bg=color_bg)
    root.resizable(False, False)

    canvas = tk.Canvas(bg=color_canvas, width=canvas_size, height=canvas_size, highlightthickness=0)
    canvas.bind('<Button-2>', select_object)
    canvas.bind('<Button-1>', press)
    canvas.bind('<B1-Motion>', drag)
    canvas.grid(row=0, columnspan=3)


def menu_bar():
    global menu_buttons
    menu_buttons = []
    w = canvas_size // 25
    
    menu = tk.Frame(root, bg=color_bg, bd=1)
    
    b = tk.Button(menu, text="Import", font=font, relief='flat', width=w, command=load_file,
        bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
        )
    menu_buttons.append(b)
    b.grid(row=0, column=0, padx=1)
    
    b = tk.Button(menu, text="Reset", font=font, relief='flat', width=w,
        bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
        )
    menu_buttons.append(b)
    b.grid(row=0, column=1, padx=1)
    
    b = tk.Button(menu, text="Exit", font=font, relief='flat', width=w, command=exit,
        bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
        )
    menu_buttons.append(b)
    b.grid(row=0, column=2, padx=1)
    
    menu.grid(row=1, column=0, sticky='we')


def console():
    while True:
        try: exec(input("~"))
        except Exception as e: print(e)


def main():
    settings()
    
    gui()
    menu_bar()
    
    load_file('objects\icosphere.obj')
    
    # root.after(10, console)
    root.mainloop()


if __name__ == '__main__': main()
