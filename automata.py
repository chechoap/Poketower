class Automata:
    def __init__(self, estados, alfabeto, transiciones, inicio, finales):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.inicio = inicio
        self.finales = finales
        self.estado_actual = inicio
        self.estado_anterior = None

    def avanzar(self, simbolo):
        """
        Avanza al siguiente estado basado en el símbolo de entrada.
        Retorna un diccionario con el resultado.
        """
        if simbolo in self.transiciones[self.estado_actual]:
            self.estado_anterior = self.estado_actual
            self.estado_actual = self.transiciones[self.estado_actual][simbolo]
            return {
                "exito": True,
                "mensaje": f"Estado Anterior: {self.estado_anterior}. Estado Actual: {self.estado_actual}",
                "estado_actual": self.estado_actual
            }
        else:
            return {
                "exito": False,
                "mensaje": f"Error. La entrada '{simbolo}' no es válida para el estado actual '{self.estado_actual}'.",
                "estado_actual": self.estado_actual
            }

    def es_estado_final(self):
        """
        Verifica si el estado actual es un estado final.
        """
        return self.estado_actual in self.finales