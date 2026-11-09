class Retorno:
    def __init__(self, seguir):
        self.seguir = seguir

    def retornar_seguir(self):
        if self.seguir == "cancelar":
            return False
        elif self.seguir == "continuar":
            return True
        elif self.seguir == "corrigir":
            return True
        elif self.seguir == "confirmar":
            pass
            return False
        