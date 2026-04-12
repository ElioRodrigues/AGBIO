# Plataforma Multiagente para Validação de Dados Toxicológicos e Geração de Relatórios Técnico-Científicos

## Visão Geral

Este projeto tem como objetivo desenvolver uma **API inteligente baseada em agentes de IA** para apoiar a análise de dados experimentais em **toxicologia pré-clínica** e a **geração automatizada de relatórios técnico-científicos**, com foco em **qualidade dos dados**, **rastreabilidade**, **reprodutibilidade**, **padronização técnica** e **conformidade documental**.

A proposta foi inspirada no contexto de soluções voltadas à modernização da análise toxicológica, especialmente em cenários onde há necessidade de integrar diferentes tipos de dados experimentais e transformar esses dados em saídas técnicas consistentes, auditáveis e úteis para fins científicos e regulatórios.

O sistema deverá atuar como uma camada de apoio técnico à análise de estudos toxicológicos, auxiliando na identificação de falhas de integridade, inconsistências, padrões relevantes, limitações analíticas e possíveis interpretações preliminares, sempre com linguagem científica cautelosa e com clara separação entre:
- dado observado
- interpretação técnica
- inferência preliminar
- conclusão sujeita à revisão humana

---

## Problema

Em fluxos experimentais de toxicologia, especialmente em ambientes acadêmicos, laboratoriais e pré-regulatórios, é comum enfrentar dificuldades como:

- dados experimentais dispersos em múltiplas planilhas ou estruturas heterogêneas
- ausência de padronização entre coletas, variáveis e identificadores
- presença de campos ausentes, inconsistências e duplicidades
- dificuldade de integrar dados bioquímicos, histológicos, comportamentais e documentais
- análise manual lenta e suscetível a erro
- esforço elevado na produção de relatórios técnico-científicos
- dificuldade de manter rastreabilidade analítica e conformidade documental
- ausência de uma trilha clara que permita auditoria das decisões tomadas ao longo da análise

Além disso, em contextos regulatórios ou de maior exigência técnica, não basta apenas produzir um texto final. É necessário garantir que a análise:
- seja tecnicamente justificável
- seja reproduzível
- esteja baseada nos dados realmente recebidos
- explicite limitações e pontos de revisão humana
- não extrapole além da evidência disponível

Este projeto surge para atacar esse problema por meio de uma arquitetura híbrida que combina:
1. **validação determinística**
2. **agentes especializados de IA**
3. **saídas estruturadas**
4. **mecanismos de auditoria e rastreabilidade**

---

## Objetivo Geral

Desenvolver uma API multiagente capaz de receber dados de estudos toxicológicos, avaliar sua qualidade, identificar inconsistências e padrões relevantes, produzir interpretações técnicas preliminares e gerar relatórios estruturados com linguagem científica e conformidade documental.

---

## Objetivos Específicos

- classificar o tipo de estudo e os domínios de dados recebidos
- validar a integridade e completude dos dados experimentais
- identificar erros, lacunas, incoerências e possíveis inconsistências documentais
- detectar padrões relevantes e valores atípicos nos dados
- apoiar a interpretação preliminar de biomarcadores e achados experimentais
- gerar relatórios técnico-científicos estruturados
- registrar uma trilha de auditoria das decisões analíticas
- manter separação clara entre observação, interpretação e conclusão
- permitir revisão humana em casos de baixa confiança, conflito de evidências ou insuficiência de dados

---

## Proposta da Solução

A solução proposta é uma **API backend orientada a agentes**, na qual cada agente possui uma responsabilidade técnica específica dentro do pipeline analítico.

Em vez de utilizar um único modelo de IA para realizar todas as tarefas, o sistema será dividido em módulos especializados, reduzindo ambiguidade, melhorando a controlabilidade e aumentando a confiabilidade das saídas.

A arquitetura combinará:
- regras determinísticas para validação estrutural e integridade
- agentes de IA para classificação contextual, interpretação textual e geração de relatório
- contratos JSON rígidos para comunicação entre módulos
- trilha de auditoria para rastreamento das decisões produzidas

---

## Escopo do Projeto

### Escopo funcional do MVP

O MVP deverá ser capaz de:

1. receber dados de um estudo experimental em formato estruturado
2. identificar o tipo de estudo e os domínios de dados presentes
3. validar consistência, completude e integridade dos dados recebidos
4. apontar erros, alertas e limitações
5. identificar padrões e outliers relevantes
6. produzir interpretação técnica preliminar, sem extrapolação indevida
7. gerar um relatório técnico estruturado
8. registrar informações de auditoria e revisão humana

### Entradas previstas no MVP

O sistema deverá aceitar, inicialmente, entradas como:
- metadados do estudo
- resumo do protocolo experimental
- datasets tabulares
- descrição dos grupos experimentais
- variáveis observadas
- objetivo regulatório ou técnico da análise

Exemplos de domínios de dados aceitos:
- bioquímicos
- comportamentais
- histológicos
- documentais
- estatísticos

### Saídas previstas no MVP

