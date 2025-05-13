import tkinter as tk

PIXEL_SIZE = 8

M_hermite = [
    [2, -2, 1, 1],
    [-3, 3, -2, -1],
    [0, 0, 1, 0],
    [1, 0, 0, 0]
]

def multiply_matrix_vector(matrix, vector):
    return [sum(matrix[r][i] * vector[i] for i in range(4)) for r in range(4)]


def hermite_curve(P1, P4, R1, R4, steps=100):
    curve = []
    for step in range(steps + 1):
        t = step / steps
        T = [t**3, t**2, t, 1]
        Gx = [P1[0], P4[0], R1[0], R4[0]]
        Gy = [P1[1], P4[1], R1[1], R4[1]]
        Cx = multiply_matrix_vector(M_hermite, Gx)
        Cy = multiply_matrix_vector(M_hermite, Gy)
        x = sum(T[i] * Cx[i] for i in range(4))
        y = sum(T[i] * Cy[i] for i in range(4))
        curve.append((x, y))
    return curve

def bezier_curve(P1, P2, P3, P4, steps=100):
    Mb = [
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ]
    curve = []
    for step in range(steps + 1):
        t = step / steps
        T = [t**3, t**2, t, 1]
        Gx = [P1[0], P2[0], P3[0], P4[0]]
        Gy = [P1[1], P2[1], P3[1], P4[1]]
        Cx = multiply_matrix_vector(Mb, Gx)
        Cy = multiply_matrix_vector(Mb, Gy)
        x = sum(T[i] * Cx[i] for i in range(4))
        y = sum(T[i] * Cy[i] for i in range(4))
        curve.append((x, y))
    return curve

def bspline_curve(points, steps=100):
    if len(points) < 4:
        return []
    Mb = [
        [-1/6,  0.5, -0.5, 1/6],
        [0.5,   -1,   0.5,   0],
        [-0.5,   0,   0.5,   0],
        [1/6,  2/3,  1/6,   0]
    ]
    curve = []
    for i in range(len(points) - 3):
        seg = points[i:i+4]
        for step in range(steps + 1):
            t = step / steps
            T = [t**3, t**2, t, 1]
            Gx = [p[0] for p in seg]
            Gy = [p[1] for p in seg]
            Cx = multiply_matrix_vector(Mb, Gx)
            Cy = multiply_matrix_vector(Mb, Gy)
            x = sum(T[j] * Cx[j] for j in range(4))
            y = sum(T[j] * Cy[j] for j in range(4))
            curve.append((x, y))
    return curve

class GraphicalEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор кривых")
        self.geometry("900x700")
        self.mode = tk.StringVar(value="Эрмит")
        self.mode.trace_add('write', self.on_mode_change)
        self.points_hermite = []
        self.points_bezier = []
        self.points_bspline = []
        self.selected_item = None
        self.last_P4 = None
        self.last_R4 = None
        self._init_ui()

    def on_mode_change(self, *args):
        mode = self.mode.get()
        if mode == "Эрмит":
            self.points_hermite.clear()
            self.last_P4 = None
            self.last_R4 = None
        elif mode == "Безье":
            self.points_bezier.clear()
        else:
            self.points_bspline.clear()
        self.selected_item = None

    def _init_ui(self):
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        for m in ["Эрмит", "Безье", "B-сплайн"]:
            b = tk.Radiobutton(
                toolbar, text=m, variable=self.mode, value=m,
                indicatoron=0, width=12
            )
            b.pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="Очистить холст", command=self.clear_canvas).pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.tag_bind("point", "<Button-3>", self.select_point)
        self.canvas.bind("<B3-Motion>", self.on_drag)
        self.draw_grid()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points_hermite.clear()
        self.points_bezier.clear()
        self.points_bspline.clear()
        self.last_P4 = None
        self.last_R4 = None
        self.selected_item = None
        self.draw_grid()

    def on_left_click(self, event):
        mode = self.mode.get()
        x, y = event.x, event.y
        if mode == "Эрмит":
            lst = self.points_hermite
        elif mode == "Безье":
            lst = self.points_bezier
        else:
            lst = self.points_bspline

        lst.append((x, y))
        self.canvas.create_oval(x-5, y-5, x+5, y+5,
                                fill='black', tags=("point", f"method_{mode}"))

        if mode == "Эрмит":
            if len(lst) == 4:
                P1, P4, R1_pt, R4_pt = lst
                R1 = (R1_pt[0] - P1[0], R1_pt[1] - P1[1])
                R4 = (R4_pt[0] - P4[0], R4_pt[1] - P4[1])
                self.last_P4 = P4
                self.last_R4 = R4
                curve = hermite_curve(P1, P4, R1, R4)
                for j in range(len(curve) - 1):
                    x0, y0 = map(int, curve[j])
                    x1, y1 = map(int, curve[j+1])
                    self.canvas.create_line(x0, y0, x1, y1, fill='blue', tags=(f"curve_{mode}"))
            elif len(lst) > 4 and len(lst) % 2 == 0:
                P4, R4_pt = lst[-2:]
                P1 = self.last_P4
                R1 = self.last_R4
                R4 = (R4_pt[0] - P4[0], R4_pt[1] - P4[1])
                curve = hermite_curve(P1, P4, R1, R4)
                for j in range(len(curve) - 1):
                    x0, y0 = map(int, curve[j])
                    x1, y1 = map(int, curve[j+1])
                    self.canvas.create_line(x0, y0, x1, y1, fill='blue', tags=(f"curve_{mode}"))
                self.last_P4 = P4
                self.last_R4 = R4
        elif mode == "Безье" and len(lst) >= 4 and (len(lst) - 4) % 3 == 0:
            seg = lst[-4:]
            curve = bezier_curve(*seg)
            for j in range(len(curve) - 1):
                x0, y0 = map(int, curve[j])
                x1, y1 = map(int, curve[j+1])
                self.canvas.create_line(x0, y0, x1, y1, fill='green', tags=(f"curve_{mode}"))
        elif mode == "B-сплайн":
            self.redraw(method=mode)

    def select_point(self, event):
        self.selected_item = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.itemconfig(self.selected_item, fill='red')
        return "break"

    def on_drag(self, event):
        if not self.selected_item:
            return
        self.canvas.coords(self.selected_item, event.x-5, event.y-5, event.x+5, event.y+5)
        tags = self.canvas.gettags(self.selected_item)
        mode = next((t.split("method_")[1] for t in tags if t.startswith("method_")), None)
        if mode == "Эрмит":
            pts = self.points_hermite
        elif mode == "Безье":
            pts = self.points_bezier
        else:
            pts = self.points_bspline
        all_pts = [item for item in self.canvas.find_withtag("point") if f"method_{mode}" in self.canvas.gettags(item)]
        idx = all_pts.index(self.selected_item)
        pts[idx] = (event.x, event.y)
        self.redraw(method=mode)

    def redraw_current(self):
        self.redraw(method=self.mode.get())

    def redraw(self, method):
        tag = f"curve_{method}"
        self.canvas.delete(tag)
        if method == "Эрмит":
            pts = self.points_hermite
            if len(pts) < 4:
                return
            i = 0
            while i + 3 < len(pts):
                if i == 0:
                    seg = pts[i:i+4]
                    P1, P4, R1_pt, R4_pt = seg
                    R1 = (R1_pt[0]-P1[0], R1_pt[1]-P1[1])
                    R4 = (R4_pt[0]-P4[0], R4_pt[1]-P4[1])
                else:
                    P1 = prev_P4
                    R1 = prev_R4
                    P4, R4_pt = pts[i:i+2]
                    R4 = (R4_pt[0]-P4[0], R4_pt[1]-P4[1])
                curve = hermite_curve(P1, P4, R1, R4)
                for j in range(len(curve)-1):
                    x0, y0 = map(int, curve[j])
                    x1, y1 = map(int, curve[j+1])
                    self.canvas.create_line(x0, y0, x1, y1, fill='blue', tags=tag)
                prev_P4 = P4
                prev_R4 = R4
                i = 4 if i == 0 else i + 2
        elif method == "Безье":
            pts = self.points_bezier
            for i in range(0, len(pts)-3, 3):
                seg = pts[i:i+4]
                curve = bezier_curve(*seg)
                for j in range(len(curve)-1):
                    x0, y0 = map(int, curve[j])
                    x1, y1 = map(int, curve[j+1])
                    self.canvas.create_line(x0, y0, x1, y1, fill='green', tags=tag)
        else:
            pts = self.points_bspline
            curve = bspline_curve(pts)
            for j in range(len(curve)-1):
                x0, y0 = map(int, curve[j])
                x1, y1 = map(int, curve[j+1])
                self.canvas.create_line(x0, y0, x1, y1, fill='purple', tags=tag)

    def draw_grid(self):
        w, h = 900, 700
        for i in range(0, w, PIXEL_SIZE):
            self.canvas.create_line(i, 0, i, h, fill="#ddd", tags="grid")
        for j in range(0, h, PIXEL_SIZE):
            self.canvas.create_line(0, j, w, j, fill="#ddd", tags="grid")

if __name__ == '__main__':
    app = GraphicalEditor()
    app.mainloop()
