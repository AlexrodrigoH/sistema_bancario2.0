"""Cadastro, consulta, atualização e análise dos clientes persistidos em PKL."""

import pickle
import os
import tempfile
from pathlib import Path
import validacao_entrada
import retorno
from datetime import date
import texto_colorido
from processo_abertura import Processo_abertura

class Dados_do_cliente:
    def __init__(self, nome = "", nascimento = "", cpf = "",endereco = None):
        """Cria um cliente com atributos próprios, inicialmente pendente de aprovação."""
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.nascimento = nascimento
        self.status = "pendente"
        self.motivo_rejeicao = None
        self.campo_correcao = None
        Processo_abertura().preparar_cliente(self)
    def calcular_idade(self):
        """Calcula a idade considerando se o aniversário já ocorreu neste ano."""
        hoje = date.today()
        idade = hoje.year - self.nascimento.year
        if (hoje.month, hoje.day) < (
            self.nascimento.month, self.nascimento.day
        ):
            idade -= 1
        return idade

    def endereco_cliente(self, bairro, rua, numero, ref = "N/A"):
        """Agrupa os campos do endereço em um dicionário exclusivo deste cliente."""
        self.endereco = {"bairro": bairro, "rua": rua, "numero": numero, "referencia": ref}
class Cliente_novo:
    def novo_cliente(self):
        """Captura e valida cada campo, exige consentimento e permite cancelar com ESC."""
        dados_cliente = Dados_do_cliente()
        validar = validacao_entrada.Validar_entrada("")
        print("Cadastrar cliente")
        texto_colorido.Texto_colorido(
            "**PARA CANCELAR O CADASTRO, "
            "APERTE A TECLA ESCAPE (ESC)**\n"
        ).cor_alaranjado()
        condicao_retorno = retorno.Retorno()
        confirmado = condicao_retorno.retornar_seguir(validar, "nome", "Nome: ", validar.validar_entrada_str)
        if not confirmado:
            return None
        dados_cliente.nome = validar.entrada
        validar.entrada = ""
        confirmado = condicao_retorno.retornar_seguir(
            validar,
            "nascimento",
            "DATA: ",
            validar.validar_nascimento
        )
        if not confirmado:
            return None
        dados_cliente.nascimento = validar.entrada
        print(
            f"Nascimento: {dados_cliente.nascimento:%d/%m/%Y}\n"
            f"Idade: {dados_cliente.calcular_idade()} anos"
        )
        validar.entrada = ""
        confirmado = condicao_retorno.retornar_seguir(
            validar,
            "cpf",
            "CPF: ",
            validar.validar_cpf
        )
        if not confirmado:
            return None
        dados_cliente.cpf = validar.entrada
        if Salvar_cliente_arquivo().cliente_existe(dados_cliente.cpf):
            texto_colorido.Texto_colorido(
                "Cliente já cadastrado com este CPF. Retornando ao menu..."
            ).cor_alaranjado()
            return None
        endereco = {}
        for campo, mensagem, validar_campo in (
            ("bairro", "Bairro: ", validar.validar_entrada_str),
            ("rua", "Rua: ", validar.validar_entrada_str),
            ("numero", "Número: ", validar.validar_entrada_nume),
            ("referencia", "Referência: ", validar.validar_entrada_str),
        ):
            validar.entrada = ""
            confirmado = condicao_retorno.retornar_seguir(
                validar, campo, mensagem, validar_campo
            )
            if not confirmado:
                break
            endereco[campo] = validar.entrada
        if not confirmado:
            return None
        dados_cliente.endereco_cliente(
            endereco["bairro"],
            endereco["rua"],
            endereco["numero"],
            endereco["referencia"],
        )
        processo = Processo_abertura()
        if not processo.solicitar_consentimento():
            return None
        processo.aceitar_termos(dados_cliente)
        return dados_cliente
