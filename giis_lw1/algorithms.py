PIXEL_SIZE = 8


class Algorithms:
    @staticmethod
    def dda(x1, y1, x2, y2, debug=False):
        points = []
        dx = x2 - x1
        dy = y2 - y1
        L = int(max(abs(dx), abs(dy)))
        if L == 0:
            return [(x1, y1)]
        x_inc = dx / L
        y_inc = dy / L
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1
        x = x1 + 0.5 * sign_x
        y = y1 + 0.5 * sign_y
        if debug:
            print(f"Step 0: x={x:.2f}, y={y:.2f} -> ({int(x)}, {int(y)})")
        points.append((int(x), int(y)))
        for i in range(L):
            x += x_inc
            y += y_inc
            if debug:
                print(f"Step {i+1}: x={x:.2f}, y={y:.2f} -> ({int(x)}, {int(y)})")
            points.append((int(x), int(y)))
        return points

    @staticmethod
    def bresenham(x1, y1, x2, y2, debug=False):
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            if debug:
                print(f"Plot: ({x1}, {y1})")
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return points

    @staticmethod
    def wu(x1, y1, x2, y2, debug=False):
        values = []
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) >= abs(dy):
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            k = dy / dx if dx != 0 else 0
            for x in range(int(x1), int(x2) + 1):
                y = y1 + k * (x - x1)
                y_int = int(y)
                y_dec = y - y_int
                in_bot = 1 - y_dec
                in_top = y_dec
                if debug:
                    print(f"x={x}, y={y:.2f}, y_int={y_int}, bot={in_bot:.2f}, top={in_top:.2f}")
                values.append([x, y_int, in_bot])
                values.append([x, y_int + 1, in_top])
        else:
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            k = dx / dy if dy != 0 else 0
            for y in range(int(y1), int(y2) + 1):
                x = x1 + k * (y - y1)
                x_int = int(x)
                x_dec = x - x_int
                in_bot = 1 - x_dec
                in_top = x_dec
                if debug:
                    print(f"y={y}, x={x:.2f}, x_int={x_int}, bot={in_bot:.2f}, top={in_top:.2f}")
                values.append([x_int, y, in_bot])
                values.append([x_int + 1, y, in_top])
        return values
