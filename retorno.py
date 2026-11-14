"""Captura teclas no Windows e coordena confirmação, correção e cancelamento dos campos."""

import msvcrt

class Retorno:
    def __init__(self, seguir="cancelar"):
        """Inicia o estado usado para acompanhar o fluxo de captura."""
        self.seguir = seguir
    def retornar_seguir(self, validar, tipo, mensagem, validar_campo):
        """Atualiza o terminal a cada tecla e retorna True somente após validar o campo completo."""
        inicial = ""
        while True:
            exibicao = inicial
            if tipo == "nascimento":
                digitos = inicial.ljust(8, "-")
                exibicao = f"{digitos[:2]}/{digitos[2:4]}/{digitos[4:]}"
            elif tipo == "cpf":
                digitos = inicial.ljust(11, "-")
                exibicao = f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
            print(
                f"\r\033[2K{mensagem}{exibicao}",
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
                if tipo == "nascimento":
                    if not validar.validar_digito_nascimento(inicial):
                        continue
                elif tipo == "cpf":
                    if not validar.validar_digito_cpf(inicial):
                        continue
                inicial += validar.entrada
            elif self.seguir == "confirmar":
                if tipo == "nome":
                    inicial = " ".join(inicial.split()).upper()
                validar.entrada = inicial
                if tipo == "nascimento":
                    validar.entrada = f"{inicial[:2]}/{inicial[2:4]}/{inicial[4:]}"
                if not validar_campo():
                    if tipo == "cpf" and len(inicial) == 11:
                        inicial = ""
                    continue
                print()
                return True
