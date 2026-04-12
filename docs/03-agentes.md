# Definição dos Agentes do Sistema

## Visão Geral

A arquitetura do sistema será baseada em múltiplos agentes especializados. Cada agente terá uma responsabilidade única e bem delimitada dentro do pipeline de análise.

Essa decisão foi adotada para evitar que um único modelo concentre tarefas heterogêneas demais, o que aumentaria:
- ambiguidade
- acoplamento
- inferência indevida
- perda de rastreabilidade
- dificuldade de depuração

Cada agente deverá operar com:
- entradas claramente definidas
- regras explícitas
- formato de saída estruturado
- limitações conhecidas
- possibilidade de revisão humana

---

## Princípios de Modelagem dos Agentes

### 1. Responsabilidade única
Cada agente deve executar uma função específica e não absorver tarefas que pertencem a outros módulos.

### 2. Saída estruturada
Toda saída de agente deve ser serializável e aderente a schema.

### 3. Sem correção silenciosa
Agentes não devem corrigir dados por conta própria. Devem apontar problemas, não mascará-los.

### 4. Linguagem proporcional à evidência
Agentes interpretativos devem usar linguagem cautelosa e tecnicamente proporcional ao que os dados sustentam.

### 5. Revisão humana quando necessário
Conflitos, ambiguidade, baixa confiança ou insuficiência de dados devem gerar sinalização explícita.

---

## Orquestrador Central

Antes dos agentes especializados, haverá um componente de orquestração.

### Função
O orquestrador será responsável por:
- receber o payload principal
- validar a estrutura inicial
- decidir a sequência de execução
- encaminhar os dados necessários para cada agente
- consolidar respostas
- interromper o pipeline em falhas críticas
- sinalizar estados de erro e revisão humana

### O que o orquestrador não deve fazer
- não deve interpretar biomarcadores
- não deve gerar relatório final sozinho
- não deve corrigir dados
- não deve substituir agentes especializados

---

## Agente 1 — Study Classifier

### Nome técnico
`study_classifier`

### Finalidade
Classificar o estudo recebido e determinar o contexto analítico inicial da execução.

### Responsabilidades
- identificar o tipo do estudo
- identificar os domínios de dados presentes
- apontar o grau inicial de completude
- sugerir template técnico de análise
- detectar ausência de informações críticas de contexto

### Entradas esperadas
- metadados do estudo
- resumo do protocolo
- descrição dos datasets
- objetivo técnico ou regulatório
- contexto experimental informado

### Saídas esperadas
- tipo de estudo
- domínios detectados
- avaliação de completude
- campos críticos ausentes
- template recomendado
- confiança da classificação

### Limites
- não interpreta resultados experimentais
- não valida números em profundidade
- não gera relatório
- não conclui sobre achados biológicos

### Riscos controlados
- inferir contexto não informado
- assumir espécie, desenho experimental ou domínio ausente
- classificar de forma excessivamente confiante sem base

---

## Agente 2 — Data Validator

### Nome técnico
`data_validator`

### Finalidade
Avaliar integridade, consistência e completude dos dados experimentais recebidos.

### Responsabilidades
- verificar campos obrigatórios
- identificar valores nulos
- validar tipos de dados
- detectar duplicidade de registros ou IDs
- encontrar inconsistências estruturais
- verificar coerência básica entre protocolo e dados
- produzir score de qualidade

### Entradas esperadas
- metadados
- datasets
- schemas esperados
- resumo do protocolo
- configuração de validação

### Saídas esperadas
- quality_score
- lista de erros
- lista de warnings
- resumo da qualidade dos dados
- indicação de revisão humana, quando aplicável

### Limites
- não interpreta relevância biológica profunda
- não exclui outliers automaticamente
- não altera os dados
- não faz limpeza silenciosa

### Observação
Este agente deverá combinar lógica determinística com eventual apoio de IA apenas para explicações textuais, nunca para regras estruturais básicas.

---

## Agente 3 — Pattern Detector

### Nome técnico
`pattern_detector`

### Finalidade
Identificar padrões relevantes e outliers nos dados experimentais.

### Responsabilidades
- detectar valores atípicos
- sinalizar tendências numéricas ou comportamentais
- comparar grupos de forma descritiva
- destacar achados potencialmente relevantes
- registrar limitações analíticas

### Entradas esperadas
- datasets validados
- grupos experimentais
- variáveis de interesse
- contexto do estudo
- resultados do validador

### Saídas esperadas
- lista de outliers
- lista de padrões
- descrição dos grupos comparados
- relevância biológica estimada
- limitações
- confiança

### Limites
- não deve atribuir causalidade
- não deve concluir toxicidade definitiva
- não deve transformar tendência em diagnóstico
- não deve atuar sem base mínima de dados

