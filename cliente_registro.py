from datetime import date

class Dados_do_cliente:
    def __init__(self, nome = "", nascimento = "", cpf = "",endereco = None):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.nascimento = nascimento
    def calcular_idade(self):
        hoje = date.today()
        idade = hoje.year - self.nascimento.year
        if (hoje.month, hoje.day) < (
            self.nascimento.month, self.nascimento.day
        ):
            idade -= 1
        return idade

    def endereco_cliente(self, bairro, rua, numero, ref = "N/A"):
        self.endereco = {"bairro": bairro, "rua": rua, "numero": numero, "referencia": ref}
class Cliente_novo:
    def novo_cliente(self):
        pass
class Salvar_cliente_arquivo:
    def cliente_salvo(self):
        pass
