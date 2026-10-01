#!/usr/bin/env python3
"""Verifica SHA-256, unidades e correspondência entre CSVs do pacote congelado."""
from pathlib import Path
import csv
import hashlib
import json
from collections import Counter

ROOT = Path(__file__).resolve().parent


def csv_ler(nome):
    with (ROOT / nome).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def verificar():
    manifesto = json.loads((ROOT / "manifesto.json").read_text(encoding="utf-8"))
    presentes = {
        p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
        if p.is_file() and p.name not in {"manifesto.json", "SHA256SUMS.txt"}
        and p.suffix != ".pyc" and "__pycache__" not in p.parts
    }
    assert presentes == set(manifesto["arquivos"]), "manifesto não cobre exatamente os arquivos distribuídos"
    for nome, esperado in manifesto["arquivos"].items():
        path = ROOT / nome
        assert path.is_file(), f"Arquivo ausente: {nome}"
        obtido = hashlib.sha256(path.read_bytes()).hexdigest()
        assert obtido == esperado["sha256"], f"SHA-256 divergente: {nome}"
        assert path.stat().st_size == esperado["bytes"], f"Tamanho divergente: {nome}"
    atos, processos = csv_ler("atos.csv"), csv_ler("processos.csv")
    confronto, relatos = csv_ler("confrontos.csv"), csv_ler("relatos.csv")
    curadoria = json.loads((ROOT / "curadoria_confrontos.json").read_text(encoding="utf-8"))
    incluidos = [x for x in confronto if x["incluir_comparativo"] == "sim"]
    assert len(atos) == len({x["CHAVE_ATO"] for x in atos})
    assert len(processos) == len({x["NR_PROCESSO"] for x in processos})
    assert {x["NR_PROCESSO"] for x in atos} == {x["NR_PROCESSO"] for x in processos}
    assert len(incluidos) == len({x["cnj"] for x in incluidos})
    assert len(relatos) == len({x["cnj"] for x in relatos})
    assert {x["cnj"] for x in incluidos} == {x["cnj"] for x in relatos}
    assert set(curadoria) == {x["cnj"] for x in confronto}
    assert {cnj for cnj, caso in curadoria.items() if caso["incluir"]} == {x["cnj"] for x in incluidos}
    por_cnj = Counter(x["NR_PROCESSO"] for x in atos)
    assert all(int(x["qtd_atos_bulk"]) == por_cnj[x["cnj"]] for x in confronto)
    campanha = json.loads((ROOT / "campanha_resumo.json").read_text(encoding="utf-8"))
    assert not campanha.get("resultados_provisorios_por_acordao_posterior")
    for lado, valores in campanha["campanhas"].items():
        grupo = [x for x in incluidos if x["campanha_autora"] == lado]
        assert len(grupo) == valores["pedidos"]
        assert sum(x["atendido"] == "sim" for x in grupo) == valores["atendidos"]
        assert sum(x["atendido"] == "não" for x in grupo) == valores["nao_atendidos"]
    resumo = json.loads((ROOT / "resumo.json").read_text(encoding="utf-8"))
    assert resumo["fim_decisao"] == "2026-09-30"
    assert resumo["controle"]["ultima_data_disponivel"] == "2026-09-30"
    assert resumo["controle"]["data_fim_parametrizada"] == "2026-09-30"
    assert (len(atos), len(processos), resumo["total_processos_comunicacao"]) == (933, 751, 286)
    assert len(incluidos) == campanha["comparaveis"] == len(relatos) == 107
    assert len(campanha["pendentes_30set"]) == 7
    assert set(campanha["pendentes_30set"]) <= set(campanha["triagem_provisoria_sem_inteiro_teor"])
    for peca in json.loads((ROOT / "pecas" / "indice_30set.json").read_text(encoding="utf-8")):
        bruto = (ROOT / "pecas" / peca["arquivo"]).read_bytes()
        assert hashlib.sha256(bruto).hexdigest() == peca["sha256"]
        assert peca["cnj"].split(".")[0].encode() in bruto
    assert len(atos) == resumo["total_atos"]
    assert len(processos) == resumo["total_processos"]
    assert sum(resumo["atos_por_tipo"].values()) == len(atos)
    assert sum(resumo["atos_por_mes"].values()) == len(atos)
    assert sum(resumo["atos_por_classe"].values()) == len(atos)
    assert sum(resumo["atos_por_autor"].values()) == len(atos)
    assert sum(resumo["processos_por_grupo_comunicacao"].values()) == len(processos)
    print(f"OK: {len(manifesto['arquivos'])} arquivos; {len(atos)} atos; "
          f"{len(processos)} processos; {len(incluidos)} confrontos e relatos idênticos.")


if __name__ == "__main__":
    verificar()
