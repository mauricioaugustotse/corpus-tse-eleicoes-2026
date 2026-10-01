#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Congela os dados processuais oficiais do TSE e gera o corpus do relatório.

Uso:
    python tse_corpus_eleicoes_2026.py --saida <pasta-nova> --data-fim 2026-09-30
    python tse_corpus_eleicoes_2026.py --saida <mesmo-diretorio> --offline

O segundo comando recompõe CSVs, resumo e gráficos apenas dos ZIPs congelados.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import tempfile
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

DATASET_URL = "https://dadosabertos.tse.jus.br/id/dataset/processual-2026"
BASE_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele/processual/"
DATA_INICIO = date(2025, 10, 3)
FONTE_ARQUIVOS = {
    "processos": "processo_eleitoral_2026.zip",
    "assuntos": "processos_eleitorais_assuntos_2026.zip",
    "decisoes": "processos_eleitorais_decisoes_2026.zip",
    "partes": "processos_eleitorais_partes_2026.zip",
    "recursos": "recursos_eleitorais_2026.zip",
}
SCHEMAS = {
    "processos": (
        "DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "NR_PROCESSO", "DT_AUTUACAO",
        "DT_BAIXA", "SG_UF_TRIBUNAL_ORIGEM", "NR_INSTANCIA_ORIGEM",
        "SG_UF_TRIBUNAL", "NR_INSTANCIA", "DT_DISTRIBUICAO",
        "CD_TIPO_DISTRIBUICAO", "DS_TIPO_DISTRIBUICAO", "CD_RELATOR",
        "NM_RELATOR", "CD_TIPO_CARGO_RELATOR", "DS_TIPO_CARGO_RELATOR",
        "CD_CLASSE", "SG_CLASSE", "DS_CLASSE", "CD_ASSUNTO_PRINCIPAL",
        "DS_ASSUNTO_PRINCIPAL", "ST_RECURSAL", "QT_DECISOES",
        "DT_ULTIMA_DECISAO", "TP_ULTIMA_DECISAO", "DS_URL_PROCESSO",
    ),
    "assuntos": (
        "DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "NR_PROCESSO",
        "SG_UF_TRIBUNAL", "NR_INSTANCIA", "SG_TRIBUNAL_ORIGEM",
        "SG_UF_TRIBUNAL_ORIGEM", "CD_ASSUNTO", "DS_ASSUNTO",
    ),
    "decisoes": (
        "DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "NR_PROCESSO",
        "SG_UF_TRIBUNAL", "SG_UF_TRIBUNAL_ORIGEM", "NR_INSTANCIA_ORIGEM",
        "NR_INSTANCIA", "SQ_DECISAO", "DT_DECISAO", "NM_AUTOR_DECISAO",
        "DS_TIPO_DECISAO",
    ),
    "partes": (
        "DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "SG_UF_TRIBUNAL",
        "SG_TRIBUNAL_ORIGEM", "NR_INSTANCIA", "NR_PROCESSO", "DS_POLO",
        "TP_PARTE", "ST_PARTE_PRINCIPAL", "NM_PARTE", "NM_SOCIAL_PARTE",
        "ST_CANDIDATO", "SQ_CANDIDATO",
    ),
    "recursos": (
        "DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "SQ_RECURSO",
        "DT_AUTUACAO", "DT_BAIXA", "NR_PROCESSO_ORIGEM",
        "SG_UF_TRIBUNAL_ORIGEM", "NR_INSTANCIA_ORIGEM",
        "SG_UF_TRIBUNAL", "NR_INSTANCIA", "DT_DISTRIBUICAO",
        "CD_TIPO_DISTRIBUICAO", "DS_TIPO_DISTRIBUICAO", "CD_RELATOR",
        "NM_RELATOR", "CD_TIPO_CARGO_RELATOR", "DS_TIPO_CARGO_RELATOR",
        "CD_CLASSE", "SG_CLASSE", "DS_CLASSE", "CD_ASSUNTO_PRINCIPAL",
        "DS_ASSUNTO_PRINCIPAL", "DS_TIPO_RECURSO", "DS_NATUREZA_RECURSO",
        "DT_ULTIMA_DECISAO", "DS_ULTIMA_DECISAO",
    ),
}


