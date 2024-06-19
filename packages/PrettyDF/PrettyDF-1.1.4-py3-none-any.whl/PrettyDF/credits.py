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

def show_credits():
    while True:
        try:
            Screen.wrapper(_credits)
            sys.exit(0)
        except ResizeScreenError:
            pass

if __name__ == "__main__":
    show_credits()
