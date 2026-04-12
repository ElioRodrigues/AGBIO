# Toxicology Domain Skill

## Objetivo

Esta skill define o contexto técnico-científico do projeto no domínio de toxicologia pré-clínica.

Ela deve orientar qualquer agente, planejamento, geração de código ou proposta técnica a respeitar a natureza dos dados experimentais analisados pelo sistema.

---

## Contexto

Este projeto trabalha com dados experimentais de toxicologia pré-clínica e com geração de relatórios técnico-científicos baseados nesses dados.

Os dados podem envolver, entre outros:
- biomarcadores bioquímicos
- achados histológicos
- observações comportamentais
- metadados experimentais
- registros documentais do estudo

---

## Diretrizes de domínio

Ao atuar neste projeto, considerar sempre a distinção entre:

### 1. Observação experimental
Aquilo que está diretamente presente nos dados.

Exemplos:
- valor alterado de uma variável
- diferença entre grupos
- presença de outlier
- ausência de registro
- inconsistência estrutural

### 2. Interpretação técnica preliminar
Leitura técnica proporcional ao que os dados sugerem, sem extrapolação indevida.

Exemplos:
- “compatível com”
- “pode sugerir”
- “indica de forma preliminar”
- “merece investigação adicional”

### 3. Conclusão
Síntese final da análise, sempre limitada pela robustez da base.

Conclusões devem ser conservadoras quando houver:
- baixa qualidade dos dados
- inconsistência
- lacunas críticas
- conflito entre domínios
- baixa confiança

---

## Regras obrigatórias

- nunca tratar correlação como causalidade
- nunca tratar indício como confirmação definitiva
- nunca afirmar mecanismo biológico sem evidência explícita
- nunca emitir diagnóstico definitivo
- nunca omitir limitação relevante
- sempre diferenciar achado, interpretação e conclusão

---

## Linguagem recomendada

Preferir expressões como:
- “compatível com”
- “pode sugerir”
- “indica preliminarmente”
- “depende de confirmação adicional”
- “não há evidência suficiente para concluir”

Evitar expressões como:
- “comprova”
- “confirma definitivamente”
- “demonstra sem dúvida”
- “estabelece causalidade”

---

## Aplicação no projeto

Usar esta skill sempre que a tarefa envolver:
- interpretação de achados
- geração de relatório técnico
- refinamento de prompts de agentes
- organização de análises toxicológicas