# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SCRIPT EXPLORATÓRIO - Painel Preço Parceiro (.pbip)                       ║
║  Objetivo: Extrair lógica de negócio e arquitetura lógica do modelo        ║
║            semântico para gerar um prompt de contexto completo.            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Uso:
    python explorar_modelo.py

O script varre todos os .tmdl e .json do projeto e gera um arquivo
"contexto_modelo_preco_parceiro.md" com a documentação completa.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
SCRIPT_DIR = Path(__file__).resolve().parent
SEMANTIC_MODEL_DIR = SCRIPT_DIR / "Painel Preço Parceiro.SemanticModel" / "definition"
REPORT_DIR = SCRIPT_DIR / "Painel Preço Parceiro.Report" / "definition"
OUTPUT_FILE = SCRIPT_DIR / "contexto_modelo_preco_parceiro.md"

# ══════════════════════════════════════════════════════════════════════════════
# 1. LEITURA DOS ARQUIVOS TMDL
# ══════════════════════════════════════════════════════════════════════════════

def ler_arquivo(caminho: Path) -> str:
    """Lê arquivo com fallback de encoding."""
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return caminho.read_text(encoding=enc)
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return ""


def listar_tmdl(pasta: Path) -> list[Path]:
    """Lista todos os .tmdl recursivamente."""
    return sorted(pasta.rglob("*.tmdl"))


# ══════════════════════════════════════════════════════════════════════════════
# 2. EXTRAÇÕES VIA REGEX
# ══════════════════════════════════════════════════════════════════════════════

# ---- 2a. Tabelas e Colunas ----
RE_TABLE = re.compile(r"^table\s+(.+?)$", re.MULTILINE)
RE_TABLE_HIDDEN = re.compile(r"^\ttisHidden", re.MULTILINE)
RE_COLUMN = re.compile(
    r"^\tcolumn\s+(?:'([^']+)'|(\S+))",
    re.MULTILINE,
)
RE_COLUMN_DATATYPE = re.compile(r"^\t\tdataType:\s*(.+)$", re.MULTILINE)
RE_COLUMN_FOLDER = re.compile(r"^\t\tdisplayFolder:\s*(.+)$", re.MULTILINE)
RE_COLUMN_HIDDEN = re.compile(r"^\t\tisHidden", re.MULTILINE)
RE_COLUMN_CALC = re.compile(
    r"^\tcolumn\s+(?:'([^']+)'|(\S+))\s*=\s*$",
    re.MULTILINE,
)

# ---- 2b. Medidas (DAX) ----
RE_MEASURE = re.compile(
    r"^\tmeasure\s+'([^']+)'\s*=\s*\n((?:\t{2,}.*\n)+)",
    re.MULTILINE,
)
RE_MEASURE_FORMAT = re.compile(r"^\t\tformatString:\s*(.+)$", re.MULTILINE)
RE_MEASURE_FOLDER = re.compile(r"^\t\tdisplayFolder:\s*(.+)$", re.MULTILINE)
RE_MEASURE_DESC = re.compile(r"^\t///\s*(.+)$", re.MULTILINE)

# ---- 2c. Partições / Power Query (M) ----
RE_PARTITION = re.compile(
    r"^\tpartition\s+.+?=\s+m\n(?:\t\t.+\n)*?\t\tsource\s*=\s*\n((?:\t{3,}.*\n)+)",
    re.MULTILINE,
)
RE_PARTITION_CALC = re.compile(
    r"^\tpartition\s+.+?=\s+calculated\n(?:\t\t.+\n)*?\t\tsource\s*=\s*\n((?:\t{3,}.*\n)+)",
    re.MULTILINE,
)

# ---- 2d. Relacionamentos ----
RE_RELATIONSHIP = re.compile(
    r"^relationship\s+\S+\n((?:\t.+\n)+)", re.MULTILINE
)
RE_REL_FROM = re.compile(r"fromColumn:\s*(.+?)$", re.MULTILINE)
RE_REL_TO = re.compile(r"toColumn:\s*(.+?)$", re.MULTILINE)
RE_REL_CROSS = re.compile(r"crossFilteringBehavior:\s*(.+?)$", re.MULTILINE)
RE_REL_CARD = re.compile(r"fromCardinality:\s*(.+?)$", re.MULTILINE)

