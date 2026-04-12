# Esquemas JSON do Sistema

## Objetivo

Este documento define os contratos estruturados de entrada e saída do sistema. Esses esquemas têm como finalidade:
- padronizar a comunicação entre módulos
- reduzir ambiguidade
- permitir validação automática
- facilitar orquestração
- melhorar robustez da integração entre agentes

Todos os esquemas aqui descritos devem ser interpretados como contratos iniciais do MVP, passíveis de refinamento, mas não de flexibilização arbitrária.

---

## Princípios Gerais dos Esquemas

### 1. Estrutura explícita
Todo payload deve possuir campos bem definidos, mesmo que alguns sejam opcionais.

### 2. JSON válido
As respostas dos agentes devem ser estritamente JSON válido quando destinadas ao pipeline interno.

### 3. Campos de controle
Sempre que aplicável, os agentes devem incluir:
- `confidence`
- `limitations`
- `requires_human_review`

### 4. Não ambiguidade
Campos devem ter nomes semanticamente claros e previsíveis.

### 5. Evolução controlada
Novos campos podem ser adicionados futuramente, mas o núcleo do contrato deve permanecer estável.

---

# 1. Schema de Entrada do Estudo

## Finalidade
Representar a estrutura mínima necessária para que o pipeline possa analisar um estudo experimental.

## Estrutura

```json
{
  "study_id": "string",
  "study_metadata": {
    "title": "string",
    "study_type": "string",
    "species": "string",
    "duration_days": 0,
    "objective": "string",
    "regulatory_target": ["string"]
  },
  "protocol_summary": "string",
  "experimental_groups": [
    {
      "group_id": "string",
      "group_name": "string",
      "description": "string"
    }
  ],
  "datasets": [
    {
      "dataset_id": "string",
      "name": "string",
      "domain": "string",
      "type": "tabular",
      "schema": {
        "field_name": "string"
      },
      "records": [
        {
          "animal_id": "string"
        }
      ]
    }
  ],
  "analysis_config": {
    "language": "pt-BR",
    "strict_validation": true,
    "enable_pattern_detection": true,
    "enable_interpretation": true
  }
}