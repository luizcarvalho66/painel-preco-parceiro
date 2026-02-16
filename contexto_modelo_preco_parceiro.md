# 📊 Contexto Completo — Modelo Semântico: Painel Preço Parceiro

> **Gerado automaticamente** pelo script `explorar_modelo.py`
> Use este arquivo como contexto (prompt) para qualquer assistente de IA.

---
## 1. Sumário Executivo

| Elemento | Quantidade |
|---|---|
| Tabelas | 18 |
| — Fatos | 2 |
| — Dimensões | 4 |
| — Parâmetros Field | 3 |
| — Documentação | 4 |
| — Outras (Medidas, Conexão, Formulário, etc.) | 5 |
| Colunas (total) | 162 |
| Medidas DAX | 32 |
| Relacionamentos | 11 |
| Roles (RLS) | 4 |
| Páginas do relatório | 8 |

---
## 2. Arquitetura de Dados / Fontes

### 2.1 Parâmetros de Conexão

- **ClusterDB** = `/sql/1.0/warehouses/ce56ec5f5d0a3e07`
- **HostDB** = `adb-7941093640821140.0.azuredatabricks.net`

### 2.2 Fontes de Dados por Tabela

| Tabela | Query Group | Fonte |
|---|---|---|
| _Medidas |  | Inline / Hardcoded |
| Conexao |  | Inline / Hardcoded |
| DimAprovadores | Dimensões | Excel/SharePoint |
| DimCalendario | Dimensões | Databricks SQL (via Azure) |
| DimCoordenadores | Dimensões | Excel/SharePoint |
| DimSupervisores | Dimensões | Excel/SharePoint |
| Doc_Colunas |  | Calculada (DAX) |
| Doc_Medidas |  | Calculada (DAX) |
| Doc_Relacionamentos |  | Calculada (DAX) |
| Doc_Tabelas |  | Calculada (DAX) |
| FactAprovacaoPrecoParceiro | Fatos | Databricks SQL (via Azure) |
| FactAprovacoesAposPrecoParceiro | Fatos | Databricks SQL (via Azure) |
| P_Aproveitamento |  | Calculada (DAX) |
| P_Travado |  | Calculada (DAX) |
| P_VA_Potencial |  | Calculada (DAX) |
| RelacaoClienteAprovador |  | Databricks SQL (via Azure) |
| RespostasFormulario |  | Excel/SharePoint |
| RespostasFormularioDistintasOS |  | Excel/SharePoint |

### 2.3 URLs de Fontes Externas (SharePoint)

- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Power BI - Produtividade Aprovação\dim_carteiras.xlsx`
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Projeto Preço Parceiro.xlsx`


---
## 3. Tabelas — Detalhamento

### 3.x — `_Medidas`


### 3.x — `Conexao` 🔒 (oculta)


**Colunas (2):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Codigo | int64 |  | Sim |  |
| Parametro | string |  | Sim |  |


### 3.x — `DimAprovadores`

**Query Group:** Dimensões

**Colunas (5):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Nome Aprovador | string |  |  |  |
| E-mail | string |  |  |  |
| dUsuario | string |  |  |  |
| Carteira | string |  |  |  |
| Supervisor | string |  |  |  |

**Fonte externa:**
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Power BI - Produtividade Aprovação\dim_carteiras.xlsx`


### 3.x — `DimCalendario`

**Query Group:** Dimensões

**Colunas (7):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| DataCompleta | dateTime |  |  |  |
| Ano | int64 |  |  |  |
| MesNumero | int64 |  |  |  |
| Semana | int64 |  |  |  |
| Dia | int64 |  |  |  |
| Mes | string |  |  |  |
| MesAbreviado | string |  |  |  |

**Hierarquia:** `Ano Hierarquia` → 

**SQL Databricks:**

```sql
SELECT
				  ReferenceDate                               AS DataCompleta,
				  ReferenceYear                               AS Ano,
				  ReferenceMonth                              As MesNumero,
				  YearWeek                                    AS Semana,
				  YearDay                                     AS Dia,
				  MonthNamePt                                 AS Mes
				FROM gold.dim_dates 
				WHERE 1=1 
				    AND ReferenceDate >= '2025-04-01'
				    AND IsTodayOrBefore = True
				ORDER BY ReferenceDate DESC
```

Tabelas SQL referenciadas: gold.dim_dates


### 3.x — `DimCoordenadores`

**Query Group:** Dimensões

**Colunas (2):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Coordenador | string |  |  |  |
| E-mail | string |  |  |  |

**Fonte externa:**
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Power BI - Produtividade Aprovação\dim_carteiras.xlsx`


### 3.x — `DimSupervisores`

**Query Group:** Dimensões

**Colunas (3):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Supervisor | string |  |  |  |
| E-mail | string |  |  |  |
| Coordenador | string |  |  |  |

