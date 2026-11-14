"""Menu principal do sistema: direciona ações e apresenta falhas de persistência."""

import pickle
import validacao_entrada
import cliente_registro
import texto_colorido

def executar_menu():
    """Mantém a navegação ativa e trata falhas de arquivo sem informar sucesso falso."""
    while True:
        print("="*30)
        print("     Banco do aprendizado     ")
        print("="*30,"\n")
        print("="*30)
        print("     Menu Principal     ")
        print("="*30)
        print("1 - Cadastrar cliente\n"
              "2 - Consultar cliente\n"
              "3 - Analisar clientes pendentes\n"
              "4 - Atualizar dados\n"
              "5 - Sair\n"
              )
        validar = validacao_entrada.Validar_entrada(input("Digite a opção desejada: "))
        if validar.validar_entrada_nume():
            opcao = validar.entrada
            if opcao < 1 or opcao > 5:
                texto_colorido.Texto_colorido("\nERROR - 000MP - Opção inválida.").cor_vermelho()
                continue
            try:
                if opcao == 1:
                    dados_cliente = cliente_registro.Cliente_novo().novo_cliente()
                    if dados_cliente is None:
                        continue
                    cliente_registro.Salvar_cliente_arquivo().cliente_salvo(dados_cliente)
                if opcao == 2:
                    print("\nConsultar cliente")
                    cliente_registro.Consultar_clientes().consultar_aprovados()
                    continue
                if opcao == 4:
                    cliente_registro.Atualizar_cliente().atualizar_dados()
                if opcao == 5:
                    texto_colorido.Texto_colorido("Finalizando execucao do programa...").cor_verde()
                    break
                if opcao == 3:
                    cliente_registro.Analisar_clientes().menu_analise()
            except (OSError, pickle.UnpicklingError, EOFError, AttributeError, ModuleNotFoundError) as erro:
                texto_colorido.Texto_colorido(f"Falha ao acessar os registros: {erro}").cor_vermelho()


if __name__ == "__main__":
    executar_menu()