def _data_br(valor: str) -> date:
    return datetime.strptime(valor, "%d/%m/%Y").date()


def _json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _zip_congelado(nome: str, destino: Path, offline: bool) -> dict:
    """Baixa uma vez e nunca troca silenciosamente o original já congelado."""
    url = BASE_URL + nome
    headers: dict[str, str] = {}
    if not destino.exists():
        if offline:
            raise FileNotFoundError(f"--offline: falta {destino}")
        pedido = urllib.request.Request(url, headers={"User-Agent": "CorpusTSEEleicoes2026/1.0"})
        with urllib.request.urlopen(pedido, timeout=120) as resposta:
            bruto = resposta.read()
            headers = {k: resposta.headers[k] for k in ("ETag", "Last-Modified", "Content-Length", "Date")
                       if k in resposta.headers}
        if headers.get("Content-Length") and len(bruto) != int(headers["Content-Length"]):
            raise ValueError(f"download incompleto: {url}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destino.parent, suffix=".part", delete=False) as fh:
            temporario = Path(fh.name)
            fh.write(bruto)
        try:
            _testar_zip(temporario)
            temporario.replace(destino)
        finally:
            temporario.unlink(missing_ok=True)
    _testar_zip(destino)
    return {"arquivo": str(destino.relative_to(destino.parent.parent)), "url": url,
            "sha256": hashlib.sha256(destino.read_bytes()).hexdigest(),
            "bytes": destino.stat().st_size, "cabecalhos_http": headers}


def _testar_zip(path: Path) -> None:
    with zipfile.ZipFile(path) as z:
        ruim = z.testzip()
        if ruim:
            raise ValueError(f"CRC inválido em {path.name}: {ruim}")
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(csvs) != 1:
            raise ValueError(f"esperado um CSV em {path.name}: {csvs}")


def _ler_fonte(path: Path, chave: str) -> tuple[list[dict], dict]:
    """Valida todas as linhas e retém apenas os registros da instância TSE."""
    with zipfile.ZipFile(path) as z:
        membro = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        with io.TextIOWrapper(z.open(membro), encoding="latin-1", newline="") as fh:
            leitor = csv.DictReader(fh, delimiter=";")
            if tuple(leitor.fieldnames or ()) != SCHEMAS[chave]:
                raise ValueError(f"schema inesperado em {path.name}: {leitor.fieldnames}")
            geracoes: set[tuple[str, str]] = set()
            filtradas: list[dict] = []
            total = 0
            for linha in leitor:
                total += 1
                if None in linha or any(v is None for v in linha.values()):
                    raise ValueError(f"linha CSV malformada em {path.name}: {total}")
                geracoes.add((linha["DT_GERACAO"], linha["HH_GERACAO"]))
                if linha["ANO_ELEICAO"] != "2026":
                    raise ValueError(f"ano eleitoral inesperado em {path.name}: {total}")
                if linha["NR_INSTANCIA"] == "3" and linha["SG_UF_TRIBUNAL"] == "DF":
                    filtradas.append(linha)
    if len(geracoes) != 1:
        raise ValueError(f"mais de uma geração no mesmo arquivo {path.name}: {geracoes}")
    dia, hora = next(iter(geracoes))
    return filtradas, {"arquivo_csv": membro, "linhas_nacionais": total,
                       "linhas_tse": len(filtradas), "DT_GERACAO": dia,
                       "HH_GERACAO": hora, "campos": list(SCHEMAS[chave])}


def _validar_geracoes(metadados: dict[str, dict]) -> None:
    instantes = [datetime.strptime(v["DT_GERACAO"] + " " + v["HH_GERACAO"],
                                  "%d/%m/%Y %H:%M:%S") for v in metadados.values()]
    if len({d.date() for d in instantes}) != 1 or max(instantes) - min(instantes) > timedelta(minutes=20):
        raise ValueError("os cinco ZIPs não pertencem à mesma rodada de geração")


def _e_tse(linha: dict) -> bool:
    return linha["NR_INSTANCIA"] == "3" and linha["SG_UF_TRIBUNAL"] == "DF"


def construir_corpus(
    fontes: dict[str, list[dict]],
    inicio: date = DATA_INICIO,
    data_fim: date | None = None,
) -> tuple[list[dict], list[dict], dict]:
    """Aplica o recorte, mantendo uma linha por ato e uma por CNJ."""
    processos: dict[str, dict] = {}
    for linha in fontes["processos"]:
        if not _e_tse(linha):
            continue
        cnj = linha["NR_PROCESSO"]
        if cnj in processos and processos[cnj] != linha:
            raise ValueError(f"processo TSE duplicado com dados diferentes: {cnj}")
        processos[cnj] = linha

    assuntos: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for linha in fontes["assuntos"]:
        if _e_tse(linha):
            assuntos[linha["NR_PROCESSO"]].add((linha["CD_ASSUNTO"], linha["DS_ASSUNTO"]))

    partes: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for linha in fontes["partes"]:
        if _e_tse(linha) and linha["TP_PARTE"] not in {"ADVOGADO", "FISCAL DA LEI"}:
            partes[linha["NR_PROCESSO"]][linha["DS_POLO"]].add(
                f"{linha['TP_PARTE']}: {linha['NM_PARTE']}")

    candidatos: list[tuple[dict, date]] = []
    for linha in fontes["decisoes"]:
        if _e_tse(linha) and linha["DS_TIPO_DECISAO"] in {"Decisão", "Acórdão"}:
            candidatos.append((linha, _data_br(linha["DT_DECISAO"])))
    if not candidatos:
        raise ValueError("não há Decisão/Acórdão do TSE no arquivo")
    ultima_data_disponivel = max(dia for _, dia in candidatos)
    if data_fim is not None and data_fim > ultima_data_disponivel:
        raise ValueError(
            f"corte {data_fim} posterior à última data disponível "
            f"({ultima_data_disponivel}); não é possível declarar o período fechado"
        )
    fim = data_fim or ultima_data_disponivel
    selecionados = [(linha, dia) for linha, dia in candidatos if inicio <= dia <= fim]

    atos: list[dict] = []
    por_cnj: dict[str, list[date]] = defaultdict(list)
    chaves: set[tuple[str, str]] = set()
    for linha, dia in sorted(selecionados, key=lambda item: (item[1], item[0]["NR_PROCESSO"], item[0]["SQ_DECISAO"])):
        cnj = linha["NR_PROCESSO"]
        if cnj not in processos:
            raise ValueError(f"ato TSE sem linha correspondente no arquivo de processos: {cnj}")
        chave = (cnj, linha["SQ_DECISAO"])
        if chave in chaves:
            raise ValueError(f"chave de ato repetida: {chave}")
        chaves.add(chave)
        proc = processos[cnj]
        topicos = {descricao for _, descricao in assuntos[cnj]}
        topicos.add(proc["DS_ASSUNTO_PRINCIPAL"])
        propaganda = any("propaganda eleitoral" in t.casefold() for t in topicos)
        dr = proc["SG_CLASSE"] == "DR"
        atos.append({"CHAVE_ATO": f"{cnj}|{linha['SQ_DECISAO']}", **linha,
                     **{f"PROCESSO_{k}": v for k, v in proc.items()},
                     "DT_DECISAO_ISO": dia.isoformat(),
                     "FL_PROPAGANDA_OFICIAL": int(propaganda),
                     "FL_DIREITO_RESPOSTA": int(dr),
                     "FL_RECORTE_COMUNICACAO": int(propaganda or dr)})
        por_cnj[cnj].append(dia)

    casos: list[dict] = []
    for cnj in sorted(por_cnj):
        proc = processos[cnj]
        topicos = assuntos[cnj]
        descricoes = {descricao for _, descricao in topicos}
        descricoes.add(proc["DS_ASSUNTO_PRINCIPAL"])
        propaganda = any("propaganda eleitoral" in t.casefold() for t in descricoes)
        dr = proc["SG_CLASSE"] == "DR"
        polos = partes[cnj]
        casos.append({**proc,
                      "CD_ASSUNTOS_OFICIAIS": " | ".join(sorted({cd for cd, _ in topicos})),
                      "DS_ASSUNTOS_OFICIAIS": " | ".join(sorted(descricoes)),
                      "PARTES_POLO_ATIVO": " | ".join(sorted(polos.get("Pólo ativo", ()))),
                      "PARTES_POLO_PASSIVO": " | ".join(sorted(polos.get("Pólo passivo", ()))),
                      "PARTES_INTERESSADAS": " | ".join(sorted(polos.get("Pólo parte interessada", ()))),
                      "QT_ATOS_RECORTE": len(por_cnj[cnj]),
                      "DT_PRIMEIRO_ATO_ISO": min(por_cnj[cnj]).isoformat(),
                      "DT_ULTIMO_ATO_ISO": max(por_cnj[cnj]).isoformat(),
                      "FL_PROPAGANDA_OFICIAL": int(propaganda),
                      "FL_DIREITO_RESPOSTA": int(dr),
                      "FL_RECORTE_COMUNICACAO": int(propaganda or dr)})

    controle = {"inicio": inicio.isoformat(), "fim": fim.isoformat(),
                "data_fim_parametrizada": data_fim.isoformat() if data_fim else None,
                "ultima_data_disponivel": ultima_data_disponivel.isoformat(),
                "atos_tse_decisao_ou_acordao_sem_corte_inicial": len(candidatos),
                "atos_anteriores_ao_inicio": sum(dia < inicio for _, dia in candidatos),
                "atos_posteriores_ao_fim": sum(dia > fim for _, dia in candidatos),
                "processos_tse_no_arquivo": len(processos)}
    return atos, casos, controle


def _escrever_csv(path: Path, linhas: list[dict]) -> None:
    if not linhas:
        raise ValueError(f"sem dados para {path}")
    campos = list(linhas[0])
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(linhas)


def _meses(inicio: date, fim: date) -> list[str]:
    atual = date(inicio.year, inicio.month, 1)
    meses = []
    while atual <= fim:
        meses.append(atual.strftime("%Y-%m"))
        atual = date(atual.year + (atual.month == 12), (atual.month % 12) + 1, 1)
    return meses


def resumir(atos: list[dict], casos: list[dict], controle: dict) -> dict:
    tipos = Counter(a["DS_TIPO_DECISAO"] for a in atos)
    mensais = Counter(a["DT_DECISAO_ISO"][:7] for a in atos)
    mes_tipo = Counter((a["DT_DECISAO_ISO"][:7], a["DS_TIPO_DECISAO"]) for a in atos)
    classes = Counter(a["PROCESSO_SG_CLASSE"] for a in atos)
    autores = Counter(a["NM_AUTOR_DECISAO"] or "Autor não informado" for a in atos)
    composicao = Counter()
    for c in casos:
        propaganda, dr = c["FL_PROPAGANDA_OFICIAL"], c["FL_DIREITO_RESPOSTA"]
        grupo = "Propaganda e DR" if propaganda and dr else (
            "Propaganda, sem DR" if propaganda else "DR, sem propaganda" if dr else "Demais assuntos")
        composicao[grupo] += 1
    serie = {m: mensais[m] for m in _meses(date.fromisoformat(controle["inicio"]),
                                              date.fromisoformat(controle["fim"]))}
    serie_tipo = {m: {tipo: mes_tipo[(m, tipo)] for tipo in ("Decisão", "Acórdão")}
                  for m in serie}
    acumulado = {}
    soma = 0
    for mes, quantidade in serie.items():
        soma += quantidade
        acumulado[mes] = soma
    return {"fonte": DATASET_URL, "unidade_ato": "NR_PROCESSO + SQ_DECISAO",
            "unidade_processo": "NR_PROCESSO", "inicio_decisao": controle["inicio"],
            "fim_decisao": controle["fim"], "filtro_tribunal": "NR_INSTANCIA=3; SG_UF_TRIBUNAL=DF",
            "tipos_incluidos": ["Decisão", "Acórdão"], "total_atos": len(atos),
            "total_processos": len(casos), "total_processos_comunicacao": sum(c["FL_RECORTE_COMUNICACAO"] for c in casos),
            "atos_por_tipo": dict(sorted(tipos.items())), "atos_por_mes": serie,
            "atos_por_mes_tipo": serie_tipo,
            "atos_acumulados_por_mes": acumulado,
            "atos_por_classe": dict(sorted(classes.items())),
            "atos_por_autor": dict(sorted(autores.items())),
            "processos_por_grupo_comunicacao": dict(sorted(composicao.items())),
            "controle": controle}


def _svg_barras(titulo: str, legenda: str, dados: list[tuple[str, int]],
                cor: str = "#155e75", denominador: int | None = None) -> str:
    largura, esquerda, direita = 900, 300, 160
    altura = max(220, 110 + len(dados) * 47)
    maximo = max((n for _, n in dados), default=1) or 1
    largura_barras = largura - esquerda - direita
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" role="img" aria-label="{html.escape(titulo)}" font-family="Arial, Helvetica, sans-serif">',
              '<rect width="100%" height="100%" fill="#fff"/>',
              f'<text x="32" y="38" font-size="24" font-weight="700" fill="#123">{html.escape(titulo)}</text>',
              f'<text x="32" y="64" font-size="14" fill="#475569">{html.escape(legenda)}</text>']
    for i, (rotulo, valor) in enumerate(dados):
        y = 88 + i * 47
        tam = round(largura_barras * valor / maximo)
        valor_texto = f"{valor} ({valor / denominador:.1%})" if denominador else str(valor)
        partes.extend([f'<text x="{esquerda - 14}" y="{y + 23}" font-size="15" text-anchor="end" fill="#123">{html.escape(rotulo)}</text>',
                       f'<rect x="{esquerda}" y="{y + 4}" width="{tam}" height="28" rx="3" fill="{cor}"/>',
                       f'<text x="{esquerda + tam + 8}" y="{y + 24}" font-size="15" fill="#123">{valor_texto}</text>'])
    partes.append('</svg>')
    return "\n".join(partes)