**Fonte externa:**
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Power BI - Produtividade Aprovação\dim_carteiras.xlsx`


### 3.x — `FactAprovacaoPrecoParceiro`

**Query Group:** Fatos

**Colunas (32):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| NumeroOS | int64 | _OS |  |  |
| TipoOS | string | _OS |  |  |
| DataAprovacao1OS | dateTime | _OS |  |  |
| NomeUsuario | string | _Aprovador |  |  |
| CodigoUsuario | int64 | _Aprovador |  |  |
| CodigoModeloManutencao | int64 | _Cliente |  |  |
| NomeCliente | string | _Cliente |  |  |
| CodigoCliente | string | _Cliente |  |  |
| InformacaoAdicional2 | string | _Cliente |  |  |
| CodigoEC | int64 | _EC |  |  |
| NomeEC | string | _EC |  |  |
| TipoEC | string | _EC |  |  |
| UFEC | string | _EC |  |  |
| CidadeEC | string | _EC |  |  |
| ChaveItem | int64 | _Peça |  |  |
| NomePeca | string | _Peça |  |  |
| ComplementoConcatenadoPeca | string | _Peça |  |  |
| FabricantePeca | string | _Peça |  |  |
| QuantidadePeca | double | _ValoresAprovação |  |  |
| ValorUnitarioPeca | double | _ValoresAprovação |  |  |
| ValorTotalPeca | double | _ValoresAprovação |  |  |
| ValorUnitarioNegociado | double | _PrecoReferencial/Negociado |  |  |
| ValorUnitarioReferencial | double | _PrecoReferencial/Negociado |  |  |
| ValorUnitarioHierarquiaReferencial | double | _PrecoReferencial/Negociado |  |  |
| ValorTotalHierarquiaReferencial | double | _PrecoReferencial/Negociado |  |  |
| AderenciaPrecoReferencial | string | _PrecoReferencial/Negociado |  |  |
| DataEnvioNegociacaoPrecoParceiro | dateTime | _PreçoParceiro |  |  |
| ValorUnitarioNegociadoPrecoParceiro | decimal | _PreçoParceiro |  |  |
| ValidadeNegociacaoMeses | int64 | _PreçoParceiro |  |  |
| ValorTotalNegociadoPrecoParceiro | decimal | _PreçoParceiro |  |  |
| DiferencaValorUnitarioReferencialXNeggociado | decimal |  |  |  |
| % DiferencaNegociadoXReferencialHierarquia | N/A |  |  | Sim |

**SQL Databricks:**

```sql
WITH param_logs AS (
  SELECT
    dmplv.ClientId AS CodigoCliente,
    CAST(dmplv.ParameterLogOrgValueModificationTimestamp AS TIMESTAMP) AS ts,
    COALESCE(dmplv.OldValueDescription, '') AS old_values,
    COALESCE(dmplv.NewValueDescription, '') AS new_values
  FROM hive_metastore.gold.Dim_MaintenanceParameterLogValue AS dmplv
  WHERE dmplv.ParameterId = 586
),
-- Normaliza old/new em arrays (aceita ; ou , como separadores; remove espaços, vazios e duplicados)
sets AS (
  SELECT
    CodigoCliente,
    ts,
    array_distinct(
      filter(
        split(regexp_replace(old_values, '\\s+', ''), '[;,]+'),
        x -> x <> ''
      )
    ) AS old_set,
    array_distinct(
      filter(
        split(regexp_replace(new_values, '\\s+', ''), '[;,]+'),
        x -> x <> ''
      )
    ) AS new_set
  FROM param_logs
),
-- Inclusões (ADD): itens presentes no new_set e ausentes no old_set
adds AS (
  SELECT
    CodigoCliente,
    ts,
    CAST(approver AS STRING) AS approver
  FROM sets
  LATERAL VIEW explode(new_set) ns AS approver
  WHERE NOT array_contains(old_set, approver)
),
-- Exclusões (REMOVE): itens presentes no old_set e ausentes no new_set
removes AS (
  SELECT
    CodigoCliente,
    ts,
    CAST(approver AS STRING) AS approver
  FROM sets
  LATERAL VIEW explode(old_set) os AS approver
  WHERE NOT array_contains(new_set, approver)
),
events AS (
  SELECT CodigoCliente, approver, ts, 'ADD'    AS event_type FROM adds
  UNION ALL
  SELECT CodigoCliente, approver, ts, 'REMOVE' AS event_type FROM removes
),
-- Para cada Cliente+Aprovador, DataInicio = ts do ADD, DataFim = ts do próximo evento (normalmente REMOVE)
param_intervals AS (
  SELECT
    CodigoCliente,
    approver AS Aprovador,
    ts  AS DataInicio,
    LEAD(ts) OVER (PARTITION BY CodigoCliente, approver ORDER BY ts) AS DataFim
  FROM events
  WHERE event_type = 'ADD'
),
----------------------------------------------------------------------------------------------------------------------------------

tabela_preco_parceiro AS (
  SELECT DISTINCT OrderServiceId
  FROM gold.dim_maintenancelogpriceregulatorpartner
  WHERE SendDate IS NOT NULL
)



