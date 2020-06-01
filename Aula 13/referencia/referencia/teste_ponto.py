class Point:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord

    def distance_to(self, other_point):
        dx = other_point.x - self.x
        dy = other_point.y - self.y
        return ((dx**2) + (dy**2)) ** 0.5

p1 = Point(4, 1)
p2 = Point(7, 5)
d = p1.distance_to(p2)
print('A distância de ({0}, {1}) a ({2}, {3}) é {4}'.format(p1.x, p1.y, p2.x, p2.y, d))