def _svg_linha(titulo: str, legenda: str, dados: list[tuple[str, int]]) -> str:
    largura, altura = 900, 440
    esq, topo, dir_, baixo = 80, 105, 40, 72
    maximo = max((n for _, n in dados), default=1) or 1
    n = len(dados)
    coords = [(esq + (largura - esq - dir_) * i / max(n - 1, 1),
               topo + (altura - topo - baixo) * (1 - valor / maximo)) for i, (_, valor) in enumerate(dados)]
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" role="img" aria-label="{html.escape(titulo)}" font-family="Arial, Helvetica, sans-serif">',
              '<rect width="100%" height="100%" fill="#fff"/>',
              f'<text x="32" y="38" font-size="24" font-weight="700" fill="#123">{html.escape(titulo)}</text>',
              f'<text x="32" y="64" font-size="14" fill="#475569">{html.escape(legenda)}</text>',
              f'<line x1="{esq}" y1="{altura - baixo}" x2="{largura - dir_}" y2="{altura - baixo}" stroke="#94a3b8"/>',
              f'<line x1="{esq}" y1="{topo}" x2="{esq}" y2="{altura - baixo}" stroke="#94a3b8"/>']
    for j in range(5):
        y = topo + (altura - topo - baixo) * j / 4
        val = round(maximo * (1 - j / 4))
        partes.extend([f'<line x1="{esq}" y1="{y:.1f}" x2="{largura-dir_}" y2="{y:.1f}" stroke="#e2e8f0"/>',
                       f'<text x="{esq-10}" y="{y+5:.1f}" text-anchor="end" font-size="14" fill="#475569">{val}</text>'])
    pontos = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    partes.append(f'<polyline fill="none" stroke="#0f766e" stroke-width="3" points="{pontos}"/>')
    for (mes, valor), (x, y) in zip(dados, coords):
        partes.extend([f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#0f766e"/>',
                       f'<text x="{x:.1f}" y="{altura-baixo+25}" font-size="13" text-anchor="middle" fill="#475569">{html.escape(_mes_pt(mes))}</text>',
                       f'<text x="{x:.1f}" y="{y-9:.1f}" font-size="13" text-anchor="middle" fill="#123">{valor}</text>'])
    partes.append('</svg>')
    return "\n".join(partes)


