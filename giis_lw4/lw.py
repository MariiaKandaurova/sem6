import tkinter as tk
from tkinter import filedialog
import math


class TransformApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Аффинные и проективные преобразования")
        self.geometry("1000x750")

        self.model_pts: list[list[float]] = []
        self.world_pts: list[list[float]] = []
        self.edges: list[tuple[int, int]] = []
        self.faces: list[tuple[int, ...]] = []

        self.scale_factor = 80
        self.d = 5.0
        self.perspective_on = False

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        tb = tk.Frame(self, bd=1, relief=tk.RAISED)
        def btn(txt, cmd): tk.Button(tb, text=txt, command=cmd)\
            .pack(side=tk.LEFT, padx=2, pady=2)
        btn("Загрузить", self.load_object)
        btn("Поворот X 30°", lambda: self.rotate_axis(30, 'x'))
        btn("Поворот Y 45°", lambda: self.rotate_axis(45, 'y'))
        btn("Поворот Z 30°", lambda: self.rotate_axis(30, 'z'))
        btn("Масштаб ×1.5", lambda: self.uniform_scale(1.5))
        btn("Отразить X", lambda: self.reflect('x'))
        btn("Отразить Y", lambda: self.reflect('y'))
        btn("Отразить Z", lambda: self.reflect('z'))
        btn("Перспектива ON/OFF", self.toggle_perspective)
        btn("Сброс", self.reset)
        tb.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _bind_keys(self):
        def wrap(func):
            return lambda e: (func(), "break")

        b = self.bind_all
        b("<Left>",  wrap(lambda: self.translate(-2, 0, 0)))
        b("<Right>", wrap(lambda: self.translate( 2, 0, 0)))
        b("<Up>",    wrap(lambda: self.translate(0,  2, 0)))
        b("<Down>",  wrap(lambda: self.translate(0, -2, 0)))
        b("<Prior>", wrap(lambda: self.translate(0, 0,  2)))
        b("<Next>",  wrap(lambda: self.translate(0, 0, -2)))

        b("w", wrap(lambda: self.rotate_axis( 10, 'y')))
        b("s", wrap(lambda: self.rotate_axis(-10, 'y')))
        b("a", wrap(lambda: self.rotate_axis( 10, 'x')))
        b("d", wrap(lambda: self.rotate_axis(-10, 'x')))
        b("q", wrap(lambda: self.rotate_axis( 10, 'z')))
        b("e", wrap(lambda: self.rotate_axis(-10, 'z')))

        b("<Key-plus>",    wrap(lambda: self.uniform_scale(1.2)))
        b("<Key-minus>",   wrap(lambda: self.uniform_scale(1/1.2)))
        b("<KP_Add>",      wrap(lambda: self.uniform_scale(1.2)))
        b("<KP_Subtract>", wrap(lambda: self.uniform_scale(1/1.2)))

        b("x", wrap(lambda: self.reflect('x')))
        b("y", wrap(lambda: self.reflect('y')))
        b("z", wrap(lambda: self.reflect('z')))

        b("p", wrap(self.toggle_perspective))
        b("r", wrap(self.reset))

    def load_object(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        self.model_pts, self.edges = [], []
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if not parts: continue
                if parts[0] == 'v' and len(parts) == 4:
                    self.model_pts.append([float(p) for p in parts[1:]] + [1])
                elif parts[0] == 'e' and len(parts) == 3:
                    self.edges.append((int(parts[1]), int(parts[2])))
                elif len(parts) == 3:                         # bare x y z
                    self.model_pts.append([float(p) for p in parts] + [1])

        if not self.edges and len(self.model_pts) == 8:
            self.edges = [
                (0,1),(1,2),(2,3),(3,0),
                (4,5),(5,6),(6,7),(7,4),
                (0,4),(1,5),(2,6),(3,7)
            ]
            self.faces = [
                (0,1,2,3),(4,5,6,7),(0,1,5,4),
                (2,3,7,6),(1,2,6,5),(0,3,7,4)
            ]
        else:
            self.faces = []

        self.world_pts = [p.copy() for p in self.model_pts]

        if self.model_pts:
            xs = [p[0] for p in self.model_pts]
            ys = [p[1] for p in self.model_pts]
            span = max(max(xs) - min(xs), max(ys) - min(ys))
            if span:
                self.scale_factor = self.canvas.winfo_height() * 0.4 / span
        self.draw()

    @staticmethod
    def _mat_translate(dx, dy, dz):
        return [[1,0,0,dx],[0,1,0,dy],[0,0,1,dz],[0,0,0,1]]

    @staticmethod
    def _mat_scale(s):
        return [[s,0,0,0],[0,s,0,0],[0,0,s,0],[0,0,0,1]]

    @staticmethod
    def _mat_reflect(axis):
        m = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        m[{'x':0,'y':1,'z':2}[axis]][{'x':0,'y':1,'z':2}[axis]] = -1
        return m

    @staticmethod
    def _mat_rotate(deg, axis):
        t = math.radians(deg); c, s = math.cos(t), math.sin(t)
        if axis == 'x':
            return [[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]]
        if axis == 'y':
            return [[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]]
        return [[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]]

    def _apply(self, M):
        self.world_pts = [
            [sum(p[j]*M[j][i] for j in range(4)) for i in range(4)]
            for p in self.world_pts
        ]
        self.draw()

    def translate(self, dx, dy, dz):
        self._apply(self._mat_translate(dx, dy, dz))

    def rotate_axis(self, ang, axis):
        self._apply(self._mat_rotate(ang, axis))

    def uniform_scale(self, s):
        self._apply(self._mat_scale(s))

    def reflect(self, axis):
        self._apply(self._mat_reflect(axis))

    def toggle_perspective(self):
        self.perspective_on = not self.perspective_on
        self.draw()

    def reset(self):
        self.world_pts = [p.copy() for p in self.model_pts]
        self.scale_factor = 80
        self.perspective_on = False
        self.draw()

    def _proj(self, x, y, z):
        if self.perspective_on and z > -self.d + 0.01:
            f = self.d / (self.d + z)
            return x*f, y*f
        return x, y

    def draw(self):
        self.canvas.delete("all")
        if not self.world_pts:
            return
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w//2, h//2

        pts2d = []
        for x, y, z, _ in self.world_pts:
            px, py = self._proj(x, y, z)
            sx, sy = cx + px*self.scale_factor, cy - py*self.scale_factor
            pts2d.append((sx, sy, z))
            self.canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill="blue")

        def visible(a, b, c):
            if not self.faces:
                return True
            pa, pb, pc = [self.world_pts[i][:3] for i in (a, b, c)]
            u = [pb[i]-pa[i] for i in range(3)]
            v = [pc[i]-pa[i] for i in range(3)]
            nz = u[0]*v[1] - u[1]*v[0]
            return nz < 0

        if self.faces:
            for face in self.faces:
                dash = () if visible(*face[:3]) else (4,2)
                for i in range(len(face)):
                    a, b = face[i], face[(i+1)%len(face)]
                    x1, y1, _ = pts2d[a]
                    x2, y2, _ = pts2d[b]
                    self.canvas.create_line(x1, y1, x2, y2, dash=dash)
        else:
            for a, b in self.edges:
                x1, y1, _ = pts2d[a]
                x2, y2, _ = pts2d[b]
                self.canvas.create_line(x1, y1, x2, y2)


if __name__ == "__main__":
    TransformApp().mainloop()