class Salvar_cliente_arquivo:
    def listar_clientes(self, caminho="clientes.pkl"):
        """Lê os objetos em sequência e completa atributos ausentes de cadastros antigos."""
        clientes = []
        try:
            with open(caminho, "rb") as arquivo:
                while arquivo.peek(1):
                    cliente = pickle.load(arquivo)
                    if not hasattr(cliente, "status"):
                        cliente.status = "pendente"
                    if not hasattr(cliente, "motivo_rejeicao"):
                        cliente.motivo_rejeicao = None
                    if not hasattr(cliente, "campo_correcao"):
                        cliente.campo_correcao = None
                    Processo_abertura().preparar_cliente(cliente)
                    clientes.append(cliente)
        except FileNotFoundError:
            return []
        return clientes

    def alterar_status(self, cpf, status, caminho="clientes.pkl", motivo_rejeicao=None,
                       campo_correcao=None, analise=None):
        """Localiza o cliente pelo CPF e persiste a decisão com as regras do P01."""
        if status not in ("aprovado", "rejeitado", "pendente"):
            return False
        if status == "pendente" and not analise and (
            motivo_rejeicao != "erro na inserção de dados"
            or campo_correcao not in (
                "nome", "nascimento", "cpf", "bairro", "rua", "numero", "referencia"
            )
        ):
            return False
        if status == "rejeitado" and motivo_rejeicao not in (
            "erro na inserção de dados", "negativado"
        ):
            return False
        clientes = self.listar_clientes(caminho)
        for cliente in clientes:
            if cliente.cpf == cpf and (
                cliente.status == "pendente" or cliente.status == "aprovado" and cliente.conta is None
            ):
                if not Processo_abertura().decidir(
                    cliente, status, motivo_rejeicao, campo_correcao, analise
                ):
                    return False
                break
        else:
            return False
        self.regravar_clientes(clientes, caminho)
        Processo_abertura().exibir_situacao(cliente)
        return True

    def regravar_clientes(self, clientes, caminho):
        """Grava todos os registros em um temporário e só depois substitui o arquivo original."""
        destino = Path(caminho).resolve()
        temporario = None
        try:
            # O original permanece intacto até o temporário estar completo e fechado.
            with tempfile.NamedTemporaryFile(mode="wb", dir=destino.parent, delete=False) as arquivo:
                temporario = Path(arquivo.name)
                for cliente in clientes:
                    pickle.dump(cliente, arquivo)
                arquivo.flush()
                os.fsync(arquivo.fileno())
            os.replace(temporario, destino)
        finally:
            if temporario is not None and temporario.exists():
                temporario.unlink()
        return True

    def salvar_correcao(self, cpf_original, valor, status, caminho="clientes.pkl",
                        motivo_rejeicao=None, analise=None):
        """Atualiza o campo marcado e salva a decisão preservando os demais clientes."""
        if status not in ("aprovado", "rejeitado", "pendente"):
            return False
        if status == "rejeitado" and motivo_rejeicao != "negativado":
            return False
        if status == "pendente" and motivo_rejeicao != "erro na inserção de dados":
            return False
        clientes = self.listar_clientes(caminho)
        for cliente in clientes:
            if cliente.cpf == cpf_original and cliente.status == "pendente" and cliente.campo_correcao:
                campo = cliente.campo_correcao
                if campo == "cpf" and any(outro.cpf == valor and outro is not cliente for outro in clientes):
                    texto_colorido.Texto_colorido("CPF já cadastrado para outro cliente.").cor_vermelho()
                    return False
                if campo in ("nome", "nascimento", "cpf"):
                    setattr(cliente, campo, valor)
                elif campo in ("bairro", "rua", "numero", "referencia"):
                    cliente.endereco[campo] = valor
                else:
                    return False
                processo = Processo_abertura()
                processo.registrar(cliente, "dado_corrigido", {"campo": campo, "valor": valor})
                if not processo.decidir(
                    cliente, status, motivo_rejeicao,
                    campo if status == "pendente" else None, analise, corrigido=True
                ):
                    return False
                self.regravar_clientes(clientes, caminho)
                processo.exibir_situacao(cliente)
                return True
        return False

    def salvar_atualizacao(self, cpf_original, campo, valor, caminho="clientes.pkl"):
        """Atualiza um campo de cliente aprovado, impedindo CPF duplicado e registrando auditoria."""
        if campo not in ("nome", "nascimento", "cpf", "bairro", "rua", "numero", "referencia"):
            return False
        clientes = self.listar_clientes(caminho)
        for cliente in clientes:
            if cliente.cpf == cpf_original and cliente.status == "aprovado":
                if campo == "cpf" and any(outro.cpf == valor and outro is not cliente for outro in clientes):
                    texto_colorido.Texto_colorido("CPF já cadastrado para outro cliente.").cor_vermelho()
                    return False
                if campo in ("nome", "nascimento", "cpf"):
                    setattr(cliente, campo, valor)
                else:
                    if cliente.endereco is None:
                        cliente.endereco = {}
                    cliente.endereco[campo] = valor
                Processo_abertura().registrar(cliente, "dado_atualizado", {"campo": campo, "valor": valor})
                Processo_abertura().notificar(cliente, f"Dado cadastral atualizado: {campo}.")
                self.regravar_clientes(clientes, caminho)
                return True
        return False

    def cliente_existe(self, cpf, caminho="clientes.pkl"):
        """Procura um CPF já cadastrado independentemente do status do cliente."""
        try:
            with open(caminho, "rb") as arquivo:
                while True:
                    try:
                        cliente = pickle.load(arquivo)
                    except EOFError:
                        return False
                    if cliente.cpf == cpf:
                        return True
        except FileNotFoundError:
            return False

    def cliente_salvo(self, dados_cliente, caminho="clientes.pkl"):
        """Exige dados v?lidos e aceite, bloqueia duplicidade e salva a solicitação pendente."""
        processo = Processo_abertura()
        processo.preparar_cliente(dados_cliente)
        if not dados_cliente.consentimento:
            texto_colorido.Texto_colorido("Cadastro não salvo: falta o aceite dos termos.").cor_vermelho()
            return False
        if processo.campo_invalido(dados_cliente) is not None:
            texto_colorido.Texto_colorido("Cadastro não salvo: existem dados inválidos.").cor_vermelho()
            return False
        if self.cliente_existe(dados_cliente.cpf, caminho):
            texto_colorido.Texto_colorido(
                "Cliente já cadastrado com este CPF. Cadastro não gravado."
            ).cor_alaranjado()
            return False
        processo.registrar(dados_cliente, "dados_validados", "Cadastro recebido após validações de entrada.")
        processo.registrar(dados_cliente, "duplicidade_verificada", "CPF ainda não cadastrado.")
        processo.notificar(dados_cliente, "Solicitação recebida. Abertura pendente de análise.")
        clientes = self.listar_clientes(caminho)
        clientes.append(dados_cliente)
        self.regravar_clientes(clientes, caminho)
        texto_colorido.Texto_colorido("Cliente cadastrado e salvo com sucesso.").cor_verde()
        texto_colorido.Texto_colorido("Status: pendente de aprovação.").cor_alaranjado()
        print(f"Notificação local: {dados_cliente.notificacoes[-1]['mensagem']}")
        return True

