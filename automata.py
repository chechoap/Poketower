class Automata:
    def __init__(self, estados, alfabeto, transiciones, inicio, finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.inicio = inicio
        self.finales = finales
        self.estado_actual = inicio
        self.estado_anterior = None

    def validar_entrada(self, entrada):
        for simbolo in entrada:
            if simbolo not in self.alfabeto:
                print(f"Error. El símbolo '{simbolo}' no está definido en el alfabeto. Saliendo del juego...")
                return False
            else:
                if self.avanzar(simbolo) == False:
                    return False
        return True
    
    def avanzar(self, simbolo):
        if simbolo in self.transiciones[self.estado_actual]:
            self.estado_anterior = self.estado_actual
            self.estado_actual = self.transiciones[self.estado_actual][simbolo]
            print(f"Estado Anterior: {self.estado_anterior}. Estado Actual: {self.estado_actual}")
            return True
        else: 
            print(f"Error. La entrada '{simbolo}' no es válida para el estado actual '{self.estado_actual}'. Saliendo del juego...")
            return False

    def es_estado_final(self, estado):
        return self.estado_actual in self.finales