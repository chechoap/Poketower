from automata import Automata

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

automata_poketower.avanzar("SIC")