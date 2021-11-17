import tkinter as tk
import math, time

bg = '#131623'
fg = 'black'
color = ('yellow', 'orange', 'blue', 'red', 'green', 'white')
l = 500
o = l // 2
p1, p2 = [100, 100], [400, 100]
p3, p4 = [400, 400], [100, 400]
p5, p6 = [100, 100], [400, 100]
p7, p8 = [400, 400], [100, 400]
points = [p1, p2, p3, p4, p5, p6, p7, p8]
zpoints = [150, 150, 150, 150, -150, -150, -150, -150]
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
        x = x_0 * math.cos(δ) - z_0 * math.sin(δ)
        y = math.cos(θ) * y_0 + math.sin(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
        z = math.sin(θ) * y_0 + math.cos(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
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


def rotation(δ, θ):
    if δ > θ:
        for a in range(δ):
            time.sleep(1/72)
            b = (θ / δ) * (a + 1)
            rotate(a+1, b)
            canvas.update()
    else:
        for a in range(θ):
            time.sleep(1/72)
            b = (δ / θ) * (a + 1)
            rotate(b, a+1)
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
root.resizable(False, False)

canvas = tk.Canvas(bg=bg, width=500, height=500)
canvas.grid()

for i in range(6):
    face = canvas.create_polygon(cube[i], outline=fg, fill=color[i], tags=color[i])
    faces.append(face)

top = tk.Toplevel()
top.resizable(False, False)
top.attributes('-topmost', 'true')

button1 = tk.Button(top, text="Revolution", command=lambda: revolution(int(spinbox.get())))
button1.grid(row=0, column=1)
spinbox = tk.Spinbox(top, from_=1, to=10)
spinbox.grid(row=0, column=0)

button2 = tk.Button(top, text="Rotation", command=lambda: rotation(scale1.get(), scale2.get()))
button2.grid(row=1, column=1, rowspan=2)
scale1 = tk.Scale(top, label="δ", from_=0, to=360, resolution=15, orient='horizontal')
scale1.grid(row=1, column=0)
scale2 = tk.Scale(top, label="θ", from_=0, to=360, resolution=15, orient='horizontal')
scale2.grid(row=2, column=0)

#root.after(10, console)
root.mainloop()

def check(points, scheme):
    for i, j in scheme[1]:  
        sum_i, sum_j = 0, 0
        for n in scheme[0][i]: sum_i += points[n][2]
        for n in scheme[0][j]: sum_j += points[n][2]
        if sum_i > sum_j: canvas.tag_raise(color[i])
        else: canvas.tag_raise(color[j])