def _top(dados: dict[str, int], limite: int = 8) -> list[tuple[str, int]]:
    pares = sorted(dados.items(), key=lambda item: (-item[1], item[0]))
    if len(pares) > limite:
        return pares[:limite] + [("Demais", sum(n for _, n in pares[limite:]))]
    return pares


def _mes_pt(mes: str) -> str:
    nomes = ("jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez")
    ano, numero = mes.split("-")
    return f"{nomes[int(numero) - 1]}/{ano[2:]}"


def _svg_meses_empilhados(titulo: str, legenda: str, dados: dict[str, dict[str, int]]) -> str:
    largura, esquerda, direita = 900, 125, 100
    altura = max(660, 145 + len(dados) * 43)
    maior = max((sum(tipos.values()) for tipos in dados.values()), default=1) or 1
    util = largura - esquerda - direita
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" role="img" aria-label="{html.escape(titulo)}" font-family="Arial, Helvetica, sans-serif">',
              '<rect width="100%" height="100%" fill="#fff"/>',
              f'<text x="32" y="38" font-size="24" font-weight="700" fill="#123">{html.escape(titulo)}</text>',
              f'<text x="32" y="64" font-size="14" fill="#475569">{html.escape(legenda)}</text>',
              '<rect x="145" y="81" width="16" height="16" fill="#155e75"/>',
              '<text x="168" y="94" font-size="15" fill="#123">Decisão</text>',
              '<rect x="259" y="81" width="16" height="16" fill="#0f766e"/>',
              '<text x="282" y="94" font-size="15" fill="#123">Acórdão</text>']
    for i, (mes, tipos) in enumerate(dados.items()):
        y = 112 + i * 43
        decisoes, acordaos = tipos["Decisão"], tipos["Acórdão"]
        larg_dec = round(util * decisoes / maior)
        larg_aco = round(util * acordaos / maior)
        partes.extend([f'<text x="{esquerda-13}" y="{y+22}" text-anchor="end" font-size="15" fill="#123">{_mes_pt(mes)}</text>',
                       f'<rect x="{esquerda}" y="{y+3}" width="{larg_dec}" height="27" fill="#155e75"/>',
                       f'<rect x="{esquerda+larg_dec}" y="{y+3}" width="{larg_aco}" height="27" fill="#0f766e"/>',
                       f'<text x="{esquerda+larg_dec+larg_aco+8}" y="{y+23}" font-size="15" fill="#123">{decisoes+acordaos}</text>'])
    partes.append('</svg>')
    return "\n".join(partes)


