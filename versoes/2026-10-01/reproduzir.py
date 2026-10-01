#!/usr/bin/env python3
"""Reproduz o corpus oficial, os confrontos, os gráficos e o relatório técnico."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, check=True)


if __name__ == "__main__":
    run("verificar_pacote.py")
    run("tse_corpus_eleicoes_2026.py", "--saida", ROOT, "--offline",
        "--data-fim", "2026-09-30")
    run("gerar_confrontos.py")
    run("gerar_relatos.py")
    run("tse_relatorio_corpus.py", "--corpus", ROOT, "--secao6", ROOT / "secao6_template.md", "--saida", ROOT / "relatorio.md")
    run("verificar_pacote.py")
