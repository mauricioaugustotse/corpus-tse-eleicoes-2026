"""Reproduz a auditoria de confrontos a partir dos ZIPs oficiais congelados.

Entradas: originais/*.zip, fontes.json, resumo.json, curadoria_confrontos.json.
Saídas: confrontos.csv, campanha_resumo.json.
Não consulta serviços externos nem bases privadas.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CURADORIA = json.loads((ROOT / "curadoria_confrontos.json").read_text(encoding="utf-8"))
SOURCES = json.loads((ROOT / "fontes.json").read_text(encoding="utf-8"))
RESUMO = json.loads((ROOT / "resumo.json").read_text(encoding="utf-8"))
DATA_INICIO = RESUMO["inicio_decisao"]
DATA_FIM = RESUMO["fim_decisao"]
GERACAO_BULK = SOURCES["decisoes"]["DT_GERACAO"] + " " + SOURCES["decisoes"]["HH_GERACAO"] + " BRT"
IDS = set(CURADORIA)
assert len(IDS) == 132


def rows_from_zip(stem: str, source_key: str):
    path = ROOT / "originais" / f"{stem}.zip"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == SOURCES[source_key]["sha256"], (path, digest)
    with zipfile.ZipFile(path) as archive:
        with archive.open(f"{stem}.csv") as raw:
            yield from csv.DictReader(io.TextIOWrapper(raw, encoding="latin1"), delimiter=";")


def normalized(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value.upper())
        if not unicodedata.combining(char)
    )


def campaign(name: str) -> str | None:
    value = normalized(name)
    if any(term in value for term in (
        "LUIZ INACIO LULA DA SILVA",
        "GERALDO JOSE RODRIGUES ALCKMIN FILHO",
        "COLIGACAO BRASIL PRONTO PRA MAIS",
        "FEDERACAO BRASIL DA ESPERANCA",
        "PARTIDO DOS TRABALHADORES (PT) - NACIONAL",
    )):
        return "Lula"
    if any(term in value for term in (
        "FLAVIO NANTES BOLSONARO", "PARTIDO LIBERAL (PL) - NACIONAL",
    )):
        return "Flávio"
    return None


def iso_date(value: str) -> str:
    if not value:
        return ""
    if re.match(r"\d{4}-\d\d-\d\d", value):
        return value[:10]
    return datetime.strptime(value[:10], "%d/%m/%Y").strftime("%Y-%m-%d")


meta = {cnj: {"processo": None, "assuntos": set(), "decisoes": [], "partes": []} for cnj in IDS}
for row in rows_from_zip("processo_eleitoral_2026", "processos"):
    if row["NR_PROCESSO"] in IDS and row["SG_UF_TRIBUNAL"] == "DF" and row["NR_INSTANCIA"] == "3":
        meta[row["NR_PROCESSO"]]["processo"] = row
for row in rows_from_zip("processos_eleitorais_assuntos_2026", "assuntos"):
    if row["NR_PROCESSO"] in IDS and row["SG_UF_TRIBUNAL"] == "DF" and row["NR_INSTANCIA"] == "3":
        meta[row["NR_PROCESSO"]]["assuntos"].add(row["DS_ASSUNTO"])
for row in rows_from_zip("processos_eleitorais_decisoes_2026", "decisoes"):
    if row["NR_PROCESSO"] in IDS and row["SG_UF_TRIBUNAL"] == "DF" and row["NR_INSTANCIA"] == "3":
        meta[row["NR_PROCESSO"]]["decisoes"].append(row)
for row in rows_from_zip("processos_eleitorais_partes_2026", "partes"):
    if row["NR_PROCESSO"] in IDS and row["SG_UF_TRIBUNAL"] == "DF" and row["NR_INSTANCIA"] == "3":
        if row["TP_PARTE"] != "ADVOGADO" and row["DS_POLO"] in ("Pólo ativo", "Pólo passivo"):
            meta[row["NR_PROCESSO"]]["partes"].append(row)


FIELDS = [
    "cnj", "incluir_comparativo", "motivo_inclusao_exclusao", "categoria_triagem",
    "campanha_autora", "polo_ativo_formal", "polo_passivo_formal", "classe_pje",
    "assunto_principal_pje", "assuntos_pje", "objeto_comunicacao",
    "pedido_principal_codificado", "desfecho_medida", "atendido", "grau_atendimento",
    "status_procedimental", "data_ultima_decisao_pje", "tipo_ultima_decisao_pje",
    "qtd_atos_bulk", "data_ato_referencia", "url_peca_oficial", "tipo_peca_oficial",
    "status_fonte", "url_andamento", "sinopse_curatorial", "geracao_bulk",
    "fonte_classificacao", "grau_certeza_triagem",
]


records = []
for cnj in sorted(IDS):
    item = meta[cnj]
    process = item["processo"]
    assert process is not None, cnj
    active = sorted({row["NM_PARTE"] for row in item["partes"] if row["DS_POLO"] == "Pólo ativo"})
    passive = sorted({row["NM_PARTE"] for row in item["partes"] if row["DS_POLO"] == "Pólo passivo"})
    active_camps = {campaign(name) for name in active} - {None}
    passive_camps = {campaign(name) for name in passive} - {None}
    if "Lula" in active_camps and "Flávio" in passive_camps:
        author = "Lula"
    elif "Flávio" in active_camps and "Lula" in passive_camps:
        author = "Flávio"
    else:
        raise AssertionError(f"polos não opostos: {cnj} {active_camps} {passive_camps}")
    acts = sorted((act for act in item["decisoes"] if iso_date(act["DT_DECISAO"]) <= DATA_FIM),
                  key=lambda row: iso_date(row["DT_DECISAO"]))
    last = acts[-1] if acts else None
    analytical_acts = [
        act for act in acts
        if act["DS_TIPO_DECISAO"] in ("Decisão", "Acórdão")
        and DATA_INICIO <= iso_date(act["DT_DECISAO"]) <= DATA_FIM
    ]
    seed = CURADORIA[cnj]
    assert seed["campanha_autora"] == author
    include = seed["incluir"]
    category = seed["categoria"]
    reason = seed["motivo"]
    object_, request = seed["objeto"], seed["pedido"]
    synopsis = seed["sinopse"]
    granted = seed["atendido"]
    outcome = "atendido" if granted is True else "não atendido" if granted is False else "sem resultado comparável"
    degree = seed["grau"]
    status = seed["status"]
    url, piece_type = seed["url_peca"], seed["tipo_peca"]
    reference_date = iso_date(seed["data_ato_referencia"])
    classification_source = seed["fonte_classificacao"]
    confidence = seed["grau_certeza"]
    source_status = seed["status_fonte"]
    if include:
        assert granted is not None, cnj
    if cnj.startswith("0601811-29"):
        piece_type = "Despacho (rotulado Decisão no bulk)"
        reference_date = "2026-09-03"
    if cnj.startswith("0601817-36"):
        reference_date = "2026-09-28"
    if cnj.startswith("0602099-74"):
        reference_date = "2026-09-23"
    record = {
        "cnj": cnj, "incluir_comparativo": "sim" if include else "não",
        "motivo_inclusao_exclusao": reason, "categoria_triagem": category,
        "campanha_autora": author, "polo_ativo_formal": " | ".join(active),
        "polo_passivo_formal": " | ".join(passive), "classe_pje": process["SG_CLASSE"],
        "assunto_principal_pje": process["DS_ASSUNTO_PRINCIPAL"],
        "assuntos_pje": " | ".join(sorted(item["assuntos"])), "objeto_comunicacao": object_,
        "pedido_principal_codificado": request, "desfecho_medida": outcome,
        "atendido": "sim" if granted is True else "não" if granted is False else "",
        "grau_atendimento": degree, "status_procedimental": status,
        "data_ultima_decisao_pje": iso_date(last["DT_DECISAO"]) if last else "",
        "tipo_ultima_decisao_pje": last["DS_TIPO_DECISAO"] if last else "",
        "qtd_atos_bulk": len(analytical_acts), "data_ato_referencia": reference_date,
        "url_peca_oficial": url, "tipo_peca_oficial": piece_type,
        "status_fonte": source_status, "url_andamento": process["DS_URL_PROCESSO"],
        "sinopse_curatorial": synopsis, "geracao_bulk": GERACAO_BULK,
        "fonte_classificacao": classification_source, "grau_certeza_triagem": confidence,
    }
    records.append(record)

assert len(records) == len(IDS)
selected = [row for row in records if row["incluir_comparativo"] == "sim"]
assert len(selected) == 107
counts = Counter((row["campanha_autora"], row["atendido"]) for row in selected)
assert sum(counts.values()) == len(selected)
assert all(row["data_ultima_decisao_pje"] <= DATA_FIM for row in records if row["data_ultima_decisao_pje"])

# O denominador de atos é o mesmo filtro aplicado em atos.csv.  O campo
# data_ultima_decisao_pje, por sua vez, conserva a última ocorrência do bulk.
with (ROOT / "atos.csv").open(encoding="utf-8-sig", newline="") as handle:
    counts_acts = Counter(
        row["NR_PROCESSO"] for row in csv.DictReader(handle, delimiter=";")
        if row["NR_PROCESSO"] in IDS
    )
assert all(int(row["qtd_atos_bulk"]) == counts_acts[row["cnj"]] for row in records)

with (ROOT / "confrontos.csv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)

with (ROOT / "processos.csv").open(encoding="utf-8-sig", newline="") as handle:
    recorte_oficial = {
        row["NR_PROCESSO"] for row in csv.DictReader(handle, delimiter=";")
        if row["FL_RECORTE_COMUNICACAO"] == "1"
    }
topical = lambda row: row["cnj"] in recorte_oficial
summary = {
    "fonte_oficial": "https://dadosabertos.tse.jus.br/id/dataset/processual-2026",
    "geracao_bulk_decisoes": GERACAO_BULK,
    "data_fim_decisao": DATA_FIM,
    "sha256_zip": {key: source["sha256"] for key, source in SOURCES.items() if "sha256" in source},
    "inventario_cnjs": len(records), "comparaveis": len(selected),
    "pendentes_30set": sorted(row["cnj"] for row in records
                               if row["grau_certeza_triagem"] == "provisório"
                               and row["data_ato_referencia"] == "2026-09-30"),
    "campanhas": {
        "Lula": {"pedidos": counts[("Lula", "sim")] + counts[("Lula", "não")],
                 "atendidos": counts[("Lula", "sim")], "nao_atendidos": counts[("Lula", "não")]},
        "Flávio": {"pedidos": counts[("Flávio", "sim")] + counts[("Flávio", "não")],
                   "atendidos": counts[("Flávio", "sim")], "nao_atendidos": counts[("Flávio", "não")]},
    },
    "cobertura_pje": {
        "processos_inventario": len(records), "com_ato_bulk": sum(bool(counts_acts[cnj]) for cnj in IDS),
        "comparaveis_com_ato_bulk": sum(bool(counts_acts[row["cnj"]]) for row in selected),
        "comparaveis_sem_ato_bulk": [row["cnj"] for row in selected if not counts_acts[row["cnj"]]],
        "comparaveis_assunto_propaganda_ou_resposta": sum(topical(row) for row in selected),
        "comparaveis_no_recorte_oficial": sum(topical(row) for row in selected),
        "comparaveis_fora_assuntos_topicos": [row["cnj"] for row in selected if not topical(row)],
    },
    "comparaveis_cnjs": [row["cnj"] for row in selected],
    "excluidos_cnjs": [{"cnj": row["cnj"], "motivo": row["motivo_inclusao_exclusao"]} for row in records if row["incluir_comparativo"] == "não"],
    "triagem_provisoria_sem_inteiro_teor": [
        row["cnj"] for row in records if row["grau_certeza_triagem"] == "provisório"
    ],
    "resultados_provisorios_por_acordao_posterior": [],
    "ressalvas": [
        "O bulk PJe não contém texto nem resultado: os desfechos são classificação editorial documentada, com fonte oficial indicada por processo.",
        "0601315-97 tem certidão oficial, mas nenhum ato no ZIP de decisões; exceção explícita.",
        "0601181-70 tem vídeo determinado de Itajaí cuja remoção foi negada e pedido futuro genérico também negado; mérito final aberto.",
        "0601817-36 concede resposta a uma de três publicações; texto e veiculação aguardam decisão integrativa.",
        f"{len(selected)} é a amostra de resultados comparáveis identificados até {DATA_FIM}, não o total de litígios bilaterais ajuizados ou pendentes.",
        "0600947-88 e 0600958-20 foram excluídos provisoriamente por assunto/classe; o inteiro teor não foi obtido devido ao bloqueio temporário da Consulta PJe.",
    ],
}
(ROOT / "campanha_resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"confrontos={len(records)}, comparáveis={len(selected)}; "
      f"Lula {counts[('Lula', 'sim')]}/{summary['campanhas']['Lula']['pedidos']}, "
      f"Flávio {counts[('Flávio', 'sim')]}/{summary['campanhas']['Flávio']['pedidos']}")
