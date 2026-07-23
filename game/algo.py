from abc import ABC, abstractmethod
from math import inf

class Algo:
    def __init__(self, map):
        self.map = map

    def next_move(self, ghost_pos, target_pos):
        g_x, g_y = ghost_pos
        t_x, t_y = target_pos

        directions = {
            "up": (g_x, g_y - 1),
            "down": (g_x, g_y + 1),
            "right": (g_x + 1, g_y),
            "left": (g_x - 1, g_y),
        }

        res = [None, inf]

        for direction, (g_x, g_y) in directions.items():
            dist_sq = (g_x - t_x) ** 2 + (g_y - t_y) ** 2
            print(direction, dist_sq)
            
            if dist_sq < res[1]:
                res[1] = dist_sq
                res[0] = direction
                
        return res[0]
