
def hello():
    import os 
    name = os.popen("whoami").read().strip()
    print(f"Hello {name}")

def table(dict):
    import pandas as pd
    from tabulate import tabulate

    df = pd.DataFrame(dict)
    structure = tabulate(df, headers='keys', tablefmt='psql')
    print(structure)

def visual(dict, style, **kwargs):
    import pandas as pd
    import warnings
    import matplotlib.pyplot as plt

    try:
        warnings.filterwarnings("ignore")

        df = pd.DataFrame(dict)
        
        if df.empty:
            raise ValueError("Empty Dataframe. Please add some values.")
        
        if style not in ['line', 'bar', 'barh', 'hist', 'box', 'area', 'scatter']:
            raise ValueError(f"Invalid plot type '{style}'. Supported types: 'line', 'bar', 'barh', 'hist', 'box', 'area', 'scatter'.")
        
        plot = df.plot(kind=style, **kwargs)
        
        if 'xlabel' not in kwargs:
            plt.xlabel("Index")
        if 'ylabel' not in kwargs:
            plt.ylabel("Values")
        if 'title' not in kwargs:
            plt.title(f"{style.capitalize()} Plot")
        
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


def credits():
    import sys
    from pyfiglet import Figlet
    from asciimatics.effects import Scroll, Mirage, Wipe, Cycle, Matrix, Stars, Print
    from asciimatics.particles import DropScreen
    from asciimatics.renderers import FigletText, SpeechBubble
    from asciimatics.scene import Scene
    from asciimatics.screen import Screen
    from asciimatics.exceptions import ResizeScreenError

    def _credits(screen):
        scenes = []

        text = Figlet(font="banner", width=200).renderText("PrettyDF")
        width = max([len(x) for x in text.split("\n")])

        effects = [
            Matrix(screen, stop_frame=200),
            Mirage(screen, FigletText("PrettyDF"), screen.height // 2 - 3, Screen.COLOUR_GREEN, start_frame=100, stop_frame=200),
            Wipe(screen, start_frame=150),
            Cycle(screen, FigletText("PrettyDF"), screen.height // 2 - 3, start_frame=200)
        ]
        scenes.append(Scene(effects, 250, clear=False))

        effects = [
            Scroll(screen, 3),
            Mirage(screen, FigletText("Crafted with"), screen.height, Screen.COLOUR_GREEN),
            Mirage(screen, FigletText("love by:"), screen.height + 8, Screen.COLOUR_GREEN),
            Mirage(screen, FigletText("Dawn Saju"), screen.height + 16, Screen.COLOUR_GREEN)
        ]
        scenes.append(Scene(effects, (screen.height + 24) * 3))

        colours = [Screen.COLOUR_RED, Screen.COLOUR_GREEN]

        effects = [
            Cycle(screen, FigletText("PrettyDF", font='big'), screen.height // 2 - 8, stop_frame=100),
            Stars(screen, (screen.width + screen.height) // 2, stop_frame=100),
            DropScreen(screen, 200, start_frame=100)
        ]
        scenes.append(Scene(effects, 300))

        effects = [
            Print(screen, SpeechBubble("Press 'X' to exit."), screen.height // 2 - 1, attr=Screen.A_BOLD)
        ]
        scenes.append(Scene(effects, -1))

        screen.play(scenes, stop_on_resize=True)

    while True:
        try:
            Screen.wrapper(_credits)
            sys.exit(0)
        except ResizeScreenError:
            pass