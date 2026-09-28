from collections import deque


class Algo:
    def __init__(self, map):
        self.map = map

    def is_walkable(self, x, y):
        maze = self.map.maze
        if y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]):
            return False
        return maze[y][x] != "#"

    def distance_map(self, start):
        dist = {start: 0}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in dist and self.is_walkable(*n):
                    dist[n] = dist[(x, y)] + 1
                    queue.append(n)
        return dist

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

    def flee_target(self, ghost_pos, pacman_pos):
        from_pac = self.distance_map(pacman_pos)
        from_ghost = self.distance_map(ghost_pos)

        best, best_key = None, None
        for cell, gd in from_ghost.items():
            pd = from_pac.get(cell)
            if pd is None or gd >= pd:
                continue
            key = (pd, -gd)
            if best_key is None or key > best_key:
                best, best_key = cell, key
        if best is not None:
            return best
        x, y = ghost_pos
        neighbors = [
            n
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if self.is_walkable(*n)
        ]
        return max(
            neighbors, key=lambda n: from_pac.get(n, 0), default=ghost_pos
        )

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
