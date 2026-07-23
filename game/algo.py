from math import inf


class Algo:
    def __init__(self, map):
        self.map = map

    def is_walkable(self, x, y):
        maze = self.map.maze
        if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
            return False
        return maze[y][x] != "#"

    def next_move(self, ghost_pos, target_pos, last_direction=None):
        g_x, g_y = ghost_pos
        t_x, t_y = target_pos

        directions = {
            "up": (g_x, g_y - 1),
            "down": (g_x, g_y + 1),
            "right": (g_x + 1, g_y),
            "left": (g_x - 1, g_y),
        }
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}

        best_direction, best_dist = None, inf

        for direction, (n_x, n_y) in directions.items():
            if last_direction and direction == opposite[last_direction]:
                continue
            if not self.is_walkable(n_x, n_y):
                continue

            dist_sq = (n_x - t_x) ** 2 + (n_y - t_y) ** 2
            if dist_sq < best_dist:
                best_dist = dist_sq
                best_direction = direction

        return best_direction
