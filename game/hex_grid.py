class HexGrid:
    def __init__(self):
        self.directions = [
            (1, 0), (1, -1), (0, -1),
            (-1, 0), (-1, 1), (0, 1)
        ]

    def get_neighbors(self, q, r):
        return [(q + dq, r + dr) for dq, dr in self.directions]

    def distance(self, q1, r1, q2, r2):
        return (abs(q1 - q2) + 
                abs(q1 + r1 - q2 - r2) + 
                abs(r1 - r2)) // 2

    def is_adjacent(self, q1, r1, q2, r2):
        return self.distance(q1, r1, q2, r2) == 1