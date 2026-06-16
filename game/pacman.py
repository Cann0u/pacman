from entity import Entity


class Pacman(Entity):
    def __init__(self, pos, coord, sprite, player: int):
        super().__init__(pos, coord, sprite)
        self.player = player
        self.score = 0

    def eat_pacgum(self, map):
        s_x, s_y = self.pos
        if map[s_x][s_y] == "p":
            self.score += 10
            map[s_x][s_y] = "*"