O sistema deverá retornar:
- classificação do estudo
- avaliação de completude
- score de qualidade dos dados
- lista de erros e avisos
- padrões detectados
- outliers identificados
- interpretações técnicas preliminares
- relatório técnico-científico estruturado
- pontos recomendados para revisão humana
- trilha de auditoria da análise

---

## Fora do Escopo do MVP

Para manter o projeto viável e bem delimitado, os seguintes itens ficam fora do escopo inicial:

- OCR avançado para leitura irrestrita de documentos digitalizados
- leitura livre e não estruturada de PDFs complexos
- integração profunda e automática com sistemas laboratoriais externos
- automação completa de decisão regulatória
- substituição de especialista humano
- emissão final de parecer oficial
- inferência clínica
- comparação simultânea aprofundada com múltiplos marcos regulatórios complexos
- frontend completo e avançado
- pipeline de produção em larga escala
- ambiente multi-tenant
- automação documental completa em PDF/DOCX na primeira versão
- conectores externos complexos via MCP na fase inicial

---

## Princípios Técnicos do Sistema

Este projeto será guiado pelos seguintes princípios:

### 1. Rastreabilidade
Toda conclusão produzida pelo sistema deve poder ser relacionada às entradas analisadas e ao agente responsável pela saída.

### 2. Reprodutibilidade
Dado o mesmo conjunto de entradas e regras, o sistema deve produzir resultados consistentes e previsíveis.

### 3. Conformidade documental
A geração de relatórios e interpretações deve seguir organização técnica adequada, com linguagem formal, objetiva e proporcional à evidência disponível.

### 4. Separação de responsabilidades
Cada agente deve executar uma função específica, evitando acúmulo indevido de responsabilidades em um único módulo.

### 5. Saída estruturada
Toda resposta que alimente outro módulo deve estar em formato JSON válido e aderente a schema definido.

### 6. Controle de inferência
O sistema não deve inventar informações ausentes, corrigir silenciosamente dados inválidos ou produzir conclusões acima do que os dados sustentam.

### 7. Revisão humana como salvaguarda
Em situações de conflito, ambiguidade, baixa confiança ou insuficiência de evidência, o sistema deve sinalizar necessidade de revisão humana.

---

## Arquitetura Conceitual

O projeto será estruturado como uma API com orquestração central e múltiplos agentes especializados.

### Agentes previstos

#### 1. Study Classifier
Responsável por identificar:
- tipo de estudo
- domínios de dados presentes
- contexto analítico
- template técnico mais adequado

#### 2. Data Validator
Responsável por verificar:
- campos obrigatórios ausentes
- valores nulos
- incompatibilidade de tipos
- duplicidades
- inconsistências entre registros
- divergências entre protocolo e dados entregues

#### 3. Pattern Detector
Responsável por detectar:
- outliers
- tendências relevantes
- padrões comparativos entre grupos
- achados que mereçam atenção técnica

#### 4. Biomarker Interpreter
Responsável por produzir interpretação preliminar de achados bioquímicos, histológicos e comportamentais, com linguagem científica cautelosa.

#### 5. Report Generator
Responsável por consolidar as saídas dos agentes anteriores em um relatório estruturado e tecnicamente coerente.

#### 6. Audit Agent
Responsável por registrar:
- entradas utilizadas
- saídas produzidas
- agentes executados
- conflitos encontrados
- pontos que exigem revisão humana

### Orquestrador
Além dos agentes, haverá um **orquestrador central**, responsável por:
- definir a sequência de execução
- encaminhar dados corretos a cada agente
- consolidar resultados
- controlar falhas e estados intermediários

---

## Estratégia Híbrida: Regras Determinísticas + IA

Um dos princípios centrais do projeto é que **nem tudo deve ser resolvido com IA**.

### Validação determinística será usada para:
- schema
- obrigatoriedade de campos
- tipos de dados
- duplicidade de identificadores
- coerência estrutural
- checagens básicas de completude
- verificação de presença mínima de colunas
- regras objetivas de consistência

### IA será usada para:
- classificação contextual do estudo
- interpretação técnica preliminar
- sumarização científica
- padronização da linguagem
- geração de seções textuais do relatório
- apoio à identificação de padrões relevantes descritos de forma técnica

Essa abordagem reduz risco de alucinação e aumenta robustez técnica do sistema.

---

## Requisitos Funcionais

- receber payload estruturado contendo dados de estudo
- classificar o estudo com base no contexto recebido
- validar integridade e completude dos dados
- gerar score de qualidade
- listar erros e avisos com severidade
- detectar padrões relevantes e outliers
- produzir interpretações preliminares com nível de confiança
- gerar relatório técnico estruturado
- registrar pontos de revisão humana
- disponibilizar trilha de auditoria das análises

---

## Requisitos Não Funcionais

- tipagem forte nos contratos internos
- validação estrita de entrada e saída
- modularidade
- extensibilidade para novos agentes e novos domínios
- previsibilidade na orquestração
- logs claros
- facilidade de teste
- clareza dos schemas JSON
- tolerância controlada a falhas
- capacidade de rejeitar ou sinalizar análises insuficientes