# ---- 2e. Expressões (Parâmetros e Fontes) ----
RE_EXPRESSION = re.compile(
    r"^expression\s+(\S+)\s*=\s*\n?((?:.*\n)*?)(?=^expression|\Z)",
    re.MULTILINE,
)

# ---- 2f. Roles (RLS) ----
RE_ROLE = re.compile(r"^role\s+(.+?)$", re.MULTILINE)
RE_TABLE_PERMISSION = re.compile(
    r"^\ttablePermission\s+(\S+)\s*=?\s*(.*?)$", re.MULTILINE
)

# ---- 2g. SQL embutido na M ----
RE_SQL_BLOCK = re.compile(r'Azure\("(.*?)"\)', re.DOTALL)
RE_SQL_INLINE = re.compile(r'Azure\("([^"]+)"\)')

# ---- 2h. Hierarquias ----
RE_HIERARCHY = re.compile(
    r"^\thierarchy\s+'([^']+)'\n((?:\t{2,}.*\n)+)", re.MULTILINE
)
RE_HIER_LEVEL = re.compile(r"^\t\tlevel\s+(\S+)", re.MULTILINE)

# ---- 2i. Fontes de dados externas (Web.Contents, Excel) ----
RE_WEB_CONTENTS = re.compile(r'Web\.Contents\("([^"]+)"\)')
RE_DATABRICKS = re.compile(r"Databricks\.Query\(([^)]+)\)")

# ---- 2j. Query Groups ----
RE_QUERY_GROUP = re.compile(r"queryGroup:\s*(.+)$", re.MULTILINE)


# ══════════════════════════════════════════════════════════════════════════════
# 3. FUNÇÕES DE PARSING
# ══════════════════════════════════════════════════════════════════════════════

