import tkinter as tk
import math, time

bg = 'black'
fg = 'white'
l = 500
o = l // 2
p1, p2 = [100, 100], [400, 100]
p3, p4 = [400, 400], [100, 400]
p5, p6 = [100, 100], [400, 100]
p7, p8 = [400, 400], [100, 400]
points = [p1, p2, p3, p4, p5, p6, p7, p8]
zp = [150, 150, 150, 150, -150, -150, -150, -150]
color = ('blue', 'red', 'green', 'yellow', 'cyan', 'magenta')
faces = []
cube = [
    [points[0], points[1], points[2], points[3]],
    [points[0], points[4], points[5], points[1]],
    [points[1], points[5], points[6], points[2]],
    [points[2], points[6], points[7], points[3]],
    [points[3], points[7], points[4], points[0]],
    [points[4], points[5], points[6], points[7]],
    ]


def xrotate(a=45):
    a = math.radians(a)
    cosa = math.cos(a)
    sina = math.sin(a)
    p = []
    for j in range(8):
        x = points[j][0] - o
        y = points[j][1] - o
        z = zp[j]
        y = sina * z + cosa * y
        p.append([x+o, y+o])
    c = [
        [p[0], p[1], p[2], p[3]],
        [p[0], p[4], p[5], p[1]],
        [p[1], p[5], p[6], p[2]],
        [p[2], p[6], p[7], p[3]],
        [p[3], p[7], p[4], p[0]],
        [p[4], p[5], p[6], p[7]],
        ]
    d = [[], [], [], [], [], []]
    for n in range(6):
        for sub in c[n]:
            d[n].extend(sub)
    print(d)
    for i in range(6):
        canvas.coords(i+1, d[i])


def yrotate(a=45):
    pass

def zrotate(a=45):
    pass


def console():
    while True:
        try:
            exec(input("Command:"))
        except Exception as e:
            print(e)


def revolution(n=1):
    for a in range(360*n):
        time.sleep(5/360)
        xrotate(a%360+1)
        canvas.update()


root = tk.Tk()
root.title("Cube")

canvas = tk.Canvas(bg=bg, width=500, height=500)
canvas.grid()

for i in range(6):
    face = canvas.create_polygon(cube[i], outline=fg, fill=color[i])
    faces.append(face)

root.after(10, console)
root.mainloop()