#!/usr/bin/env python3
"""Organiza os relatos documentais sem inferir o mérito dos metadados."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def gerar():
    curadoria = json.loads((ROOT / "curadoria_confrontos.json").read_text(encoding="utf-8"))
    incluidos = {cnj for cnj, caso in curadoria.items() if caso["incluir"]}
    relatos = {cnj: caso["relato"] for cnj, caso in curadoria.items() if "relato" in caso}
    assert set(relatos) == incluidos
    assert sorted(item["numero"] for item in relatos.values()) == list(range(1, len(relatos) + 1))
    linhas = [
        {"numero": item["numero"], "cnj": cnj, "titulo": item["titulo"], "texto": item["texto"]}
        for cnj, item in sorted(relatos.items(), key=lambda par: par[1]["numero"])
    ]
    with (ROOT / "relatos.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["numero", "cnj", "titulo", "texto"], delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(linhas)
    print(f"{len(linhas)} relatos organizados a partir da curadoria.")


if __name__ == "__main__":
    gerar()