def parse_tabela(conteudo: str, nome_arquivo: str) -> dict:
    """Extrai metadados de uma tabela TMDL."""
    tab_match = RE_TABLE.search(conteudo)
    if not tab_match:
        return {}

    nome_tabela = tab_match.group(1).strip("'").strip()
    is_hidden = bool(re.search(r"^\tisHidden", conteudo, re.MULTILINE))

    # Colunas
    colunas = []
    # Dividir o conteúdo por blocos de coluna
    col_blocks = re.split(r"(?=^\tcolumn\s)", conteudo, flags=re.MULTILINE)
    for blk in col_blocks:
        col_m = RE_COLUMN.match(blk)
        if not col_m:
            continue
        col_name = col_m.group(1) or col_m.group(2)
        dt = RE_COLUMN_DATATYPE.search(blk)
        folder = RE_COLUMN_FOLDER.search(blk)
        hidden = bool(RE_COLUMN_HIDDEN.search(blk))
        is_calc = "=" in blk.split("\n")[0] if blk else False
        colunas.append({
            "nome": col_name,
            "tipo": dt.group(1).strip() if dt else "N/A",
            "displayFolder": folder.group(1).strip() if folder else "",
            "oculta": hidden,
            "calculada": is_calc,
        })

    # Medidas
    medidas = []
    measure_blocks = re.split(r"(?=^\tmeasure\s)", conteudo, flags=re.MULTILINE)
    for blk in measure_blocks:
        m = re.match(r"^\tmeasure\s+'([^']+)'\s*=", blk, re.MULTILINE)
        if not m:
            continue
        measure_name = m.group(1)

        # Extrair DAX (tudo entre o = e a próxima propriedade de nível \t\t que não é DAX)
        dax_lines = []
        lines = blk.split("\n")
        capturing = False
        for line in lines:
            if line.strip().startswith("measure "):
                continue
            if capturing:
                # Parar se encontrar formatString, displayFolder, lineageTag, annotation
                if re.match(r"^\t\t(formatString|displayFolder|lineageTag|annotation)", line):
                    break
                if re.match(r"^\t///", line):
                    break
                dax_lines.append(line)
            if "=" in line and not capturing and "measure" not in line.lower():
                pass
            if line.strip() == "" and not capturing:
                continue
            if re.match(r"^\t\t\t", line) and not capturing:
                capturing = True
                dax_lines.append(line)

        dax_raw = "\n".join(dax_lines).strip()
        # Limpar marcadores ```
        dax_raw = re.sub(r"```", "", dax_raw).strip()

        fmt = RE_MEASURE_FORMAT.search(blk)
        folder = RE_MEASURE_FOLDER.search(blk)
        desc_lines = RE_MEASURE_DESC.findall(blk)

        medidas.append({
            "nome": measure_name,
            "dax": dax_raw,
            "formatString": fmt.group(1).strip() if fmt else "",
            "displayFolder": folder.group(1).strip() if folder else "",
            "descricao": " ".join(desc_lines).strip() if desc_lines else "",
        })

    # Partição / Fonte M
    fonte_m = ""
    part_m = RE_PARTITION.search(conteudo)
    if part_m:
        fonte_m = part_m.group(1).strip()
    part_calc = RE_PARTITION_CALC.search(conteudo)
    if part_calc:
        fonte_m = "[CALCULADA] " + part_calc.group(1).strip()

    # SQL embutido
    sql_queries = []
    for sq in RE_SQL_BLOCK.finditer(conteudo):
        raw_sql = sq.group(1)
        # Decodificar #(lf) → \n e #(tab) → \t
        raw_sql = raw_sql.replace("#(lf)", "\n").replace("#(tab)", "\t")
        sql_queries.append(raw_sql.strip())

    # Fontes externas
    fontes_externas = RE_WEB_CONTENTS.findall(conteudo)

    # Query Group
    qg = RE_QUERY_GROUP.search(conteudo)
    query_group = qg.group(1).strip() if qg else ""

    # Hierarquias
    hierarquias = []
    for hier_m in RE_HIERARCHY.finditer(conteudo):
        h_name = hier_m.group(1)
        levels = RE_HIER_LEVEL.findall(hier_m.group(2))
        hierarquias.append({"nome": h_name, "niveis": levels})

    return {
        "nome": nome_tabela,
        "arquivo": nome_arquivo,
        "oculta": is_hidden,
        "queryGroup": query_group,
        "colunas": colunas,
        "medidas": medidas,
        "fonteM": fonte_m,
        "sqlQueries": sql_queries,
        "fontesExternas": fontes_externas,
        "hierarquias": hierarquias,
    }


def parse_relacionamentos(conteudo: str) -> list[dict]:
    """Extrai relacionamentos do relationships.tmdl."""
    rels = []
    for m in RE_RELATIONSHIP.finditer(conteudo):
        blk = m.group(1)
        fr = RE_REL_FROM.search(blk)
        to = RE_REL_TO.search(blk)
        cross = RE_REL_CROSS.search(blk)
        card = RE_REL_CARD.search(blk)
        if fr and to:
            from_col = fr.group(1).strip()
            to_col = to.group(1).strip()
            from_table = from_col.split(".")[0] if "." in from_col else ""
            to_table = to_col.split(".")[0] if "." in to_col else ""
            rels.append({
                "de_tabela": from_table,
                "de_coluna": from_col,
                "para_tabela": to_table,
                "para_coluna": to_col,
                "crossFilter": cross.group(1).strip() if cross else "singleDirection",
                "cardinalidade_from": card.group(1).strip() if card else "many",
            })
    return rels


