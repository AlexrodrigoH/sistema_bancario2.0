import validacao_entrada
import cliente_registro
import texto_colorido
import msvcrt

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
    validar = validacao_entrada.Validar_entrada(input("Digite a opção desejada: "))
    if validar.validar_entrada_nume():
        opcao = validar.entrada
        if opcao < 1 or opcao > 3:
            texto_colorido.Texto_colorido("\nERROR - 000MP - Opção inválida.").cor_vermelho()
            continue
        if opcao == 1:
            print("Cadastrar cliente")
            validar.entrada = ""
            print("**PARA CANCELAR O CADASTRO, APERTE A TECLA ESCAPE (ESC)**\n")
            print("Nome: ")
            while True:
                print(f"\r\033[2K{validar.entrada}", end="", flush=True)
                validar.entrada += msvcrt.getwch()
                teste = validar.fluxo_entrada()
                if teste == "cancelar":
                    break
                elif teste == "continuar":
                    continue
                elif teste == "confirmar":
                    if not validacao_entrada.Validar_entrada(validar.entrada).validar_entrada_str():
                        validar.entrada = ""
                        continue
                    break
            print(f"\nNome digitado: {validar.entrada}\ntamanho: {len(validar.entrada)}\n")
            print(f"\nTetse de fluxo de entrada: {validar.entrada}\n")
        if opcao == 2:
            print("\nConsultar cliente")
            print("Funcao ainda nao implementada.\n")
            continue
        if opcao == 3:
            texto_colorido.Texto_colorido("Finalizando execucao do programa...").cor_verde()
            break

    #parada de emergencia
    #break