-------------------------------------------------------------------------------------------------------------------------------------
SELECT
    fmi.MaintenanceId                                                       AS NumeroOS,
    fmt.MaintenanceType                                                     AS TipoOS,
    fms.FirstApprovalTimestamp                                              AS DataAprovacao1OS,

    dwu.WebUserName                                                         AS NomeUsuario,
    dwu.WebUserSourceCode                                                   AS CodigoUsuario,

    dmv.MaintenanceVehicleModelId                                           AS CodigoModeloManutencao,
    dfc.CustomerShortName                                                   AS NomeCliente,
    dmv.CustomerId                                                          AS CodigoCliente,
    dmv.AdditionalInformation2Description                                   AS InformacaoAdicional2,

    dmm.SourceNumber                                                        AS CodigoEC,
    dmm.MerchantShortenedName                                               AS NomeEC,
    dmm.NameMerchantsTypes                                                  AS TipoEC,
    dmm.StateName                                                           AS UFEC,
    dmm.CityName                                                            AS CidadeEC,


    fmi.Sk_MaintenanceItem                                                  AS ChaveItem,
    dmp.PartName                                                            AS NomePeca,
    dmc.ComplementDescription                                               AS ComplementoConcatenadoPeca,
    dmif.PartManufacturerName                                               AS FabricantePeca,

    fmi.PartQuantity                                                        AS QuantidadePeca,
    fmi.PartUnitaryPrice                                                    AS ValorUnitarioPeca,
    QuantidadePeca * ValorUnitarioPeca                                      AS ValorTotalPeca,

    COALESCE(fmi.PartPriceNegociatedCustomer, fmi.PartPriceNegociated)      AS ValorUnitarioNegociado,
    COALESCE(fmi.PartPriceReferenceCustomer, fmi.PartReferencePrice)        AS ValorUnitarioReferencial,
    COALESCE(ValorUnitarioNegociado,ValorUnitarioReferencial)               AS ValorUnitarioHierarquiaReferencial,
    QuantidadePeca * ValorUnitarioHierarquiaReferencial                     AS ValorTotalHierarquiaReferencial,

    CASE
      WHEN ValorUnitarioPeca IS NULL THEN 'NA'
      WHEN ValorUnitarioPeca <= 0.01 THEN 'NA'
      WHEN ValorUnitarioHierarquiaReferencial IS NULL THEN 'NA'
      WHEN ValorUnitarioHierarquiaReferencial <= 0.01 THEN 'NA'
      WHEN ValorUnitarioPeca > ValorUnitarioHierarquiaReferencial THEN 'NOK'
      ELSE 'OK' END                                                         AS AderenciaPrecoReferencial,

    dmlprp.SendDate                                                         AS DataEnvioNegociacaoPrecoParceiro,
    dmlprp.PricePartInfo                                                    AS InfoPrecoParceiro
    
    
    
    
    
    

FROM hive_metastore.gold.fact_maintenanceitems AS fmi

  LEFT JOIN hive_metastore.gold.dim_maintenanceparts AS dmp
    ON fmi.Sk_MaintenancePart = dmp.Sk_MaintenancePart

  LEFT JOIN hive_metastore.gold.dim_maintenancecomplements AS dmc
    ON fmi.Sk_MaintenanceComplement = dmc.Sk_MaintenanceComplement

  LEFT JOIN hive_metastore.gold.fact_maintenanceservices AS fms
    ON fmi.MaintenanceId = fms.OrderServiceCode

  LEFT JOIN hive_metastore.gold.dim_maintenancetypes AS fmt
    ON fms.Sk_MaintenanceType = fmt.Sk_MaintenanceType

  LEFT JOIN hive_metastore.gold.dim_maintenancemerchants AS dmm
    ON fms.Sk_MaintenanceMerchant = dmm.Sk_MaintenanceMerchant

  LEFT JOIN hive_metastore.gold.dim_maintenancevehicles AS dmv
    ON fms.Sk_MaintenanceVehicle = dmv.Sk_MaintenanceVehicle

  LEFT JOIN hive_metastore.gold.dim_fuelcustomers AS dfc
    ON fms.Sk_FuelCustomer = dfc.Sk_FuelCustomer

  LEFT JOIN hive_metastore.gold.dim_webusers AS dwu
    ON fms.FirstApproverCode = dwu.WebUserSourceCode
  
  LEFT JOIN gold.dim_maintenancelogpriceregulatorpartner AS dmlprp
    ON fmi.MaintenanceItemSourceCode = dmlprp.OrderServiceItemId

  LEFT JOIN hive_metastore.gold.dim_maintenanceitemmanufacturers AS dmif
    ON fmi.Sk_ServiceItemManufacturer = dmif.Sk_ServiceItemManufacturer

  LEFT JOIN tabela_preco_parceiro
    ON fmi.MaintenanceId = tabela_preco_parceiro.OrderServiceId

  LEFT JOIN hive_metastore.gold.dim_maintenancelabors AS dml
    ON fmi.Sk_MaintenanceLabor = dml.Sk_MaintenanceLabor

WHERE 1=1
  AND fmi.CancellationTimestamp IS NULL
  AND fmi.ItemDisapprovalTimestamp IS NULL
  AND fms.FirstApprovalTimestamp >= TIMESTAMP '2025-04-01'
  -- Excluir serviços de guincho
  AND (dml.LaborName IS NULL OR dml.LaborName NOT LIKE '%GUINCHO%')
  -- Filtro de aprovadores ativos: apenas aprovadores que estavam ativos na data de aprovação
  AND (
    -- Caso 1: OS com negociação de preço parceiro (sempre incluir)
    tabela_preco_parceiro.OrderServiceId IS NOT NULL
    OR
    -- Caso 2: Aprovador estava ativo na data de aprovação
    EXISTS (
      SELECT 1
      FROM param_intervals pi
      WHERE pi.CodigoCliente = dmv.CustomerId
        AND pi.Aprovador = CAST(dwu.WebUserSourceCode AS STRING)
        AND fms.FirstApprovalTimestamp >= pi.DataInicio
        AND (pi.DataFim IS NULL OR fms.FirstApprovalTimestamp < pi.DataFim)
    )
  )
