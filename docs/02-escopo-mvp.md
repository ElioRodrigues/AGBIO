# Escopo do MVP

## Objetivo do MVP

O MVP deste projeto tem como finalidade validar a viabilidade técnica de uma API multiagente para apoio à análise de dados toxicológicos e geração de relatórios técnico-científicos estruturados.

O foco do MVP não é cobrir todos os cenários possíveis da toxicologia pré-clínica, mas sim demonstrar, de forma robusta, um fluxo funcional completo que integre:
- ingestão de dados estruturados
- classificação do estudo
- validação de integridade
- detecção de padrões e outliers
- interpretação técnica preliminar
- geração de relatório
- auditoria da análise

---

## Pergunta que o MVP precisa responder

O MVP deve ser capaz de responder, de forma convincente, à seguinte pergunta:

> É possível construir uma API com agentes especializados que receba dados experimentais estruturados, avalie sua qualidade, identifique achados relevantes e gere relatórios técnicos preliminares com rastreabilidade e controle de inferência?

Se a resposta prática for sim, o MVP já terá cumprido sua função principal.

---

## Escopo Funcional Incluído

### 1. Ingestão de estudo estruturado
O sistema deverá aceitar um payload estruturado contendo, no mínimo:
- metadados do estudo
- resumo do protocolo experimental
- datasets tabulares
- grupos experimentais
- objetivo técnico ou regulatório da análise

### 2. Classificação do estudo
O sistema deverá identificar:
- tipo de estudo informado ou inferível a partir do contexto
- domínios de dados presentes
- completude inicial do material enviado
- template técnico sugerido para o relatório

### 3. Validação de integridade e completude
O sistema deverá realizar verificações básicas e intermediárias, como:
- presença de campos obrigatórios
- tipos de dados compatíveis
- valores nulos ou vazios
- duplicidade de identificadores
- inconsistência entre grupos e registros
- divergência entre protocolo resumido e estrutura dos dados entregues

### 4. Detecção de padrões e outliers
O sistema deverá ser capaz de:
- sinalizar valores atípicos
- destacar diferenças relevantes entre grupos
- descrever padrões numéricos ou comportamentais que mereçam atenção
- registrar limitações da análise

### 5. Interpretação técnica preliminar
O sistema deverá produzir interpretações textuais preliminares que:
- usem linguagem cautelosa
- não afirmem causalidade sem base
- diferenciem observação de interpretação
- explicitem necessidade de confirmação adicional quando aplicável

### 6. Geração de relatório técnico estruturado
O sistema deverá consolidar as saídas anteriores em um relatório com seções bem definidas, como:
- resumo do estudo
- avaliação da qualidade dos dados
- visão geral dos resultados
- interpretação técnica preliminar
- limitações
- conclusão preliminar
- pontos recomendados para revisão humana

### 7. Auditoria e rastreabilidade
O sistema deverá registrar:
- quais agentes foram executados
- quais entradas foram utilizadas
- onde houve conflito, limitação ou baixa confiança
- quais pontos exigem revisão humana

---

## Entradas Suportadas no MVP

### Formato geral
O MVP aceitará inicialmente apenas **dados estruturados**, preferencialmente em formato JSON no corpo da requisição.

### Conteúdos mínimos esperados
- identificador do estudo
- título ou descrição resumida
- tipo de estudo
- resumo do protocolo
- datasets tabulares
- nomes das variáveis
- grupos experimentais
- alvo regulatório ou finalidade técnica

### Tipos de domínio de dados priorizados
No MVP, o sistema será desenhado para lidar principalmente com:
- dados bioquímicos
- dados comportamentais
- dados histológicos simplificados
- metadados documentais
- estruturas tabulares de resultados experimentais

---

## Saídas Esperadas no MVP

O sistema deverá retornar, em formato estruturado:
- classificação do estudo
- avaliação de completude
- score de qualidade dos dados
- lista de erros
- lista de avisos
- padrões detectados
- outliers identificados
- interpretações técnicas preliminares
- relatório técnico estruturado
- trilha de auditoria
- campos de confiança e revisão humana quando aplicável

---

## Escopo Técnico Incluído

