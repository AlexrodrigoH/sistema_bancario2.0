class Texto_colorido:
    def __init__(self, colorido):
        self.colorido = colorido
    def cor_verde(self):
        print(f"\033[32m{self.colorido}\033[0m")
    def cor_vermelho(self):
        print(f"\033[31m{self.colorido}\033[0m")
    def cor_alaranjado(self):
        print(f"\033[38;5;208m{self.colorido}\033[0m")