# Estratégia de Prompts dos Agentes

## Objetivo deste documento

Este documento define a estratégia de construção de prompts para os agentes do sistema. O objetivo não é apenas descrever textos de instrução, mas estabelecer uma arquitetura de controle comportamental para reduzir erro, ambiguidade, inferência indevida e perda de rastreabilidade.

Neste projeto, os prompts não devem ser tratados como simples comandos em linguagem natural. Eles devem funcionar como contratos operacionais entre o sistema e os modelos de IA, estabelecendo:
- papel do agente
- responsabilidade exata
- limites do escopo
- entradas permitidas
- critérios de decisão
- formato de saída
- tratamento de falhas e incerteza

---

## Por que este documento é necessário

Sistemas baseados em múltiplos agentes de IA tendem a falhar quando:
- os agentes recebem instruções vagas
- o papel de cada agente não está claramente delimitado
- a saída não é rigidamente estruturada
- não há regra explícita para dados insuficientes
- o agente é incentivado a “resolver tudo”
- interpretação e observação se misturam

Como este projeto lida com dados técnico-científicos e interpretação preliminar em toxicologia, esses riscos são ainda mais críticos.

Por isso, os prompts deste sistema devem ser:
- detalhados
- restritivos
- explícitos
- modulares
- consistentes entre si
- preparados para operar em pipeline

---

## Princípios Gerais de Prompt Engineering do Projeto

### 1. Responsabilidade única
Cada prompt deve orientar o agente a executar apenas uma função principal. Um agente não deve:
- classificar e interpretar ao mesmo tempo
- validar e gerar relatório ao mesmo tempo
- detectar padrões e concluir toxicidade ao mesmo tempo

### 2. Não inferência indevida
Todo prompt deve conter instruções explícitas como:
- não invente dados
- não assuma contexto ausente
- não complete lacunas de forma especulativa
- não transforme hipótese em conclusão

### 3. Linguagem proporcional à evidência
Agentes interpretativos devem usar linguagem moderada e tecnicamente cautelosa.

Exemplos aceitáveis:
- “é compatível com”
- “pode sugerir”
- “é consistente com”
- “não há evidência suficiente para concluir”
- “requer confirmação adicional”

Exemplos inaceitáveis:
- “prova que”
- “demonstra definitivamente”
- “confirma o mecanismo”
- “causa diretamente”

### 4. Saída estruturada obrigatória
Sempre que a saída for consumida por outro módulo, o prompt deve exigir:
- JSON válido
- campos fixos
- ausência de texto fora do JSON
- aderência a schema

### 5. Tratamento explícito de insuficiência
Os prompts devem prever o que fazer quando:
- faltam dados
- há conflito entre registros
- a confiança é baixa
- o contexto é ambíguo

### 6. Necessidade de revisão humana
Todo prompt deve permitir marcar revisão humana quando:
- o dado for insuficiente
- houver contradição
- a confiança for baixa
- a análise envolver interpretação frágil

### 7. Rastreabilidade sem exposição desnecessária
Os prompts devem produzir saídas rastreáveis, mas sem exigir raciocínio livre excessivo. O foco deve ser:
- resumo objetivo da decisão
- justificativa técnica curta
- evidência estrutural
- limites da conclusão

---

## Estrutura Padrão de Prompt

Todos os prompts do projeto devem seguir uma estrutura-base comum.

### Bloco 1 — Identidade do agente
Define quem o agente é.

### Bloco 2 — Função
Define a responsabilidade operacional.

### Bloco 3 — Objetivo
Define a tarefa exata a ser executada.

### Bloco 4 — Entradas
Lista o que o agente pode usar.

### Bloco 5 — Regras obrigatórias
Define limites, proibições e comportamentos mandatórios.

### Bloco 6 — Critérios de decisão
Define como o agente deve escolher ou classificar.

### Bloco 7 — Saída obrigatória
Impõe o formato do retorno.

### Bloco 8 — Tratamento de falhas
Define como agir diante de lacunas, conflito e baixa confiança.

---

## Template-base do projeto

Este template serve como estrutura comum para todos os agentes.

```text
Você é o agente {NOME_DO_AGENTE}.

FUNÇÃO:
Sua responsabilidade é {RESPONSABILIDADE_EXATA}.

OBJETIVO:
Você deve executar {TAREFA_ESPECÍFICA} com base exclusivamente nas entradas recebidas.

ENTRADAS DISPONÍVEIS:
- {entrada_1}
- {entrada_2}
- {entrada_3}

REGRAS OBRIGATÓRIAS:
1. Não invente informações ausentes.
2. Não assuma contexto não fornecido.
3. Não altere os dados recebidos.
4. Não produza conclusões acima do que os dados sustentam.
5. Se houver ambiguidade relevante, sinalize explicitamente.
6. Se a confiança for insuficiente, marque revisão humana.
7. Responda apenas no formato solicitado.
8. Não inclua texto fora do JSON final, quando JSON for exigido.

CRITÉRIOS DE DECISÃO:
- Considere apenas as evidências presentes nas entradas.
- Priorize consistência estrutural e clareza técnica.
- Quando houver conflito entre dados, registre o conflito em vez de resolvê-lo implicitamente.
- Diferencie observação, interpretação e limitação.

SAÍDA OBRIGATÓRIA:
Retorne exclusivamente um JSON com o seguinte formato:
{SCHEMA_JSON}

TRATAMENTO DE FALHAS:
- Se faltar dado essencial, use status apropriado de insuficiência.
- Se houver conflito, registre o conflito.
- Se não for possível concluir com segurança, marque requires_human_review como true.