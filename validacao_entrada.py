import texto_colorido

class Validar_entrada:
    def __init__(self, entrada):
        self.entrada = entrada
    def validar_entrada_nume(self):
        self.entrada = self.entrada.strip()
        if not self.entrada.isdigit():
            texto_colorido.Texto_colorido("\nERROR - 000VN - DIGITE APENAS NÚMEROS.").cor_vermelho()
            return False
        caractere = "0123456789"
        for num in self.entrada:
            if num not in caractere:
                texto_colorido.Texto_colorido("\nERROR - 001VN -  Digite apenas números.").cor_vermelho()
                return False
        try:
            self.entrada = int(self.entrada)
            return True
        except ValueError:
            return False
    def validar_entrada_str(self):
        self.entrada = self.entrada.strip()
        if self.entrada == "" or self.entrada == "\r":
            texto_colorido.Texto_colorido("\nERROR - 002VS - Entrada vazia nao permitida.").cor_vermelho()
            return False
        nome_split = self.entrada.split()
        change = 0
        for nome in nome_split:
            nome_tratado = ""
            cont = 0
            nome = nome.strip("'")
            for letra in nome:
                if letra == "'":
                    cont += 1
                    if cont > 1:
                        continue
                nome_tratado += letra
            nome = nome_tratado.strip("'")
            nome_split[change] = nome
            if nome[:1] == "'" or nome[-1:] == "'":
                if nome[:1] == "'":
                    nome_split[change] = nome[1:]
                if nome[-1:] == "'":
                    nome_split[change] = nome[:-1]
            change += 1
            test = nome.replace("'", "")
            if not test.isalpha():
                texto_colorido.Texto_colorido("\nERROR - 006VS - Digite apenas letras.").cor_vermelho()
                return False
        self.entrada = " ".join(nome_split).strip()
        if len(self.entrada) > 100 or len(self.entrada) < 3:
            texto_colorido.Texto_colorido("\nERROR - 003VS - Nome nao permitido.").cor_vermelho()
            return False
        for nome in nome_split:
            cont = 0
            for letra in nome:
                if cont + 2 >= len(nome):
                    break
                if letra == nome[cont+1] and letra == nome[cont+2]:
                    texto_colorido.Texto_colorido("\nERROR - 007VS - Nome incorreto.").cor_vermelho()
                    return False
                cont += 1
        return True
    def validar_entrada_teclado(self):
        if self.entrada == "" or self.entrada == "\r":
            texto_colorido.Texto_colorido("\nERROR - 008VT - Entrada vazia nao permitida.").cor_vermelho()
            return False
        match self.tipo:
            case "nome":
                if not self.entrada.isalpha() and self.entrada not in " '":
                    return False
            case "nascimento":
                if not self.entrada.isdigit() and self.entrada not in "/":
                    return False
            case "cpf":
                if not self.entrada.isdigit() and self.entrada not in ".-":
                    return False
        return True
    def fluxo_entrada(self, tipo = ""):
        self.tipo = tipo
        nome = self.entrada
        if nome[0] == "\x1b" or nome[-1] == "\x1b":
            self.entrada = nome[:-1]
            texto_colorido.Texto_colorido("\nRetornando ao menu...").cor_alaranjado()
            return "cancelar"
        if nome == "\x08":
            self.entrada = ""
            return "corrigir"
        if nome == "\r":
            self.entrada = ""
            return "confirmar"
        if not self.validar_entrada_teclado():
            self.entrada = ""
        return "continuar"