class Consultar_clientes:
    def consultar_aprovados(self, caminho="clientes.pkl"):
        """Exibe somente clientes aprovados e informa a situação de suas contas."""
        aprovados = [cliente for cliente in Salvar_cliente_arquivo().listar_clientes(caminho)
                     if cliente.status == "aprovado"]
        if not aprovados:
            texto_colorido.Texto_colorido("Nenhum cliente aprovado para consulta.").cor_alaranjado()
            return
        for cliente in aprovados:
            print("=" * 30)
            print(f"Nome: {cliente.nome}\nCPF: {cliente.cpf}\nNascimento: {cliente.nascimento:%d/%m/%Y}")
            for campo, valor in (cliente.endereco or {}).items():
                print(f"{campo}: {valor}")
            texto_colorido.Texto_colorido("Status: aprovado.").cor_verde()
            if cliente.conta:
                print(f"Conta: {cliente.conta.numero} | Situação: {cliente.conta.status}")
            else:
                texto_colorido.Texto_colorido("Cadastro antigo: conclua a abertura no menu de análise.").cor_alaranjado()

class Atualizar_cliente:
    def atualizar_dados(self, caminho="clientes.pkl"):
        """Pesquisa por nome ou CPF, valida o novo valor e grava somente após confirmação."""
        salvar = Salvar_cliente_arquivo()
        validar = validacao_entrada.Validar_entrada(input(
            "Pesquisar por:\n1 - Nome\n2 - CPF\n0 - Voltar\nOpção: "
        ))
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if validar.entrada not in (1, 2):
            texto_colorido.Texto_colorido("Opção inválida.").cor_vermelho()
            return
        tipo_busca = validar.entrada
        termo = input("Nome ou CPF (0 para voltar): ").strip()
        if termo == "0":
            return
        if not termo:
            texto_colorido.Texto_colorido("Informe o nome ou CPF para pesquisar.").cor_vermelho()
            return
        clientes = [cliente for cliente in salvar.listar_clientes(caminho)
                    if cliente.status == "aprovado"]
        if tipo_busca == 1:
            termo = " ".join(termo.split()).casefold()
            encontrados = [cliente for cliente in clientes if termo in cliente.nome.casefold()]
        else:
            termo = termo.replace(".", "").replace("-", "")
            encontrados = [cliente for cliente in clientes if cliente.cpf == termo]
        if not encontrados:
            texto_colorido.Texto_colorido("Nenhum cliente aprovado encontrado.").cor_alaranjado()
            return
        for indice, cliente in enumerate(encontrados, start=1):
            print(f"{indice} - {cliente.nome} | CPF: {cliente.cpf}")
        validar.entrada = input("Escolha o cliente (0 para voltar): ")
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if not 1 <= validar.entrada <= len(encontrados):
            texto_colorido.Texto_colorido("Cliente inválido.").cor_vermelho()
            return
        cliente = encontrados[validar.entrada - 1]
        cpf_original = cliente.cpf
        campos = ("nome", "nascimento", "cpf", "bairro", "rua", "numero", "referencia")
        for indice, campo in enumerate(campos, start=1):
            print(f"{indice} - {campo}")
        validar.entrada = input("Campo para atualizar (0 para voltar): ")
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if not 1 <= validar.entrada <= len(campos):
            texto_colorido.Texto_colorido("Campo inválido.").cor_vermelho()
            return
        campo = campos[validar.entrada - 1]
        validacoes = {
            "nome": validar.validar_entrada_str,
            "nascimento": validar.validar_nascimento,
            "cpf": validar.validar_cpf,
            "bairro": validar.validar_entrada_str,
            "rua": validar.validar_entrada_str,
            "numero": validar.validar_entrada_nume,
            "referencia": validar.validar_entrada_str,
        }
        texto_colorido.Texto_colorido("Digite o novo valor. ESC cancela sem salvar.").cor_alaranjado()
        if not retorno.Retorno().retornar_seguir(validar, campo, f"{campo}: ", validacoes[campo]):
            return
        valor = validar.entrada
        if campo == "cpf" and valor != cpf_original and salvar.cliente_existe(valor, caminho):
            texto_colorido.Texto_colorido("CPF já cadastrado para outro cliente.").cor_vermelho()
            return
        if campo in ("nome", "nascimento", "cpf"):
            setattr(cliente, campo, valor)
        else:
            if cliente.endereco is None:
                cliente.endereco = {}
            cliente.endereco[campo] = valor
        print(f"Nome: {cliente.nome}\nCPF: {cliente.cpf}\nNascimento: {cliente.nascimento:%d/%m/%Y}")
        for chave, dado in (cliente.endereco or {}).items():
            print(f"{chave}: {dado}")
        texto_colorido.Texto_colorido("Status: aprovado.").cor_verde()
        validar.entrada = input("1 - Confirmar atualização\n0 - Cancelar sem salvar\nOpção: ")
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if validar.entrada != 1:
            texto_colorido.Texto_colorido("Opção inválida. Atualização não salva.").cor_vermelho()
            return
        if salvar.salvar_atualizacao(cpf_original, campo, valor, caminho):
            texto_colorido.Texto_colorido("Dados atualizados e salvos com sucesso.").cor_verde()
        else:
            texto_colorido.Texto_colorido("Atualização não salva. Verifique o cadastro do cliente.").cor_vermelho()

