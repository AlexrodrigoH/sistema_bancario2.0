class Cliente_valido:
    def __init__(self, idade = 0, ano = 0, cpf = 0):
        self.idade = idade
        self.ano = ano
        self.cpf = cpf
class Validar_idade:
    def idade_valida(self,idade):
        pass
class Validar_ano:
    def ano_valido(self, ano):
        pass
class Validar_cpf:
    def calcular_digito(self, cpf):
        soma = 0
        peso = len(cpf) + 1
        for numero in cpf:
            soma += int(numero) * peso
            peso -= 1
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    def cpf_valido(self, cpf):
        if len(cpf) != 11 or any(numero not in "0123456789" for numero in cpf):
            return False
        if len(set(cpf)) == 1:
            return False
        if int(cpf[9]) != self.calcular_digito(cpf[:9]):
            return False
        return int(cpf[10]) == self.calcular_digito(cpf[:10])
