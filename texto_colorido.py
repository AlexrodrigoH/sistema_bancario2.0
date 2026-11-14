"""Centraliza as cores das mensagens de sucesso, erro e aviso no terminal."""

class Texto_colorido:
    def __init__(self, colorido):
        """Guarda o texto que será exibido por um dos métodos de cor."""
        self.colorido = colorido
    def cor_verde(self):
        """Exibe uma confirmação em verde e restaura a cor padrão do terminal."""
        print(f"\033[32m{self.colorido}\033[0m")
    def cor_vermelho(self):
        """Exibe um erro em vermelho e restaura a cor padrão do terminal."""
        print(f"\033[31m{self.colorido}\033[0m")
    def cor_alaranjado(self):
        """Exibe um aviso em laranja e restaura a cor padrão do terminal."""
        print(f"\033[38;5;208m{self.colorido}\033[0m")