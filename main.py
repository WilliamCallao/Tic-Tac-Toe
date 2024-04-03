from tkinter import Tk
from game_ui import TicTacToeUI
from game_logic import GameLogic

if __name__ == "__main__":
    window = Tk()
    ui = TicTacToeUI(window)
    game_logic = GameLogic(ui)
    window.resizable(False, False)
    window.mainloop()
