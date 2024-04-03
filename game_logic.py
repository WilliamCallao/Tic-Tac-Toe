from tkinter import messagebox

class GameLogic:
    def __init__(self, ui):
        self.ui = ui
        self.current_player = "X"
        self.board = [""] * 9

        for i, button in enumerate(self.ui.game_buttons):  # Asegúrate de que ahora se llamen game_buttons en tu clase UI
            button.config(command=lambda i=i: self.button_click(i))

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.update_status_message()  # Opcional: Actualiza un mensaje de estado si tienes uno

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
            self.ui.game_buttons[i]["image"] = self.ui.cross_image if self.current_player == "X" else self.ui.circle_image
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Fin del Juego", f"¡El ganador es {winner}!" if winner != "Empate" else "¡Es un empate!")
                self.update_scores(winner)
                self.reset_game()
            else:
                self.switch_player()

    def update_scores(self, winner):
        if winner == "X":
            self.ui.player1_score += 1
            self.ui.game_canvas.itemconfig(self.ui.player1_score_text, text=str(self.ui.player1_score))
        elif winner == "O":
            self.ui.player2_score += 1
            self.ui.game_canvas.itemconfig(self.ui.player2_score_text, text=str(self.ui.player2_score))
        # No actualiza puntuaciones en caso de empate, pero podrías manejarlo de manera diferente si lo deseas

    def reset_game(self):
        self.board = [""] * 9
        for button in self.ui.game_buttons:
            button.config(image=self.ui.empty_slot_image)
        self.current_player = "X"  # O podrías decidir quién comienza el siguiente juego de alguna manera

    def update_status_message(self):
        # Opcional: Actualiza un mensaje en la UI para indicar quién es el próximo jugador
        pass
