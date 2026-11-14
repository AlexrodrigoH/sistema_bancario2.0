"""Verifica o formato e os dígitos verificadores do CPF."""

class Validar_cpf:
    def calcular_digito(self, cpf):
        """Calcula um dígito verificador usando a soma ponderada e o resto por onze."""
        soma = 0
        peso = len(cpf) + 1
        for numero in cpf:
            soma += int(numero) * peso
            peso -= 1
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    def cpf_valido(self, cpf):
        """Confere tamanho, dígitos ASCII, repetição e os dois verificadores; não consulta identidade real."""
        if len(cpf) != 11 or any(numero not in "0123456789" for numero in cpf):
            return False
        if len(set(cpf)) == 1:
            return False
        if int(cpf[9]) != self.calcular_digito(cpf[:9]):
            return False
        return int(cpf[10]) == self.calcular_digito(cpf[:10])
