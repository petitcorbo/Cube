import tkinter as tk

bg = '#131623'
fg = 'black'
canvas_side = 500
origin = canvas_side // 2
delta_x = 0
delta_y = 0


def on_press(evt):
    global x1, y1, delta_x, delta_y
    x1 = evt.x
    y1 = evt.y


def on_touch_scroll(evt):
    global x1, y1, delta_x, delta_y
    x2 = evt.x
    y2 = evt.y
    if x1 < x2: delta_x += x2 - x1
    elif x1 > x2: delta_x -= x1 - x2
    if y1 < y2: delta_y += y2 - y1
    elif y1 > y2: delta_y -= y1 - y2
    x1 = x2
    y1 = y2
    canvas.coords(item, origin+delta_x, origin+delta_y, origin+delta_x+1, origin+delta_y+1)


root = tk.Tk()
root.title("Cube")
root.resizable(False, False)

canvas = tk.Canvas(bg=bg, width=canvas_side, height=canvas_side)
canvas.grid()

item = canvas.create_line(origin, origin, origin+1, origin+1, fill='white')

canvas.bind('<Enter>', lambda _: canvas.bind_all('<Button-1>', on_press), '+')
canvas.bind('<Leave>', lambda _: canvas.unbind_all('<Button-1>'), '+')
canvas.bind('<Enter>', lambda _: canvas.bind_all('<B1-Motion>', on_touch_scroll), '+')
canvas.bind('<Leave>', lambda _: canvas.unbind_all('<B1-Motion>'), '+')

root.mainloop()