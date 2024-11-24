import tkinter as tk
from tkinter import ttk
from automata import Automata
from pokemon import Pokemon

class PoketowerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Poketower - Autómata")
        self.root.geometry("800x600")

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
                "q7": {"SFT": "q8", "SSN": "q9", "FJ": "q10"},
                "q8": {"SIT": "q1"},
                "q9": {"SIT": "q1"},
                "q10": {}
            },
            inicio="q0",
            finales={"q11"}
        )

        self.pokemon_aliados = [
            Pokemon("Pikachu", "Electrico", ["Impactrueno", "Curar"], 100, 50, 30, ["Tierra"], "Aliado"),
            Pokemon("Bulbasaur", "Planta", ["Latigo Cepa", "Curar"], 100, 50, 30, ["Fuego"], "Aliado")
        ]
        self.pokemon_enemigo = [
            Pokemon("Charmander", "Fuego", ["Lanzallamas", "Curar"], 100, 50, 30, ["Agua"], "Enemigo")
        ]

        # Variables de estado
        self.pokemon_seleccionado = None
        self.enemigo_seleccionado = None

        # Widgets
        self.vida_pokemon_aliado = None
        self.vida_pokemon_enemigo = None
        self.tabla = None

        # Diseño
        self.header = tk.Frame(root, bg="lightblue", height=100)
        self.header.pack(fill=tk.X, side=tk.TOP)

        self.canvas = tk.Canvas(root, bg="white", height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer = tk.Frame(root, bg="lightgray", height=50)
        self.footer.pack(fill=tk.X, side=tk.BOTTOM)

        # Renderizar contenido inicial
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

    def renderizar_estado_actual(self):
        estado_actual = self.automata.estado_actual
        self.limpiar_footer()

        match estado_actual:
            case "q0":
                # Botón de iniciar combate con un estilo más destacado
                boton_sic = tk.Button(
                    self.footer,
                    text="Iniciar Combate (SIC)",
                    command=lambda: self.avanzar_estado("SIC")
                )
                boton_sic.pack(pady=10)

                # Contenedor para los Pokémon aliados y enemigos
                marco_pokemones = tk.Frame(self.canvas, bg="white")
                marco_pokemones.pack(fill=tk.BOTH, expand=True, pady=10)

                # Mostrar la vida de todos los Pokémon aliados en un marco separado
                marco_aliados = tk.LabelFrame(marco_pokemones, text="Pokemones Aliados", font=("Arial", 14, "bold"), bg="#d4f1f4", padx=10, pady=10)
                marco_aliados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

                for pokemon in self.pokemon_aliados:
                    etiqueta_aliado = tk.Label(
                        marco_aliados,
                        text=f"{pokemon.nombre} ({pokemon.tipo}): {pokemon.vida} HP",
                        font=("Arial", 12),
                        bg="#d4f1f4",
                        anchor="w",
                        padx=10
                    )
                    etiqueta_aliado.pack(fill=tk.X, pady=5)

                # Mostrar la vida de todos los Pokémon enemigos en otro marco
                marco_enemigos = tk.LabelFrame(marco_pokemones, text="Pokemones Enemigos", font=("Arial", 14, "bold"), bg="#f8d7da", padx=10, pady=10)
                marco_enemigos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

                for pokemon in self.pokemon_enemigo:
                    self.vida_pokemon_enemigo = tk.Label(
                        marco_enemigos,
                        text=f"{pokemon.nombre} ({pokemon.tipo}): {pokemon.vida} HP",
                        font=("Arial", 12),
                        bg="#f8d7da",
                        anchor="w",
                        padx=10
                    )
                    self.vida_pokemon_enemigo.pack(fill=tk.X, pady=5)

            case "q1":
                for pokemon in self.pokemon_aliados:
                    boton_sp = tk.Button(
                        self.footer,
                        text=f"Seleccionar {pokemon.nombre} ({pokemon.tipo})",
                        command=lambda pokemon=pokemon: self.seleccionar_pokemon(pokemon)
                    )
                    boton_sp.pack(pady=5)

            case "q2":
                self.limpiar_footer()
                boton_sab = tk.Button(self.footer, text="Usar Ataque Básico (SAB)", command=lambda: self.avanzar_estado("SAB"))
                boton_sho = tk.Button(self.footer, text=f"Usar {self.pokemon_seleccionado.habilidades[0]} (SHO)", command=lambda: self.avanzar_estado("SHO"))
                boton_shd = tk.Button(self.footer, text=f"Usar {self.pokemon_seleccionado.habilidades[1]} (SHD)", command=lambda: self.avanzar_estado("SHD"))
                boton_sab.pack(pady=5)
                boton_sho.pack(pady=5)
                boton_shd.pack(pady=5)

            case "q3" | "q4" | "q5":
                for pokemon in self.pokemon_enemigo:
                    boton_se = tk.Button(
                        self.footer,
                        text=f"Atacar a {pokemon.nombre} ({pokemon.tipo})",
                        command=lambda pokemon=pokemon: self.seleccionar_enemigo(pokemon)
                    )
                    boton_se.pack(pady=5)

            case "q6":
                self.limpiar_footer()
                boton_eah = tk.Button(self.footer, text="Ejecutar Ataque o Habilidad (EAH)", command=lambda: self.avanzar_estado("EAH"))
                boton_eah.pack(pady=5)

            case "q7":
                if self.enemigo_seleccionado:
                    self.enemigo_seleccionado.vida -= self.pokemon_seleccionado.ataque
                    self.vida_pokemon_enemigo.config(
                        text=f"{self.enemigo_seleccionado.nombre} ({self.enemigo_seleccionado.tipo}): {self.enemigo_seleccionado.vida} HP"
                    )
                    todos_derrotados = all(pokemon.vida <= 0 for pokemon in self.pokemon_enemigo)

                    if todos_derrotados:
                        boton_sn = tk.Button(self.footer, text="Siguiente Nivel (SSN)", command=lambda: self.avanzar_estado("SSN"))
                        boton_sn.pack(pady=5)
                    else:
                        boton_ft = tk.Button(self.footer, text="Finalizar Turno (SFT)", command=lambda: self.avanzar_estado("SFT"))
                        boton_ft.pack(pady=5)
                

    def avanzar_estado(self, simbolo):
        if self.automata.avanzar(simbolo):
            self.renderizar_estado_actual()
            self.tabla.item(self.tabla.get_children()[0], values=(simbolo, f"{self.automata.estado_anterior}: {self.automata.estados[self.automata.estado_anterior]}", f"{self.automata.estado_actual}: {self.automata.estados[self.automata.estado_actual]}"))

    def mostrar_tabla(self):
        if not self.tabla:
            self.tabla = ttk.Treeview(self.header, columns=("columna1", "columna2", "columna3"), show="headings", height=1)

            self.tabla.heading("columna1", text="Simbolo Recibido")
            self.tabla.heading("columna2", text="Estado Anterior")
            self.tabla.heading("columna3", text="Estado Actual")

            self.tabla.column("columna1", width=150, anchor="center")
            self.tabla.column("columna2", width=150, anchor="center")
            self.tabla.column("columna3", width=250, anchor="center")

            estado_actual = f"{self.automata.estado_actual}: {self.automata.estados[self.automata.estado_actual]}"
            self.tabla.insert("", "end", values=("N/A", "N/A", estado_actual))

            self.tabla.pack(fill=tk.X, expand=False, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = PoketowerApp(root)
    root.mainloop()