```

Tabelas SQL referenciadas: adds, events, gold.dim_maintenancelogpriceregulatorpartner, hive_metastore.gold.Dim_MaintenanceParameterLogValue, hive_metastore.gold.dim_fuelcustomers, hive_metastore.gold.dim_maintenancecomplements, hive_metastore.gold.dim_maintenanceitemmanufacturers, hive_metastore.gold.dim_maintenancelabors, hive_metastore.gold.dim_maintenancemerchants, hive_metastore.gold.dim_maintenanceparts, hive_metastore.gold.dim_maintenancetypes, hive_metastore.gold.dim_maintenancevehicles, hive_metastore.gold.dim_webusers, hive_metastore.gold.fact_maintenanceitems, hive_metastore.gold.fact_maintenanceservices, param_intervals, param_logs, removes, sets, tabela_preco_parceiro


### 3.x — `FactAprovacoesAposPrecoParceiro`

**Query Group:** Fatos

**Colunas (9):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| NumeroOS | int64 |  |  |  |
| CodigoCliente | string |  |  |  |
| NomeCliente | string |  |  |  |
| DataAprovacao | dateTime |  |  |  |
| AprovacaoAutomatica | boolean |  |  |  |
| TipoManutencao | string |  |  |  |
| ValorAprovado | double |  |  |  |
| TotalItensAprovadosNegociados | int64 |  |  |  |
| ValorAprovadoNegociado | double |  |  |  |

**SQL Databricks:**

```sql
WITH CTE AS (
  SELECT
    fmi.Sk_MaintenanceItem
    , fmi.MaintenanceID
    , fmi.PartPriceApproved
  FROM hive_metastore.gold.fact_maintenanceitems AS fmi
  
    LEFT JOIN hive_metastore.gold.dim_maintenancelogpriceregulatorpartner AS pr1
      ON pr1.PricePartReferencePriceNegId = fmi.PartPriceNegociatedId

    LEFT JOIN hive_metastore.gold.dim_maintenancelogpriceregulatorpartner AS pr2
      ON pr2.PricePartReferencePriceNegId = fmi.PartPriceNegociatedCustomerId

    LEFT JOIN hive_metastore.gold.dim_maintenancelabors AS dml
      ON fmi.Sk_MaintenanceLabor = dml.Sk_MaintenanceLabor
  
  WHERE 1=1
    AND fmi.ApprovalTimestamp IS NOT NULL
    AND (pr1.Sk_PriceRegulatorPartner IS NOT NULL OR pr2.Sk_PriceRegulatorPartner IS NOT NULL)
    AND (dml.LaborName IS NULL OR dml.LaborName NOT LIKE '%GUINCHO%')
)
SELECT
    fms.OrderServiceCode                                           AS NumeroOS
  , COUNT(DISTINCT CTE.Sk_MaintenanceItem)                         AS TotalItensAprovadosNegociados
  , SUM(CTE.PartPriceApproved)                                     AS ValorAprovadoNegociado
  , (fms.PartValue + fms.LaborValue)                               AS ValorAprovado
  , dfc.CustomerSourceCode                                         AS CodigoCliente
  , dfc.CustomerShortName                                          AS NomeCliente
  , date_format(fms.ApprovalTimestamp, 'yyyy-MM-dd')               AS DataAprovacao
  , dmt.MaintenanceType                                            AS TipoManutencao
  , fms.IsAutomaticApproval                                        AS AprovacaoAutomatica 

FROM hive_metastore.gold.fact_maintenanceservices AS fms
  
  LEFT JOIN hive_metastore.gold.dim_fuelcustomers AS dfc
    ON fms.Sk_FuelCustomer = dfc.Sk_FuelCustomer
  
  LEFT JOIN hive_metastore.gold.dim_maintenancetypes AS dmt
    ON fms.Sk_MaintenanceType = dmt.Sk_MaintenanceType
  
  RIGHT JOIN CTE
    ON CTE.maintenanceid = fms.OrderServiceCode

WHERE 1=1
  AND fms.ApprovalTimestamp >= '2025-04-01' 
  AND fms.OrderServiceCode = 18748595 -----------------------------Testando

GROUP BY
    fms.OrderServiceCode
  , fms.PartValue
  , fms.LaborValue
  , dfc.CustomerSourceCode
  , dfc.CustomerShortName
  , fms.ApprovalTimestamp
  , dmt.MaintenanceType
  , fms.IsAutomaticApproval
```

Tabelas SQL referenciadas: CTE, hive_metastore.gold.dim_fuelcustomers, hive_metastore.gold.dim_maintenancelabors, hive_metastore.gold.dim_maintenancelogpriceregulatorpartner, hive_metastore.gold.dim_maintenancetypes, hive_metastore.gold.fact_maintenanceitems, hive_metastore.gold.fact_maintenanceservices


### 3.x — `P_Aproveitamento` 🔒 (oculta)


**Colunas (3):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| P_Aproveitamento | N/A |  | Sim |  |
| P_Aproveitamento Campos | N/A |  | Sim |  |
| P_Aproveitamento Pedido | N/A |  | Sim |  |


### 3.x — `P_Travado` 🔒 (oculta)


**Colunas (3):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| P_Travado | N/A |  | Sim |  |
| P_Travado Campos | N/A |  | Sim |  |
| P_Travado Pedido | N/A |  | Sim |  |


### 3.x — `P_VA_Potencial` 🔒 (oculta)


**Colunas (3):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| P_VA_Potencial | N/A |  | Sim |  |
| P_VA_Potencial Campos | N/A |  | Sim |  |
| P_VA_Potencial Pedido | N/A |  | Sim |  |


### 3.x — `RelacaoClienteAprovador`


**Colunas (6):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| CodigoCliente | string |  |  |  |
| Aprovador | string |  |  |  |
| nome_aprovador | string |  |  |  |
| DataInicio | dateTime |  |  |  |
| DataFim | dateTime |  |  |  |
| NomeCliente | string |  |  |  |

**SQL Databricks:**

```sql
WITH logs AS (
  SELECT
    dmplv.ClientId AS CodigoCliente,
    CAST(dmplv.ParameterLogOrgValueModificationTimestamp AS TIMESTAMP) AS ts,
    COALESCE(dmplv.OldValueDescription, '') AS old_values,
    COALESCE(dmplv.NewValueDescription, '') AS new_values
  FROM hive_metastore.gold.Dim_MaintenanceParameterLogValue AS dmplv
  WHERE dmplv.ParameterId = 586
    -- opcional: limitar a um cliente específico
    -- AND dmplv.ClientId IN (37514,150797,158555)
),

