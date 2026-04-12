# Regras do Workspace

## Objetivo deste arquivo

Este arquivo define as regras operacionais e arquiteturais que devem orientar qualquer planejamento, geração de código, refatoração, criação de agentes ou proposta técnica dentro deste projeto.

Estas regras funcionam como instruções permanentes do projeto e devem ser consideradas em conjunto com:
- `README.md`
- arquivos da pasta `docs/`
- arquivos da pasta `prompts/`

---

## Contexto do projeto

Este projeto implementa uma **API multiagente para avaliação da qualidade de dados experimentais em toxicologia pré-clínica e geração automatizada de relatórios técnico-científicos**.

O sistema deve apoiar:
- validação de integridade de dados
- detecção de padrões e outliers
- interpretação técnica preliminar
- geração estruturada de relatórios
- rastreabilidade e auditoria

O projeto não tem como objetivo substituir especialista humano nem emitir decisão regulatória final.

---

## Prioridades obrigatórias

Toda proposta, implementação ou alteração neste projeto deve priorizar:

1. rastreabilidade
2. reprodutibilidade
3. conformidade documental
4. clareza arquitetural
5. modularidade
6. separação entre validação e interpretação
7. saídas estruturadas em JSON
8. revisão humana em cenários críticos

---

## Restrições obrigatórias

Ao atuar neste projeto, é obrigatório respeitar as seguintes restrições:

- não inventar dados ausentes
- não corrigir silenciosamente dados inválidos
- não assumir contexto experimental não fornecido
- não misturar validação estrutural com interpretação biológica
- não misturar observação com conclusão
- não gerar conclusões acima da evidência disponível
- não transformar o MVP em uma arquitetura excessivamente complexa
- não concentrar múltiplas responsabilidades em um único agente
- não usar texto livre como contrato principal entre módulos quando houver schema definido

---

## Diretrizes de arquitetura

A arquitetura deve seguir estas diretrizes:

### 1. MVP primeiro
As decisões devem favorecer uma primeira versão funcional, demonstrável e tecnicamente coerente, evitando expansão prematura de escopo.

### 2. Separação de responsabilidades
Cada agente deve possuir uma responsabilidade única e bem delimitada.

### 3. Orquestração explícita
O sistema deve possuir um orquestrador central responsável por coordenar o pipeline sem absorver funções dos agentes especializados.

### 4. Estratégia híbrida
Sempre que possível:
- usar validação determinística para checagens estruturais
- usar IA para classificação contextual, interpretação textual e geração de relatório

### 5. Contratos explícitos
Toda saída que alimente outro módulo deve seguir schema definido e previsível.

---

## Diretrizes de engenharia

Toda implementação deve, preferencialmente:

- usar tipagem forte
- usar validação explícita de entrada e saída
- manter organização modular
- usar nomes claros para arquivos, módulos e funções
- preservar consistência com os documentos existentes
- refletir os agentes definidos em `docs/03-agentes.md`
- respeitar os esquemas definidos em `docs/04-esquemas-json.md`
- usar os prompts da pasta `prompts/` como fonte principal de comportamento dos agentes

Evitar:
- abstrações excessivas
- camadas desnecessárias para o MVP
- dependências complexas sem necessidade
- múltiplos estilos arquiteturais conflitantes

---

## Diretrizes para geração de código

Ao gerar código, seguir esta ordem:

1. primeiro explicar o plano
2. depois indicar quais arquivos serão criados ou alterados
3. só então propor o código

Toda geração de código deve:
- manter coerência com o README e a pasta `docs/`
- refletir a estrutura dos agentes já definida
- preservar o foco em backend
- manter possibilidade de teste
- evitar comportamento implícito difícil de auditar

---

## Diretrizes para agentes

Todo agente do sistema deve:

- ter papel específico
- possuir entradas claramente definidas
- devolver saída estruturada
- explicitar limitações
- sinalizar `requires_human_review` quando necessário
- operar com linguagem proporcional à evidência disponível

Nenhum agente deve:
- assumir função de outro agente
- tomar decisão regulatória final
- mascarar incerteza
- preencher lacunas com suposição

---

## Diretrizes para interpretação técnica

Toda interpretação deve ser:

- preliminar
- cautelosa
- proporcional à evidência
- explicitamente limitada quando necessário

São preferíveis formulações como:
- “compatível com”
- “pode sugerir”
- “indica de forma preliminar”
- “depende de confirmação adicional”
- “não há evidência suficiente para concluir”

Devem ser evitadas formulações como:
- “comprova”
- “confirma definitivamente”
- “demonstra sem dúvida”
- “evidencia causalidade direta”

---

## Diretrizes para relatórios

Relatórios gerados pelo sistema devem:

- ser formais
- ser objetivos
- destacar limitações
- separar observação, interpretação e conclusão
- refletir qualidade da base analisada
- recomendar revisão humana quando apropriado

O relatório não deve:
- parecer mais conclusivo do que os dados permitem
- omitir erros críticos
- mascarar baixa qualidade dos dados

---

## Diretrizes para evolução do projeto

Quando houver dúvida entre:
- uma solução mais sofisticada
- uma solução mais simples e coerente com o MVP

deve-se preferir a solução mais simples, desde que tecnicamente sólida.

Evoluções futuras só devem ser introduzidas se:
- não quebrarem a clareza do pipeline
- não comprometerem rastreabilidade
- não confundirem responsabilidades
- não deslocarem o foco do MVP

---

## Regra de ouro deste projeto

Se existir qualquer conflito entre sofisticação e controle, priorizar controle.

Se existir qualquer conflito entre automação e segurança analítica, priorizar segurança analítica.

Se existir qualquer conflito entre conclusão forte e evidência insuficiente, priorizar explicitação da limitação.