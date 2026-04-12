# JSON Output Contracts Skill

## Objetivo

Esta skill define a política de saída estruturada do projeto.

Ela existe para garantir previsibilidade, integração segura entre módulos e redução de ambiguidade na comunicação entre agentes e backend.

---

## Princípio central

Toda saída destinada a outro agente, ao orquestrador ou à API deve ser retornada em JSON válido e aderente ao schema esperado.

---

## Regras obrigatórias

- não retornar texto fora do JSON quando a tarefa exigir saída estruturada
- não omitir silenciosamente campos obrigatórios
- preferir listas vazias a campos ausentes quando o schema exigir o campo
- usar nomes de campos consistentes com a documentação
- respeitar os esquemas definidos em `docs/04-esquemas-json.md`

---

## Campos transversais importantes

Sempre que aplicável, incluir:
- `confidence`
- `limitations`
- `requires_human_review`

---

## Regras para insuficiência e conflito

Quando houver:
- baixa confiança
- insuficiência de dados
- conflito entre informações
- inconsistência relevante

o agente deve refletir isso explicitamente no JSON, e não apenas insinuar no texto.

---

## Regras de integração

Ao projetar ou implementar código:
- tratar o JSON como contrato formal
- validar a saída dos agentes
- rejeitar ou tratar respostas inválidas
- evitar parsing frágil baseado em texto livre

---

## Aplicação no projeto

Usar esta skill sempre que a tarefa envolver:
- criação de prompts
- implementação dos agentes
- definição de schemas
- orquestração entre módulos
- validação de saída da IA