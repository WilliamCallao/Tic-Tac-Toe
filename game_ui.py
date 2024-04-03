from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
from tkinter import Label

class TicTacToeUI:
    def __init__(self, root):
        self.main_window = root
        self.main_window.geometry("800x550")
        self.main_window.configure(bg="black")

        # Cargando imágenes para la interfaz de usuario
        self.bg_image = PhotoImage(file=self.relative_to_assets("bg_image.png"))
        self.cross_image = PhotoImage(file=self.relative_to_assets("cross_image.png"))
        self.circle_image = PhotoImage(file=self.relative_to_assets("circle_image.png"))
        self.empty_slot_image = PhotoImage(file=self.relative_to_assets("empty_slot_image.png"))

        self.restart_button_image = PhotoImage(file=self.relative_to_assets("restart_button_image.png"))
        self.circle_place_holder_image = PhotoImage(file=self.relative_to_assets("circle_place_holder_image.png"))
        self.cross_place_holder_image = PhotoImage(file=self.relative_to_assets("cross_place_holder_image.png"))
        
        # Inicializando puntuaciones
        self.player1_score = 0
        self.player2_score = 0
        
        # Configurando el canvas
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
        
    def relative_to_assets(self, path: str) -> Path:
        current_folder = Path(__file__).parent
        assets_folder = current_folder / Path("D:/Proyectos/IA/assets")
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
                image=self.empty_slot_image,
                borderwidth=0,
                highlightthickness=0,
                relief="flat"
            )
            game_button.place(x=x, y=y, width=80.0, height=80.0)
            self.game_buttons.append(game_button)
            self.game_canvas.create_window(x, y, anchor="nw", window=game_button, width=80, height=80)

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
        # Reiniciar el tablero
        for button in self.game_buttons:
            button.config(image=self.empty_slot_image)

        # Restablecer los puntajes
        self.player1_score = 0
        self.player2_score = 0

        # Actualizar el texto de los puntajes en la interfaz
        self.game_canvas.itemconfig(self.player1_score_text, text=str(self.player1_score))
        self.game_canvas.itemconfig(self.player2_score_text, text=str(self.player2_score))


