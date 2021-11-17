import tkinter as tk
import math


def settings():
    global color_canvas, color_bg, color_fg, color_buttons, color_faces
    color_canvas = '#131623'
    color_bg = '#060915'
    color_fg = 'lightgrey'
    color_buttons = '#222734'
    color_faces = ('yellow', 'orange', 'blue', 'red', 'green', 'white')
    global canvas_size, coef, origin
    canvas_size = 500
    coef = 360 / canvas_size
    origin = canvas_size // 2


class Shape:

    def __init__(self, shape='cube', edge_size=250):
        if shape == 'cube':
            self.scheme = (
                ((0, 1, 2, 3), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0), (4, 5, 6, 7)),
                ((2, 4), (1, 3), (0, 5)),
                ((0, 3, 4), (0, 3, 2), (0, 2, 1), (0, 1, 4), (3, 4, 5), (3, 2, 5), (2, 1, 5), (1, 4, 5))
            )
        if shape == 'prism':
            self.scheme = (
                ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)),
                ((2, 4), (1, 3), (0, 5)),
                ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
            )
        self.shape = shape
        self.edge_size = edge_size
        self.sigma = 0
        self.theta = 0
        self.verticies = get_verticies(self.shape, edge_size)
        for sub, color in zip(self.scheme[0], color_faces):
            canvas.create_polygon([self.verticies[i][:2] for i in sub], outline='black', fill=color, tags=color)


    def rotate(self, s=0, t=0):
        self.sigma += s
        self.theta += t
        δ, θ = math.radians(self.sigma), math.radians(self.theta)
        
        temp_verticies = []
        for x_0, y_0, z_0 in self.verticies:
            x_0 -= origin
            y_0 -= origin
            x = x_0 * math.cos(δ) - z_0 * math.sin(δ)
            y = math.cos(θ) * y_0 + math.sin(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
            z = math.sin(θ) * y_0 + math.cos(θ) * (math.cos(δ) * z_0 + math.sin(δ) * x_0)
            temp_verticies.append([x+origin, y+origin, z])
        
        self.check(temp_verticies)
        self.update(temp_verticies)


    def reset(self):
        self.sigma = 0
        self.theta = 0
        self.rotate()


    def check(self, verticies):
        temp_list = [sub[2] for sub in verticies]
        i = temp_list.index(min(temp_list))
        for n in self.scheme[2][i]: canvas.tag_raise(color_faces[n])


    def update(self, verticies):
        for i, sub in enumerate(self.scheme[0]):
            face = [x for y in sub for x in verticies[y][:2]]
            canvas.coords(i+1, face)


    def scale(self, edge_size):
        self.verticies = get_verticies(self.shape, self.edge_size)
        self.rotate()


    def rotation_δ(self, δ):
        self.sigma = int(δ)
        self.rotate()



    def rotation_θ(self, θ):
        self.theta = int(θ)
        self.rotate()


def get_verticies(edge_size):
    xy1 = (canvas_size - int(edge_size)) // 2
    xy2 = (canvas_size + int(edge_size)) // 2
    z1 = xy2 - origin
    z2 = xy1 - origin
    verticies = [
        [xy1, xy1, z1],
        [xy2, xy1, z1],
        [xy2, xy2, z1],
        [xy1, xy2, z1],
        [xy1, xy1, z2],
        [xy2, xy1, z2],
        [xy2, xy2, z2],
        [xy1, xy2, z2]
        ]
    return verticies


def get_verticies(shape, edge_size):
    xy1 = (canvas_size - int(edge_size)) // 2
    xy2 = (canvas_size + int(edge_size)) // 2
    z1 = xy2 - origin
    z2 = xy1 - origin
    if shape == 'cube':
        verticies = [
            [xy1, xy1, z1],
            [xy2, xy1, z1],
            [xy2, xy2, z1],
            [xy1, xy2, z1],
            [xy1, xy1, z2],
            [xy2, xy1, z2],
            [xy2, xy2, z2],
            [xy1, xy2, z2]
            ]
    if shape == 'prism':
            verticies = [
                [xy1, xy1, z1],
                [xy2, xy1, z1],
                [xy1, xy2, z1],
                [xy1, xy1, z2]
                ]
    return verticies


def get_center(verticies):
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for x, y, z in verticies:
        sum_x += x
        sum_y += y
        sum_z += z
    n = len(verticies)
    return [sum_x/n, sum_y/n, sum_z/n]


def create_cube():
    return scheme


def create_cube():
    return scheme


def create_cube():
    return scheme


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
    cube.rotate(delta_x*coef, delta_y*coef)


def gui():
    # Zoom #
    s_cube = tk.Scale(
        label="Cube Size", from_=0, to=500, resolution=5, length=400, command=cube.scale,
        orient='horizontal', bd=1, sliderrelief='flat', tickinterval=250,
        bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
        )
    s_cube.set(250)
    s_cube.grid(row=1, column=0, columnspan=2)

    # Rotation #
    button_reset = tk.Button(text="Reset Rotation", command=cube.reset,
        bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
        )
    button_reset.grid(row=1, column=2)

    button_cmd = tk.Button(text="Console", command=console,
        bg=color_buttons, fg=color_fg, activebackground=color_canvas, activeforeground=color_fg
        )
    button_cmd.grid(row=2, column=2)

    scale_δ = tk.Scale(
        label="δ", from_=-360, to=360, resolution=15, length=200, command=cube.rotation_δ,
        orient='horizontal', bd=1, sliderrelief='flat', tickinterval=120,
        bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
        )
    scale_δ.grid(row=2, column=0)

    scale_θ = tk.Scale(
        label="θ", from_=-360, to=360, resolution=15, length=200, command=cube.rotation_θ,
        orient='horizontal', bd=1, sliderrelief='flat', tickinterval=120,
        bg=color_bg, fg=color_fg, troughcolor=color_buttons, highlightthickness=0
        )
    scale_θ.grid(row=2, column=1)


def console():
    while True:
        try: exec(input("~"))
        except Exception as e: print(e)


def main():
    global cube
    settings()
    global root, canvas
    root = tk.Tk()
    root.title("Cube")
    root.configure(bg=color_bg)
    root.resizable(False, False)

    canvas = tk.Canvas(bg=color_canvas, width=canvas_size, height=canvas_size, highlightthickness=0)
    canvas.bind('<Button-1>', press)
    canvas.bind('<B1-Motion>', drag)
    canvas.grid(row=0, columnspan=3)
    
    cube = Shape("cube")
    gui()
    
    # root.after(10, console)
    root.mainloop()


if __name__ == '__main__': main()

"""
If you want to rotate a vector you should construct what is known as a rotation matrix.
Rotation in 2D

Say you want to rotate a vector or a point by θ, then trigonometry states that the new
coordinates are

    x' = x cos θ − y sin θ
    y' = x sin θ + y cos θ

To demo this, let's take the cardinal axes X and Y; when we rotate the X-axis 90°
counter-clockwise, we should end up with the X-axis transformed into Y-axis. Consider

    Unit vector along X axis = <1, 0>
    x' = 1 cos 90 − 0 sin 90 = 0
    y' = 1 sin 90 + 0 cos 90 = 1
    New coordinates of the vector, <x', y'> = <0, 1>  ⟹  Y-axis

When you understand this, creating a matrix to do this becomes simple. A matrix is just
a athematical tool to perform this in a comfortable, generalized manner so that various
transformations like rotation, scale and translation (moving) can be combined and performed
in a single step, using one common method. From linear algebra, to rotate a point or vector
in 2D, the matrix to be built is

    |cos θ   −sin θ| |x| = |x cos θ − y sin θ| = |x'|
    |sin θ    cos θ| |y|   |x sin θ + y cos θ|   |y'|

Rotation in 3D

That works in 2D, while in 3D we need to take in to account the third axis. Rotating a vector
round the origin (a point) in 2D simply means rotating it around the Z-axis (a line) in 3D;
ince we're rotating around Z-axis, its coordinate should be kept constant i.e. 0° (rotation
happens on the XY plane in 3D). In 3D rotating around the Z-axis would be

    |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
    |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    |  0       0      1| |z|   |        z        |   |z'|

around the Y-axis would be

    | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
    |   0      1       0| |y| = |         y        | = |y'|
    |−sin θ    0   cos θ| |z|   |−x sin θ + z cos θ|   |z'|

around the X-axis would be

    |1     0           0| |x|   |        x        |   |x'|
    |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|
    |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|

Note 1: axis around which rotation is done has no sine or cosine elements in the matrix.

Note 2: This method of performing rotations follows the Euler angle rotation system, which
is simple to teach and easy to grasp. This works perfectly fine for 2D and for simple 3D cases;
but when rotation needs to be performed around all three axes at the same time then Euler angles
may not be sufficient due to an inherent deficiency in this system which manifests itself
as Gimbal lock. People resort to Quaternions in such situations, which is more advanced
than this but doesn't suffer from Gimbal locks when used correctly.

I hope this clarifies basic rotation.
Rotation not Revolution

The aforementioned matrices rotate an object at a distance r = √(x² + y²) from the origin
along a circle of radius r; lookup polar coordinates to know why. This rotation will be
with respect to the world space origin a.k.a revolution. Usually we need to rotate an object
around its own frame/pivot and not around the world's i.e. local origin. This can also be seen
as a special case where r = 0. Since not all objects are at the world origin, simply rotating
using these matrices will not give the desired result of rotating around the object's own frame.
You'd first translate (move) the object to world origin (so that the object's origin would
align with the world's, thereby making r = 0), perform the rotation with one (or more)
of these matrices and then translate it back again to its previous location. The order
in which the transforms are applied matters. Combining multiple transforms together is called
oncatenation or composition.
Composition

I urge you to read about linear and affine transformations and their composition to perform
multiple transformations in one shot, before playing with transformations in code. Without
understanding the basic maths behind it, debugging transformations would be a nightmare.
I found this lecture video to be a very good resource. Another resource is this tutorial
on transformations that aims to be intuitive and illustrates the ideas with animation
(caveat: authored by me!).
Rotation around Arbitrary Vector

A product of the aforementioned matrices should be enough if you only need rotations
around cardinal axes (X, Y or Z) like in the question posted. However, in many situations
you might want to rotate around an arbitrary axis/vector. The Rodrigues' formula
(a.k.a. axis-angle formula) is a commonly prescribed solution to this problem. However,
resort to it only if you’re stuck with just vectors and matrices. If you're using Quaternions,
just build a quaternion with the required vector and angle. Quaternions are a superior
alternative for storing and manipulating 3D rotations; it's compact and fast e.g.
concatenating two rotations in axis-angle representation is fairly expensive, moderate
with matrices but cheap in quaternions. Usually all rotation manipulations are done with
quaternions and as the last step converted to matrices when uploading to the rendering pipeline.
See Understanding Quaternions for a decent primer on quaternions.
"""
