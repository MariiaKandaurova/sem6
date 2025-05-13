import tkinter as tk
from collections import defaultdict
from math import inf

GRID = 8
GRID_COLOR = "#e0e0e0"


class DelaunayTriangulation:
    def __init__(self, points):
        self.points = points[:]
        self.triangles = []
        if len(points) >= 3:
            self._create_super()
            for p in points:
                self._add_point(p)
            self._remove_super()

    def _create_super(self):
        xs, ys = zip(*self.points)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        w, h = max_x - min_x, max_y - min_y
        p1 = (min_x - w,     min_y - 2*h)
        p2 = (max_x + w,     min_y - 2*h)
        p3 = (min_x + w/2,   max_y + 2*h)
        self.super = (p1, p2, p3)
        self.triangles.append(self.super)

    def _add_point(self, p):
        bad = [t for t in self.triangles if self._in_circumcircle(p, t)]
        edge_counter = defaultdict(int)
        for t in bad:
            for i in range(3):
                e = tuple(sorted((t[i], t[(i+1)%3])))
                edge_counter[e] += 1
        border = [e for e, c in edge_counter.items() if c == 1]

        for t in bad:
            self.triangles.remove(t)
        for e in border:
            self.triangles.append((e[0], e[1], p))

    def _remove_super(self):
        a, b, c = self.super
        self.triangles = [t for t in self.triangles if a not in t and b not in t and c not in t]

    @staticmethod
    def _in_circumcircle(p, tri):
        (ax, ay), (bx, by), (cx, cy) = tri
        px, py = p
        d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
        if d == 0:
            return False
        ux = ((ax**2+ay**2)*(by-cy)+(bx**2+by**2)*(cy-ay)+(cx**2+cy**2)*(ay-by))/d
        uy = ((ax**2+ay**2)*(cx-bx)+(bx**2+by**2)*(ax-cx)+(cx**2+cy**2)*(bx-ax))/d
        return (px-ux)**2 + (py-uy)**2 <= (ax-ux)**2 + (ay-uy)**2 + 1e-9

    def voronoi_edges(self):
        if not self.triangles:
            return []
        centers = {t: self._circumcenter(t) for t in self.triangles}
        edges = []
        for t in self.triangles:
            for i in range(3):
                nb = self._neighbor(t, i)
                if nb:
                    edges.append((centers[t], centers[nb]))
        return edges

    @staticmethod
    def _circumcenter(tri):
        (ax, ay), (bx, by), (cx, cy) = tri
        d = 2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
        if d == 0:
            return (inf, inf)
        ux = ((ax**2+ay**2)*(by-cy)+(bx**2+by**2)*(cy-ay)+(cx**2+cy**2)*(ay-by))/d
        uy = ((ax**2+ay**2)*(cx-bx)+(bx**2+by**2)*(ax-cx)+(cx**2+cy**2)*(bx-ax))/d
        return (ux, uy)

    def _neighbor(self, tri, i):
        a, b = tri[i], tri[(i+1)%3]
        for t in self.triangles:
            if t is tri:
                continue
            if {a, b}.issubset(t):
                return t
        return None


class App(tk.Tk):
    R = 3

    def __init__(self):
        super().__init__()
        self.title("Триангуляция Делоне и диаграмма Вороного")
        self.geometry("900x700")

        top = tk.Frame(self, padx=10, pady=5)
        top.pack(side="top", fill="x")

        tk.Button(top, text="Очистить", command=self.clear)\
            .pack(side="left", padx=(0, 15))

        self.show_tri = tk.BooleanVar(value=True)
        self.show_vor = tk.BooleanVar(value=True)

        tk.Checkbutton(top, text="Триангуляция",
                       variable=self.show_tri, command=self.redraw)\
            .pack(side="left")
        tk.Checkbutton(top, text="Вороной",
                       variable=self.show_vor, command=self.redraw)\
            .pack(side="left", padx=(10, 0))

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.add_point)
        self.points, self.triangles, self.v_edges = [], [], []

    def add_point(self, event):
        self.points.append((event.x, event.y))
        self.rebuild()
        self.redraw()

    def clear(self):
        self.points.clear()
        self.triangles.clear()
        self.v_edges.clear()
        self.canvas.delete("all")
        self._draw_grid()

    def rebuild(self):
        if len(self.points) < 3:
            self.triangles, self.v_edges = [], []
            return
        d = DelaunayTriangulation(self.points)
        self.triangles, self.v_edges = d.triangles, d.voronoi_edges()

    def _draw_grid(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        for x in range(0, w, GRID):
            self.canvas.create_line(x, 0, x, h, fill=GRID_COLOR)
        for y in range(0, h, GRID):
            self.canvas.create_line(0, y, w, y, fill=GRID_COLOR)

    def redraw(self):
        self.canvas.delete("all")
        self._draw_grid()

        if self.show_tri.get():
            for t in self.triangles:
                self.canvas.create_polygon(*sum(t, ()),
                                           outline="#8000FF", fill="", width=1)

        if self.show_vor.get():
            for (x1, y1), (x2, y2) in self.v_edges:
                if abs(x1) == inf or abs(x2) == inf:
                    continue
                self.canvas.create_line(x1, y1, x2, y2,
                                        fill="#008800", width=1)

        for x, y in self.points:
            self.canvas.create_oval(x-self.R, y-self.R,
                                    x+self.R, y+self.R,
                                    fill="#FF3333", outline="#FF3333")


if __name__ == "__main__":
    App().mainloop()