def parse_expressoes(conteudo: str) -> list[dict]:
    """Extrai expressões/parâmetros do expressions.tmdl."""
    resultados = []
    blocos = re.split(r"(?=^expression\s)", conteudo, flags=re.MULTILINE)
    for blk in blocos:
        m = re.match(r"^expression\s+(\S+)\s*=", blk)
        if not m:
            continue
        nome = m.group(1)
        is_param = "IsParameterQuery=true" in blk
        qg = RE_QUERY_GROUP.search(blk)
        # Extrair valor
        valor_match = re.search(r'=\s*"([^"]+)"', blk)
        valor_m = re.search(r"let\s*\n((?:.*\n)*?)\s*in\s*\n", blk, re.MULTILINE)
        resultados.append({
            "nome": nome,
            "parametro": is_param,
            "valor": valor_match.group(1) if valor_match else "",
            "queryGroup": qg.group(1).strip() if qg else "",
            "expressaoM": valor_m.group(0).strip() if valor_m else "",
        })
    return resultados


def parse_roles(pasta_roles: Path) -> list[dict]:
    """Extrai roles de segurança (RLS)."""
    roles = []
    for f in sorted(pasta_roles.glob("*.tmdl")):
        conteudo = ler_arquivo(f)
        role_m = RE_ROLE.search(conteudo)
        if not role_m:
            continue
        nome = role_m.group(1)
        perms = []
        for tp in RE_TABLE_PERMISSION.finditer(conteudo):
            tabela = tp.group(1)
            expressao = tp.group(2).strip() if tp.group(2) else ""
            perms.append({"tabela": tabela, "expressao": expressao})
        roles.append({"nome": nome, "permissoes": perms})
    return roles


def parse_paginas(report_dir: Path) -> list[dict]:
    """Extrai informações das páginas do relatório."""
    pages_json = report_dir / "pages" / "pages.json"
    if not pages_json.exists():
        return []

    meta = json.loads(ler_arquivo(pages_json))
    page_order = meta.get("pageOrder", [])
    paginas = []

    for page_id in page_order:
        page_json = report_dir / "pages" / page_id / "page.json"
        if page_json.exists():
            page_data = json.loads(ler_arquivo(page_json))
            nome = page_data.get("displayName", page_id)
            visuals_dir = report_dir / "pages" / page_id / "visuals"
            num_visuais = 0
            if visuals_dir.exists():
                num_visuais = len([d for d in visuals_dir.iterdir() if d.is_dir()])
            paginas.append({
                "id": page_id,
                "nome": nome,
                "numVisuais": num_visuais,
            })
    return paginas


def analisar_dependencias_medidas(medidas_all: list[dict]) -> dict:
    """Analisa dependências entre medidas (quais medidas usam quais)."""
    nomes = {m["nome"] for m in medidas_all}
    deps = {}
    for m in medidas_all:
        usadas = set()
        for outra in nomes:
            if outra != m["nome"] and outra in m["dax"]:
                usadas.add(outra)
        # Também capturar referências a tabelas/colunas
        tabelas_ref = re.findall(
            r"(FactAprovacaoPrecoParceiro|FactAprovacoesAposPrecoParceiro|RespostasFormulario|"
            r"DimAprovadores|DimSupervisores|DimCoordenadores|DimCalendario|RelacaoClienteAprovador)\[([^\]]+)\]",
            m["dax"],
        )
        deps[m["nome"]] = {
            "medidas_dependentes": sorted(usadas),
            "colunas_referenciadas": [f"{t}[{c}]" for t, c in tabelas_ref],
        }
    return deps


def extrair_tabelas_sql(sql: str) -> list[str]:
    """Extrai nomes de tabelas referenciadas em SQL."""
    pattern = r"(?:FROM|JOIN)\s+([\w.]+)"
    return list(set(re.findall(pattern, sql, re.IGNORECASE)))


# ══════════════════════════════════════════════════════════════════════════════
# 4. GERAÇÃO DO RELATÓRIO MARKDOWN
# ══════════════════════════════════════════════════════════════════════════════

