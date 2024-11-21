class Automata:
    def __init__(self, estados, alfabeto, transiciones, inicio, finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.inicio = inicio
        self.finales = finales
        self.estado_actual = inicio
    
    def avanzar(self, entrada):
        if entrada in self.transiciones[self.estado_actual]:
            self.estado_actual = self.transiciones[self.estado_actual][entrada]
            print(f"Estado actualizado: {self.estado_actual}.")
        else:
            print("Entrada no válida para el estado actual.")

    def es_estado_final(self):
        return self.estado_actual in self.finales