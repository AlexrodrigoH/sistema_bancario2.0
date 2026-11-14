# Sistema Bancário 2.0

**ATENÇÃO -> PRIMEIRO ANO DE ADS, CONHECIMENTOS SUPERFICIAIS, CADA INTEGRACAO E AVANÇO CONDIZ COM AS NOVIDADES APRENDIDAS!**

**Sistema bancário simulado em Python, desenvolvido para estudo de programação, orientação a objetos e modelagem de processos com BPMN 2.0.**

> **Status:** P01 implementado como simulação local: cadastro, consentimento, KYC com listas fictícias, revisão manual, criação e ativação de conta, auditoria e notificações no terminal. Os fluxos possuem testes automatizados; a conferência de identidade é uma etapa manual do exercício.

## Sobre o projeto

O **Sistema Bancário 2.0** é um projeto de aprendizado construído progressivamente, com foco em compreender e implementar o funcionamento de um sistema bancário: do cadastro de clientes às operações financeiras e aos controles internos.

O desenvolvimento segue um **mapeamento BPMN 2.0**, que documenta atividades, decisões, exceções e responsabilidades. Cada processo é dividido em etapas menores, implementadas e testadas antes do avanço para o próximo fluxo.

O objetivo é exercitar **Python, POO, organização em módulos, validação de entradas, depuração, Git e GitHub**, sem depender de soluções prontas.

**Aviso:** este software é exclusivamente educacional. Não é uma instituição financeira, não realiza movimentações reais e não comprova conformidade com requisitos regulatórios.

## Tecnologias e ferramentas

- **Python** — lógica e orientação a objetos;
- **`msvcrt`** — captura de teclas no terminal do Windows;
- **Sequências ANSI** — mensagens coloridas e atualização da linha do terminal;
- **VS Code** — edição e depuração com breakpoints;
- **Git e GitHub** — versionamento do projeto;
- **BPMN 2.0** — modelagem dos processos de negócio.

## Estrutura atual

```text
sistema_bancario2.0/
├── banco_facul.py
├── cliente_registro.py
├── processo_abertura.py
├── listas_simuladas.json
├── retorno.py
├── test_p01.py
├── texto_colorido.py
├── validacao_entrada.py
├── verificacao_de_cliente.py
├── .gitignore
└── README.md
```

| Módulo | Responsabilidade atual ou prevista |

| `banco_facul.py`              | Menu principal, navegação e apresentação de falhas de persistência. 
| `cliente_registro.py`         | Dados do cliente, captura do cadastro, consulta, atualização, análise e persistência em PKL. 
| `processo_abertura.py`        | Consentimento, conferência de identidade, KYC simulado, conta, auditoria e notificações locais. 
| `listas_simuladas.json`       | CPFs fictícios para os caminhos de recusa e revisão manual. 
| `retorno.py`                 | Captura de teclas, máscaras e confirmação ou cancelamento dos campos. 
| `test_p01.py`                | Testes automatizados em arquivos temporários. 
| `texto_colorido.py`           | Apresentação de mensagens no terminal em verde, vermelho e laranja. 
| `validacao_entrada.py`        | Validação de números, strings, teclas e tratamento do fluxo de captura. 
| `verificacao_de_cliente.py`   | Validação do formato e dos dígitos verificadores do CPF. 

> Algumas classes e métodos ainda estão em construção. A presença de um arquivo não significa que sua funcionalidade já esteja concluída.

## O que foi desenvolvido até agora

### Menu e organização

- [x] Menu inicial com opções de cadastrar cliente, consultar cliente e sair.
- [x] Validação inicial da opção digitada, com conversão numérica quando válida.
- [x] Separação de responsabilidades em arquivos e classes.
- [x] Mensagens de saída coloridas com uma classe reutilizável.
- [x] Consulta de clientes aprovados, atualização e pesquisa por nome ou CPF.

### Captura e validação de nomes

