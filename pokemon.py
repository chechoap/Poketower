class Pokemon:
    def __init__(self, nombre, tipo, habilidades, vida, ataque, defensa, debilidades, equipo):
        self.nombre = nombre
        self.tipo = tipo
        self.habilidades = habilidades
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.debilidades = debilidades  
        self.esta_muerto = False
        self.equipo = equipo

    def recibir_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.esta_muerto = True
            print(f"{self.nombre} ha muerto.")

    def usar_habilidad(self, habilidad, objetivo):
        if habilidad in self.habilidades:
            print(f"{self.nombre} usa {habilidad} contra {objetivo.nombre}")
        else:
            print(f"{self.nombre} no tiene esa habilidad.")

    def __str__(self):
        return (f"Nombre: {self.nombre}\n"
                f"Tipo: {self.tipo}\n"
                f"Habilidades: {', '.join([habilidad for habilidad in self.habilidades])}\n"
                f"Vida: {self.vida}\n"
                f"Ataque: {self.ataque}\n"
                f"Defensa: {self.defensa}\n"
                f"Debilidades: {', '.join([debilidad for debilidad in self.debilidades])}")