---

## Restrições do Projeto

- o sistema não substitui especialista humano
- o sistema não deve emitir conclusões definitivas sem base suficiente
- o sistema não deve inferir causalidade automaticamente
- o sistema não deve corrigir dados silenciosamente
- o sistema não deve mascarar incerteza
- toda interpretação deve ser explicitamente limitada pela evidência disponível
- toda comunicação entre módulos deve ser estruturada

---

## Público-Alvo

Este projeto é voltado, prioritariamente, para contextos como:
- pesquisadores da área de toxicologia
- laboratórios acadêmicos e experimentais
- equipes que trabalham com dados pré-clínicos
- grupos envolvidos em organização e análise de estudos toxicológicos
- contextos de apoio à documentação técnico-científica e regulatória

---

## Exemplo de Fluxo de Uso

1. Um estudo é enviado à API com metadados, protocolo resumido e datasets.
2. O sistema classifica o estudo e identifica os domínios dos dados.
3. O validador analisa a integridade e qualidade da entrada.
4. O detector de padrões verifica outliers e comportamentos relevantes.
5. O interpretador produz leituras técnicas preliminares.
6. O gerador de relatório consolida os resultados.
7. O agente de auditoria registra o processo.
8. A API retorna um pacote estruturado com achados, relatório e pontos de revisão humana.

---

## Exemplo de Estrutura de Resposta Esperada

As respostas do sistema deverão seguir contratos estruturados, como:

- `study_classification`
- `quality_assessment`
- `patterns_and_outliers`
- `technical_interpretation`
- `report`
- `audit_trace`

Cada módulo deverá informar, quando aplicável:
- `confidence`
- `limitations`
- `requires_human_review`

---

## Stack Inicial Pretendida

A stack inicial sugerida para o MVP é:

- **FastAPI** para a API backend
- **Pydantic** para schemas e validação
- **PostgreSQL** para persistência
- **Redis** para suporte a cache ou filas, se necessário
- **serviços de agentes** desacoplados por módulo
- **Antigravity** como ambiente de construção, organização e evolução do projeto

Essa stack foi escolhida por favorecer:
- velocidade de implementação
- clareza de contratos
- facilidade de validação
- modularidade
- boa aderência a APIs orientadas a dados estruturados

---

## Como executar localmente

### Pré-requisitos

Antes de rodar o projeto localmente, é recomendado ter:

- Python 3.10 ou superior
- ambiente Linux, macOS ou Windows com terminal
- `python3-venv` disponível no sistema
- acesso ao terminal na raiz do projeto

---

### 1. Criar e ativar ambiente virtual

No Ubuntu ou sistemas compatíveis:

```bash
python3 -m venv .venv
source .venv/bin/activate

No Windows PowerShell:

python -m venv .venv
.venv\Scripts\Activate.ps1

2. Instalar dependências

Com o ambiente virtual ativado:

pip install -r requirements.txt

3. Criar o arquivo .env

cp .env.example .env

Se estiver no Windows PowerShell:

Copy-Item .env.example .env

4. Escolher o modo de execução

O projeto pode rodar em dois modos:

Modo stub

Nesse modo, o sistema funciona sem chamar modelos reais de IA.
É o modo mais seguro para desenvolvimento inicial, demonstrações estruturais e execução por colegas sem chave de API.

Exemplo de .env:

APP_NAME="Toxicology Meta-Agent API"
LLM_PROVIDER="stub"
GEMINI_MODEL="gemini-2.5-flash"

Modo gemini

Nesse modo, agentes integrados usam a Gemini API real.

Exemplo de .env:

APP_NAME="Toxicology Meta-Agent API"
LLM_PROVIDER="gemini"
GEMINI_API_KEY="SUA_CHAVE_AQUI"
GEMINI_MODEL="gemini-2.5-flash"

5. Subir a API localmente

Na raiz do projeto:

PYTHONPATH=src uvicorn src.main:app --reload

Se tudo estiver correto, a API ficará disponível em:

http://127.0.0.1:8000

A documentação interativa Swagger ficará em:

http://127.0.0.1:8000/docs

6. Testar a API

O endpoint principal do MVP é:

POST /api/v1/studies/analyze

Você pode testá-lo:

pelo Swagger (/docs)
por curl
com os exemplos da pasta examples/

Arquivos de exemplo disponíveis:

examples/valid_study.json
examples/invalid_study_missing_datasets.json
examples/invalid_study_missing_groups.json

Exemplo de teste com curl:

curl -X POST "http://127.0.0.1:8000/api/v1/study/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d @examples/valid_study.json


  7. Comportamento esperado
Quando o payload for válido

A API deve:

passar pela validação determinística
executar o pipeline
retornar classificação, validação, relatório e auditoria
Quando o payload for inválido

A API deve:

falhar na validação determinística
interromper o pipeline
retornar pipeline_status: "aborted_due_to_structural_errors"