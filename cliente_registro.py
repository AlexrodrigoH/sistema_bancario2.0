class Dados_do_cliente:
    def __init__(self, nome = "", nascimento = "", cpf = "",endereco = None):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.nacimento = nascimento
    def endereco_cliente(self, bairro, rua, numero, ref = "N/A"):
        self.endereco = {"bairro": bairro, "rua": rua, "numero": numero, "referencia": ref}
class Cliente_novo:
    def novo_cliente(self):
        pass
class Salvar_cliente_arquivo:
    def cliente_salvo(self):
        pass