def gerar_graficos(destino: Path, resumo: dict) -> list[str]:
    destino.mkdir(parents=True, exist_ok=True)
    inicio = date.fromisoformat(resumo["inicio_decisao"]).strftime("%d/%m/%Y")
    fim = date.fromisoformat(resumo["fim_decisao"]).strftime("%d/%m/%Y")
    intervalo = f"{inicio} a {fim}; n={resumo['total_atos']} atos; fonte: PJe/TSE"
    graficos = {
        "01_tipos_ato": _svg_barras("Tipos de ato", intervalo, _top(resumo["atos_por_tipo"]),
                                     denominador=resumo["total_atos"]),
        "02_atos_por_mes": _svg_meses_empilhados("Atos por mês e tipo", intervalo,
                                                  resumo["atos_por_mes_tipo"]),
        "03_ritmo_acumulado": _svg_linha("Atos acumulados", intervalo, list(resumo["atos_acumulados_por_mes"].items())),
        "04_classes_por_ato": _svg_barras("Classes dos atos", intervalo, _top(resumo["atos_por_classe"])),
        "05_autores_dos_atos": _svg_barras("Autores dos atos", intervalo + "; NM_AUTOR_DECISAO não é relatoria", _top(resumo["atos_por_autor"], limite=10)),
        "06_composicao_comunicacao": _svg_barras("Composição dos processos", f"Até {fim}; n={resumo['total_processos']} CNJs; fonte: PJe/TSE. Propaganda: assunto; DR: classe", _top(resumo["processos_por_grupo_comunicacao"]), "#0f766e"),
    }
    for nome, svg in graficos.items():
        (destino / f"{nome}.svg").write_text(svg + "\n", encoding="utf-8")
        html_doc = ("<!doctype html><html lang=\"pt-BR\"><meta charset=\"utf-8\">"
                    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
                    f"<title>{html.escape(nome)}</title><style>body{{margin:0;padding:1rem;background:#f8fafc;"
                    "font-family:Arial,sans-serif}svg{max-width:100%;height:auto;display:block;margin:auto}</style>"
                    f"<body>{svg}</body></html>\n")
        (destino / f"{nome}.html").write_text(html_doc, encoding="utf-8")
    return sorted(graficos)