- [x] Captura individual de teclas com `msvcrt.getwch()`.
- [x] Exibição do nome na mesma linha, sem limpar a tela inteira.
- [x] Tratamento de Backspace, Enter e ESC no fluxo de captura.
- [x] Filtragem de caracteres digitados com regra de permissões.
- [x] Aceitação de letras Unicode, incluindo caracteres acentuados como `ü`.
- [x] Aceitação de espaços em nomes compostos.
- [x] Rejeição de entradas vazias e com comprimento fora dos limites definidos.
- [x] Verificações iniciais para apóstrofos, caracteres não alfabéticos e três letras idênticas consecutivas.
- [x] Testes manuais de entradas válidas e inválidas, incluindo nomes compostos, caracteres especiais e teclas de controle.
- [ ] Consolidar os comportamentos de confirmação e cancelamento com testes adicionais.
- [ ] Refinar regras para nomes legítimos incomuns e tratamento de apóstrofos.
- [ ] Remover saídas temporárias de depuração antes da entrega do cadastro.

As regras de nomes são **heurísticas de validação de formato**; não comprovam a identidade de uma pessoa e não substituem análise cadastral.

### Padrão de mensagens de erro

Os códigos de validação são organizados por categoria:

| Sufixo | Significado |

| `VN` | Validação numérica 
| `VS` | Validação de strings 
| `VT` | Validação de teclado 
| `MP` | Menu principal 

Os identificadores numéricos e as mensagens podem evoluir durante o desenvolvimento.

## Mapeamento BPMN 2.0

O roadmap está organizado em **11 processos (P00–P10)**:

| Processo | Descrição | Estado |

| **P00** | Jornada bancária — visão geral e integração | Planejado / modelagem 
| **P01** | Cadastro e abertura de conta | **Em desenvolvimento** 
| **P02** | Autenticação, sessões e autorização | Planejado 
| **P03** | Depósitos | Planejado 
| **P04** | Saques | Planejado 
| **P05** | Transferências internas | Planejado 
| **P06** | Consultas de saldo, extratos e comprovantes | Planejado 
| **P07** | Atualização cadastral e encerramento de contas | Planejado 
| **P08** | Conciliação e integridade financeira | Planejado 
| **P09** | Segurança e antifraude | Planejado 
| **P10** | Contestações, estornos e compensações | Planejado 

### P01 — Cadastro e abertura de conta

O fluxo desenhado no BPMN compreende:

1. **Solicitar abertura** de conta.
2. **Informar dados e aceitar termos.**
3. **Validar campos e consentimento.**
4. **Decidir se os dados são válidos.**
5. **Verificar identidade duplicada** e existência de cadastro anterior.
6. **Executar KYC simulado** e checagens em listas fictícias de restrição.
7. **Decidir o resultado da análise:** aprovação, revisão manual ou recusa.
8. **Criar cliente e conta inicialmente inativa**, quando aplicável.
9. **Ativar a conta após aprovação** e registrar auditoria.
10. **Disponibilizar a conta e notificar** o cliente, ou registrar pendência/recusa.

O BPMN original detalha esse fluxo em 16 elementos/etapas. A implementação cobre o exercício local, com identidade conferida manualmente, listas fictícias e notificações registradas no próprio sistema.

**Entregas do P01:**

- [x] Coletar nome, endereço, CPF e data de nascimento.
- [x] Validar matematicamente os dígitos verificadores do CPF.
- [x] Calcular a idade pela data de nascimento e verificar os limites atuais do projeto.
- [x] Executar verificações cadastrais simuladas e permitir revisão manual justificada.
- [x] Detectar clientes duplicados.
- [x] Exigir aceite de termos e registrar aprovação, pendência ou recusa.
- [x] Persistir cliente, conta, histórico e notificações no PKL com substituição por arquivo temporário.
- [x] Testar os caminhos de sucesso, cancelamento e falhas de persistência.

### Uso do fluxo de abertura

