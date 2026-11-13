import msvcrt

class Retorno:
    def __init__(self, seguir="cancelar"):
        self.seguir = seguir
    def retornar_seguir(self, validar, tipo, mensagem, validar_campo):
        inicial = ""
        while True:
            print(
                f"\r\033[2K{mensagem}{inicial}",
                end="",
                flush=True
            )
            validar.entrada = msvcrt.getwch()
            if validar.entrada in ("\x00", "\xe0"):
                msvcrt.getwch()
                continue
            self.seguir = validar.fluxo_entrada(tipo)
            if self.seguir == "cancelar":
                validar.entrada = ""
                return False
            elif self.seguir == "corrigir":
                inicial = inicial[:-1]
            elif self.seguir == "continuar":
                inicial += validar.entrada
            elif self.seguir == "confirmar":
                if tipo == "nome":
                    inicial = " ".join(inicial.split()).upper()
                validar.entrada = inicial
                if not validar_campo():
                    continue
                print()
                return True