import tkinter as tk
from automata import Automata
from tkinter import ttk

automata_poketower = Automata(
    estados={
        "q0": "Juego Iniciado",
        "q1": "Seleccionar Pokemon",
        "q2": "Pokemon Seleccionado",
        "q3": "Habilidad Seleccionada",
        "q4": "Ataque Basico Seleccionado",
        "q5": "Habilidad Ofensiva Seleccionada",
        "q6": "Habilidad Defensiva Seleccionada",
        "q7": "Objetivo Seleccionado",
        "q8": "Resolviendo Combate",
        "q9": "Cambio de Turno",
        "q10": "Siguiente Nivel",
        "q11": "Juego Completado"
    },
    alfabeto={
        "SIC": "Seleccionar Iniciar Combate",
        "SP": "Seleccionar Pokemon",
        "SH": "Seleccionar Habilidad",
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
        "q2": {"SH": "q3"},
        "q3": {"SAB": "q4", "SHO": "q5", "SHD": "q6"},
        "q4": {"SO": "q7"},
        "q5": {"SO": "q7"},
        "q6": {"SO": "q7"},
        "q7": {"EAH": "q8"},
        "q8": {"SFT": "q9", "FJ": "q11", "SSN": "q10"},
        "q9": {"SIT": "q1"},
        "q10": {"SIT": "q1"},
        "q11": {}
    },
    inicio="q0",
    finales={"q11"}
)

root = tk.Tk()
root.geometry("500x200")
root.title("Poketower - Autómata")

def limpiar_root():
    for widget in root.winfo_children():
        widget.destroy()

def mostrar_interfaz_inicial(mostrar):
    if mostrar:
        global entrada, mensaje_label, boton_validar
        entrada_label = tk.Label(root, text="Ingresa la secuencia (separada por comas):", font=("Arial", 12))
        entrada_label.pack(pady=20)

        entrada = tk.Entry(root, font=("Arial", 10), width='40')
        entrada.pack(pady=10)

        mensaje_label = tk.Label(root, text="", font=("Arial", 10))
        mensaje_label.pack(pady=10)

        boton_validar = tk.Button(root, text="Validar Entrada", command=validar_entrada_completa, font=("Arial", 12))
        boton_validar.pack(pady=10)
    else:
        limpiar_root()

def validar_entrada_completa():
    if not entrada.get():
        mensaje_label.config(text="✖ Debes ingresar una secuencia de entrada.", fg="red")
        return
    
    global entrada_usuario, lista_simbolos
    entrada_usuario = entrada.get()
    lista_simbolos = entrada_usuario.split(",")
    resultado = automata_poketower.validar_entrada(entrada_usuario)

    if resultado["exito"]:
        mensaje_label.config(text=f"✔ Cadena aceptada. Iniciando autómata...", fg="green")
        boton_validar.config(state="disabled")
        entrada.config(state="disabled")
        root.after(2000, lambda: cambiar_a_interfaz_principal())
    else:
        mensaje_label.config(text=f"✖ {resultado['mensaje']}", fg="red")

def avanzar_estado():
    automata_poketower.avanzar(lista_simbolos[0])

def cambiar_a_interfaz_principal():
    mostrar_interfaz_inicial(False)

    root.config(width=800, height=600)
    root.geometry("800x600")
    tabla = ttk.Treeview(root, columns=("columna1", "columna2", "columna3", "columna4"),show="headings", height=1)

    # Definir las columnas
    tabla.heading("columna1", text="Cadena")
    tabla.heading("columna2", text="Símbolo")
    tabla.heading("columna3", text="Estado Anterior")
    tabla.heading("columna4", text="Estado Actual")

    # Definir el ancho de las columnas
    tabla.column("columna1", width=150, anchor="center")
    tabla.column("columna2", width=150, anchor="center")
    tabla.column("columna3", width=150, anchor="center")
    tabla.column("columna4", width=150, anchor="center")
    tabla.insert("", "end", values=(entrada_usuario, lista_simbolos[0], automata_poketower.estado_anterior, automata_poketower.estado_actual))

    avanzar_boton = tk.Button(root, text="Avanzar", command=avanzar_estado, font=("Arial", 12))
    avanzar_boton.pack(pady=10)

    tabla.pack(fill=tk.X, expand=False, pady=10)

# Mostrar la interfaz inicial al iniciar la aplicación
mostrar_interfaz_inicial(True)

# Iniciar el loop principal
root.mainloop()