import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time

PIX = 10
FILL_COLOR = "#00ff00"


class PixelCanvas(tk.Canvas):

    def __init__(self, master, w=1000, h=800):
        super().__init__(master, width=w, height=h, bg="white",
                         highlightthickness=0)
        self.buf: dict[tuple[int, int], str] = {}
        self.draw_grid()

    def g2c(self, gx, gy):
        return gx*PIX, gy*PIX

    def c2g(self, x, y):
        return x//PIX, y//PIX

    def pixel(self, gx, gy, color="#000"):
        self.buf[(gx, gy)] = color
        x0, y0 = self.g2c(gx, gy)
        self.create_rectangle(x0, y0, x0+PIX, y0+PIX,
                              outline="", fill=color, tags="pix")

    def color(self, gx, gy):
        return self.buf.get((gx, gy), "#ffffff")

    def draw_grid(self):
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        for x in range(0, w, PIX):
            self.create_line(x, 0, x, h, fill="#e0e0e0")
        for y in range(0, h, PIX):
            self.create_line(0, y, w, y, fill="#e0e0e0")

    def clear_pixels(self):
        self.delete("pix"); self.buf.clear()


class PolygonEditor(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.cnv = PixelCanvas(self); self.cnv.pack(fill="both", expand=True)

        # ─ state ─
        self.points: list[tuple[int, int]] = []
        self.is_drawing = True
        self.line_alg = tk.StringVar(value="Bresenham")
        self.debug = tk.BooleanVar(value=False)
        self.seed_mode = False;  self.line_mark = False
        self.seed_pt = None
        self.seg_a = self.seg_b = None
        self.fill_alg = "Simple Seed Fill"
        self.cnv.bind("<Button-1>", self.on_click)
        self.cnv.bind("<Double-Button-1>", self.on_double)

    def draw_line(self, p, q):
        gx1, gy1 = p; gx2, gy2 = q
        if self.line_alg.get() == "CDA":
            dx, dy = gx2-gx1, gy2-gy1
            steps = int(max(abs(dx), abs(dy)))
            x, y = gx1, gy1
            for _ in range(steps+1):
                self.cnv.pixel(round(x), round(y))
                x += dx/steps; y += dy/steps
        elif self.line_alg.get() == "Wu":
            def plot(x, y, c):
                v = int(255*(1-c)); col = f"#{v:02x}{v:02x}{v:02x}"
                self.cnv.pixel(x, y, col)
            x0, y0 = gx1, gy1; x1, y1 = gx2, gy2
            steep = abs(y1-y0) > abs(x1-x0)
            if steep: x0, y0, x1, y1 = y0, x0, y1, x1
            if x0 > x1: x0, x1, y0, y1 = x1, x0, y1, y0
            dx, dy = x1-x0, y1-y0
            grad = dy/dx if dx else 1
            y = y0 + grad
            for x in range(x0, x1+1):
                fy = y - int(y)
                plot(int(y), x, 1-fy) if steep else plot(x, int(y), 1-fy)
                plot(int(y)+1, x, fy)  if steep else plot(x, int(y)+1, fy)
                y += grad
        else:
            x, y = gx1, gy1; dx = abs(gx2-gx1); dy = abs(gy2-gy1)
            sx = 1 if gx1 < gx2 else -1; sy = 1 if gy1 < gy2 else -1
            err = dx-dy
            while True:
                self.cnv.pixel(x, y)
                if (x, y) == (gx2, gy2): break
                e2 = 2*err
                if e2 > -dy: err -= dy; x += sx
                if e2 <  dx: err += dx; y += sy

    def seed_fill(self, gx, gy):
        target = self.cnv.color(gx, gy)
        if target == FILL_COLOR: return
        if self.fill_alg == "Simple Seed Fill":
            st=[(gx,gy)]
            while st:
                x,y = st.pop()
                if self.cnv.color(x,y)==target:
                    self.cnv.pixel(x,y,FILL_COLOR)
                    if self.debug.get(): self.cnv.update(); time.sleep(.01)
                    st.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
        elif self.fill_alg == "Scanline Seed Fill":
            st=[(gx,gy)]; vis=set()
            while st:
                x,y=st.pop()
                if (x,y) in vis or self.cnv.color(x,y)!=target: continue
                xl=x; xr=x
                while self.cnv.color(xl-1,y)==target: xl-=1
                while self.cnv.color(xr+1,y)==target: xr+=1
                for px in range(xl,xr+1):
                    self.cnv.pixel(px,y,FILL_COLOR); vis.add((px,y))
                for px in range(xl,xr+1):
                    for ny in (y-1,y+1):
                        if self.cnv.color(px,ny)==target and (px,ny) not in vis:
                            st.append((px,ny))
                if self.debug.get(): self.cnv.update(); time.sleep(.01)
        else:
            self.edge_list_fill(active=(self.fill_alg=="Active Edge List"))

    def edge_list_fill(self, active=True):
        if len(self.points)<3: return
        edges=[]
        for i in range(len(self.points)):
            (x1,y1)=self.points[i]; (x2,y2)=self.points[(i+1)%len(self.points)]
            if y1==y2: continue
            if y1>y2: x1,y1,x2,y2 = x2,y2,x1,y1
            inv = (x2-x1)/(y2-y1)
            edges.append([y1,y2,x1,inv])
        edges.sort(key=lambda e:e[0])
        y = min(e[0] for e in edges)
        ymax = max(e[1] for e in edges)
        A=[]
        while y<ymax:
            A += [e for e in edges if e[0]==y]
            A = [e for e in A if e[1]>y]
            A.sort(key=lambda e:e[2])
            for a,b in zip(A[0::2],A[1::2]):
                xs=int((a[2]+PIX)//PIX); xe=int((b[2])//PIX)
                for gx in range(xs,xe):
                    self.cnv.pixel(gx,int(y//PIX),FILL_COLOR)
            for e in A: e[2]+=e[3]*PIX if active else e[3]
            y+=PIX if active else 1
            if self.debug.get(): self.cnv.update(); time.sleep(.01)

    def is_convex(self):
        if len(self.points)<3: return False
        sign=None
        for i in range(len(self.points)):
            p,q,r=self.points[i],self.points[(i+1)%len(self.points)],self.points[(i+2)%len(self.points)]
            cross=(q[0]-p[0])*(r[1]-q[1])-(q[1]-p[1])*(r[0]-q[0])
            if cross!=0:
                if sign is None: sign=cross>0
                elif (cross>0)!=sign: return False
        return True

    def hull_graham(self):
        pts=sorted(self.points)
        if len(pts)<3: return []
        def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
        low=[]; upp=[]
        for p in pts:
            while len(low)>=2 and cross(low[-2],low[-1],p)<=0: low.pop()
            low.append(p)
        for p in reversed(pts):
            while len(upp)>=2 and cross(upp[-2],upp[-1],p)<=0: upp.pop()
            upp.append(p)
        return low[:-1]+upp[:-1]

    def hull_jarvis(self):
        pts=self.points
        if len(pts)<3: return []
        left=min(pts)
        hull=[]; p=left
        while True:
            hull.append(p); q=pts[0]
            for r in pts:
                orient=(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
                if q==p or orient<0: q=r
            p=q
            if p==left: break
        return hull

    def compute_normals(self):
        if len(self.points) < 3 or not self.is_convex():
            return []
        s = 0
        for i in range(-1, len(self.points) - 1):
            x1, y1 = self.points[i]; x2, y2 = self.points[i + 1]
            s += (x2 - x1) * (y2 + y1)
        orient = 1 if s < 0 else -1
        normals = []
        for i in range(len(self.points)):
            x1, y1 = self.points[i]; x2, y2 = self.points[(i + 1) % len(self.points)]
            vx, vy = x2 - x1, y2 - y1
            nx, ny = -vy * orient, vx * orient
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            normals.append((mx // PIX, my // PIX, nx, ny))
        return normals

    def draw_normals(self):
        for mx, my, nx, ny in self.compute_normals():
            x0, y0 = mx, my
            scale = 2
            mag = max(abs(nx), abs(ny)) or 1
            x1 = x0 + int(nx / mag * scale)
            y1 = y0 + int(ny / mag * scale)
            self.cnv.pixel(x0, y0, "#0000ff")
            self.cnv.create_line(*self.cnv.g2c(x0, y0),
                                 *self.cnv.g2c(x1, y1),
                                 fill="blue", arrow=tk.LAST)

    def on_click(self,event):
        gx,gy = self.cnv.c2g(event.x,event.y)
        if self.seed_mode:
            self.seed_mode=False; self.seed_fill(gx,gy); return
        if self.line_mark:
            if not self.seg_a:
                self.seg_a=(gx,gy); self.cnv.pixel(gx,gy,"blue")
            else:
                self.seg_b=(gx,gy); self.cnv.pixel(gx,gy,"blue")
                self.draw_line(self.seg_a,self.seg_b)
                inter=self.intersections()
                for x,y in inter: self.cnv.pixel(x,y,"#ff0000")
                messagebox.showinfo("Intersections",f"Найдено: {len(inter)}")
                self.seg_a=self.seg_b=None; self.line_mark=False
            return
        if self.is_drawing:
            self.points.append((gx*PIX,gy*PIX))
            self.cnv.pixel(gx,gy)
            if len(self.points)>1:
                p=self.points[-2]; q=self.points[-1]
                self.draw_line((p[0]//PIX,p[1]//PIX),(q[0]//PIX,q[1]//PIX))

    def on_double(self, event):
        if self.is_drawing and len(self.points)>2:
            p=self.points[-1]; q=self.points[0]
            self.draw_line((p[0]//PIX,p[1]//PIX),(q[0]//PIX,q[1]//PIX))
            self.is_drawing=False

    def intersections(self):
        if not (self.seg_a and self.seg_b): return []
        res=[]
        def det(a,b,c,d): return a*d-b*c
        sx1,sy1=self.seg_a; sx2,sy2=self.seg_b
        for i in range(len(self.points)):
            p1=self.points[i]; p2=self.points[(i+1)%len(self.points)]
            x1,y1=p1[0]//PIX,p1[1]//PIX; x2,y2=p2[0]//PIX,p2[1]//PIX
            den=det(sx1-sx2,sy1-sy2,x1-x2,y1-y2)
            if den==0: continue
            px=det(det(sx1,sy1,sx2,sy2),sx1-sx2,det(x1,y1,x2,y2),x1-x2)/den
            py=det(det(sx1,sy1,sx2,sy2),sy1-sy2,det(x1,y1,x2,y2),y1-y2)/den
            if (min(sx1,sx2)<=px<=max(sx1,sx2) and
                min(sy1,sy2)<=py<=max(sy1,sy2) and
                min(x1,x2)<=px<=max(x1,x2) and
                min(y1,y2)<=py<=max(y1,y2)):
                res.append((int(px),int(py)))
        return res

    def reset(self):
        self.cnv.clear_pixels(); self.points.clear()
        self.is_drawing=True; self.line_mark=self.seed_mode=False


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор полигонов (Tkinter)")
        self.geometry("1100x850")

        tb = tk.Frame(self); tb.pack(side="top", fill="x")
        self.ed = PolygonEditor(self); self.ed.pack(fill="both", expand=True)
        ttk.Label(tb, text="Линия:").pack(side="left")
        cmb = ttk.Combobox(tb, values=["Брезенхем", "ЦДА", "Ву"], state="readonly", width=12,
                           textvariable=self.ed.line_alg)

        cmb.pack(side="left", padx=2)

        tk.Button(tb, text="Сброс", command=self.ed.reset).pack(side="left", padx=2)
        tk.Button(tb, text="Выпуклый?", command=lambda: messagebox.showinfo("Проверка выпуклости",
                                                                            "Да" if self.ed.is_convex() else "Нет")).pack(
            side="left", padx=2)
        tk.Button(tb, text="Оболочка (Грэхем)", command=lambda: self.draw_hull(self.ed.hull_graham())).pack(side="left")
        tk.Button(tb, text="Оболочка (Джарвис)", command=lambda: self.draw_hull(self.ed.hull_jarvis())).pack(
            side="left")
        tk.Button(tb, text="Нормали", command=self.ed.draw_normals).pack(side="left")
        tk.Button(tb, text="Пересечения", command=self.start_seg).pack(side="left")
        tk.Button(tb, text="Заливка", command=self.ask_fill).pack(side="left")
        debug_checkbox = tk.Checkbutton(tb, text="Отладка", variable=self.ed.debug)
        debug_checkbox.pack(side="left", padx=2)

    def draw_hull(self, hull):
        if not hull: return
        self.ed.cnv.clear_pixels()
        for gx,gy in [(x//PIX,y//PIX) for x,y in self.ed.points]:
            self.ed.cnv.pixel(gx,gy,"#640000")
        for i in range(len(hull)):
            p=hull[i]; q=hull[(i+1)%len(hull)]
            self.ed.draw_line((p[0]//PIX,p[1]//PIX),(q[0]//PIX,q[1]//PIX))

    def start_seg(self):
        self.ed.line_mark=True; self.ed.is_drawing=False
        messagebox.showinfo("Segment","Щёлкните две точки")

    def ask_fill(self):
        al = simpledialog.askstring("Заливка",
                                    "Алгоритм (Упорядоченный / Активный / Простой / Построчный):",
                                    initialvalue="Упорядоченный")
        if not al: return

        mp = {
            "упорядоченный": "Ordered Edge List",
            "активный": "Active Edge List",
            "простой": "Simple Seed Fill",
            "построчный": "Scanline Seed Fill"
        }

        for k, v in mp.items():
            if al.lower().startswith(k):
                self.ed.fill_alg = v
        self.ed.seed_mode = True
        messagebox.showinfo("Затравка", "Щёлкните точку затравки")


if __name__ == "__main__":
    App().mainloop()
