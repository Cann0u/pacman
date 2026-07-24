from collections import deque


class Algo:
    def __init__(self, map):
        self.map = map

    def is_walkable(self, x, y):
        maze = self.map.maze
        if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
            return False
        return maze[y][x] != "#"

    def next_move(self, ghost_pos, target_pos, last_direction=None):
        path = self._shortest_path(ghost_pos, target_pos)
        if not path or len(path) < 2:
            return None

        n_x, n_y = path[1]
        g_x, g_y = ghost_pos
        dx, dy = n_x - g_x, n_y - g_y

        if dx == 1:
            return "right"
        if dx == -1:
            return "left"
        if dy == 1:
            return "down"
        if dy == -1:
            return "up"
        return None

    def _shortest_path(self, start, goal):
        if start == goal:
            return [start]

        visited = {start}
        queue = deque([[start]])
        best_path, best_dist = [start], self._dist(start, goal)

        while queue:
            path = queue.popleft()
            x, y = path[-1]
            for n_x, n_y in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (n_x, n_y) in visited or not self.is_walkable(n_x, n_y):
                    continue
                new_path = path + [(n_x, n_y)]
                if (n_x, n_y) == goal:
                    return new_path
                d = self._dist((n_x, n_y), goal)
                if d < best_dist:
                    best_dist = d
                    best_path = new_path
                visited.add((n_x, n_y))
                queue.append(new_path)

        return best_path

    @staticmethod
    def _dist(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
