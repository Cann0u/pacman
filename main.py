import mazegen
from render import Render


def main():
    print("Hello from pacman!")
    maze = mazegen.MazeGenerator(
        mazegen.MazeConfig(
            height=25,
            width=25,
            entry_coord=(0, 0),
            exit_coord=(1, 0),
            output_file="output.txt",
        )
    )
    maze.generate()
    render = Render()
    for line in maze.maze:
        print(" ".join(line))
    render.on_exec()

    from game.algo import Algo
    algo = Algo(maze.maze)
    print(algo.next_move((1,1), (2,1)))


if __name__ == "__main__":
    main()
