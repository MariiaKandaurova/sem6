import tkinter as tk
from algorithms import Algorithms, PIXEL_SIZE


class GraphicalEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор")
        self.geometry("900x700")
        self.mode = tk.StringVar(value="ЦДА")
        self.start_point = None
        self.scale = 1.0
        self.debug_mode = False
        self.current_pts = []
        self.current_index = 0
        self.create_widgets()

    def create_widgets(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        for m in ["ЦДА", "Брезенхем", "Ву"]:
            b = tk.Radiobutton(toolbar, text=m, variable=self.mode, value=m,
                               indicatoron=0, width=12)
            b.pack(side=tk.LEFT, padx=2, pady=2)
        btn_clear = tk.Button(toolbar, text="Очистить холст", command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=2, pady=2)
        self.btn_debug = tk.Button(toolbar, text="Отладка: OFF", command=self.toggle_debug)
        self.btn_debug.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-3>", self.pan_start)
        self.canvas.bind("<B3-Motion>", self.pan_move)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_grid()

    def toggle_debug(self):
        self.debug_mode = not self.debug_mode
        state = "ON" if self.debug_mode else "OFF"
        self.btn_debug.config(text=f"Отладка: {state}")

    def pan_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.start_point = None

    def on_canvas_click(self, event):
        if self.start_point is None:
            self.start_point = (event.x, event.y)
            self.draw_pixel(event.x, event.y, "red")
        else:
            end_point = (event.x, event.y)
            self.draw_pixel(event.x, event.y, "red")
            mode = self.mode.get()
            x1, y1 = self.start_point[0] // PIXEL_SIZE, self.start_point[1] // PIXEL_SIZE
            x2, y2 = end_point[0] // PIXEL_SIZE, end_point[1] // PIXEL_SIZE

            if mode == "ЦДА":
                pts = Algorithms.dda(x1, y1, x2, y2, self.debug_mode)
                if self.debug_mode:
                    self.draw_step_by_step(pts)
                else:
                    for pt in pts:
                        self.plot_block(pt[0], pt[1], 75)
            elif mode == "Брезенхем":
                pts = Algorithms.bresenham(x1, y1, x2, y2, self.debug_mode)
                if self.debug_mode:
                    self.draw_step_by_step(pts)
                else:
                    for pt in pts:
                        self.plot_block(pt[0], pt[1], 75)
            elif mode == "Ву":
                pts = Algorithms.wu((self.start_point[0] / PIXEL_SIZE) + 0.5,
                                    (self.start_point[1] / PIXEL_SIZE) + 0.5,
                                    (end_point[0] / PIXEL_SIZE) + 0.5,
                                    (end_point[1] / PIXEL_SIZE) + 0.5,
                                    self.debug_mode)
                if self.debug_mode:
                    self.draw_step_by_step(pts, wu=True)
                else:
                    for pt in pts:
                        value = int(75 * pt[2])
                        self.plot_block(pt[0], pt[1], value)

            self.start_point = None

    def draw_step_by_step(self, points, wu=False):
        self.current_pts = points
        self.current_index = 0
        self._draw_next(wu)

    def _draw_next(self, wu):
        if self.current_index >= len(self.current_pts):
            return
        pt = self.current_pts[self.current_index]
        if wu:
            value = int(75 * pt[2])
            self.plot_block(pt[0], pt[1], value)
        else:
            self.plot_block(pt[0], pt[1], 75)
        self.current_index += 1
        self.after(100, lambda: self._draw_next(wu))  # 100 мс между шагами

    def draw_pixel(self, x, y, color):
        r = 2
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

    def plot_block(self, x, y, value, color=None):
        size = PIXEL_SIZE
        X = x * PIXEL_SIZE
        Y = y * PIXEL_SIZE
        if color is None:
            gray = int(255 * (1 - value / 75))
            color = f"#{gray:02x}{gray:02x}{gray:02x}"
        self.canvas.create_rectangle(X, Y, X + size, Y + size, fill=color, outline="black")

    def draw_grid(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        for i in range(0, width, PIXEL_SIZE):
            self.canvas.create_line(i, 0, i, height, fill="#ddd", tags="grid")
        for j in range(0, height, PIXEL_SIZE):
            self.canvas.create_line(0, j, width, j, fill="#ddd", tags="grid")
        self.after(500, self.draw_grid)


