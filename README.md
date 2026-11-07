# Sistema Bancário 2.0

**ATENÇÃO -> PRIMEIRO ANO DE ADS, CONHECIMENTOS SUPERFICIAIS, CADA INTEGRACAO E AVANÇO CONDIZ COM AS NOVIDADES APRENDIDAS!**

**Sistema bancário simulado em Python, desenvolvido para estudo de programação, orientação a objetos e modelagem de processos com BPMN 2.0.**

> **Status:** em desenvolvimento — etapa **P01: Cadastro e abertura de conta**. A captura e a validação inicial de nomes já possuem uma implementação funcional e foram submetidas a testes manuais. O cadastro bancário completo ainda não está concluído.

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
├── texto_colorido.py
├── validacao_entrada.py
├── verificacao_de_cliente.py
├── .gitignore
└── README.md
```

| Módulo | Responsabilidade atual ou prevista |

| `banco_facul.py`              | Menu principal, navegação e captura de dados do usuário. 
| `cliente_registro.py`         | Modelagem dos dados do cliente, incluindo endereço e estrutura inicial de registro/persistência. 
| `texto_colorido.py`           | Apresentação de mensagens no terminal em verde, vermelho e laranja. 
| `validacao_entrada.py`        | Validação de números, strings, teclas e tratamento do fluxo de captura. 
| `verificacao_de_cliente.py`   | Estrutura inicial para verificar idade, nascimento e CPF. 

> Algumas classes e métodos ainda estão em construção. A presença de um arquivo não significa que sua funcionalidade já esteja concluída.

## O que foi desenvolvido até agora

### Menu e organização

- [x] Menu inicial com opções de cadastrar cliente, consultar cliente e sair.
- [x] Validação inicial da opção digitada, com conversão numérica quando válida.
- [x] Separação de responsabilidades em arquivos e classes.
- [x] Mensagens de saída coloridas com uma classe reutilizável.
- [ ] Consulta efetiva de clientes cadastrados.

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
2. **Informar dados e aceitar termos.** ← **etapa atual**, com foco inicial nas entradas e validações.
3. **Validar campos e consentimento.**
4. **Decidir se os dados são válidos.**
5. **Verificar identidade duplicada** e existência de cadastro anterior.
6. **Executar KYC simulado** e checagens em listas fictícias de restrição.
7. **Decidir o resultado da análise:** aprovação, revisão manual ou recusa.
8. **Criar cliente e conta inicialmente inativa**, quando aplicável.
9. **Ativar a conta após aprovação** e registrar auditoria.
10. **Disponibilizar a conta e notificar** o cliente, ou registrar pendência/recusa.

O BPMN original detalha esse fluxo em 16 elementos/etapas. A etapa atual **não equivale ao P01 concluído**.

**Próximas entregas previstas para P01:**

- [ ] Completar a coleta de nome, endereço, CPF e data de nascimento.
- [ ] Validar matematicamente os dígitos verificadores do CPF.
- [ ] Conferir coerência entre idade declarada e data de nascimento, considerando o aniversário no ano corrente.
- [ ] Implementar verificações cadastrais simuladas sob regras definidas pelo projeto.
- [ ] Detectar clientes duplicados.
- [ ] Implementar aceite de termos, estados de aprovação, pendência e recusa.
- [ ] Persistir os dados do cliente e da conta com tratamento adequado de erros.
- [ ] Criar testes para caminhos de sucesso e exceção previstos no BPMN.

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

**Ainda não há indicação de uma suíte automatizada de testes neste estágio.** Testes automatizados fazem parte da evolução planejada.

## Documentação BPMN

O planejamento utiliza arquivos `.bpmn`, mapas visuais e checklists de implementação. Caso os arquivos sejam adicionados ao repositório, recomenda-se organizá-los em uma pasta `docs/bpmn/`, mantendo uma referência para cada processo.

Ferramentas para abrir os diagramas: [bpmn.io](https://demo.bpmn.io/new) ou Camunda Modeler.(ainda sera disponibilizado)

Padrão de referência: [OMG — BPMN 2.0.2](https://www.omg.org/spec/BPMN/).

## Objetivo de aprendizado

Mais do que entregar um programa que funcione, o projeto busca compreender **por que cada decisão de implementação é necessária**, como os módulos se comunicam, como identificar erros com depuração e como construir um sistema progressivamente mais completo e rastreável.

**Projeto em evolução.** As funcionalidades marcadas como planejadas ainda não devem ser consideradas implementadas.
