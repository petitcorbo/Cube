import tkinter as tk
import math, time

bg = '#131623'
fg = 'black'
color = ('yellow', 'orange', 'blue', 'red', 'green', 'white')
canvas_side = 500
origin = canvas_side // 2
sigma, theta = 0, 0
faces = []


def create_cube(side=300):
    global points, scheme
    scheme = (((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 5, 6, 7)),
        ((2, 4), (1, 3), (0, 5)),
        ((0, 3, 4), (0, 3, 2), (0, 2, 1), (0, 1, 4), (3, 4, 5), (3, 2, 5), (2, 1, 5), (1, 4, 5)))
    xy1 = (canvas_side - side) // 2
    xy2 = (canvas_side + side) // 2
    z1 = xy2 - origin
    z2 = xy1 - origin
    points = get_points(xy1, xy2, z1, z2)
    cube = [[points[i][:2] for i in j] for j in scheme[0]]
    for i in range(6):
        face = canvas.create_polygon(cube[i], outline=fg, fill=color[i], tags=color[i])
        faces.append(face)


def get_points(xy1, xy2, z1, z2):
        points = [
        [xy1, xy1, z1],
        [xy2, xy1, z1],
        [xy2, xy2, z1],
        [xy1, xy2, z1],
        [xy1, xy1, z2],
        [xy2, xy1, z2],
        [xy2, xy2, z2],
        [xy1, xy2, z2]
        ]
        return points


def rotate(a=0, b=0):
    global sigma, theta
    sigma += a
    theta += b
    δ, θ = math.radians(sigma), math.radians(theta)
    temp_points = []
    for x_0, y_0, z_0 in points:
        x_0 -= origin
        y_0 -= origin
        x = x_0 * math.cos(δ) - z_0 * math.sin(δ)
        y = math.cos(θ) * y_0 + math.sin(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
        z = math.sin(θ) * y_0 + math.cos(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
        temp_points.append([x+origin, y+origin, z])
    check(temp_points, scheme)
    update_cube(temp_points, scheme)


def check(points, scheme):
    temp_list = [sub[2] for sub in points]
    i = temp_list.index(min(temp_list))
    for n in scheme[2][i]: canvas.tag_raise(color[n])


def update_cube(points, scheme):
    global cube
    cube = []
    for sub in scheme[0]:
        temp = [y for x in sub for y in points[x][:2]]
        cube.append(temp)
    for i in range(6):
        canvas.coords(i+1, cube[i])


def revolution(n=1):
    for a in range(360*n):
        time.sleep(5/360)
        rotate(a%360+1, a%360+1)
        canvas.update()


def rotation(δ, θ):
    if δ > θ:
        for a in range(δ):
            time.sleep(1/72)
            rotate(1, (θ / δ))
            canvas.update()
    else:
        for a in range(θ):
            time.sleep(1/72)
            rotate((δ / θ), 1)
            canvas.update()


def console():
    while True:
        try: exec(input("Command:"))
        except Exception as e: print(e)


root = tk.Tk()
root.title("Cube")
root.resizable(False, False)

canvas = tk.Canvas(bg=bg, width=canvas_side, height=canvas_side)
canvas.grid()

create_cube()

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

# root.after(10, console)
root.mainloop()