def _documentacao(destino: Path, resumo: dict) -> None:
    readme = f"""# Corpus oficial — atos do TSE no ciclo das Eleições 2026

Fonte primária: {DATASET_URL} (Secretaria Judiciária do TSE, sistema PJe).

Recorte de `DT_DECISAO`: **{resumo['inicio_decisao']} a {resumo['fim_decisao']}**, inclusive. A data final foi informada em `--data-fim`; a última data disponível nos ZIPs é **{resumo['controle']['ultima_data_disponivel']}**. Geração dos arquivos e SHA-256: `fontes.json`.

`atos.csv` tem uma linha por `NR_PROCESSO + SQ_DECISAO` da instância 3, `SG_UF_TRIBUNAL=DF`, e inclui apenas `DS_TIPO_DECISAO` igual a `Decisão` ou `Acórdão`. `processos.csv` tem uma linha por CNJ com ao menos um ato selecionado. Os dois CSVs usam UTF-8 com BOM e ponto e vírgula. As colunas originais do arquivo de decisões ficam sem prefixo em `atos.csv`; as de processo recebem `PROCESSO_`. Em `processos.csv`, os campos originais de processo ficam sem prefixo. Os arquivos oficiais completos, inclusive LEIAME em PDF, estão em `originais/`.

Os gráficos em `graficos/` usam somente estas duas tabelas. Cada HTML contém seu SVG e abre sem internet; o SVG também é fornecido separadamente. `resumo.json` contém os valores usados nos gráficos. A classe DR e os assuntos oficiais que contêm `Propaganda Eleitoral` formam um recorte objetivo de comunicação; o grupo não mede procedência, remoção, favorecimento ou resultado de mérito.

**Limites:** `DT_DECISAO` é a data do ato no arquivo PJe; data de sessão e data de publicação são fatos diferentes. `NM_AUTOR_DECISAO` é o autor do ato, não necessariamente o relator do processo. O rótulo oficial `DS_TIPO_DECISAO=Decisão` pode incluir peça materialmente intitulada despacho; a qualificação do teor exige conferência individual. O catálogo processual não fornece dispositivo ou URL direta de cada peça. A seleção por processo não substitui exame jurídico individual.

Reprodução offline: `python tse_corpus_eleicoes_2026.py --saida <esta-pasta> --offline`. Os ZIPs congelados nunca são sobrescritos automaticamente.
"""
    (destino / "README.md").write_text(readme, encoding="utf-8")
    dicionario = """# Dicionário do corpus

O significado integral das colunas originais consta nos PDFs LEIAME de cada ZIP em `originais/`. A grafia dos campos oficiais foi conservada.

| Coluna | Arquivo | Definição |
|---|---|---|
| `NR_PROCESSO` | ambos | Número CNJ; chave do processo. |
| `SQ_DECISAO` | atos | Sequencial oficial do ato no arquivo de decisões. Pode mudar em outra extração. |
| `CHAVE_ATO` | atos | `NR_PROCESSO|SQ_DECISAO`; chave única nesta extração. |
| `DT_DECISAO` | atos | Data do ato no PJe, formato original `dd/mm/aaaa`. |
| `DT_DECISAO_ISO` | atos | Mesma data, em `aaaa-mm-dd`. |
| `DS_TIPO_DECISAO` | atos | Categoria fornecida pelo TSE: Decisão ou Acórdão. |
| `NM_AUTOR_DECISAO` | atos | Autor do ato segundo o TSE; não é a relatoria. |
| `PROCESSO_*` | atos | Cópia literal do campo `*` do arquivo oficial Processo Eleitoral. |
| `CD_ASSUNTOS_OFICIAIS`, `DS_ASSUNTOS_OFICIAIS` | processos | União ordenada dos assuntos da tabela oficial Assuntos e do assunto principal do processo; separador ` | `. |
| `PARTES_POLO_ATIVO`, `PARTES_POLO_PASSIVO`, `PARTES_INTERESSADAS` | processos | `TP_PARTE: NM_PARTE`, provenientes do arquivo oficial Partes; advogados e fiscais da lei omitidos. |
| `QT_ATOS_RECORTE` | processos | Quantidade de atos presentes em `atos.csv` para o CNJ. |
| `DT_PRIMEIRO_ATO_ISO`, `DT_ULTIMO_ATO_ISO` | processos | Primeira e última `DT_DECISAO` selecionadas. |
| `FL_PROPAGANDA_OFICIAL` | ambos | 1 se qualquer assunto oficial, inclusive principal, contém `Propaganda Eleitoral`; senão 0. |
| `FL_DIREITO_RESPOSTA` | ambos | 1 se `SG_CLASSE=DR`; senão 0. |
| `FL_RECORTE_COMUNICACAO` | ambos | União lógica das duas bandeiras anteriores. |

`#NULO#` e outros vazios dos arquivos oficiais não são inferidos nem preenchidos nos campos originais. `fontes.json` registra URL, hash, esquema, geração e totais de cada um dos cinco ZIPs. A chave identifica registros dentro deste pacote, mas não substitui a leitura das peças ao analisar o resultado de um processo.
"""
    (destino / "dicionario.md").write_text(dicionario, encoding="utf-8")


