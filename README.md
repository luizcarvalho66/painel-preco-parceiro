# Documentação Técnica: Painel Preço Parceiro

## 1. Visão Geral do Projeto

O **Painel Preço Parceiro** é a interface analítica central para o monitoramento e auditoria da conformidade de preços na rede de manutenção. Seu objetivo é garantir que as negociações realizadas ("Preço Parceiro") estejam aderentes às tabelas referenciais, maximizando a eficiência de custos (Savings).

### Contexto de Negócio

- **Problema**: Disparidade entre preços de peças em concessionárias/oficinas e os valores de referência de mercado.
- **Solução**: Um painel que cruza dados de OS (Ordens de Serviço), Aprovadores e Tabelas de Preço para identificar desvios.
- **Público-Alvo**: Coordenadores de Manutenção, Auditores e Gerentes de Rede.

---

## 2. Arquitetura de Dados

### 2.1 Fonte de Dados (Azure Databricks)

O projeto conecta-se ao Data Lake da Edenred via conector nativo do Databricks para Power BI.

- **Método de Conexão**: DirectQuery (para tabelas dimensão grandes) ou Import (para tabelas otimizadas), gerenciado via TMDL.
- **Servidor (Host)**: `adb-7941093640821140.0.azuredatabricks.net`
- **SQL Warehouse (Cluster)**: `4dc5e8e336ea177a` / Caminho HTTP: `/sql/1.0/warehouses/4dc5e8e336ea177a`
- **Schema Principal**: `hive_metastore.gold`

### 2.2 Modelagem Semântica (Star Schema)

O modelo gira em torno de uma tabela fato central enriquecida por múltiplas dimensões e tabelas auxiliares de relacionamento.

#### Tabela Fato: `FactAprovacaoPrecoParceiro`

Construída via consulta nativa (SQL) complexa, responsável por:

1.  **Reconstrução de Histórico**: Utiliza logs (`Dim_MaintenanceParameterLogValue`) para determinar quem era o aprovador responsável no momento exato de cada OS.
2.  **Cálculo de Aderência**:
    - Cruza `ValorUnitarioPeca` (Real) vs. `ValorUnitarioReferencial` (Meta).
    - Classifica a transação como `OK` (Aderente), `NOK` (Não Aderente) ou `NA` (Não Aplicável).
3.  **Normalização**: Aplica filtros de negócio como validação de datas (`>= 2025-04-01`) e exclusão de cancelamentos.

#### Principais Dimensões

- `DimCalendario`: Tabela de datas padrão para inteligência de tempo.
- `DimAprovadores` / `DimSupervisores` / `DimCoordenadores`: Hierarquia de usuários.
- `RespostasFormulario`: Feedback qualitativo dos estabelecimentos sobre as negociações.

---

## 3. Dicionário de Medidas (DAX)

A lógica de negócio é implementada através de medidas DAX categorizadas.

### 3.1 Grupo `_Aprovações` (Financeiro & Potencial)

Foco em valores monetários e eficiência da negociação.

| Medida                 | Fórmula (Simplificada)                                                              | Descrição Técnica                                                                                      |
| :--------------------- | :---------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| **VA Peças**           | `SUM(ValorTotalPeca)`                                                               | Valor absoluto aprovado em peças.                                                                      |
| **VA Peças Potencial** | `CALCULATE([VA Peças], Referencial > 0, Sem Negociado, TipoEC != "Concessionaria")` | Valor em risco: peças que tinham preço de referência mas não foram negociadas. Exclui concessionárias. |
| **VA Peças Travado**   | `CALCULATE([VA Potencial], Tem Negociacao = TRUE)`                                  | Montante onde o processo "Preço Parceiro" foi aplicado com sucesso.                                    |
| **% Aproveitamento**   | `[VA Travado] / [VA Potencial]`                                                     | KPI de Eficiência: Quanto do potencial "atacável" foi efetivamente negociado.                          |

### 3.2 Grupo `_Auditoria` (Compliance)

Qualidade do valor travado.

| Medida                      | Classificação                      | Lógica de Negócio                                                           |
| :-------------------------- | :--------------------------------- | :-------------------------------------------------------------------------- |
| **VA Travado Aderente**     | `OK`                               | Preço da Peça <= Preço Referencial. (Savings garantido).                    |
| **VA Travado Não Aderente** | `NOK`                              | Preço da Peça > Preço Referencial. (Perda financeira mesmo com negociação). |
| **VA Travado Sem Ref.**     | `NA`                               | Preço Referencial não existia ou era inválido.                              |
| **% VA Incorreto**          | `([NOK] + [NA]) / [Total Travado]` | Percentual de negociações que não geraram o resultado esperado.             |

### 3.3 Grupo `_Efetividade` (Operacional)

Volume e Automação.

- **Total OS RI PP**: Contagem de Ordens de Serviço aprovadas automaticamente pelo **Robô Inteligente**.
- **Total Recusas Formulário**: Volume de negativas explícitas registradas pelos parceiros.

---

## 4. Design System & UX/UI

A interface utiliza uma abordagem **Low-Code/SVG** para garantir performance e aderência estrita ao Brandbook Edenred.

### 4.1 Identidade Visual

- **Cor Primária**: `#E20613` (Edenred Red). Usada em destaques e call-to-actions.
- **Tipografia**: Família **Ubuntu**.
- **Estilo**: Minimalista, uso intensivo de "White Space" e cards com sombras suaves.

### 4.2 Componentes Dinâmicos (SVG Measures)

Os elementos visuais não são imagens estáticas, mas sim códigos SVG gerados pelo Power BI.

#### Header (`_Layout[Background Header]`)

- **Código**: SVG `<rect>` com filtro `feDropShadow` e `fill='#E20613'`.
- **Função**: Cria o cabeçalho curvo padrão em todas as páginas.

#### KPI Card (`_Layout[Background KPI]`)

- **Código**: SVG `<rect>` branco com uma barra lateral (`<path>`) vermelha.
- **Função**: Container padronizado para métricas, substituindo o visual padrão de "Cartão".

### 4.3 Iconografia (`_Icons`)

Biblioteca **Bootstrap Icons** convertida para Data URLs (`data:image/svg+xml...`):

- ✅ `Icon Check`: Indicador de sucesso/aderência.
- 🚫 `Icon Error`: Indicador de falha/recusa.
- 🔍 `Icon Search`: Contexto de busca/detalhe.

---

## 5. Estrutura do Projeto (TMDL)

O projeto adota o formato **TMDL (Tabular Model Definition Language)** para controle de versão granular.

- `/definition/model.tmdl`: Arquivo raiz do modelo.
- `/definition/tables/*.tmdl`: Uma tabela por arquivo (facilita merges no Git).
- `/definition/relationships.tmdl`: Definição isolada dos relacionamentos.
- `/definition/expressions.tmdl`: Parâmetros de conexão (M Parameters).

## 6. Instruções de Deploy

1.  **Clone o Repositório**.
2.  Abra o arquivo `.pbip` no Power BI Desktop (feature "Power BI Project" deve estar habilitada).
3.  Ao publicar, configure as credenciais do **Data Source** para usar _OAuth2_ ou _Service Principal_ com acesso ao Workspace do Databricks.
4.  Atualize os Parâmetros `ClusterDB` e `HostDB` se estiver mudando entre ambientes (Dev/Prod).
