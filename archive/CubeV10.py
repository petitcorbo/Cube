import tkinter as tk
import math, time

color_canvas = '#131623'
color_bg = '#060915'
color_fg = 'lightgrey'
color_buttons = '#222734'
color_faces = ('yellow', 'orange', 'blue', 'red', 'green', 'white')
canvas_size = 500
origin = canvas_size // 2
sigma, theta = 0, 0
faces = []


def reset():
    global sigma, theta
    sigma, theta = 0, 0
    rotate()


def create_cube(side=250):
    global points, scheme
    scheme = (((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 5, 6, 7)),
        ((2, 4), (1, 3), (0, 5)),
        ((0, 3, 4), (0, 3, 2), (0, 2, 1), (0, 1, 4), (3, 4, 5), (3, 2, 5), (2, 1, 5), (1, 4, 5)))
    xy1 = (canvas_size - side) // 2
    xy2 = (canvas_size + side) // 2
    z1 = xy2 - origin
    z2 = xy1 - origin
    points = get_points(xy1, xy2, z1, z2)
    cube = [[points[i][:2] for i in j] for j in scheme[0]]
    for face, color in zip(cube, color_faces):
        face = canvas.create_polygon(face, outline='black', fill=color, tags=color)
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
    check(temp_points)
    update_cube(temp_points)


def check(points):
    temp_list = [sub[2] for sub in points]
    i = temp_list.index(min(temp_list))
    for n in scheme[2][i]: canvas.tag_raise(color_faces[n])


def update_cube(points):
    for i, sub in enumerate(scheme[0]):
        face = [x for y in sub for x in points[y][:2]]
        canvas.coords(i+1, face)


def scale_cube(side):
    global points
    xy1 = (canvas_size - int(side)) // 2
    xy2 = (canvas_size + int(side)) // 2
    z1 = xy2 - origin
    z2 = xy1 - origin
    points = get_points(xy1, xy2, z1, z2)
    rotate()


def revolution(n=1):
    for a in range(360*n):
        time.sleep(5/360)
        rotate(a%360+1, a%360+1)
        canvas.update()


def rotation_δ(δ):
    global sigma
    sigma = int(δ)
    rotate()



def rotation_θ(θ):
    global theta
    theta = int(θ)
    rotate()


def console():
    while True:
        try: exec(input("Command:"))
        except Exception as e: print(e)


coef = 360 / canvas_size


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
    rotate(delta_x*coef, delta_y*coef)

# GUI #
root = tk.Tk()
root.title("Cube")
root.configure(bg=color_bg)
root.resizable(False, False)

# Canvas #
canvas = tk.Canvas(bg=color_canvas, width=canvas_size, height=canvas_size, highlightthickness=0)
canvas.bind('<Button-1>', press)
canvas.bind('<B1-Motion>', drag)
canvas.grid(row=0, columnspan=3)

# Cube #
create_cube()

scale_cube = tk.Scale(
    label="Cube Size", from_=0, to=500, resolution=5, length=400, command=scale_cube,
    orient='horizontal', bd=1, sliderrelief='flat', tickinterval=250,
    bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
    )
scale_cube.set(250)
scale_cube.grid(row=1, column=0, columnspan=2)

# Rotation #
button_reset = tk.Button(text="Reset Rotation", command=reset,
    bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
    )
button_reset.grid(row=1, column=2)

button_rotation = tk.Button(text="Revolution", command=revolution,
    bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
    )
button_rotation.grid(row=2, column=2)

scale_δ = tk.Scale(
    label="δ", from_=-360, to=360, resolution=15, length=200, command=rotation_δ,
    orient='horizontal', bd=1, sliderrelief='flat', tickinterval=120,
    bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
    )
scale_δ.grid(row=2, column=0)

scale_θ = tk.Scale(
    label="θ", from_=-360, to=360, resolution=15, length=200, command=rotation_θ,
    orient='horizontal', bd=1, sliderrelief='flat', tickinterval=120,
    bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
    )
scale_θ.grid(row=2, column=1)

# root.after(10, console)
root.mainloop()