### Observação
Este agente pode combinar heurísticas estatísticas simples com formulação textual técnica controlada.

---

## Agente 4 — Biomarker Interpreter

### Nome técnico
`biomarker_interpreter`

### Finalidade
Produzir interpretações técnicas preliminares para achados experimentais, com foco em linguagem científica cautelosa.

### Responsabilidades
- interpretar biomarcadores bioquímicos
- interpretar achados histológicos simplificados
- interpretar sinais comportamentais relevantes
- sintetizar relações entre domínios
- explicitar quando a interpretação é dependente de confirmação adicional

### Entradas esperadas
- dados validados
- padrões detectados
- contexto do estudo
- variáveis experimentais
- metadados e grupos

### Saídas esperadas
- lista de interpretações por domínio
- sumário transversal entre domínios
- limitações
- pontos que exigem confirmação
- confiança

### Limites
- não faz diagnóstico definitivo
- não afirma mecanismo biológico sem evidência
- não substitui interpretação especializada humana
- não pode omitir limitações dos dados

### Linguagem esperada
Deve usar formulações como:
- “compatível com”
- “pode sugerir”
- “é consistente com”
- “requer confirmação adicional”
- “não há evidência suficiente para concluir”

---

## Agente 5 — Report Generator

### Nome técnico
`report_generator`

### Finalidade
Consolidar todas as saídas do pipeline em um relatório técnico-científico estruturado.

### Responsabilidades
- organizar o conteúdo em seções formais
- separar dados observados de interpretação
- destacar limitações e advertências
- padronizar a linguagem científica
- produzir uma estrutura clara e legível para uso técnico

### Entradas esperadas
- classificação do estudo
- resultado da validação
- padrões e outliers
- interpretações preliminares
- metadados e protocolo

### Saídas esperadas
- título do relatório
- seções estruturadas
- apêndice de erros e avisos
- conclusão preliminar
- pontos recomendados para revisão humana

### Limites
- não cria resultados inexistentes
- não resolve conflitos sozinho
- não omite falhas críticas
- não deve parecer conclusivo quando o material é insuficiente

---

## Agente 6 — Audit Agent

### Nome técnico
`audit_agent`

### Finalidade
Registrar rastreabilidade do processo analítico e consolidar pontos críticos de revisão.

### Responsabilidades
- mapear quais agentes rodaram
- registrar quais entradas foram utilizadas
- resumir quais saídas cada agente produziu
- listar conflitos, limitações e incertezas
- consolidar pontos de revisão humana
- produzir visão de confiança global do pipeline

### Entradas esperadas
- resultados de todos os agentes
- plano de execução do orquestrador
- metadados do estudo
- status de processamento

### Saídas esperadas
- trilha de rastreabilidade
- review_points
- conflicts
- final_confidence
- resumo de auditoria

### Limites
- não reinterpretar achados biológicos
- não alterar resultados dos outros agentes
- não ocultar conflito ou incerteza

---

## Possíveis Agentes Futuramente

Embora não entrem no MVP, o sistema pode evoluir para incluir:

### Regulatory Mapper
Para mapear seções do relatório a exigências específicas de órgãos reguladores.

### Scientific Language Normalizer
Para padronização mais refinada da escrita científica.

### Document Template Renderer
Para exportação estruturada em DOCX/PDF com formatação mais avançada.

### Evidence Linking Agent
Para associar cada afirmação textual a evidências específicas de entrada.

### Cross-Study Comparator
Para comparação entre estudos diferentes.

---

## Relação Entre os Agentes

O fluxo inicial previsto será:

1. orquestrador recebe o estudo
2. study_classifier define o contexto
3. data_validator avalia integridade
4. pattern_detector analisa padrões e outliers
5. biomarker_interpreter produz leitura técnica preliminar
6. report_generator consolida relatório
7. audit_agent registra rastreabilidade e revisão humana

---

## Critérios de Qualidade para Todos os Agentes

Todos os agentes devem:
- trabalhar com base apenas nas entradas recebidas
- evitar suposições implícitas
- devolver JSON válido
- informar confiança quando aplicável
- marcar `requires_human_review` quando necessário
- registrar limitações
- manter escopo restrito à sua responsabilidade

---

## Erros de Arquitetura a Evitar

### 1. Agente genérico demais
Evitar agentes que façam validação, interpretação e relatório ao mesmo tempo.

### 2. Mistura entre observação e conclusão
Achados observados devem ser separados de interpretações.

### 3. Falta de schema
Nenhum agente deve depender de texto livre como contrato principal com outros módulos.

### 4. Falta de rastreabilidade
Toda saída relevante deve poder ser atribuída ao agente que a gerou.

### 5. Omissão de incerteza
Baixa confiança, insuficiência de dados e conflito precisam aparecer explicitamente.