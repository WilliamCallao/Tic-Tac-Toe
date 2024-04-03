from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

class GameUI:
    def __init__(self, root):
        self.setup_window(root)
        self.load_images()
        self.setup_canvas()
        self.initialize_game_variables()
        self.create_buttons()
        self.create_texts()
        self.add_transferred_buttons()

    def setup_window(self, root):
        """Configura la ventana principal."""
        self.window = root
        self.window.geometry("800x550")
        self.window.configure(bg="black")

    def load_images(self):
        """Carga las imágenes necesarias para la interfaz del juego."""
        self.background_image = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.image_x = PhotoImage(file=self.relative_to_assets("button_9.png"))
        self.image_o = PhotoImage(file=self.relative_to_assets("button_10.png"))
        self.image_empty = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.jugar_de_nuevo = PhotoImage(file=self.relative_to_assets("jugar_de_nuevo.png"))
        self.place_circulo = PhotoImage(file=self.relative_to_assets("place_circulo.png"))
        self.place_cruz = PhotoImage(file=self.relative_to_assets("place_cruz.png"))

    def setup_canvas(self):
        """Inicializa el canvas."""
        self.canvas = Canvas(self.window, bg="black", height=550, width=800, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

    def initialize_game_variables(self):
        """Inicializa las variables del juego."""
        self.score_player1 = 0
        self.score_player2 = 0
        self.buttons = []

    def relative_to_assets(self, path: str) -> Path:
        """Devuelve la ruta absoluta del archivo dado relativo a la carpeta de assets."""
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path("D:/Proyectos/IA/assets")
        return ASSETS_PATH / Path(path)

    def create_buttons(self):
        """Crea los botones del tablero."""
        button_positions = [
            (266.0, 140.0), (361.0, 140.0), (454.0, 140.0),
            (266.0, 235.0), (361.0, 235.0), (454.0, 235.0),
            (266.0, 330.0), (361.0, 330.0), (454.0, 330.0)
        ]
        for x, y in button_positions:
            button = Button(image=self.image_empty, borderwidth=0, highlightthickness=0, relief="flat")
            button.place(x=x, y=y, width=80.0, height=80.0)
            self.buttons.append(button)
            self.canvas.create_window(x, y, anchor="nw", window=button, width=80, height=80)

    def create_texts(self):
        """Crea los textos para la puntuación y nombres de los jugadores."""
        self.text_score_player1 = self.canvas.create_text(
            92.0, 275.0, anchor="nw", text=str(self.score_player1), fill="#FFFFFF", font=("Inter ExtraBold", 46 * -1)
        )
        self.text_score_player2 = self.canvas.create_text(
            677.0, 275.0, anchor="nw", text=str(self.score_player2), fill="#FFFFFF", font=("Inter ExtraBold", 46 * -1)
        )
        # Otros textos
        self.canvas.create_text(74.0, 249.0, anchor="nw", text="SCORE", fill="#FFFFFF", font=("Inter ExtraBold", 19 * -1))
        self.canvas.create_text(70.0, 226.0, anchor="nw", text="Player 1", fill="#FFFFFF", font=("Inter ExtraBold", 19 * -1))
        self.canvas.create_text(655.0, 226.0, anchor="nw", text="Player 2", fill="#FFFFFF", font=("Inter ExtraBold", 19 * -1))
        self.canvas.create_text(659.0, 249.0, anchor="nw", text="SCORE", fill="#FFFFFF", font=("Inter ExtraBold", 19 * -1))

    def add_transferred_buttons(self):
        """Añade botones adicionales a la interfaz."""
        Button(self.window, image=self.jugar_de_nuevo, borderwidth=0, highlightthickness=0, relief="flat").place(x=304.0, y=465.0, width=193.0, height=38.0)
        Button(self.window, image=self.place_circulo, borderwidth=0, highlightthickness=0, relief="flat").place(x=83.0, y=133.0, width=50.0, height=50.0)
        Button(self.window, image=self.place_cruz, borderwidth=0, highlightthickness=0, relief="flat").place(x=668.0, y=133.0, width=50.0, height=50.0)

    def reset_game(self):
        """Reinicia el juego limpiando el tablero."""
        for button in self.buttons:
            button.config(image=self.image_empty)
        # Aquí se reiniciaría también la lógica del juego, si fuera necesario.