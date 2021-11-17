import tkinter as tk
import math, time

bg = '#292c33'
fg = 'black'
l = 500
o = l // 2
p1, p2 = [100, 100], [400, 100]
p3, p4 = [400, 400], [100, 400]
p5, p6 = [100, 100], [400, 100]
p7, p8 = [400, 400], [100, 400]
points = [p1, p2, p3, p4, p5, p6, p7, p8]
zpoints = [150, 150, 150, 150, -150, -150, -150, -150]
color = ('yellow', 'orange', 'green', 'red', 'blue', 'white')
faces = []
cube = [
    [points[0], points[1], points[2], points[3]],
    [points[0], points[4], points[5], points[1]],
    [points[1], points[5], points[6], points[2]],
    [points[2], points[6], points[7], points[3]],
    [points[3], points[7], points[4], points[0]],
    [points[4], points[5], points[6], points[7]],
    ]


def rotate(δ=0, θ=0):
    δ, θ = math.radians(δ), math.radians(θ)
    p, zp = [], []
    for j in range(8):
        x_0 = points[j][0] - o
        y_0 = points[j][1] - o
        z_0 = zpoints[j]
        x = math.sin(δ) * y_0 + math.cos(δ) * x_0
        y = math.sin(θ) * z_0 + math.cos(θ) * (math.cos(δ) * y_0 - math.sin(δ) * x_0)
        z = math.cos(θ) * z_0 + math.sin(θ) * (math.cos(δ) * y_0 - math.sin(δ) * x_0)
        p.append([x+o, y+o])
        zp.append(z)
    check(zp)
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
    for i in range(6):
        canvas.coords(i+1, d[i])


def console():
    while True:
        try:
            exec(input("Command:"))
        except Exception as e:
            print(e)


def revolution(n=1):
    for a in range(360*n):
        time.sleep(5/360)
        rotate(a%360+1, a%360+1)
        canvas.update()


def check(zp):
    if zp[1] + zp[5] + zp[6] + zp[2] > zp[3] + zp[7] + zp[4] + zp[0]:
        canvas.tag_raise('green')
    else: canvas.tag_raise('blue')
    if zp[0] + zp[4] + zp[5] + zp[1] > zp[2] + zp[6] + zp[7] + zp[3]:
        canvas.tag_raise('orange')
    else: canvas.tag_raise('red')
    if zp[0] + zp[1] + zp[2] + zp[3] > zp[4] + zp[5] + zp[6] + zp[7]:
        canvas.tag_raise('white')
    else: canvas.tag_raise('yellow')


root = tk.Tk()
root.title("Cube")

canvas = tk.Canvas(bg=bg, width=500, height=500)
canvas.grid()

for i in range(6):
    face = canvas.create_polygon(cube[i], outline=fg, fill=color[i], tags=color[i])
    faces.append(face)

root.after(10, console)
root.mainloop()