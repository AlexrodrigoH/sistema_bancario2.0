"""Regras educacionais do P01: consentimento, KYC local, conta e histórico.

As listas são fictícias. Confirmar identidade neste terminal representa a
conferência manual do exercício, sem consultar documentos ou serviços reais.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from texto_colorido import Texto_colorido


class Conta_bancaria:
    """Conta vinculada ao objeto cliente, com identificação independente do CPF."""

    def __init__(self):
        """Cria uma conta inativa; a ativação acontece somente após aprovação."""
        self.numero = uuid4().hex
        self.status = "inativa"


class Processo_abertura:
    """Concentra as transições do processo sem gravar arquivos por conta própria."""

    def preparar_cliente(self, cliente):
        """Adiciona atributos ausentes em PKLs antigos sem inventar aceite ou análise."""
        padroes = {
            "consentimento": False, "consentimento_em": None,
            "identidade_verificada": False, "analise_kyc": None,
            "conta": None, "auditoria": [], "notificacoes": [],
        }
        for atributo, valor in padroes.items():
            if not hasattr(cliente, atributo):
                setattr(cliente, atributo, valor)

    def registrar(self, cliente, evento, detalhes):
        """Acrescenta evento datado ao histórico particular deste cliente."""
        cliente.auditoria.append({
            "data": datetime.now(timezone.utc).isoformat(),
            "evento": evento, "detalhes": detalhes,
        })

    def notificar(self, cliente, mensagem):
        """Registra uma notificação local e auditável; não envia e-mail ou SMS."""
        cliente.notificacoes.append({
            "data": datetime.now(timezone.utc).isoformat(), "mensagem": mensagem,
        })
        self.registrar(cliente, "notificacao_local", mensagem)

    def aceitar_termos(self, cliente):
        """Registra o aceite explícito e sua data, sem renovar um aceite existente."""
        if not cliente.consentimento:
            cliente.consentimento = True
            cliente.consentimento_em = datetime.now(timezone.utc).isoformat()
            self.registrar(cliente, "consentimento", "Termos educacionais P01 v1 aceitos.")

    def solicitar_consentimento(self):
        """Apresenta os termos do exercício e retorna True somente para aceite explícito."""
        print(
            "Termos educacionais P01 v1: os dados serão gravados localmente para "
            "simular cadastro, análise e abertura de conta. Não há operação bancária real."
        )
        escolha = input("1 - Aceitar\n0 - Não aceitar e voltar\nOpção: ").strip()
        if escolha != "1":
            Texto_colorido("Sem aceite, a abertura não pode continuar.").cor_alaranjado()
            return False
        return True

    def avaliar_kyc(self, cpf, caminho=None):
        """Consulta exclusivamente as listas fictícias, dando prioridade à restrição."""
        caminho = Path(caminho) if caminho else Path(__file__).with_name("listas_simuladas.json")
        with caminho.open(encoding="utf-8") as arquivo:
            listas = json.load(arquivo)
        if not isinstance(listas, dict) or any(
            not isinstance(listas.get(chave), list)
            or any(not isinstance(cpf_lista, str) for cpf_lista in listas[chave])
            for chave in ("negativados", "revisao_manual")
        ):
            raise ValueError("Formato inválido das listas simuladas.")
        if cpf in listas["negativados"]:
            return "rejeitado"
        if cpf in listas["revisao_manual"]:
            return "revisao_manual"
        return "aprovado"

    def solicitar_analise(self, cliente):
        """Coleta a conferência de identidade e resolve o resultado do KYC simulado."""
        if self.campo_invalido(cliente) is not None:
            Texto_colorido("Há dados inválidos. Marque o campo para correção antes de aprovar.").cor_vermelho()
            return None
        if not cliente.consentimento and not self.solicitar_consentimento():
            return None
        print("Conferência manual simulada: confira nome, nascimento e CPF exibidos.")
        escolha = input("1 - Identidade conferida\n2 - Identidade não confirmada\n0 - Cancelar\nOpção: ").strip()
        if escolha not in ("1", "2"):
            return None
        analise = {"consentimento": True, "identidade": escolha == "1",
                   "resultado": "revisao_manual", "motivo": "identidade não confirmada"}
        if escolha == "2":
            return analise
        try:
            resultado = self.avaliar_kyc(cliente.cpf)
        except (OSError, ValueError):
            Texto_colorido("Não foi possível consultar as listas simuladas. Nenhuma decisão salva.").cor_vermelho()
            return None
        analise.update(resultado=resultado, motivo=None)
        if resultado == "rejeitado":
            analise["motivo"] = "negativado"
            Texto_colorido("CPF na lista fictícia de negativados. Abertura recusada.").cor_alaranjado()
        elif resultado == "revisao_manual":
            Texto_colorido("CPF na lista fictícia de revisão manual.").cor_alaranjado()
            escolha = input("1 - Manter em revisão\n2 - Aprovar após revisão\n3 - Recusar após revisão\n0 - Cancelar\nOpção: ").strip()
            if escolha not in ("1", "2", "3"):
                return None
            justificativa = input("Justificativa da revisão: ").strip()
            if not justificativa:
                Texto_colorido("Informe a justificativa. Nenhuma decisão salva.").cor_vermelho()
                return None
            analise.update(resultado={"1": "revisao_manual", "2": "aprovado", "3": "rejeitado"}[escolha],
                           motivo="recusa na revisão manual" if escolha == "3" else None,
                           revisao_manual=True, justificativa=justificativa)
        return analise

    def decidir(self, cliente, status, motivo=None, campo=None, analise=None, corrigido=False):
        """Aplica uma decisão válida; uma aprovação cria e ativa a conta em sequência."""
        self.preparar_cliente(cliente)
        if status not in ("aprovado", "rejeitado", "pendente"):
            return False
        if status == "aprovado":
            if self.campo_invalido(cliente) is not None:
                return False
            if cliente.campo_correcao is not None and not corrigido:
                return False
            if not analise or not analise.get("consentimento"):
                return False
            if analise.get("resultado") == "aprovado" and not analise.get("identidade"):
                return False
        if analise:
            if analise.get("resultado") not in ("aprovado", "rejeitado", "revisao_manual"):
                return False
            if analise["resultado"] == "aprovado" and (
                not analise.get("consentimento") or not analise.get("identidade")
            ):
                return False
            if analise.get("consentimento"):
                self.aceitar_termos(cliente)
            cliente.identidade_verificada = analise["identidade"]
            cliente.analise_kyc = dict(analise)
            self.registrar(cliente, "identidade_verificada", str(cliente.identidade_verificada))
            self.registrar(cliente, "kyc_simulado", dict(analise))
            status = {"aprovado": "aprovado", "rejeitado": "rejeitado",
                      "revisao_manual": "pendente"}[analise["resultado"]]
            motivo = analise.get("motivo")
        cliente.motivo_rejeicao = motivo if status != "aprovado" else None
        cliente.campo_correcao = campo if status == "pendente" else None
        if status == "aprovado":
            if cliente.conta is None:
                cliente.conta = Conta_bancaria()
                self.registrar(cliente, "conta_criada", {"numero": cliente.conta.numero, "status": "inativa"})
            cliente.status = "aprovado"
            self.registrar(cliente, "cliente_aprovado", "Análise concluída.")
            cliente.conta.status = "ativa"
            self.registrar(cliente, "conta_ativada", cliente.conta.numero)
            mensagem = f"Abertura aprovada. Conta {cliente.conta.numero} ativa e disponível."
        else:
            cliente.status = status
            self.registrar(cliente, "decisao", {"status": status, "motivo": motivo, "campo": campo})
            mensagem = f"Abertura {status}. Motivo: {motivo or 'revisão manual'}."
            if campo:
                mensagem += f" Corrigir: {campo}."
        self.notificar(cliente, mensagem)
        return True

    def campo_invalido(self, cliente):
        """Revalida o cadastro completo antes da abertura, incluindo dados de PKLs antigos."""
        from datetime import date
        from validacao_entrada import Validar_entrada

        campos = (("nome", cliente.nome), ("cpf", cliente.cpf))
        for campo, valor in campos:
            validar = Validar_entrada(valor)
            if not isinstance(valor, str):
                return campo
            if not (validar.validar_cpf() if campo == "cpf" else validar.validar_entrada_str()):
                return campo
        if not isinstance(cliente.nascimento, date) or not Validar_entrada("").nascimento_permitido(cliente.nascimento):
            return "nascimento"
        if not isinstance(cliente.endereco, dict):
            return "bairro"
        for campo in ("bairro", "rua", "numero", "referencia"):
            valor = cliente.endereco.get(campo)
            if campo == "numero":
                if type(valor) is not int or valor < 0:
                    return campo
            elif not isinstance(valor, str) or not Validar_entrada(valor).validar_entrada_str():
                return campo
        return None

    def exibir_situacao(self, cliente):
        """Mostra o status real e os dados da conta após a decisão salva."""
        mensagem = Texto_colorido(f"Status: {cliente.status}.")
        if cliente.status == "aprovado":
            mensagem.cor_verde()
        else:
            mensagem.cor_alaranjado()
        if cliente.conta:
            print(f"Conta: {cliente.conta.numero} | Situação: {cliente.conta.status}")
        if cliente.notificacoes:
            print(f"Notificação local: {cliente.notificacoes[-1]['mensagem']}")