### Backend
- API REST
- orquestrador central
- agentes especializados
- validação de schema
- logs básicos
- estrutura de teste inicial

### Modelagem de agentes
O MVP incluirá agentes especializados com responsabilidade definida, evitando agentes genéricos com escopo amplo demais.

### Contratos estruturados
Toda troca entre módulos deverá ocorrer com base em schemas explícitos e saídas JSON válidas.

### Estratégia híbrida
Parte da lógica será determinística e parte será orientada por IA. O MVP deverá demonstrar claramente essa separação.

---

## Fora do Escopo do MVP

### 1. OCR avançado
O MVP não fará leitura irrestrita de imagens, laudos escaneados ou PDFs complexos e desestruturados.

### 2. Interpretação regulatória profunda automatizada
O MVP não emitirá parecer regulatório final nem realizará enquadramento legal automatizado completo.

### 3. Integrações externas complexas
Não estão incluídas inicialmente integrações com:
- sistemas laboratoriais externos
- ERPs
- bancos regulatórios externos
- ambientes corporativos de terceiros
- conectores avançados via MCP

### 4. Frontend completo
O MVP é focado no backend e na demonstração funcional da API. Interfaces gráficas podem ser adicionadas depois.

### 5. Geração final sofisticada de documentos
Relatórios em PDF ou DOCX altamente formatados não são prioridade inicial. O foco é primeiro consolidar o conteúdo técnico estruturado.

### 6. Suporte a todos os desenhos experimentais
O MVP não pretende cobrir toda a diversidade de estudos toxicológicos existentes. O foco é um subconjunto controlado e viável.

### 7. Processamento estatístico avançado completo
Embora o sistema possa detectar padrões e outliers, ele não substituirá um pipeline estatístico aprofundado na primeira versão.

### 8. Autonomia total
O sistema não será desenhado para operar como decisor final. Sempre deverá existir possibilidade de revisão humana.

---

## Critérios de Sucesso do MVP

O MVP será considerado bem-sucedido se conseguir:

1. receber um estudo estruturado sem ambiguidade de contrato
2. classificar adequadamente o contexto básico do estudo
3. apontar erros e avisos relevantes de integridade
4. identificar padrões ou outliers simples e úteis
5. gerar interpretação técnica preliminar cautelosa
6. consolidar um relatório técnico inteligível e coerente
7. registrar rastreabilidade da análise
8. sinalizar revisão humana nos casos necessários

---

## Premissas do MVP

- as entradas serão previamente organizadas em formato estruturado
- haverá escopo reduzido e controlado de tipos de estudo
- o sistema trabalhará com linguagem técnica, mas não substituirá especialista
- cada agente operará com papel claramente delimitado
- o backend validará a estrutura dos dados antes de repassar conteúdo à IA

---

## Restrições do MVP

- prazo reduzido de implementação
- necessidade de arquitetura simples o suficiente para ser apresentada e explicada
- limitação do escopo para garantir demonstrabilidade
- necessidade de evitar excesso de dependência de IA em tarefas determinísticas
- exigência de previsibilidade e clareza dos resultados

---

## Casos de Uso Prioritários

### Caso de uso 1 — análise básica de estudo consistente
O usuário envia um estudo com metadados e datasets consistentes. O sistema valida, interpreta e gera relatório.

### Caso de uso 2 — estudo com lacunas estruturais
O usuário envia um estudo com campos ausentes, duplicidades ou inconsistências. O sistema sinaliza o problema e reduz confiança.

### Caso de uso 3 — estudo com padrões atípicos
O usuário envia dados com possíveis outliers ou diferenças relevantes entre grupos. O sistema destaca achados e limitações.

### Caso de uso 4 — estudo com material insuficiente
O usuário envia dados incompletos demais para interpretação. O sistema recusa conclusão forte e marca revisão humana.

---

## Entregável Esperado do MVP

Ao final do MVP, deverá existir uma base funcional capaz de demonstrar:
- o fluxo completo da API
- a separação entre agentes
- a combinação entre validação determinística e IA
- a geração de saída técnica estruturada
- a possibilidade de evolução futura para cenários mais complexos