-- Normaliza old/new em arrays (aceita ; ou , como separadores, remove espaços, vazios e duplicados)
sets AS (
  SELECT
    CodigoCliente,
    ts,
    array_distinct(
      filter(
        split(regexp_replace(old_values, '\\s+', ''), '[;,]+'),
        x -> x <> ''
      )
    ) AS old_set,
    array_distinct(
      filter(
        split(regexp_replace(new_values, '\\s+', ''), '[;,]+'),
        x -> x <> ''
      )
    ) AS new_set
  FROM logs
),

-- Inclusões: itens presentes em new_set e ausentes em old_set (ADD)
adds AS (
  SELECT
    CodigoCliente,
    ts,
    CAST(approver AS STRING) AS approver
  FROM sets
  LATERAL VIEW explode(new_set) ns AS approver
  WHERE NOT array_contains(old_set, approver)
),

-- Exclusões: itens presentes em old_set e ausentes em new_set (REMOVE)
removes AS (
  SELECT
    CodigoCliente,
    ts,
    CAST(approver AS STRING) AS approver
  FROM sets
  LATERAL VIEW explode(old_set) os AS approver
  WHERE NOT array_contains(new_set, approver)
),

events AS (
  SELECT CodigoCliente, approver, ts, 'ADD'    AS event_type FROM adds
  UNION ALL
  SELECT CodigoCliente, approver, ts, 'REMOVE' AS event_type FROM removes
),

-- Para cada cliente+aprovador, pegue o próximo evento após um ADD como DataFim
ordered AS (
  SELECT
    CodigoCliente,
    approver,
    event_type,
    ts,
    LEAD(ts) OVER (PARTITION BY CodigoCliente, approver ORDER BY ts)         AS next_ts,
    LEAD(event_type) OVER (PARTITION BY CodigoCliente, approver ORDER BY ts) AS next_event_type
  FROM events
)

SELECT
  CodigoCliente,
  dfc.CustomerShortName AS NomeCliente,
  -- Se preferir numérico:
  -- CAST(approver AS BIGINT) AS Aprovador,
  approver AS Aprovador,
  dwu.WebUserName AS nome_aprovador,
  date_format(ts, 'yyyy-MM-dd HH:mm') AS DataInicio,
  date_format(next_ts, 'yyyy-MM-dd HH:mm') AS DataFim
FROM ordered
LEFT JOIN hive_metastore.gold.dim_webusers AS dwu
  ON dwu.WebUserSourceCode = ordered.approver
LEFT JOIN hive_metastore.gold.dim_fuelcustomers AS dfc
  ON ordered.codigocliente = dfc.CustomerSourceCode
WHERE 1=1
AND event_type = 'ADD'

ORDER BY CodigoCliente, Aprovador, DataInicio
```

Tabelas SQL referenciadas: adds, events, hive_metastore.gold.Dim_MaintenanceParameterLogValue, hive_metastore.gold.dim_fuelcustomers, hive_metastore.gold.dim_webusers, logs, ordered, removes, sets


### 3.x — `RespostasFormulario`


**Colunas (18):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Id | string |  |  |  |
| Hora de início | string |  |  |  |
| Hora de conclusão | string |  |  |  |
| Email | string |  |  |  |
| Nome | string |  |  |  |
| Número da ordem | string |  |  |  |
| Data negociação | string |  |  |  |
| Cliente | string |  |  |  |
| EC aceitou a negociação? | string |  |  |  |
| Qual o motivo da recusa? | string |  |  |  |
| Período de trava | string |  |  |  |
| Qual o formato aceito pelo EC? | string |  |  |  |
| Número de itens travados | string |  |  |  |
| Descreva o valor referencial da ordem de serviço e o valor adequado para o item: | string |  |  |  |
| Qual é a peça com erro de referencial? | string |  |  |  |
| Arquivo complementar (print OS; Cilia; etc) | string |  |  |  |
| Inclua o ID da ligação Genesys | string |  |  |  |
| Coluna1 | string |  |  |  |

**Fonte externa:**
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Projeto Preço Parceiro.xlsx`


### 3.x — `RespostasFormularioDistintasOS` 🔒 (oculta)


**Colunas (1):**

| Coluna | Tipo | Pasta | Oculta | Calculada |
|---|---|---|---|---|
| Número da ordem | string |  | Sim |  |

**Fonte externa:**
- `https://edenred-my.sharepoint.com/personal/lucas_malessa_edenred_com/Documents/Projeto Preço Parceiro.xlsx`



---
## 4. Medidas DAX — Lógica de Negócio

### 📁 (sem pasta)

#### `OS Com Preço Travado`
- **Tabela:** _Medidas
- **Formato:** ``
- **Usa medidas:** Total VA travado

```dax
IF([Total VA travado] > 0, "Sim", "Não")
```

#### `OS Com Formulário Preenchido`
- **Tabela:** _Medidas
- **Formato:** ``
- **Usa medidas:** Total de respostas formulário

```dax
IF([Total de respostas formulário] > 0, "Sim", "Não")
```

### 📁 _Aprovações

#### `VA Peças`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[ValorTotalPeca]

```dax
SUM(FactAprovacaoPrecoParceiro[ValorTotalPeca])
```

#### `VA Peças Referencial Sem Negociado`
> VA Peças com Referencial, sem Negociado e desconsiderando ECs do tipo Concessionária
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[ValorUnitarioReferencial], FactAprovacaoPrecoParceiro[ValorUnitarioNegociado]