def gerar_markdown(
    tabelas: list[dict],
    rels: list[dict],
    expressoes: list[dict],
    roles: list[dict],
    paginas: list[dict],
    deps_medidas: dict,
) -> str:
    md = []
    md.append("# 📊 Contexto Completo — Modelo Semântico: Painel Preço Parceiro\n")
    md.append("> **Gerado automaticamente** pelo script `explorar_modelo.py`")
    md.append("> Use este arquivo como contexto (prompt) para qualquer assistente de IA.\n")

    # ---- SUMÁRIO EXECUTIVO ----
    md.append("---\n## 1. Sumário Executivo\n")
    total_tab = len(tabelas)
    total_col = sum(len(t["colunas"]) for t in tabelas)
    total_med = sum(len(t["medidas"]) for t in tabelas)
    total_rel = len(rels)
    total_roles = len(roles)
    total_pages = len(paginas)
    tabs_fato = [t for t in tabelas if t["nome"].startswith("Fact")]
    tabs_dim = [t for t in tabelas if t["nome"].startswith("Dim")]
    tabs_param = [t for t in tabelas if t["nome"].startswith("P_")]
    tabs_doc = [t for t in tabelas if t["nome"].startswith("Doc_")]
    tabs_outras = [t for t in tabelas if t not in tabs_fato + tabs_dim + tabs_param + tabs_doc]

    md.append(f"| Elemento | Quantidade |")
    md.append(f"|---|---|")
    md.append(f"| Tabelas | {total_tab} |")
    md.append(f"| — Fatos | {len(tabs_fato)} |")
    md.append(f"| — Dimensões | {len(tabs_dim)} |")
    md.append(f"| — Parâmetros Field | {len(tabs_param)} |")
    md.append(f"| — Documentação | {len(tabs_doc)} |")
    md.append(f"| — Outras (Medidas, Conexão, Formulário, etc.) | {len(tabs_outras)} |")
    md.append(f"| Colunas (total) | {total_col} |")
    md.append(f"| Medidas DAX | {total_med} |")
    md.append(f"| Relacionamentos | {total_rel} |")
    md.append(f"| Roles (RLS) | {total_roles} |")
    md.append(f"| Páginas do relatório | {total_pages} |")

    # ---- ARQUITETURA DE DADOS ----
    md.append("\n---\n## 2. Arquitetura de Dados / Fontes\n")

    md.append("### 2.1 Parâmetros de Conexão\n")
    for expr in expressoes:
        if expr["parametro"]:
            md.append(f"- **{expr['nome']}** = `{expr['valor']}`")
    md.append("")

    md.append("### 2.2 Fontes de Dados por Tabela\n")
    md.append("| Tabela | Query Group | Fonte |")
    md.append("|---|---|---|")
    for t in tabelas:
        fonte_tipo = "Calculada (DAX)" if t["fonteM"].startswith("[CALCULADA]") else ""
        if t["sqlQueries"]:
            fonte_tipo = "Databricks SQL (via Azure)"
        elif t["fontesExternas"]:
            fonte_tipo = "Excel/SharePoint"
        elif not fonte_tipo:
            fonte_tipo = "Inline / Hardcoded"
        md.append(f"| {t['nome']} | {t['queryGroup']} | {fonte_tipo} |")
    md.append("")

    # Agrupar fontes SharePoint
    todas_fontes = set()
    for t in tabelas:
        for f in t["fontesExternas"]:
            todas_fontes.add(f)
    if todas_fontes:
        md.append("### 2.3 URLs de Fontes Externas (SharePoint)\n")
        for url in sorted(todas_fontes):
            md.append(f"- `{url}`")
        md.append("")

    # ---- TABELAS DETALHADAS ----
    md.append("\n---\n## 3. Tabelas — Detalhamento\n")

    for t in tabelas:
        if t["nome"].startswith("Doc_"):
            continue  # Skip documentation tables
        hidden_tag = " 🔒 (oculta)" if t["oculta"] else ""
        md.append(f"### 3.x — `{t['nome']}`{hidden_tag}\n")
        if t["queryGroup"]:
            md.append(f"**Query Group:** {t['queryGroup']}")

        # Colunas
        if t["colunas"]:
            md.append(f"\n**Colunas ({len(t['colunas'])}):**\n")
            md.append("| Coluna | Tipo | Pasta | Oculta | Calculada |")
            md.append("|---|---|---|---|---|")
            for c in t["colunas"]:
                md.append(
                    f"| {c['nome']} | {c['tipo']} | {c['displayFolder']} "
                    f"| {'Sim' if c['oculta'] else ''} "
                    f"| {'Sim' if c['calculada'] else ''} |"
                )
            md.append("")

        # Hierarquias
        for h in t["hierarquias"]:
            md.append(f"**Hierarquia:** `{h['nome']}` → {' > '.join(h['niveis'])}\n")

        # SQL embutido
        if t["sqlQueries"]:
            md.append("**SQL Databricks:**\n")
            for i, sql in enumerate(t["sqlQueries"]):
                md.append(f"```sql\n{sql}\n```\n")
                # Tabelas referenciadas
                tabs_sql = extrair_tabelas_sql(sql)
                if tabs_sql:
                    md.append(f"Tabelas SQL referenciadas: {', '.join(sorted(tabs_sql))}\n")

        # Fontes externas
        if t["fontesExternas"]:
            md.append("**Fonte externa:**")
            for url in t["fontesExternas"]:
                md.append(f"- `{url}`")
            md.append("")

        md.append("")

    # ---- MEDIDAS DAX ----
    md.append("\n---\n## 4. Medidas DAX — Lógica de Negócio\n")

    # Agrupar por displayFolder
    medidas_por_folder = defaultdict(list)
    for t in tabelas:
        for m in t["medidas"]:
            folder = m["displayFolder"] or "(sem pasta)"
            medidas_por_folder[folder].append({**m, "tabela": t["nome"]})

    for folder in sorted(medidas_por_folder.keys()):
        md.append(f"### 📁 {folder}\n")
        for m in medidas_por_folder[folder]:
            md.append(f"#### `{m['nome']}`")
            if m["descricao"]:
                md.append(f"> {m['descricao']}")
            md.append(f"- **Tabela:** {m['tabela']}")
            md.append(f"- **Formato:** `{m['formatString']}`")

            # Dependências
            if m["nome"] in deps_medidas:
                dep = deps_medidas[m["nome"]]
                if dep["medidas_dependentes"]:
                    md.append(f"- **Usa medidas:** {', '.join(dep['medidas_dependentes'])}")
                if dep["colunas_referenciadas"]:
                    md.append(f"- **Colunas filtradas:** {', '.join(dep['colunas_referenciadas'])}")

            md.append(f"\n```dax\n{m['dax']}\n```\n")

    # ---- RELACIONAMENTOS ----
    md.append("\n---\n## 5. Relacionamentos\n")
    md.append("| De (Tabela.Coluna) | Para (Tabela.Coluna) | Cross-Filter | Card. From |")
    md.append("|---|---|---|---|")
    for r in rels:
        md.append(
            f"| {r['de_coluna']} | {r['para_coluna']} "
            f"| {r['crossFilter']} | {r['cardinalidade_from']} |"
        )

    # Diagrama textual
    md.append("\n### Diagrama de Relacionamentos (texto)\n")
    md.append("```")
    for r in rels:
        card = "1:N" if r["cardinalidade_from"] == "many" else "1:1"
        md.append(f"  {r['de_tabela']}  ──({card})──▶  {r['para_tabela']}")
        md.append(f"     .{r['de_coluna'].split('.')[-1]}  →  .{r['para_coluna'].split('.')[-1]}")
    md.append("```\n")

    # ---- RLS / SEGURANÇA ----
    md.append("\n---\n## 6. Segurança em Nível de Linha (RLS)\n")
    for role in roles:
        md.append(f"### Role: `{role['nome']}`\n")
        if not role["permissoes"]:
            md.append("- Sem filtros de tabela (Admin/read-all)\n")
        for p in role["permissoes"]:
            if p["expressao"]:
                md.append(f"- **{p['tabela']}:** `{p['expressao']}`")
            else:
                md.append(f"- **{p['tabela']}:** (sem expressão explícita — herda)")
        md.append("")

    # ---- PÁGINAS DO RELATÓRIO ----
    md.append("\n---\n## 7. Páginas do Relatório\n")
    md.append("| # | Nome | ID | Visuais |")
    md.append("|---|---|---|---|")
    for i, p in enumerate(paginas, 1):
        md.append(f"| {i} | {p['nome']} | {p['id']} | {p['numVisuais']} |")
    md.append("")

    # ---- LÓGICA DE NEGÓCIO RESUMO ----
    md.append("\n---\n## 8. Resumo da Lógica de Negócio\n")
    md.append("""
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
""")

    # ---- FIELD PARAMETERS ----
    md.append("\n---\n## 9. Field Parameters (Parâmetros de Campo)\n")
    for t in tabelas:
        if t["nome"].startswith("P_"):
            md.append(f"### `{t['nome']}`\n")
            md.append(f"**Fonte:** {t['fonteM']}\n")
            md.append("Permite alternância dinâmica de medidas em visuais do relatório.\n")

    # ---- DOCUMENTAÇÃO INTERNA ----
    md.append("\n---\n## 10. Tabelas de Auto-Documentação\n")
    md.append("O modelo inclui tabelas calculadas via `INFO.VIEW.*()` para auto-documentação:\n")
    for t in tabelas:
        if t["nome"].startswith("Doc_"):
            md.append(f"- **{t['nome']}**: {t['fonteM']}")
    md.append("")

    # ---- PROMPT TEMPLATE ----
    md.append("\n---\n## 11. Template de Prompt Sugerido\n")
    md.append("""
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
""")

    return "\n".join(md)


