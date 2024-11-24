import tkinter as tk
from automata import Automata
from tkinter import ttk
from pokemon import Pokemon

automata = Automata(
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
pokemon_aliados = [
    Pokemon("Pikachu", "Electrico", ["Impactrueno", "Curar"], 100, 50, 30, ["Tierra"], "Aliado"),
    Pokemon("Bulbasaur", "Planta", ["Latigo Cepa", "Curar"], 100, 50, 30, ["Fuego"], "Aliado")
]
pokemon_enemigo = [
    Pokemon("Charmander", "Fuego", ["Lanzallamas", "Curar"], 100, 50, 30, ["Agua"], "Enemigo")
]

root = tk.Tk()
root.geometry("800x600")
root.title("Poketower - Autómata")
width = 800
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

root.geometry(f"{width}x{height}+{x}+{y}")

# Header
header = tk.Frame(root, bg="lightblue", height=100)
header.pack(fill=tk.X, side=tk.TOP)

# Canva
canvas = tk.Canvas(root, bg="white", height=400)
canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Footer
footer = tk.Frame(root, bg="lightgray", height=50)
footer.pack(fill=tk.X, side=tk.BOTTOM)

tabla = None
global pokemon_seleccionado
global enemigo_seleccionado

def limpiar_footer():
    for widget in footer.winfo_children():
        widget.destroy()

def seleccionar_pokemon(pokemon):
    global pokemon_seleccionado
    pokemon_seleccionado = pokemon
    avanzar_estado("SP")

def seleccionar_enemigo(pokemon):
    global enemigo_seleccionado
    enemigo_seleccionado = pokemon
    print(f"Enemigo seleccionado: {enemigo_seleccionado.nombre}")
    avanzar_estado("SO")  # Avanza al siguiente estado automáticamente

def renderizar_estado_actual():
    """
    Esta función renderiza widgets específicos dependiendo del estado actual del autómata.
    """

    estado_actual = automata.estado_actual

    match estado_actual:
        case "q0":
            boton_sic = tk.Button(footer, text="Iniciar Combate (SIC)", command=lambda: avanzar_estado("SIC"))
            boton_sic.pack(pady=5)
        case "q1":
            limpiar_footer()
            for pokemon in pokemon_aliados:
                boton_sp = tk.Button(
                    footer, 
                    text=f"Seleccionar {pokemon.nombre} ({pokemon.tipo})",
                    command=lambda pokemon=pokemon: seleccionar_pokemon(pokemon)
                )
                boton_sp.pack(pady=5, anchor="center")
        case "q2":
            limpiar_footer()
            boton_sab = tk.Button(footer, text="Usar Ataque Básico (SAB)", command=lambda: avanzar_estado("SAB"))
            boton_sho = tk.Button(footer, text=f"Usar {pokemon_seleccionado.habilidades[0]} (SHO)", command=lambda: avanzar_estado("SHO"))
            boton_shd = tk.Button(footer, text=f"Usar {pokemon_seleccionado.habilidades[1]} (SHD)", command=lambda: avanzar_estado("SHD"))
            boton_sab.pack(pady=5)
            boton_sho.pack(pady=5)
            boton_shd.pack(pady=5)
        case "q3" | "q4" | "q5":
            limpiar_footer()
            for pokemon in pokemon_enemigo:
                boton_sp = tk.Button(
                    footer,
                    text=f"Atacar a {pokemon.nombre} ({pokemon.tipo})",
                    command=lambda pokemon=pokemon: seleccionar_enemigo(pokemon)
                )
                boton_sp.pack(pady=5, anchor="center")
        case "q6":
            limpiar_footer()
            boton_so = tk.Button(footer, text="Seleccionar Objetivo (SO)", command=lambda: avanzar_estado("SO"))
            boton_so.pack(pady=5)
        case "q7":
            limpiar_footer()
            boton_ft = tk.Button(footer, text="Finalizar Turno (FT)", command=lambda: avanzar_estado("FT"))
            boton_sn = tk.Button(footer, text="Siguiente Nivel (SN)", command=lambda: avanzar_estado("SN"))
            boton_fj = tk.Button(footer, text="Finalizar Juego (FJ)", command=lambda: avanzar_estado("FJ"))
        case "q8":
            limpiar_footer()
            boton_sft = tk.Button(footer, text="Finalizar Turno (SFT)", command=lambda: avanzar_estado("SFT"))
            boton_sft.pack(pady=5)
        
            boton_ssn = tk.Button(footer, text="Siguiente Nivel (SSN)", command=lambda: avanzar_estado("SSN"))
            boton_ssn.pack(pady=5)

            boton_fj = tk.Button(footer, text="Finalizar Juego (FJ)", command=lambda: avanzar_estado("FJ"))
            boton_fj.pack(pady=5)
        case "q11":
            limpiar_footer()
            mensaje_label = tk.Label(footer, text="¡Felicidades! Has completado el juego.", font=("Arial", 14), fg="green")
            mensaje_label.pack(pady=10)

def avanzar_estado(simbolo):
    """
    Intenta avanzar el autómata al siguiente estado dependiendo del símbolo dado.
    """
    if automata.avanzar(simbolo):
        renderizar_estado_actual()
        tabla.item(tabla.get_children()[0], values=(simbolo, automata.estado_anterior, automata.estado_actual))

    else:
        print(f"✖ No se puede avanzar con el símbolo '{simbolo}'.")
        mensaje_label = tk.Label(root, text=f"✖ No se puede avanzar con el símbolo '{simbolo}'.", font=("Arial", 10), fg="red")
        mensaje_label.pack(pady=10)

def mostrar_tabla():
    """
    Muestra la tabla con el historial del autómata y el botón para avanzar manualmente.
    """
    global tabla
    if tabla is None:
        tabla = ttk.Treeview(header, columns=("columna1", "columna2", "columna3"), show="headings", height=1)

        tabla.heading("columna1", text="Simbolo Recibido") 
        tabla.heading("columna2", text="Estado Anterior")
        tabla.heading("columna3", text="Estado Actual")

        tabla.column("columna1", width=150, anchor="center")
        tabla.column("columna2", width=150, anchor="center")
        tabla.column("columna3", width=250, anchor="center")

        estado_actual = f"{automata.estado_actual}: {automata.estados[automata.estado_actual]}"
        tabla.insert("", "end", values=("N/A", "N/A", estado_actual))

        tabla.pack(fill=tk.X, expand=False, pady=10)

mostrar_tabla()
renderizar_estado_actual()

root.mainloop()