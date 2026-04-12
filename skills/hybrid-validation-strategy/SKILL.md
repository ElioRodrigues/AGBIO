# Hybrid Validation Strategy Skill

## Objetivo

Esta skill define a estratégia híbrida do projeto, separando claramente o que deve ser feito por validação determinística e o que pode ser apoiado por IA.

---

## Princípio central

Nem tudo deve ser resolvido com IA.

Neste projeto, a IA deve ser usada apenas onde ela agrega valor interpretativo, classificatório ou redacional.

As verificações estruturais e objetivas devem ser tratadas preferencialmente por lógica determinística.

---

## Usar validação determinística para

- campos obrigatórios
- tipos de dados
- nulidade
- duplicidade de identificadores
- presença mínima de colunas
- coerência estrutural básica
- checagem de schema
- validações previsíveis e objetivas

---

## Usar IA para

- classificação contextual do estudo
- interpretação técnica preliminar
- descrição textual de padrões
- padronização de linguagem científica
- geração de relatório técnico
- sumarização estruturada das saídas analíticas

---

## Regras obrigatórias

- não delegar à IA aquilo que pode ser validado com regra objetiva simples
- não usar IA para corrigir dados automaticamente
- não permitir que interpretação substitua validação estrutural
- não misturar etapas determinísticas com inferência sem deixar isso claro na arquitetura

---

## Diretriz de projeto

Ao implementar qualquer módulo, sempre perguntar:

1. esta tarefa é objetiva e determinística?
2. esta tarefa exige interpretação contextual?
3. esta tarefa depende de linguagem natural técnica?
4. esta tarefa pode ser validada por schema ou regra simples?

Se a resposta for objetiva e verificável, preferir lógica determinística.

Se a resposta exigir interpretação contextual ou formulação textual técnica, a IA pode ser usada com controle adequado.

---

## Aplicação no projeto

Usar esta skill sempre que a tarefa envolver:
- desenho da arquitetura
- implementação do validador
- desenho do pipeline
- refinamento do orquestrador
- decisões sobre uso de IA versus regras fixas