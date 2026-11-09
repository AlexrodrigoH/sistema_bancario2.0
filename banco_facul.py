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
            validar.entrada = ""
            inicial = ""
            print("**PARA CANCELAR O CADASTRO, APERTE A TECLA ESCAPE (ESC)**\n")
            while True:
                print(f"\r\033[2KNome: {inicial}", end="", flush=True)
                validar.entrada = msvcrt.getwch()
                teste = validar.fluxo_entrada("nome")
                if teste == "cancelar":
                    break
                elif teste == "corrigir":
                    inicial = inicial[:-1]
                    continue
                elif teste == "continuar":
                    inicial += validar.entrada
                    continue
                elif teste == "confirmar":
                    inicial = " ".join(inicial.split()).upper()
                    validar.entrada = inicial
                    if not validar.validar_entrada_str():
                        continue
                    break
            print(f"\nFAIXA TESTE - {validar.entrada}\n") 
            dados_cliente.nome = validar.entrada
            validar.entrada = ""
            print(f"\nTeste - aqui deve estar vazio -> {validar.entrada}\n")
            while True:
                print(f"\r\033[2kAno de nascimento (dd/mm/aaaa): {validar.entrada}", end="", flush=True)
                validar.entrada += msvcrt.getwch()
                teste = validar.fluxo_entrada("nascimento")
                if teste == "cancelar":
                    break
                elif teste == "continuar":
                    continue
                elif teste == "confirmar":
                    if not validar.validar_entrada_nume():
                        validar.entrada = ""
                        continue
                    else:
                        validar.entrada = "".join(validar.entrada.strip().split())
                    break
                print(f"\nAno de nascimento digitado: {validar.entrada}\n")
        if opcao == 2:
            print("\nConsultar cliente")
            print("Funcao nao implementada.\n")
            continue
        if opcao == 3:
            texto_colorido.Texto_colorido("Finalizando execucao do programa...").cor_verde()
            break

    #parada de emergencia
    #break