```dax
CALCULATE(
			    [VA Peças],
			    FactAprovacaoPrecoParceiro[ValorUnitarioReferencial] > 0                    -- Com preço referencial
			    && FactAprovacaoPrecoParceiro[ValorUnitarioNegociado] = BLANK()             -- Sem preço negociado
			)
```

#### `VA Peças Potencial`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças, VA Peças Referencial Sem Negociado
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[TipoEC]

```dax
CALCULATE(
			    [VA Peças Referencial Sem Negociado],
			    FactAprovacaoPrecoParceiro[TipoEC] <> "Concessionaria"
			)
```

#### `VA Peças Travado Preço Parceiro`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças, VA Peças Potencial
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro], FactAprovacaoPrecoParceiro[DataEnvioNegociacaoPrecoParceiro]

```dax
CALCULATE(
			    [VA Peças Potencial],
			    FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro] <> BLANK()
			    && FactAprovacaoPrecoParceiro[DataEnvioNegociacaoPrecoParceiro] <> BLANK()
			)
```

#### `% Aproveitamento`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** VA Peças, VA Peças Potencial, VA Peças Travado Preço Parceiro

```dax
DIVIDE([VA Peças Travado Preço Parceiro],[VA Peças Potencial])
```

#### `VA Peças Potencial Aderente`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças, VA Peças Potencial
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial]

```dax
CALCULATE(
			    [VA Peças Potencial],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "OK"
			)
```

#### `VA Peças Travado Preço Parceiro Aderente`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças, VA Peças Travado Preço Parceiro
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial]

```dax
CALCULATE(
			    [VA Peças Travado Preço Parceiro],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "OK"
			)
```

#### `% Aproveitamento Aderente`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** VA Peças, VA Peças Potencial, VA Peças Potencial Aderente, VA Peças Travado Preço Parceiro, VA Peças Travado Preço Parceiro Aderente

```dax
DIVIDE([VA Peças Travado Preço Parceiro Aderente],[VA Peças Potencial Aderente])
```

#### `VA Peças Travado Preço Parceiro Não Aderente`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças, VA Peças Travado Preço Parceiro
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial]

```dax
CALCULATE(
			    [VA Peças Travado Preço Parceiro],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "NOK"
			)
```

#### `% Travado não aderente`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** VA Peças, VA Peças Travado Preço Parceiro, VA Peças Travado Preço Parceiro Não Aderente

```dax
DIVIDE([VA Peças Travado Preço Parceiro Não Aderente],[VA Peças Travado Preço Parceiro])
```

### 📁 _Auditoria

#### `VA Travado Não Aderente`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial], FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro]

```dax
CALCULATE(
			    [VA Peças],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "NOK"
			    && FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro] > 0
			)
```

#### `VA Travado Aderente`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial], FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro]

```dax
CALCULATE(
			    [VA Peças],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "OK" 
			    && FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro] > 0
			)
```

#### `VA Travado Sem Referencial`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Peças
- **Colunas filtradas:** FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial], FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro]

```dax
CALCULATE(
			    [VA Peças],
			    FactAprovacaoPrecoParceiro[AderenciaPrecoReferencial] = "NA"
			    && FactAprovacaoPrecoParceiro[ValorUnitarioNegociadoPrecoParceiro] > 0
			)
```

#### `Total VA travado`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Travado Aderente, VA Travado Não Aderente, VA Travado Sem Referencial

```dax
[VA Travado Não Aderente] + [VA Travado Sem Referencial] + [VA Travado Aderente]
```

#### `% VA Travado Aderente`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** Total VA travado, VA Travado Aderente

```dax
DIVIDE([VA Travado Aderente], [Total VA travado])
```

#### `% VA Travado Não Aderente`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** Total VA travado, VA Travado Não Aderente

```dax
DIVIDE([VA Travado Não Aderente], [Total VA travado])
```

#### `% VA Travado Sem Referencial`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** Total VA travado, VA Travado Sem Referencial

```dax
DIVIDE([VA Travado Sem Referencial], [Total VA travado])
```

#### `VA Travado Incorreto`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** VA Travado Não Aderente, VA Travado Sem Referencial

```dax
[VA Travado Não Aderente] + [VA Travado Sem Referencial]
```

#### `% VA Travado Incorreto`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** Total VA travado, VA Travado Incorreto

```dax
DIVIDE([VA Travado Incorreto], [Total VA travado])
```

### 📁 _Efetividade

#### `Total OS PP`
- **Tabela:** _Medidas
- **Formato:** `0`
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[NumeroOS]

```dax
DISTINCTCOUNT(FactAprovacoesAposPrecoParceiro[NumeroOS])
```

#### `Total OS RI PP`
- **Tabela:** _Medidas
- **Formato:** `0`
- **Usa medidas:** Total OS PP
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica]

```dax
CALCULATE(
			    [Total OS PP],
			    FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica] = TRUE()
			)
```

#### `Total OS PP Sem RI`
- **Tabela:** _Medidas
- **Formato:** `0`
- **Usa medidas:** Total OS PP
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica]

```dax
CALCULATE(
			    [Total OS PP],
			    FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica] = FALSE()
			)
```

#### `Total VA PP`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[ValorAprovado]

```dax
SUM(FactAprovacoesAposPrecoParceiro[ValorAprovado])
```

#### `Total VA RI PP`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Usa medidas:** Total VA PP
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica]

```dax
CALCULATE(
			    [Total VA PP],
			    FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica] = TRUE()
			)
```

