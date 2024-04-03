from tkinter import Tk, Canvas, Button, PhotoImage, Label, messagebox
from pathlib import Path

class TicTacToeUI:
    def __init__(self, root):
        self.main_window = root
        self.main_window.geometry("800x550")
        self.main_window.configure(bg="black")

        # Cargar imágenes para la interfaz de usuario
        self.bg_image = PhotoImage(file=self.relative_to_assets("bg_image.png"))
        self.cross_image = PhotoImage(file=self.relative_to_assets("cross_image.png"))
        self.circle_image = PhotoImage(file=self.relative_to_assets("circle_image.png"))
        self.empty_slot_image = PhotoImage(file=self.relative_to_assets("empty_slot_image.png"))
        self.restart_button_image = PhotoImage(file=self.relative_to_assets("restart_button_image.png"))
        self.circle_place_holder_image = PhotoImage(file=self.relative_to_assets("circle_place_holder_image.png"))
        self.cross_place_holder_image = PhotoImage(file=self.relative_to_assets("cross_place_holder_image.png"))

        # Inicializar puntuaciones
        self.player1_score = 0
        self.player2_score = 0

        # Configurar el canvas
        self.game_canvas = Canvas(
            self.main_window,
            bg="black",
            height=550,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.game_canvas.place(x=0, y=0)
        self.game_canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.game_buttons = []
        self.create_game_buttons()
        self.create_score_texts()
        self.add_sidebar_buttons()

        # Integrar la lógica del juego
        self.game_logic = GameLogic(self)

    def relative_to_assets(self, path: str) -> Path:
        current_folder = Path(__file__).parent
        assets_folder = current_folder / Path("assets")  # Modificado para relativo
        return assets_folder / Path(path)

    def create_game_buttons(self):
        positions = [
            (266.0, 140.0), (361.0, 140.0), (454.0, 140.0),
            (266.0, 235.0), (361.0, 235.0), (454.0, 235.0),
            (266.0, 330.0), (361.0, 330.0), (454.0, 330.0)
        ]
        for position in positions:
            x, y = position
            game_button = Button(
                self.main_window, image=self.empty_slot_image, borderwidth=0,
                highlightthickness=0, relief="flat",
                command=lambda pos=position: self.game_logic.button_click(positions.index(pos))
            )
            game_button.place(x=x, y=y, width=80.0, height=80.0)
            self.game_buttons.append(game_button)

    def create_score_texts(self):
        self.game_canvas.create_text(
            74.0, 249.0, anchor="nw", text="SCORE", fill="#FFFFFF",
            font=("Inter ExtraBold", 19 * -1)
        )
        self.player1_score_text = self.game_canvas.create_text(
            92.0, 275.0, anchor="nw", text=str(self.player1_score), fill="#FFFFFF",
            font=("Inter ExtraBold", 46 * -1)
        )
        self.game_canvas.create_text(
            70.0, 226.0, anchor="nw", text="Player 1", fill="#FFFFFF",
            font=("Inter ExtraBold", 19 * -1)
        )
        self.game_canvas.create_text(
            655.0, 226.0, anchor="nw", text="Player 2", fill="#FFFFFF",
            font=("Inter ExtraBold", 19 * -1)
        )
        self.game_canvas.create_text(
            659.0, 249.0, anchor="nw", text="SCORE", fill="#FFFFFF",
            font=("Inter ExtraBold", 19 * -1)
        )
        self.player2_score_text = self.game_canvas.create_text(
            677.0, 275.0, anchor="nw", text=str(self.player2_score), fill="#FFFFFF",
            font=("Inter ExtraBold", 46 * -1)
        )

    def add_sidebar_buttons(self):
        restart_game_button = Button(
            self.main_window, image=self.restart_button_image, borderwidth=0,
            highlightthickness=0, command=self.reset_game, relief="flat"  # Aquí pasas self.reset_game directamente
        )
        restart_game_button.place(x=304.0, y=465.0, width=193.0, height=38.0)
        
        place_circle_image = Label(
            self.main_window, image=self.circle_place_holder_image, borderwidth=0,
            highlightthickness=0
        )
        place_circle_image.place(x=83.0, y=133.0, width=50.0, height=50.0)

        place_cross_image = Label(
            self.main_window, image=self.cross_place_holder_image, borderwidth=0,
            highlightthickness=0
        )
        place_cross_image.place(x=668.0, y=133.0, width=50.0, height=50.0)

    def reset_game(self):
        self.game_logic.reset_game_logic()
        for button in self.game_buttons:
            button.config(image=self.empty_slot_image)
        self.update_score_display()

    def update_score_display(self):
        self.game_canvas.itemconfig(self.player1_score_text, text=str(self.player1_score))
        self.game_canvas.itemconfig(self.player2_score_text, text=str(self.player2_score))

class GameLogic:
    def __init__(self, ui):
        self.ui = ui
        self.current_player = "X"
        self.board = [""] * 9

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for condition in win_conditions:
            if self.board[condition[0]] and self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]]:
                return self.board[condition[0]]
        if "" not in self.board:
            return "Empate"
        return None

    def button_click(self, i):
        if self.board[i] == "" and self.check_winner() is None:
            self.board[i] = self.current_player
            image = self.ui.cross_image if self.current_player == "X" else self.ui.circle_image
            self.ui.game_buttons[i].config(image=image)
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Fin del Juego", f"¡El ganador es {winner}!" if winner != "Empate" else "¡Es un empate!")
                self.update_scores(winner)
                self.ui.reset_game()
            else:
                self.switch_player()

    def update_scores(self, winner):
        if winner == "X":
            self.ui.player1_score += 1
            self.ui.game_canvas.itemconfig(self.ui.player1_score_text, text=str(self.ui.player1_score))
        elif winner == "O":
            self.ui.player2_score += 1
            self.ui.game_canvas.itemconfig(self.ui.player2_score_text, text=str(self.ui.player2_score))

    def reset_game_logic(self):
        self.board = [""] * 9
        self.current_player = "X"

if __name__ == "__main__":
    window = Tk()
    ui = TicTacToeUI(window)
    window.resizable(False, False)
    window.mainloop()
