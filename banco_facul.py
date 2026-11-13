import validacao_entrada
import cliente_registro
import texto_colorido
import msvcrt
import retorno

while True:
    print("="*30)
    print("     Banco do aprendizado     ")
    print("="*30,"\n")
    print("="*30)
    print("     Menu Principal     ")
    print("="*30)
    print("1 - Cadastrar cliente\n"
          "2 - Consultar cliente\n"
          "3 - Sair\n")
    dados_cliente = cliente_registro.Dados_do_cliente()
    validar = validacao_entrada.Validar_entrada(input("Digite a opção desejada: "))
    if validar.validar_entrada_nume():
        opcao = validar.entrada
        if opcao < 1 or opcao > 3:
            texto_colorido.Texto_colorido("\nERROR - 000MP - Opção inválida.").cor_vermelho()
            continue
        if opcao == 1:
            print("Cadastrar cliente")
            print(
                "**PARA CANCELAR O CADASTRO, "
                "APERTE A TECLA ESCAPE (ESC)**\n"
            )
            condicao_retorno = retorno.Retorno()
            confirmado = condicao_retorno.retornar_seguir(
                validar,
                "nome",
                "Nome: ",
                validar.validar_entrada_str
            )
            if not confirmado:
                continue
            dados_cliente.nome = validar.entrada
            print(f"\nFAIXA TESTE - {dados_cliente.nome}\n")
            validar.entrada = ""
        if opcao == 2:
            print("\nConsultar cliente")
            print("Funcao nao implementada.\n")
            continue
        if opcao == 3:
            texto_colorido.Texto_colorido("Finalizando execucao do programa...").cor_verde()
            break

    #parada de emergencia
    #break