#### `Total Itens Aprovados PP`
- **Tabela:** _Medidas
- **Formato:** `#,0`
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[TotalItensAprovadosNegociados]

```dax
SUM(FactAprovacoesAposPrecoParceiro[TotalItensAprovadosNegociados])
```

#### `Total OS Sem RI PP`
- **Tabela:** _Medidas
- **Formato:** `#,0`
- **Usa medidas:** Total OS PP
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica]

```dax
CALCULATE(
			    [Total OS PP],
			    FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica] = FALSE()
			)
```

#### `Total VA Items Aprovação Manual PP`
- **Tabela:** _Medidas
- **Formato:** `"R$"\ #,0;-"R$"\ #,0;"R$"\ #,0`
- **Colunas filtradas:** FactAprovacoesAposPrecoParceiro[ValorAprovadoNegociado], FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica]

```dax
CALCULATE(
			    SUM(FactAprovacoesAposPrecoParceiro[ValorAprovadoNegociado]),
			    FactAprovacoesAposPrecoParceiro[AprovacaoAutomatica] = FALSE()
			)
```

### 📁 _Formulário

#### `Total de recusas`
- **Tabela:** _Medidas
- **Formato:** `0`
- **Usa medidas:** Total de respostas formulário
- **Colunas filtradas:** RespostasFormulario[EC aceitou a negociação?]

```dax
CALCULATE(
			    [Total de respostas formulário],
			    RespostasFormulario[EC aceitou a negociação?] = "Não"
			)
```

#### `Total de respostas formulário`
- **Tabela:** _Medidas
- **Formato:** `0`
- **Colunas filtradas:** RespostasFormulario[Número da ordem]

```dax
COUNT(RespostasFormulario[Número da ordem])
```

#### `% Recusas formulário`
- **Tabela:** _Medidas
- **Formato:** `0.00%;-0.00%;0.00%`
- **Usa medidas:** Total de recusas, Total de respostas formulário

```dax
DIVIDE([Total de recusas], [Total de respostas formulário])
```


---
## 5. Relacionamentos

| De (Tabela.Coluna) | Para (Tabela.Coluna) | Cross-Filter | Card. From |
|---|---|---|---|
| DimSupervisores.Coordenador | DimCoordenadores.Coordenador | bothDirections | many |
| DimAprovadores.Supervisor | DimSupervisores.Supervisor | bothDirections | many |
| RelacaoClienteAprovador.nome_aprovador | DimAprovadores.dUsuario | bothDirections | many |
| RespostasFormulario.'Número da ordem' | RespostasFormularioDistintasOS.'Número da ordem' | bothDirections | many |
| FactAprovacaoPrecoParceiro.NomeUsuario | DimAprovadores.dUsuario | bothDirections | many |
| FactAprovacaoPrecoParceiro.NumeroOS | RespostasFormularioDistintasOS.'Número da ordem' | bothDirections | many |
| FactAprovacaoPrecoParceiro.DataAprovacao1OS | DimCalendario.DataCompleta | bothDirections | many |
| P_VA_Potencial.'P_VA_Potencial Pedido' | Conexao.Codigo | bothDirections | one |
| P_Travado.'P_Travado Pedido' | Conexao.Codigo | bothDirections | one |
| P_Aproveitamento.'P_Aproveitamento Pedido' | Conexao.Codigo | bothDirections | one |
| FactAprovacoesAposPrecoParceiro.DataAprovacao | DimCalendario.DataCompleta | singleDirection | many |

### Diagrama de Relacionamentos (texto)

```
  DimSupervisores  ──(1:N)──▶  DimCoordenadores
     .Coordenador  →  .Coordenador
  DimAprovadores  ──(1:N)──▶  DimSupervisores
     .Supervisor  →  .Supervisor
  RelacaoClienteAprovador  ──(1:N)──▶  DimAprovadores
     .nome_aprovador  →  .dUsuario
  RespostasFormulario  ──(1:N)──▶  RespostasFormularioDistintasOS
     .'Número da ordem'  →  .'Número da ordem'
  FactAprovacaoPrecoParceiro  ──(1:N)──▶  DimAprovadores
     .NomeUsuario  →  .dUsuario
  FactAprovacaoPrecoParceiro  ──(1:N)──▶  RespostasFormularioDistintasOS
     .NumeroOS  →  .'Número da ordem'
  FactAprovacaoPrecoParceiro  ──(1:N)──▶  DimCalendario
     .DataAprovacao1OS  →  .DataCompleta
  P_VA_Potencial  ──(1:1)──▶  Conexao
     .'P_VA_Potencial Pedido'  →  .Codigo
  P_Travado  ──(1:1)──▶  Conexao
     .'P_Travado Pedido'  →  .Codigo
  P_Aproveitamento  ──(1:1)──▶  Conexao
     .'P_Aproveitamento Pedido'  →  .Codigo
  FactAprovacoesAposPrecoParceiro  ──(1:N)──▶  DimCalendario
     .DataAprovacao  →  .DataCompleta
```


---
## 6. Segurança em Nível de Linha (RLS)

### Role: `Admin`

- Sem filtros de tabela (Admin/read-all)


### Role: `Aprovadores`

- **DimAprovadores:** `DimAprovadores[E-mail] == USERNAME()`

### Role: `Coordenadores`

- **DimAprovadores:** `tablePermission DimCoordenadores = DimCoordenadores[E-mail] == USERNAME()`

### Role: `Supervisores`

- **DimSupervisores:** `DimSupervisores[E-mail] == USERNAME()`


---
## 7. Páginas do Relatório