class Analisar_clientes:
    def consultar_historico(self, caminho="clientes.pkl"):
        """Pesquisa um CPF em qualquer status e mostra seus eventos e notificações locais."""
        cpf = input("CPF para consultar o histórico (0 para voltar): ").strip().replace(".", "").replace("-", "")
        if cpf == "0":
            return
        for cliente in Salvar_cliente_arquivo().listar_clientes(caminho):
            if cliente.cpf != cpf:
                continue
            print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
            processo = Processo_abertura()
            processo.exibir_situacao(cliente)
            print("Histórico de auditoria:")
            for evento in cliente.auditoria:
                print(f"{evento['data']} | {evento['evento']} | {evento['detalhes']}")
            print("Notificações locais:")
            for aviso in cliente.notificacoes:
                print(f"{aviso['data']} | {aviso['mensagem']}")
            if not cliente.auditoria:
                texto_colorido.Texto_colorido("Cadastro antigo sem histórico registrado.").cor_alaranjado()
            return
        texto_colorido.Texto_colorido("Cliente não encontrado.").cor_alaranjado()

    def menu_analise(self, caminho="clientes.pkl"):
        """Direciona para análise, correções ou consulta do histórico sem alterar o menu principal."""
        validar = validacao_entrada.Validar_entrada(input(
            "1 - Analisar pendentes ou concluir abertura antiga\n2 - Corrigir dados marcados\n"
            "3 - Histórico e notificações\n0 - Voltar\nOpção: "
        ))
        if not validar.validar_entrada_nume():
            return
        match validar.entrada:
            case 1:
                self.analisar_pendentes(caminho)
            case 2:
                self.corrigir_cliente(caminho)
            case 3:
                self.consultar_historico(caminho)
            case 0:
                return
            case _:
                texto_colorido.Texto_colorido("Opção inválida.").cor_vermelho()

    def corrigir_cliente(self, caminho="clientes.pkl"):
        """Corrige o campo marcado e exige confirmação dos dados e decisão antes de salvar."""
        salvar = Salvar_cliente_arquivo()
        clientes = [cliente for cliente in salvar.listar_clientes(caminho)
                    if cliente.status == "pendente" and cliente.campo_correcao]
        if not clientes:
            texto_colorido.Texto_colorido("Nenhum cliente com correção marcada.").cor_alaranjado()
            return
        for indice, cliente in enumerate(clientes, start=1):
            print(f"{indice} - {cliente.nome} | CPF: {cliente.cpf} | Corrigir: {cliente.campo_correcao}")
        validar = validacao_entrada.Validar_entrada(input("Cliente (0 para voltar): "))
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if not 1 <= validar.entrada <= len(clientes):
            texto_colorido.Texto_colorido("Cliente inválido.").cor_vermelho()
            return
        cliente = clientes[validar.entrada - 1]
        cpf_original = cliente.cpf
        campo = cliente.campo_correcao
        validacoes = {
            "nome": validar.validar_entrada_str,
            "nascimento": validar.validar_nascimento,
            "cpf": validar.validar_cpf,
            "bairro": validar.validar_entrada_str,
            "rua": validar.validar_entrada_str,
            "numero": validar.validar_entrada_nume,
            "referencia": validar.validar_entrada_str,
        }
        while True:
            texto_colorido.Texto_colorido("Digite o valor corrigido. ESC cancela sem salvar.").cor_alaranjado()
            if not retorno.Retorno().retornar_seguir(validar, campo, f"{campo}: ", validacoes[campo]):
                return
            valor = validar.entrada
            if campo == "cpf" and valor != cpf_original and salvar.cliente_existe(valor, caminho):
                texto_colorido.Texto_colorido("CPF já cadastrado para outro cliente.").cor_vermelho()
                continue
            if campo in ("nome", "nascimento", "cpf"):
                setattr(cliente, campo, valor)
            else:
                cliente.endereco[campo] = valor
            print(f"Nome: {cliente.nome}\nCPF: {cliente.cpf}\nNascimento: {cliente.nascimento:%d/%m/%Y}")
            for chave, dado in (cliente.endereco or {}).items():
                print(f"{chave}: {dado}")
            texto_colorido.Texto_colorido("Status: pendente.").cor_alaranjado()
            validar.entrada = input("Os dados estão corretos?\n1 - Sim\n2 - Corrigir novamente\n0 - Cancelar sem salvar\nOpção: ")
            if not validar.validar_entrada_nume() or validar.entrada == 0:
                return
            if validar.entrada == 2:
                continue
            if validar.entrada != 1:
                texto_colorido.Texto_colorido("Opção inválida. Alteração não salva.").cor_vermelho()
                return
            break
        validar.entrada = input("1 - Aprovar\n2 - Reprovar\n0 - Cancelar sem salvar\nDecisão: ")
        if not validar.validar_entrada_nume() or validar.entrada == 0:
            return
        if validar.entrada not in (1, 2):
            texto_colorido.Texto_colorido("Decisão inválida. Alteração não salva.").cor_vermelho()
            return
        status = "aprovado" if validar.entrada == 1 else "rejeitado"
        motivo = None
        if status == "rejeitado":
            validar.entrada = input("1 - Erro na inserção de dados\n2 - Negativado\n0 - Cancelar sem salvar\nMotivo: ")
            if not validar.validar_entrada_nume() or validar.entrada == 0:
                return
            if validar.entrada not in (1, 2):
                texto_colorido.Texto_colorido("Motivo inválido. Alteração não salva.").cor_vermelho()
                return
            motivo = "erro na inserção de dados" if validar.entrada == 1 else "negativado"
            if validar.entrada == 1:
                status = "pendente"
        analise = None
        if status == "aprovado":
            analise = Processo_abertura().solicitar_analise(cliente)
            if analise is None:
                return
        if salvar.salvar_correcao(cpf_original, valor, status, caminho, motivo, analise):
            texto_colorido.Texto_colorido("Correção e decisão salvas com sucesso.").cor_verde()
            print("Retornando ao menu principal...")
        else:
            texto_colorido.Texto_colorido("Correção não salva. Verifique a pendência do cliente.").cor_vermelho()

    def analisar_pendentes(self, caminho="clientes.pkl"):
        """Analisa pendentes e cadastros antigos sem conta, registrando recusa ou abrindo a conta."""
        salvar = Salvar_cliente_arquivo()
        pendentes = [cliente for cliente in salvar.listar_clientes(caminho)
                     if cliente.status == "pendente"
                     or cliente.status == "aprovado" and cliente.conta is None]
        if not pendentes:
            texto_colorido.Texto_colorido("Nenhum cliente pendente de aprovação.").cor_alaranjado()
            return
        for indice, cliente in enumerate(pendentes, start=1):
            print(f"{indice} - {cliente.nome} | CPF: {cliente.cpf}")
        validar = validacao_entrada.Validar_entrada(
            input("Escolha o cliente (0 para voltar): ")
        )
        if not validar.validar_entrada_nume():
            return
        if validar.entrada == 0:
            return
        if not 1 <= validar.entrada <= len(pendentes):
            texto_colorido.Texto_colorido("Cliente inválido.").cor_vermelho()
            return
        cliente = pendentes[validar.entrada - 1]
        if cliente.campo_correcao is not None:
            texto_colorido.Texto_colorido(
                f"Correção necessária: {cliente.campo_correcao}. Motivo: {cliente.motivo_rejeicao}."
            ).cor_alaranjado()
        print(f"Nome: {cliente.nome}\nCPF: {cliente.cpf}\nNascimento: {cliente.nascimento:%d/%m/%Y}")
        for campo, valor in (cliente.endereco or {}).items():
            print(f"{campo}: {valor}")
        Processo_abertura().exibir_situacao(cliente)
        validar.entrada = input("1 - Aprovar\n2 - Rejeitar\n0 - Voltar\nDecisão: ")
        if not validar.validar_entrada_nume():
            return
        if validar.entrada == 0:
            return
        if validar.entrada not in (1, 2):
            texto_colorido.Texto_colorido("Decisão inválida.").cor_vermelho()
            return
        status = "aprovado" if validar.entrada == 1 else "rejeitado"
        motivo_rejeicao = None
        campo_correcao = None
        if status == "rejeitado":
            validar.entrada = input(
                "Motivo da rejeição:\n"
                "1 - Erro na inserção de dados\n"
                "2 - Negativado\n"
                "0 - Voltar sem salvar\nMotivo: "
            )
            if not validar.validar_entrada_nume():
                return
            if validar.entrada == 0:
                return
            if validar.entrada not in (1, 2):
                texto_colorido.Texto_colorido("Motivo inválido.").cor_vermelho()
                return
            motivo_rejeicao = (
                "erro na inserção de dados" if validar.entrada == 1 else "negativado"
            )
            if validar.entrada == 1:
                campos = ("nome", "nascimento", "cpf", "bairro", "rua", "numero", "referencia")
                print("Qual dado precisa ser corrigido?")
                for indice, campo in enumerate(campos, start=1):
                    print(f"{indice} - {campo}")
                validar.entrada = input("Campo (0 para voltar sem salvar): ")
                if not validar.validar_entrada_nume():
                    return
                if validar.entrada == 0:
                    return
                if not 1 <= validar.entrada <= len(campos):
                    texto_colorido.Texto_colorido("Campo inválido.").cor_vermelho()
                    return
                campo_correcao = campos[validar.entrada - 1]
                status = "pendente"
        analise = None
        if status == "aprovado":
            if cliente.campo_correcao:
                texto_colorido.Texto_colorido("Corrija o campo marcado na subopção 2 antes de aprovar.").cor_alaranjado()
                return
            analise = Processo_abertura().solicitar_analise(cliente)
            if analise is None:
                return
        if salvar.alterar_status(cliente.cpf, status, caminho, motivo_rejeicao, campo_correcao, analise):
            texto_colorido.Texto_colorido("Decisão salva com sucesso.").cor_verde()
            if status == "pendente":
                texto_colorido.Texto_colorido(
                    f"Correção necessária: {campo_correcao}. Cliente pendente. Retornando ao menu..."
                ).cor_alaranjado()
                return
        else:
            texto_colorido.Texto_colorido("Cliente não está mais pendente.").cor_alaranjado()