# ══════════════════════════════════════════════════════════════════════════════
# 5. MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  EXPLORADOR DE MODELO SEMÂNTICO — Painel Preço Parceiro")
    print("=" * 70)

    # 1. Parsear tabelas
    tabelas = []
    tables_dir = SEMANTIC_MODEL_DIR / "tables"
    if tables_dir.exists():
        for f in sorted(tables_dir.glob("*.tmdl")):
            conteudo = ler_arquivo(f)
            parsed = parse_tabela(conteudo, f.name)
            if parsed:
                tabelas.append(parsed)
                print(f"  ✓ Tabela: {parsed['nome']} "
                      f"({len(parsed['colunas'])} cols, {len(parsed['medidas'])} medidas)")

    # 2. Parsear relacionamentos
    rel_file = SEMANTIC_MODEL_DIR / "relationships.tmdl"
    rels = parse_relacionamentos(ler_arquivo(rel_file)) if rel_file.exists() else []
    print(f"\n  ✓ Relacionamentos: {len(rels)}")

    # 3. Parsear expressões
    expr_file = SEMANTIC_MODEL_DIR / "expressions.tmdl"
    expressoes = parse_expressoes(ler_arquivo(expr_file)) if expr_file.exists() else []
    print(f"  ✓ Expressões/Parâmetros: {len(expressoes)}")

    # 4. Parsear roles
    roles_dir = SEMANTIC_MODEL_DIR / "roles"
    roles = parse_roles(roles_dir) if roles_dir.exists() else []
    print(f"  ✓ Roles (RLS): {len(roles)}")

    # 5. Parsear páginas
    paginas = parse_paginas(REPORT_DIR) if REPORT_DIR.exists() else []
    print(f"  ✓ Páginas: {len(paginas)}")

    # 6. Analisar dependências de medidas
    todas_medidas = []
    for t in tabelas:
        todas_medidas.extend(t["medidas"])
    deps = analisar_dependencias_medidas(todas_medidas)

    # 7. Gerar markdown
    md = gerar_markdown(tabelas, rels, expressoes, roles, paginas, deps)

    # 8. Salvar
    OUTPUT_FILE.write_text(md, encoding="utf-8")
    print(f"\n{'=' * 70}")
    print(f"  ✅ Arquivo gerado: {OUTPUT_FILE}")
    print(f"  📋 Use o conteúdo desse arquivo como contexto para seus prompts!")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
