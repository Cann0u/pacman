import mazegen
import sys
from render import Render


def main():
    print("Hello from pacman!")
    if len(sys.argv) != 2:
        print("""To few argument, usage:
    uv run pac-man.py [config_file.json]""")
        return
    render = Render(sys.argv[1])
    render.on_exec()

    from game.algo import Algo
    algo = Algo(maze.maze)
    print(algo.next_move((1,1), (2,1)))


if __name__ == "__main__":
    main()