def executar(destino: Path, offline: bool = False, data_fim: date | None = None) -> dict:
    destino.mkdir(parents=True, exist_ok=True)
    originais = destino / "originais"
    anterior_path = destino / "fontes.json"
    anterior = json.loads(anterior_path.read_text(encoding="utf-8")) if anterior_path.exists() else {}
    metadados: dict[str, dict] = {}
    fontes: dict[str, list[dict]] = {}
    for chave, nome in FONTE_ARQUIVOS.items():
        path = originais / nome
        meta = _zip_congelado(nome, path, offline)
        if chave in anterior:
            if anterior[chave]["sha256"] != meta["sha256"]:
                raise ValueError(f"ZIP congelado mudou desde fontes.json: {nome}")
            meta["cabecalhos_http"] = anterior[chave].get("cabecalhos_http", {})
        fontes[chave], valida = _ler_fonte(path, chave)
        metadados[chave] = {**meta, **valida}
    _validar_geracoes(metadados)
    _json(anterior_path, metadados)
    atos, casos, controle = construir_corpus(fontes, data_fim=data_fim)
    _escrever_csv(destino / "atos.csv", atos)
    _escrever_csv(destino / "processos.csv", casos)
    resumo = resumir(atos, casos, controle)
    resumo["geracao_oficial"] = metadados["decisoes"]["DT_GERACAO"]
    resumo["graficos"] = gerar_graficos(destino / "graficos", resumo)
    _json(destino / "resumo.json", resumo)
    _documentacao(destino, resumo)
    return resumo


def main() -> None:
    hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()
    default = Path(__file__).resolve().parent / "Artefatos/reports/corpus_eleicoes_2026" / hoje
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, default=default)
    parser.add_argument("--offline", action="store_true", help="reproduz somente dos ZIPs já congelados")
    parser.add_argument("--data-fim", type=date.fromisoformat, help="corte inclusivo de DT_DECISAO, no formato AAAA-MM-DD")
    args = parser.parse_args()
    resumo = executar(args.saida.resolve(), offline=args.offline, data_fim=args.data_fim)
    print(json.dumps({k: resumo[k] for k in ("inicio_decisao", "fim_decisao", "total_atos",
                                               "total_processos", "total_processos_comunicacao")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
