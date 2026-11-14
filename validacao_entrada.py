"""Valida campos e teclas e traduz entradas em estados do fluxo de captura."""

import texto_colorido
import verificacao_de_cliente
from datetime import date, datetime

class Validar_entrada:
    def __init__(self, entrada):
        """Guarda a entrada que será validada ou normalizada pelos métodos desta instância."""
        self.entrada = entrada
    def validar_entrada_nume(self):
        """Aceita somente dígitos ASCII e converte a entrada válida para inteiro."""
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
        """Normaliza espaços e apóstrofos e aplica as regras atuais de letras e tamanho."""
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
        """Filtra cada tecla conforme o tipo do campo que está sendo preenchido."""
        if self.entrada == "" or self.entrada == "\r":
            texto_colorido.Texto_colorido("\nERROR - 008VT - Entrada vazia nao permitida.").cor_vermelho()
            return False
        match self.tipo:
            case "nome" | "bairro" | "rua" | "referencia":
                if not self.entrada.isalpha() and self.entrada not in " '":
                    return False
            case "numero":
                if self.entrada not in "0123456789":
                    return False
            case "nascimento":
                if self.entrada not in "0123456789":
                    return False
            case "cpf":
                if self.entrada not in "0123456789":
                    return False
        return True
    def fluxo_entrada(self, tipo = ""):
        """Distingue ESC, Backspace, Enter e caracteres comuns para orientar a captura."""
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
    def validar_digito_nascimento(self, inicial):
        """Impede dígitos que tornariam a data parcial ou completa inválida."""
        if self.entrada not in "0123456789" or not self.entrada:
            return False
        candidato = inicial + self.entrada
        tamanho = len(candidato)
        if tamanho > 8:
            return False
        if tamanho == 1:
            return candidato in "0123"
        dia = int(candidato[:2])
        if not 1 <= dia <= 31:
            return False
        if tamanho == 3:
            return candidato[2] in "01"
        if tamanho >= 4:
            mes = int(candidato[2:4])
            try:
                date(2000, mes, dia)
            except ValueError:
                return False
        if tamanho == 8:
            try:
                nascimento = date(int(candidato[4:]), mes, dia)
            except ValueError:
                return False
            return self.nascimento_permitido(nascimento)
        return True

    def validar_digito_cpf(self, inicial):
        """Limita o CPF a onze dígitos durante a digitação."""
        if not self.entrada or self.entrada not in "0123456789":
            return False
        candidato = inicial + self.entrada
        if len(candidato) > 11:
            return False
        return True

    def validar_cpf(self):
        """Delega a validação matemática do CPF ao módulo de verificação."""
        return verificacao_de_cliente.Validar_cpf().cpf_valido(self.entrada)

    def nascimento_permitido(self, nascimento):
        """Rejeita datas futuras e idades fora do intervalo atual de zero a 130 anos."""
        hoje = date.today()
        if nascimento > hoje:
            return False
        idade = hoje.year - nascimento.year
        if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
            idade -= 1
        return 0 <= idade <= 130

    def validar_nascimento(self):
        """Converte a data completa em objeto date quando formato e idade são v?lidos."""
        entrada = self.entrada.strip()
        try:
            nascimento = datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            return False
        if nascimento.strftime("%d/%m/%Y") != entrada:
            return False
        if not self.nascimento_permitido(nascimento):
            return False
        self.entrada = nascimento
        return True