1. **Cadastrar cliente:** valida os dados e solicita o aceite dos termos educacionais. Sem aceite, não grava o cadastro.
2. **Analisar clientes pendentes → Analisar pendentes ou concluir abertura antiga:** apresenta os dados, permite marcar erros e solicita a conferência manual de identidade antes da aprovação. O KYC consulta apenas `listas_simuladas.json`.
3. **Revisão manual:** um CPF marcado para revisão exige justificativa. É possível manter pendente, aprovar ou recusar a abertura. Identidade não confirmada mantém o cliente pendente e não cria conta.
4. **Aprovação:** cria uma conta com identificador próprio e estado inativo; registra a aprovação, ativa a conta e registra a notificação local. Os eventos preservam a sequência dessas transições.
5. **Histórico e notificações:** dentro do menu de análise, pesquise pelo CPF para conferir os eventos datados e as mensagens de qualquer status. As datas do histórico usam UTC, indicado pelo deslocamento `+00:00`.

As listas iniciais são exclusivamente fictícias: `11144477735` exercita recusa e `12345678909` exercita revisão manual. `52998224725` permite testar o caminho de aprovação após conferência de identidade. Esses exemplos não informam a situação real de nenhuma pessoa.

Clientes antigos não recebem aceite, conta ou análise presumidos. Os aprovados que ainda não têm conta aparecem também na opção de concluir abertura antiga. O arquivo existente só é atualizado após uma ação confirmada.

O menu principal mantém **4 — Atualizar dados** e **5 — Sair**. A atualização de um cadastro aprovado preserva seu status e número de conta e acrescenta eventos ao histórico. Uma correção ainda marcada precisa ser resolvida pela subopção de correções antes da aprovação.

## Diretrizes para os próximos processos

Conforme a evolução do projeto, serão estudados e implementados:

- **Identidade e acesso:** login, credenciais protegidas, autorização e controle de sessões.
- **Movimentações:** depósitos, saques e transferências com validações de saldo, limites e estados.
- **Histórico financeiro:** lançamentos, extratos, comprovantes e auditoria.
- **Integridade:** operações rastreáveis, idempotência e prevenção de movimentações duplicadas.
- **Controles:** conciliação, tratamento de falhas, revisão de risco e estornos documentados.

Para valores monetários, a arquitetura planejada prevê **`Decimal` ou centavos inteiros**, evitando `float` nos cálculos contábeis. Quando o projeto exigir atomicidade, a persistência deverá evoluir para uma solução transacional; arquivos JSON podem ser úteis no protótipo, mas não oferecem essas garantias isoladamente.

## Execução

**Requisitos atuais:** Python 3 e **Windows** para a captura por `msvcrt`.

No terminal, dentro da pasta do projeto:

```bash
python banco_facul.py
```

Em ambientes que utilizam o comando `py`:

```bash
py banco_facul.py
```

> A implementação atual é voltada ao terminal do Windows e utiliza sequências ANSI. O funcionamento em Linux ou macOS exigirá adaptação da captura de teclado.

## Desenvolvimento e testes

A implementação é incremental: cada novo comportamento é testado no terminal e revisado com o debugger do VS Code. Os cenários testados até aqui incluem campos vazios, nomes compostos, acentuação, caracteres inválidos, repetições excessivas e interação com teclas especiais.

Execute a suíte do P01 no Windows:

```bash
python -B -m unittest test_p01 -v
```

Os testes usam arquivos temporários e entradas simuladas; não alteram `clientes.pkl`. Cada módulo e função Python possui uma docstring explicando sua responsabilidade. A validação de nascimento e idade fica em `Validar_entrada`; a verificação matemática do CPF fica em `Validar_cpf`.

## Documentação BPMN

O planejamento utiliza arquivos `.bpmn`, mapas visuais e checklists de implementação. Caso os arquivos sejam adicionados ao repositório, recomenda-se organizá-los em uma pasta `docs/bpmn/`, mantendo uma referência para cada processo.

Ferramentas para abrir os diagramas: [bpmn.io](https://demo.bpmn.io/new) ou Camunda Modeler.(ainda sera disponibilizado)

Padrão de referência: [OMG — BPMN 2.0.2](https://www.omg.org/spec/BPMN/).

## Objetivo de aprendizado

Mais do que entregar um programa que funcione, o projeto busca compreender **por que cada decisão de implementação é necessária**, como os módulos se comunicam, como identificar erros com depuração e como construir um sistema progressivamente mais completo e rastreável.

**Projeto em evolução.** As funcionalidades marcadas como planejadas ainda não devem ser consideradas implementadas.
