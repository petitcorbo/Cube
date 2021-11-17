import tkinter as tk
import math, time

bg = 'black'
fg = 'white'
l = 500
o = l // 2
points = [[100, 100], [400, 100], [400, 400], [100, 400]]

def rotate(a):
    global points
    a = math.radians(a)
    c = math.cos(a)
    s = math.sin(a)
    p = []
    for x, y in points:
        x -= o
        y -= o
        x, y = (x * c - y * s), (x * s + y * c)
        p.extend((x + o, y + o))
    canvas.coords(carre, p)


def console():
    while True:
        try:
            exec(input("Command:"))
        except Exception as e:
            print(e)


def revolution(n=1):
    for a in range(360*n):
        time.sleep(5/360)
        rotate(a%360+1)
        canvas.update()


root = tk.Tk()
root.title("Cube")

canvas = tk.Canvas(bg=bg, width=500, height=500)
canvas.grid()

carre = canvas.create_polygon(points, outline=fg)

root.after(10, console)
root.mainloop()