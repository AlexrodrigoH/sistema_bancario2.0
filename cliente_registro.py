class Dados_do_cliente:
    def __init__(self, nome, idade, endereco, cpf, nascimento):
        self.nome = nome
        self.idade = idade
        self.endereco = endereco
        self.cpf = cpf
        self.nacimento = nascimento
    def endereco_cliente(self, bairro, rua, numero, ref = "NA"):
        self.endereco = {"bairro": bairro, "rua": rua, "numero": numero, "referencia": ref}
class Cliente_novo:
    def novo_cliente(self):
        pass
class Salvar_cliente_arquivo:
    def cliente_salvo(self):
        pass