| # | Nome | ID | Visuais |
|---|---|---|---|
| 1 | Visão geral de produtividade | b7bffaef152260be2e1e | 23 |
| 2 | Visão clientes e ECs | 50978c7363c43d1c4cdc | 23 |
| 3 | Visão auditoria | 2919a16523745073c901 | 21 |
| 4 | Tabelas extração aprovações | d62e089609626cd335b7 | 18 |
| 5 | Tabelas extração formulário | 844640615c392a20d4c7 | 17 |
| 6 | Relação aprovadores X clientes | 055c5fbd60e506904d2b | 15 |
| 7 | Eficiência Preço Parceiro Aprovação Manual | 23f4337278228043e014 | 8 |
| 8 | Eficiência Preço Parceiro RI | a2a460c0e8b862a68484 | 8 |


---
## 8. Resumo da Lógica de Negócio


### Contexto do Negócio
O **Painel Preço Parceiro** monitora a **negociação de preços de peças** entre 
a Edenred (gestão de frotas/manutenção) e os **Estabelecimentos Comerciais (ECs)** 
— oficinas mecânicas e concessionárias — que prestam serviços de manutenção.

### Conceitos-Chave

1. **Aprovação de OS (Ordem de Serviço):** Cada OS contém itens de peças aprovados 
   por um aprovador (WebUser) com valores unitários, referenciais e negociados.

2. **Preço Referencial:** Preço de referência cadastrado no sistema para cada peça, 
   hierarquicamente: pode ser do cliente-específico ou genérico.

3. **Preço Negociado (Preço Parceiro):** Valor travado/negociado com o EC para 
   uma peça específica, com validade em meses. Vem do módulo "Preço Regulador Parceiro".

4. **Aderência:** 
   - **OK** = Valor da peça ≤ Referencial hierárquico (correto)
   - **NOK** = Valor da peça > Referencial hierárquico (incorreto/acima)
   - **NA** = Sem referencial ou valor insignificante (≤ 0.01)

5. **VA Peças Potencial:** Valor de peças que TÊM preço referencial mas NÃO têm 
   negociado, excluindo concessionárias → é o universo onde PP deveria atuar.

6. **VA Peças Travado Preço Parceiro:** Subconjunto do Potencial onde já existe 
   negociação PP travada → é a contribuição real do processo.

7. **% Aproveitamento:** DIVIDE(Travado, Potencial) — eficiência do processo PP.

8. **Formulário de Respostas:** Registro manual (Excel) de contato com ECs sobre 
   aceitação/recusa da negociação de preço.

9. **Efetividade:** Análise das aprovações POSTERIORES ao travamento de preço, 
   verificando se o preço negociado foi realmente aplicado (RI = Aprovação Automática).

### Cadeia Hierárquica (RLS)
```
Coordenador → Supervisor → Aprovador → Clientes (via carteira)
```
Cada nível vê apenas os dados de sua hierarquia. Admin vê tudo.

### Fontes de Dados
- **Databricks (Azure):** Tabelas fato e calendário (SQL sobre gold layer)
- **SharePoint Excel:** Dimensões de carteira (Coordenadores, Supervisores, Aprovadores) 
  e respostas do formulário de negociação


---
## 9. Field Parameters (Parâmetros de Campo)

### `P_Aproveitamento`

**Fonte:** [CALCULADA] {
				    ("% Aproveitamento VA Aderente", NAMEOF('_Medidas'[% Aproveitamento Aderente]), 1),
				    ("% Aproveitamento VA", NAMEOF('_Medidas'[% Aproveitamento]), 0)
				}

Permite alternância dinâmica de medidas em visuais do relatório.

### `P_Travado`

**Fonte:** [CALCULADA] {
				    ("VA Peças Travado Preço Parceiro Aderente", NAMEOF('_Medidas'[VA Peças Travado Preço Parceiro Aderente]), 1),
				    ("VA Peças Travado Preço Parceiro", NAMEOF('_Medidas'[VA Peças Travado Preço Parceiro]), 0)
				}

Permite alternância dinâmica de medidas em visuais do relatório.

### `P_VA_Potencial`

**Fonte:** [CALCULADA] {
				    ("VA Peças Potencial Aderente", NAMEOF('_Medidas'[VA Peças Potencial Aderente]), 1),
				    ("VA Peças Potencial", NAMEOF('_Medidas'[VA Peças Potencial]), 0)
				}

Permite alternância dinâmica de medidas em visuais do relatório.


---
## 10. Tabelas de Auto-Documentação

O modelo inclui tabelas calculadas via `INFO.VIEW.*()` para auto-documentação:

- **Doc_Colunas**: [CALCULADA] INFO.VIEW.COLUMNS()
- **Doc_Medidas**: [CALCULADA] INFO.VIEW.MEASURES()
- **Doc_Relacionamentos**: [CALCULADA] INFO.VIEW.RELATIONSHIPS()
- **Doc_Tabelas**: [CALCULADA] INFO.VIEW.TABLES()


---
## 11. Template de Prompt Sugerido


Copie e cole o conteúdo **das seções 1 a 10** acima como contexto inicial de qualquer 
prompt para a IA. Exemplo de uso:

```
Contexto: [COLE O CONTEÚDO DAS SEÇÕES 1-10 AQUI]

Tarefa: [DESCREVA SUA TAREFA]

Exemplos de tarefas:
- Criar nova medida DAX para calcular X
- Adicionar nova coluna calculada na tabela Y
- Modificar o SQL da FactAprovacaoPrecoParceiro para incluir Z
- Criar novo role RLS para perfil W
- Explicar a lógica da medida '% Aproveitamento'
- Otimizar a query SQL com CTE para melhor performance
```
