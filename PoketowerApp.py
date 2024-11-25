import tkinter as tk
from tkinter import ttk
from automata import Automata
from pokemon import Pokemon
import random
import time

class PoketowerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poketower - Autómata")
        self.root.geometry("800x600")

        self.control_turno = "jugador"

        self.automata = Automata(
            estados={
                "q0": "Juego Iniciado",
                "q1": "Seleccionar Pokemon",
                "q2": "Pokemon Seleccionado",
                "q3": "Ataque Basico Seleccionado",
                "q4": "Habilidad Ofensiva Seleccionada",
                "q5": "Habilidad Defensiva Seleccionada",
                "q6": "Objetivo Seleccionado",
                "q7": "Resolviendo Combate",
                "q8": "Cambio de Turno",
                "q9": "Siguiente Nivel",
                "q10": "Juego Completado"
            },
            alfabeto={
                "SIC": "Seleccionar Iniciar Combate",
                "SP": "Seleccionar Pokemon",
                "SAB": "Seleccionar Ataque Basico",
                "SHO": "Seleccionar Habilidad Ofensiva",
                "SHD": "Seleccionar Habilidad Defensiva",
                "SO": "Seleccionar Objetivo",
                "EAH": "Ejecutar Ataque o Habilidad",
                "SFT": "Seleccionar Finalizar Turno",
                "SIT": "Seleccionar Iniciar Turno",
                "SSN": "Seleccionar Siguiente Nivel",
                "RJ": "Reiniciar Juego",
                "FJ": "Finalizar Juego"
            },
            transiciones={
                "q0": {"SIC": "q1"},
                "q1": {"SP": "q2"},
                "q2": {"SAB": "q3", "SHO": "q4", "SHD": "q5"},
                "q3": {"SO": "q6"},
                "q4": {"SO": "q6"},
                "q5": {"SO": "q6"},
                "q6": {"EAH": "q7"},
                "q7": {"SFT": "q8", "SSN": "q9", "FJ": "q10", "RJ": "q0"},
                "q8": {"SIT": "q1"},
                "q9": {"SIT": "q1"},
                "q10": {}
            },
            inicio="q0",
            finales={"q11"}
        )

        self.pokemon_aliados = [
            Pokemon("Pikachu", "Electrico", ["Impactrueno", "Curar"], 100, 50, 30, ["Tierra"], "Aliado"),
            #Pokemon("Bulbasaur", "Planta", ["Latigo Cepa", "Curar"], 100, 50, 30, ["Fuego"], "Aliado"),
        ]
        self.pokemon_enemigos = [
            Pokemon("Charmander", "Fuego", ["Lanzallamas", "Curar"], 100, 100, 30, ["Agua"], "Enemigo"),
            Pokemon("Squirtle", "Agua", ["Hidrobomba", "Curar"], 100, 100, 30, ["Planta"], "Enemigo"),
        ]

        self.pokemon_seleccionado = None
        self.enemigo_seleccionado = None

        self.vida_pokemon_aliado = None
        self.vida_pokemon_enemigo = None
        self.etiqueta_aliado = None
        self.etiqueta_enemigo = None
        self.marco_aliados = None
        self.marco_enemigos = None
        self.tabla = None
        self.nivel = 1

        self.header = tk.Frame(root, bg="lightblue", height=100)
        self.header.pack(fill=tk.X, side=tk.TOP)

        self.canvas = tk.Canvas(root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer = tk.Frame(root, bg="lightgray", height=50)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

        self.mostrar_tabla()
        self.renderizar_estado_actual()

    def limpiar_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

    def seleccionar_pokemon(self, pokemon):
        self.pokemon_seleccionado = pokemon
        self.avanzar_estado("SP")

    def seleccionar_enemigo(self, pokemon):
        self.enemigo_seleccionado = pokemon
        self.avanzar_estado("SO")
    
    def cambiar_turno(self):
        if self.control_turno == "jugador":
            self.control_turno = "enemigo"
        else:
            self.control_turno = "jugador"

    def proceso_turno_enemigo(self, paso):
        if paso == 1:
            pokemones_vivos = [pokemon for pokemon in self.pokemon_enemigos if pokemon.vida > 0]
            self.pokemon_seleccionado = random.choice(pokemones_vivos)
            self.avanzar_estado("SP")

            self.root.after(1000, lambda: self.proceso_turno_enemigo(2))

        elif paso == 2:
            self.habilidad_seleccionada = random.choice(self.pokemon_seleccionado.habilidades)
            self.avanzar_estado("SHO")

            self.root.after(1000, lambda: self.proceso_turno_enemigo(3))

        elif paso == 3:
            self.enemigo_seleccionado = random.choice(self.pokemon_aliados)
            self.avanzar_estado("SO")

            self.root.after(1000, lambda: self.proceso_turno_enemigo(4))

        elif paso == 4:
            self.avanzar_estado("EAH")

            self.root.after(1000, lambda: self.proceso_turno_enemigo(5))
        
        elif paso == 5:
            self.enemigo_seleccionado.vida -= self.pokemon_seleccionado.ataque
            self.actualizar_canvas()
            self.avanzar_estado("SFT")

            todos_enemigos_derrotados = all(pokemon.vida <= 0 for pokemon in self.pokemon_aliados)
            if todos_enemigos_derrotados:
                self.limpiar_footer()
                boton_fj = tk.Button(self.footer, text="Reiniciar Juego (RJ)", command=lambda: self.reiniciar_juego())
                boton_fj.pack(pady=5)

                boton_salir = tk.Button(self.footer, text="Salir del Juego (SJ)", command=lambda: self.root.destroy())
                boton_salir.pack(pady=5)
            else:
                self.root.after(1000, lambda: self.proceso_turno_enemigo(6))
        
        elif paso == 6:
            self.cambiar_turno()
            self.avanzar_estado("SIT")
    
    def reiniciar_juego(self):
        self.automata.estado_actual = "q0"
        self.nivel = 1
        self.pokemon_seleccionado = None
        self.enemigo_seleccionado = None
        self.control_turno = "jugador"
        self.renderizar_estado_actual()
        self.mostrar_tabla()
        self.resetear_pokemon()
        self.actualizar_canvas()

    def actualizar_canvas(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        marco_aliados = tk.LabelFrame(self.canvas, text="Pokémon Aliados", font=("Arial", 14, "bold"), bg="#d4f1f4", padx=10, pady=10)
        marco_aliados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=20)

        for pokemon in self.pokemon_aliados:
            if pokemon.vida > 0:
                etiqueta_aliado = tk.Label(
                    marco_aliados,
                    text=f"{pokemon.nombre} ({pokemon.tipo}): {pokemon.vida} HP",
                    font=("Arial", 12),
                    bg="#d4f1f4",
                    anchor="w",
                    padx=10
                )
                etiqueta_aliado.pack(fill=tk.X, pady=5)

        marco_enemigos = tk.LabelFrame(self.canvas, text="Pokémon Enemigos", font=("Arial", 14, "bold"), bg="#f8d7da", padx=10, pady=10)
        marco_enemigos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=20)

        for pokemon in self.pokemon_enemigos:
            if pokemon.vida > 0:
                etiqueta_enemigo = tk.Label(
                    marco_enemigos,
                    text=f"{pokemon.nombre} ({pokemon.tipo}): {pokemon.vida} HP",
                    font=("Arial", 12),
                    bg="#f8d7da",
                    anchor="w",
                    padx=10
                )
                etiqueta_enemigo.pack(fill=tk.X, pady=5)

    def resetear_pokemon(self):
        for pokemon in self.pokemon_aliados:
            pokemon.vida = 100

        for pokemon in self.pokemon_enemigos:
            pokemon.vida = 100

    def renderizar_estado_actual(self):
        estado_actual = self.automata.estado_actual

        match estado_actual:
            case "q0":
                self.limpiar_footer()
                if self.control_turno == "jugador":
                    self.actualizar_canvas()
                    boton_sic = tk.Button(self.footer, text="Iniciar Combate (SIC)", command=lambda: self.avanzar_estado("SIC"))
                    boton_sic.pack(pady=5)

            case "q1":
                self.limpiar_footer()

                if self.control_turno == "jugador":
                    for pokemon in self.pokemon_aliados:
                        if pokemon.vida > 0:
                            boton_sp = tk.Button(
                                self.footer,
                                text=f"Seleccionar {pokemon.nombre} ({pokemon.tipo})",
                                command=lambda pokemon=pokemon: self.seleccionar_pokemon(pokemon)
                            )
                            boton_sp.pack(pady=5)

            case "q2":
                self.limpiar_footer()
                if self.control_turno == "jugador":
                    boton_sab = tk.Button(self.footer, text="Usar Ataque Básico (SAB)", command=lambda: self.avanzar_estado("SAB"))
                    boton_sho = tk.Button(self.footer, text=f"Usar {self.pokemon_seleccionado.habilidades[0]} (SHO)", command=lambda: self.avanzar_estado("SHO"))
                    boton_shd = tk.Button(self.footer, text=f"Usar {self.pokemon_seleccionado.habilidades[1]} (SHD)", command=lambda: self.avanzar_estado("SHD"))
                    boton_sab.pack(pady=5)
                    boton_sho.pack(pady=5)
                    boton_shd.pack(pady=5)

            case "q3" | "q4" | "q5":
                self.limpiar_footer()
                if self.control_turno == "jugador":
                    for pokemon in self.pokemon_enemigos:
                        if pokemon.vida > 0:
                            boton_se = tk.Button(
                                self.footer,
                                text=f"Atacar a {pokemon.nombre} ({pokemon.tipo})",
                                command=lambda pokemon=pokemon: self.seleccionar_enemigo(pokemon)
                            )
                            boton_se.pack(pady=5)

            case "q6":
                self.limpiar_footer()
                if self.control_turno == "jugador":
                    boton_eah = tk.Button(self.footer, text="Ejecutar Ataque o Habilidad (EAH)", command=lambda: self.avanzar_estado("EAH"))
                    boton_eah.pack(pady=5)

            case "q7":
                self.limpiar_footer()

                if self.control_turno == "jugador":
                    if self.enemigo_seleccionado:
                        self.enemigo_seleccionado.vida -= self.pokemon_seleccionado.ataque
                        self.actualizar_canvas()
                        todos_enemigos_derrotados = all(pokemon.vida <= 0 for pokemon in self.pokemon_enemigos)

                        if todos_enemigos_derrotados:
                            boton_sn = tk.Button(self.footer, text="Siguiente Nivel (SSN)", command=lambda: self.avanzar_estado("SSN"))
                            boton_sn.pack(pady=5)

                            if self.nivel == 1:
                                self.limpiar_footer()
                                boton_fj = tk.Button(self.footer, text="Finalizar Juego (FJ)", command=lambda: self.avanzar_estado("FJ"))
                                boton_fj.pack(pady=5)
                        else:
                            boton_ft = tk.Button(self.footer, text="Finalizar Turno (SFT)", command=lambda: self.avanzar_estado("SFT"))
                            boton_ft.pack(pady=5)

            case "q8":
                if self.control_turno == "jugador":
                    self.limpiar_footer()
                    self.cambiar_turno()
                    self.avanzar_estado("SIT")
                    self.root.after(1000, lambda: self.proceso_turno_enemigo(1))

            case "q9":
                self.limpiar_footer()     
                self.resetear_pokemon()
                self.avanzar_estado("SIT")
                self.actualizar_canvas()
                self.nivel += 1

            case "q10":
                self.limpiar_footer()
                self.actualizar_canvas()
                self.canvas.destroy()
                juego_completado = tk.Label(self.root, text="¡Juego completado!", font=("Arial", 24, "bold"), bg="lightgray")
                juego_completado.pack(fill=tk.BOTH, expand=True)

    def avanzar_estado(self, simbolo):
        if self.automata.avanzar(simbolo):
            self.renderizar_estado_actual()
            self.tabla.item(self.tabla.get_children()[0], values=(simbolo, f"{self.automata.estado_anterior}: {self.automata.estados[self.automata.estado_anterior]}", f"{self.automata.estado_actual}: {self.automata.estados[self.automata.estado_actual]}", self.nivel))

    def mostrar_tabla(self):
        if not self.tabla:
            self.tabla = ttk.Treeview(self.header, columns=("columna1", "columna2", "columna3", "columna4"), show="headings", height=1)

            self.tabla.heading("columna1", text="Simbolo Recibido")
            self.tabla.heading("columna2", text="Estado Anterior")
            self.tabla.heading("columna3", text="Estado Actual")
            self.tabla.heading("columna4", text="Nivel")

            self.tabla.column("columna1", width=150, anchor="center")
            self.tabla.column("columna2", width=150, anchor="center")
            self.tabla.column("columna3", width=250, anchor="center")
            self.tabla.column("columna4", width=250, anchor="center")

            estado_actual = f"{self.automata.estado_actual}: {self.automata.estados[self.automata.estado_actual]}"
            self.tabla.insert("", "end", values=("N/A", "N/A", estado_actual, self.nivel))

            self.tabla.pack(fill=tk.X, expand=False, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PoketowerApp(root)
    root.mainloop()