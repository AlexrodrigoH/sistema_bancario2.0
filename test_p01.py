"""Testes do P01 com cadastros fictícios e arquivos temporários, sem tocar clientes.pkl.

Execute com: python -B -m unittest test_p01 -v
"""

import ast
import io
import pickle
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path
from unittest.mock import patch

import banco_facul
import cliente_registro as registro
from processo_abertura import Processo_abertura


class Testar_p01(unittest.TestCase):
    """Verifica decisões, persistência, compatibilidade e navegação do processo."""

    def setUp(self):
        """Isola os arquivos e captura as mensagens para deixar a execução legível."""
        self.pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self.pasta.cleanup)
        self.caminho = Path(self.pasta.name) / "clientes.pkl"
        self.saida = io.StringIO()
        captura = redirect_stdout(self.saida)
        captura.__enter__()
        self.addCleanup(captura.__exit__, None, None, None)
        self.salvar = registro.Salvar_cliente_arquivo()
        self.processo = Processo_abertura()

    def criar_cliente(self, cpf="52998224725", nome="ANA SILVA", aceite=True):
        """Monta uma solicitação válida com endereço e aceite explícito opcional."""
        cliente = registro.Dados_do_cliente(nome, date(2000, 1, 1), cpf)
        cliente.endereco_cliente("Centro", "Flores", 12, "Praca")
        if aceite:
            self.processo.aceitar_termos(cliente)
        return cliente

    def analisar(self, cliente, respostas):
        """Executa a análise real substituindo somente as respostas de teclado."""
        with patch("builtins.input", side_effect=respostas):
            return self.processo.solicitar_analise(cliente)

    def carregar(self):
        """Recupera o primeiro cadastro do arquivo temporário do teste."""
        return self.salvar.listar_clientes(self.caminho)[0]

    def test_consentimento_obrigatorio_e_duplicidade(self):
        """Impede gravação sem aceite e impede acrescentar CPF repetido."""
        cliente = self.criar_cliente(aceite=False)
        self.assertFalse(self.salvar.cliente_salvo(cliente, self.caminho))
        self.assertFalse(self.caminho.exists())
        with patch("builtins.input", return_value="0"):
            self.assertFalse(self.processo.solicitar_consentimento())
        self.processo.aceitar_termos(cliente)
        self.assertTrue(self.salvar.cliente_salvo(cliente, self.caminho))
        original = self.caminho.read_bytes()
        self.assertFalse(self.salvar.cliente_salvo(cliente, self.caminho))
        self.assertEqual(original, self.caminho.read_bytes())
        self.assertTrue(self.carregar().consentimento_em)

    def test_aprovacao_cria_conta_e_auditoria(self):
        """Exige identidade e KYC antes de criar a conta inativa e depois ativá-la."""
        cliente = self.criar_cliente()
        self.salvar.cliente_salvo(cliente, self.caminho)
        original = self.caminho.read_bytes()
        self.assertFalse(self.salvar.alterar_status(cliente.cpf, "aprovado", self.caminho))
        self.assertEqual(original, self.caminho.read_bytes())
        analise = self.analisar(cliente, ["1"])
        self.assertTrue(self.salvar.alterar_status(cliente.cpf, "aprovado", self.caminho, analise=analise))
        salvo = self.carregar()
        self.assertEqual(salvo.status, "aprovado")
        self.assertEqual(salvo.conta.status, "ativa")
        eventos = [evento["evento"] for evento in salvo.auditoria]
        self.assertLess(eventos.index("conta_criada"), eventos.index("cliente_aprovado"))
        self.assertLess(eventos.index("cliente_aprovado"), eventos.index("conta_ativada"))
        criacao = next(evento for evento in salvo.auditoria if evento["evento"] == "conta_criada")
        self.assertEqual(criacao["detalhes"]["status"], "inativa")
        numero = salvo.conta.numero
        self.assertFalse(self.salvar.alterar_status(cliente.cpf, "aprovado", self.caminho, analise=analise))
        self.assertEqual(self.carregar().conta.numero, numero)
        self.assertIn("ativa", salvo.notificacoes[-1]["mensagem"])

    def test_listas_simuladas_e_revisao(self):
        """Cobre negativação, revisão pendente, aprovação manual e recusa manual."""
        cenarios = [
            ("11144477735", ["1"], "rejeitado"),
            ("12345678909", ["1", "1", "Aguardando conferência"], "pendente"),
            ("12345678909", ["1", "2", "Conferência concluída"], "aprovado"),
            ("12345678909", ["1", "3", "Inconsistência confirmada"], "rejeitado"),
            ("52998224725", ["2"], "pendente"),
        ]
        for indice, (cpf, respostas, esperado) in enumerate(cenarios):
            with self.subTest(cpf=cpf, status=esperado):
                caminho = self.caminho.with_name(f"cenario_{indice}.pkl")
                cliente = self.criar_cliente(cpf)
                self.salvar.cliente_salvo(cliente, caminho)
                analise = self.analisar(cliente, respostas)
                self.assertTrue(self.salvar.alterar_status(cpf, "aprovado", caminho, analise=analise))
                salvo = self.salvar.listar_clientes(caminho)[0]
                self.assertEqual(salvo.status, esperado)
                self.assertEqual(salvo.conta is not None, esperado == "aprovado")

    def test_cancelamento_e_falha_nas_listas(self):
        """Não decide quando o operador cancela, omite justificativa ou faltam listas."""
        cliente = self.criar_cliente("12345678909")
        self.salvar.cliente_salvo(cliente, self.caminho)
        original = self.caminho.read_bytes()
        for respostas in (["0"], ["1", "0"], ["1", "2", ""]):
            self.assertIsNone(self.analisar(cliente, respostas))
        with patch.object(Processo_abertura, "avaliar_kyc", side_effect=OSError("indisponível")):
            self.assertIsNone(self.analisar(cliente, ["1"]))
        self.assertEqual(original, self.caminho.read_bytes())

    def test_correcao_revalida_cpf_e_preserva_outros_clientes(self):
        """Troca o CPF marcado, executa o KYC do novo CPF e mantém o outro registro intacto."""
        cliente = self.criar_cliente()
        outro = self.criar_cliente("11144477735", "BIA SILVA")
        self.salvar.cliente_salvo(cliente, self.caminho)
        self.salvar.cliente_salvo(outro, self.caminho)
        self.salvar.alterar_status(cliente.cpf, "pendente", self.caminho,
                                 "erro na inserção de dados", "cpf")
        original = self.caminho.read_bytes()
        self.assertFalse(self.salvar.salvar_correcao(cliente.cpf, outro.cpf, "aprovado", self.caminho))
        self.assertEqual(original, self.caminho.read_bytes())
        with patch("builtins.input", side_effect=["1", "1", "1", "1"]), patch.object(
            registro.retorno.msvcrt, "getwch", side_effect=list("16899535009\r")
        ):
            registro.Analisar_clientes().corrigir_cliente(self.caminho)
        clientes = self.salvar.listar_clientes(self.caminho)
        self.assertEqual(clientes[0].cpf, "16899535009")
        self.assertEqual(clientes[0].status, "aprovado")
        self.assertIsNone(clientes[0].campo_correcao)
        self.assertEqual(vars(clientes[1]), vars(outro))

    def test_campo_marcado_bloqueia_aprovacao_direta(self):
        """Impede ignorar uma correção ainda pendente no menu de análise."""
        cliente = self.criar_cliente()
        self.salvar.cliente_salvo(cliente, self.caminho)
        self.salvar.alterar_status(cliente.cpf, "pendente", self.caminho,
                                 "erro na inserção de dados", "nome")
        original = self.caminho.read_bytes()
        with patch("builtins.input", side_effect=["1", "1"]):
            registro.Analisar_clientes().analisar_pendentes(self.caminho)
        self.assertEqual(original, self.caminho.read_bytes())

    def test_legado_nao_inventa_consentimento_ou_conta(self):
        """Carrega um objeto antigo e só conclui sua abertura após análise explícita."""
        cliente = self.criar_cliente(aceite=False)
        cliente.status = "aprovado"
        for atributo in ("conta", "auditoria", "notificacoes", "consentimento",
                         "consentimento_em", "analise_kyc", "identidade_verificada"):
            delattr(cliente, atributo)
        with self.caminho.open("wb") as arquivo:
            pickle.dump(cliente, arquivo)
        salvo = self.carregar()
        self.assertFalse(salvo.consentimento)
        self.assertIsNone(salvo.conta)
        with patch("builtins.input", side_effect=["1", "1", "1", "1"]):
            registro.Analisar_clientes().analisar_pendentes(self.caminho)
        self.assertEqual(self.carregar().conta.status, "ativa")
        self.assertTrue(self.carregar().consentimento)

    def test_falha_de_gravacao_preserva_original(self):
        """Simula falha na substituição e verifica integridade do arquivo anterior."""
        cliente = self.criar_cliente()
        self.salvar.cliente_salvo(cliente, self.caminho)
        original = self.caminho.read_bytes()
        with patch.object(registro.os, "replace", side_effect=PermissionError("arquivo bloqueado")):
            with self.assertRaises(PermissionError):
                self.salvar.alterar_status(cliente.cpf, "rejeitado", self.caminho, "negativado")
        self.assertEqual(original, self.caminho.read_bytes())
        self.assertEqual(list(Path(self.pasta.name).iterdir()), [self.caminho])

    def test_historico_individual_e_atualizacao(self):
        """Mantém conta e histórico vinculados ao cliente após uma atualização cadastral."""
        cliente = self.criar_cliente()
        self.salvar.cliente_salvo(cliente, self.caminho)
        analise = self.analisar(cliente, ["1"])
        self.salvar.alterar_status(cliente.cpf, "aprovado", self.caminho, analise=analise)
        numero = self.carregar().conta.numero
        self.salvar.salvar_atualizacao(cliente.cpf, "rua", "Jardins", self.caminho)
        self.assertEqual(self.carregar().conta.numero, numero)
        self.assertEqual(self.carregar().endereco["rua"], "Jardins")
        with patch("builtins.input", return_value=cliente.cpf):
            registro.Analisar_clientes().consultar_historico(self.caminho)
        self.assertIn("dado_atualizado", self.saida.getvalue())

    def test_menu_trata_falha_e_mantem_saida_cinco(self):
        """Apresenta erro de persistência e permite sair normalmente na opção cinco."""
        with patch("builtins.input", side_effect=["2", "5"]), patch.object(
            registro.Consultar_clientes, "consultar_aprovados", side_effect=OSError("falha simulada")
        ):
            banco_facul.executar_menu()
        self.assertIn("Falha ao acessar os registros", self.saida.getvalue())

    def test_cadastro_completo_pelo_teclado(self):
        """Percorre a captura real dos sete campos e exige aceite antes de retornar o objeto."""
        teclas = "ANA SILVA\r01012000\r52998224725\rCentro\rFlores\r12\rPraca\r"
        with patch("builtins.input", return_value="1"), patch.object(
            registro.retorno.msvcrt, "getwch", side_effect=list(teclas)
        ), patch.object(registro.Salvar_cliente_arquivo, "cliente_existe", return_value=False):
            cliente = registro.Cliente_novo().novo_cliente()
        self.assertTrue(cliente.consentimento)
        self.assertEqual(cliente.endereco["numero"], 12)
        self.assertTrue(self.salvar.cliente_salvo(cliente, self.caminho))
        self.assertIsNone(self.carregar().conta)
        with patch("builtins.input", return_value="0"), patch.object(
            registro.retorno.msvcrt, "getwch", side_effect=list(teclas)
        ), patch.object(registro.Salvar_cliente_arquivo, "cliente_existe", return_value=False):
            self.assertIsNone(registro.Cliente_novo().novo_cliente())

    def test_correcao_dos_sete_campos_e_cancelamento(self):
        """Exercita as validações de cada campo e verifica que cancelar não grava nada."""
        valores = [
            ("nome", "MARIA SILVA", "MARIA SILVA"),
            ("nascimento", "02022001", date(2001, 2, 2)),
            ("cpf", "16899535009", "16899535009"),
            ("bairro", "Jardim", "Jardim"),
            ("rua", "Rosas", "Rosas"),
            ("numero", "A42", 42),
            ("referencia", "Igreja", "Igreja"),
        ]
        for campo, entrada, esperado in valores:
            with self.subTest(campo=campo):
                cliente = self.criar_cliente()
                cliente.campo_correcao = campo
                self.salvar.regravar_clientes([cliente], self.caminho)
                with patch("builtins.input", side_effect=["1", "1", "1", "1"]), patch.object(
                    registro.retorno.msvcrt, "getwch", side_effect=list(entrada + "\r")
                ):
                    registro.Analisar_clientes().corrigir_cliente(self.caminho)
                salvo = self.carregar()
                valor = getattr(salvo, campo) if campo in ("nome", "cpf", "nascimento") else salvo.endereco[campo]
                self.assertEqual(valor, esperado)
                self.assertEqual(salvo.status, "aprovado")
        cliente = self.criar_cliente()
        cliente.campo_correcao = "nome"
        self.salvar.regravar_clientes([cliente], self.caminho)
        original = self.caminho.read_bytes()
        with patch("builtins.input", side_effect=["1", "0"]), patch.object(
            registro.retorno.msvcrt, "getwch", side_effect=list("MARIA\r")
        ):
            registro.Analisar_clientes().corrigir_cliente(self.caminho)
        self.assertEqual(original, self.caminho.read_bytes())

    def test_clientes_possuem_contas_e_historicos_independentes(self):
        """Confere a separação dos objetos, números de conta e eventos de dois clientes."""
        primeiro = self.criar_cliente()
        segundo = self.criar_cliente("16899535009", "BIA SILVA")
        for cliente in (primeiro, segundo):
            self.salvar.cliente_salvo(cliente, self.caminho)
            analise = self.analisar(cliente, ["1"])
            self.salvar.alterar_status(cliente.cpf, "aprovado", self.caminho, analise=analise)
        a, b = self.salvar.listar_clientes(self.caminho)
        self.assertNotEqual(a.conta.numero, b.conta.numero)
        self.assertIsNot(a.auditoria, b.auditoria)
        self.assertIsNot(a.notificacoes, b.notificacoes)
        self.assertIsNot(a.endereco, b.endereco)
        self.assertNotIn(a.conta.numero, str(b.auditoria))

    def test_registro_truncado_nao_e_sobrescrito(self):
        """Uma leitura incompleta interrompe a gravação e preserva o arquivo para investigação."""
        cliente = self.criar_cliente()
        with self.caminho.open("wb") as arquivo:
            arquivo.write(pickle.dumps(cliente)[:-4])
        original = self.caminho.read_bytes()
        with self.assertRaises((pickle.UnpicklingError, EOFError)):
            self.salvar.cliente_salvo(self.criar_cliente("16899535009"), self.caminho)
        self.assertEqual(original, self.caminho.read_bytes())

    def test_modulos_e_funcoes_documentados(self):
        """Confere que todos os módulos e métodos Python possuem comentários explicativos."""
        for caminho in Path(__file__).parent.glob("*.py"):
            arvore = ast.parse(caminho.read_text(encoding="utf-8"))
            self.assertTrue(ast.get_docstring(arvore), str(caminho))
            for no in ast.walk(arvore):
                if isinstance(no, ast.FunctionDef):
                    self.assertTrue(ast.get_docstring(no), f"{caminho.name}: {no.name}")

if __name__ == "__main__":
    unittest.main()
