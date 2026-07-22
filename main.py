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


if __name__ == "__main__":
    main()
