import math
import tkinter as tk
from tkinter import ttk
import time

PIXEL_SIZE = 8
class SecondOrderAlgorithms:
    @staticmethod
    def draw_circle(xc, yc, R, debug=False, draw_callback=None):
        x, y = 0, R
        d = 2 - 2 * R
        def plot_points(x, y):
            pts = [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]
            for px, py in pts:
                draw_callback(px, py, "black")
                if debug:
                    tk._default_root.update(); time.sleep(0.03)

        while y >= x:
            plot_points(x, y)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    @staticmethod
    def draw_ellipse(xc, yc, a, b, debug=False, draw_callback=None):
        x, y = 0, b
        a2, b2 = a*a, b*b
        d = b2 + a2 * (b - 0.5)**2 - a2 * b2

        def plot_points(x, y):
            pts = [(xc + x, yc + y), (xc - x, yc + y),
                   (xc + x, yc - y), (xc - x, yc - y)]
            for px, py in pts:
                draw_callback(px, py, "blue")
                if debug:
                    tk._default_root.update(); time.sleep(0.03)

        while b2 * x < a2 * y:
            plot_points(x, y)
            if d < 0:
                d += b2 * (2 * x + 3)
            else:
                d += b2 * (2 * x + 3) + a2 * (-2 * y + 2)
                y -= 1
            x += 1
        d = b2 * (x + 0.5)**2 + a2 * (y - 1)**2 - a2 * b2
        while y >= 0:
            plot_points(x, y)
            if d > 0:
                d += a2 * (-2 * y + 3)
            else:
                d += b2 * (2 * x + 2) + a2 * (-2 * y + 3)
                x += 1
            y -= 1

    @staticmethod
    def draw_parabola(xc, yc, p, direction="Вправо", debug=False, draw_callback=None):
        max_val = 100
        if direction in ("Вправо", "Влево"):
            x = 0
            while x <= max_val:
                y = int(round(math.sqrt(2 * p * x))) if x else 0
                if direction == "Вправо":
                    pts = [(xc + x, yc + y), (xc + x, yc - y)]
                else:
                    pts = [(xc - x, yc + y), (xc - x, yc - y)]
                for px, py in pts:
                    draw_callback(px, py, "green")
                    if debug:
                        tk._default_root.update(); time.sleep(0.03)
                x += 1
        else:
            y = 0
            while y <= max_val:
                x = int(round(math.sqrt(2 * p * y))) if y else 0
                if direction == "Вверх":
                    pts = [(xc + x, yc - y), (xc - x, yc - y)]
                else:
                    pts = [(xc + x, yc + y), (xc - x, yc + y)]
                for px, py in pts:
                    draw_callback(px, py, "green")
                    if debug:
                        tk._default_root.update(); time.sleep(0.03)
                y += 1


    @staticmethod
    def draw_hyperbola(xc, yc, a, b, debug=False, draw_callback=None):
        x = a
        max_x = a + 100
        while x <= max_x:
            try:
                y_val = int(round(b * math.sqrt(x*x / (a*a) - 1)))
            except ValueError:
                x += 1; continue
            for px, py in (
                (xc + x, yc + y_val), (xc + x, yc - y_val),
                (xc - x, yc + y_val), (xc - x, yc - y_val)
            ):
                draw_callback(px, py, "purple")
                if debug:
                    tk._default_root.update(); time.sleep(0.03)
            x += 1


class SecondOrderGraphicalEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор: линии второго порядка")
        self.geometry("900x700")
        self.mode = tk.StringVar(value="Окружность")
        self.dir_var = tk.StringVar(value="Вправо")
        self.start_point = None
        self.debug_mode = False
        self._build_ui()


    def _build_ui(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        tk.Label(toolbar, text="Фигура:").pack(side=tk.LEFT, padx=5)
        curve_box = ttk.Combobox(toolbar, textvariable=self.mode,
                                 state="readonly", width=12,
                                 values=("Окружность", "Эллипс", "Парабола", "Гипербола"))
        curve_box.pack(side=tk.LEFT, padx=5)
        self.r_var = tk.IntVar(value=20)
        self.a_var = tk.IntVar(value=20)
        self.b_var = tk.IntVar(value=10)
        self.p_var = tk.IntVar(value=10)

        for lab, var in (("R:", self.r_var), ("a:", self.a_var),
                         ("b:", self.b_var), ("p:", self.p_var)):
            tk.Label(toolbar, text=lab).pack(side=tk.LEFT)
            tk.Entry(toolbar, textvariable=var, width=4).pack(side=tk.LEFT, padx=2)


        tk.Label(toolbar, text="Напр. параболы:").pack(side=tk.LEFT, padx=(10,2))
        dir_box = ttk.Combobox(toolbar, textvariable=self.dir_var,
                               state="readonly", width=7,
                               values=("Вправо", "Влево", "Вверх", "Вниз"))
        dir_box.pack(side=tk.LEFT, padx=2)


        tk.Button(toolbar, text="Построить", command=self.draw).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
        self.btn_debug = tk.Button(toolbar, text="Отладка: OFF", command=self.toggle_debug)
        self.btn_debug.pack(side=tk.LEFT, padx=5)

        toolbar.pack(side=tk.TOP, fill=tk.X)


        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_click)
        self._draw_grid()


    def _on_click(self, event):
        self.start_point = (event.x // PIXEL_SIZE, event.y // PIXEL_SIZE)
        self.plot_block(*self.start_point, color="red")

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        self.btn_debug.config(text=f"Отладка: {'ON' if self.debug_mode else 'OFF'}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self._draw_grid()


    def draw(self):
        if self.start_point is None:
            print("Сначала укажите центр фигуры кликом по холсту.")
            return
        x0, y0 = self.start_point
        mode = self.mode.get()
        if mode == "Окружность":
            SecondOrderAlgorithms.draw_circle(x0, y0, self.r_var.get(),
                                              debug=self.debug_mode,
                                              draw_callback=self.plot_block)
        elif mode == "Эллипс":
            SecondOrderAlgorithms.draw_ellipse(x0, y0, self.a_var.get(), self.b_var.get(),
                                               debug=self.debug_mode,
                                               draw_callback=self.plot_block)
        elif mode == "Парабола":
            SecondOrderAlgorithms.draw_parabola(x0, y0, self.p_var.get(),
                                                direction=self.dir_var.get(),
                                                debug=self.debug_mode,
                                                draw_callback=self.plot_block)
        elif mode == "Гипербола":
            SecondOrderAlgorithms.draw_hyperbola(x0, y0, self.a_var.get(), self.b_var.get(),
                                                 debug=self.debug_mode,
                                                 draw_callback=self.plot_block)

    def plot_block(self, x, y, color):
        X, Y = x * PIXEL_SIZE, y * PIXEL_SIZE
        self.canvas.create_rectangle(X, Y, X + PIXEL_SIZE, Y + PIXEL_SIZE,
                                     fill=color, outline="black")

    def _draw_grid(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for i in range(0, w, PIXEL_SIZE):
            self.canvas.create_line(i, 0, i, h, fill="#ddd", tags="grid")
        for j in range(0, h, PIXEL_SIZE):
            self.canvas.create_line(0, j, w, j, fill="#ddd", tags="grid")
        self.after(500, self._draw_grid)


if __name__ == "__main__":
    app = SecondOrderGraphicalEditor()
    app.mainloop()
