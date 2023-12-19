import tkinter as tk
import random
import time
from utiles import *

class FPetrisGUI:
    def __init__(self, master):
        self.master = master
        master.title("FPetris")        
        master.resizable(False, False)

        self.ancho_tablero = 10
        self.alto_tablero = 20
        self.tam_casilla = 30
        self.retardo = 500
        self.retardo_min = 100

        self.tablero_canvas = tk.Canvas(master, width=self.ancho_tablero * self.tam_casilla,
                               height=self.alto_tablero * self.tam_casilla)
        self.tablero_canvas.pack()

        self.piezas_y_colores = [
            ([[True, True, True, True]], 'magenta'),  # I shape
            ([[True, True, True], [False, True, False]], 'purple2'),  # T shape
            ([[False, True, True], [True, True, False]], 'green3'),  # S shape
            ([[True, True, False], [False, True, True]], 'red'),  # Z shape
            ([[True, True], [True, True]], 'yellow3'),  # O shape
            ([[True, True, True], [True, False, False]], 'orange'),  # L shape
            ([[True, True, True], [False, False, True]], 'blue')   # J shape
        ]

        self.siguientes_piezas_y_colores = self.piezas_y_colores[:] * 2


        self.tablero = inicializa_tablero(self.ancho_tablero, self.alto_tablero)

        # Atributos para puntuación y tiempo
        self.puntuacion = 0
        self.comienzo_time = time.time()
        
        # Crear el panel para puntuación y reloj
        color_fondo = "#fffff0" 
        self.panel_info = tk.Frame(master, bg=color_fondo)
        self.panel_info.pack(side="bottom", fill="x")

        # Etiqueta para la puntuación
        self.puntuacion_label = tk.Label(self.panel_info, text="Puntuación: 0", bg=color_fondo)
        self.puntuacion_label.pack(side="left")

        # Etiqueta para el reloj
        self.tiempo_label = tk.Label(self.panel_info, text="Tiempo: 00:00", bg=color_fondo)
        self.tiempo_label.pack(side="right")


        # Configurar el manejo de eventos de teclado
        self.master.bind("<Left>", self.mueve_izquierda)
        self.master.bind("<Right>", self.mueve_derecha)
        self.master.bind("<Down>", self.mueve_abajo)
        self.master.bind("<Up>", self.rota_pieza)

        # Iniciar actualización del reloj
        self.actualiza_reloj()

        self.cae_nueva_pieza()
        self.loop_juego()

    def actualiza_reloj(self):
        tiempo_juego = int(time.time() - self.comienzo_time)
        minutos, segundos = divmod(tiempo_juego, 60)
        self.tiempo_label.config(text=f"Tiempo: {minutos:02}:{segundos:02}")
        self.master.after(1000, self.actualiza_reloj)

    def actualiza_puntuacion(self, points):
        self.puntuacion += points
        self.puntuacion_label.config(text=f"Puntuación: {self.puntuacion}")

    # Métodos para manejar la entrada del teclado
    def mueve_izquierda(self, event):
        self.mueve_pieza(-1, 0)
        self.dibuja_tablero()

    def mueve_derecha(self, event):
        self.mueve_pieza(1, 0)
        self.dibuja_tablero()

    def mueve_abajo(self, event):
        self.mueve_pieza(0, 1)
        self.dibuja_tablero()

    def rota_pieza(self, event):
        # Rotar la pieza actual
        pieza_rotada = rota_pieza(self.pieza_actual)
        copia_pieza = self.pieza_actual
        self.pieza_actual = pieza_rotada

        # Verificar si la nueva posición es válida, si no, revertir
        if not posicion_valida(self.tablero, self.pieza_actual, self.pieza_actual_x, self.pieza_actual_y):
            self.pieza_actual = copia_pieza
        self.dibuja_tablero()

    def loop_juego(self):
        if not self.mueve_pieza(0, 1):
            coloca_pieza(self.tablero, self.pieza_actual, self.pieza_actual_x, self.pieza_actual_y, self.color_actual)        
            self.dibuja_tablero()
            self.elimina_lineas()
            if not self.cae_nueva_pieza(): # Devuelve falso si la pieza nueva no cabe
                self.tablero_canvas.create_text(self.ancho_tablero * self.tam_casilla / 2,
                                   self.alto_tablero * self.tam_casilla / 2,
                                   text="Game Over", font=("Helvetica", 34), fill="black")
                return # Se acaba el juego
        self.dibuja_tablero()
        self.master.after(self.retardo, self.loop_juego)

    def cae_nueva_pieza(self):
        siguiente_pieza = random.choice(self.siguientes_piezas_y_colores)
        self.siguientes_piezas_y_colores.remove(siguiente_pieza)
        if len(self.siguientes_piezas_y_colores) == 0:
            self.siguientes_piezas_y_colores = self.piezas_y_colores[:] * 2

        self.pieza_actual, self.color_actual = siguiente_pieza

        self.pieza_actual_x = int(self.ancho_tablero / 2) - int(len(self.pieza_actual[0]) / 2)
        self.pieza_actual_y = 0

        if not posicion_valida(self.tablero, self.pieza_actual, self.pieza_actual_x, self.pieza_actual_y):            
            return False
        self.dibuja_pieza_actual()
        return True

    def mueve_pieza(self, dx, dy):
        self.pieza_actual_x += dx
        self.pieza_actual_y += dy
        if posicion_valida(self.tablero, self.pieza_actual, self.pieza_actual_x, self.pieza_actual_y):
            return True
        self.pieza_actual_x -= dx
        self.pieza_actual_y -= dy
        return False

    def elimina_lineas(self):
        lineas_a_borrar = busca_filas_completas(self.tablero)                
        self.actualiza_puntuacion(len(lineas_a_borrar))
        self.retardo = self.retardo - 5*len(lineas_a_borrar) if self.retardo > self.retardo_min else self.retardo_min
        for num_fila in lineas_a_borrar:
            del self.tablero[num_fila]
            self.tablero.insert(0, [None] * self.ancho_tablero)
        self.dibuja_tablero()

    def dibuja_tablero(self):
        self.tablero_canvas.delete("all")
        for y, fila in enumerate(self.tablero):
            for x, color in enumerate(fila):
                if color != None: 
                    self.dibuja_celda(x, y, color)
        self.dibuja_pieza_actual()

    def dibuja_pieza_actual(self):
        for y, fila in enumerate(self.pieza_actual):
            for x, celda in enumerate(fila):
                if celda: # True si está ocupada
                    self.dibuja_celda(x + self.pieza_actual_x, y + self.pieza_actual_y, self.color_actual)

    def dibuja_celda(self, x, y, color):
        self.tablero_canvas.create_rectangle(x * self.tam_casilla, y * self.tam_casilla,
                                    (x + 1) * self.tam_casilla, (y + 1) * self.tam_casilla,
                                    fill=color, outline="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = FPetrisGUI(root)
    root.mainloop()
