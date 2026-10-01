#!/usr/bin/env python3
"""Atualiza os hashes dos arquivos distribuídos nesta versão pública."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXCLUIR = {"manifesto.json", "SHA256SUMS.txt"}


def arquivos() -> list[Path]:
    return sorted(
        caminho for caminho in ROOT.rglob("*")
        if caminho.is_file()
        and caminho.name not in EXCLUIR
        and caminho.suffix != ".pyc"
        and "__pycache__" not in caminho.parts
    )


def main() -> None:
    entradas = {}
    linhas_sha = []
    for caminho in arquivos():
        nome = caminho.relative_to(ROOT).as_posix()
        sha = hashlib.sha256(caminho.read_bytes()).hexdigest()
        entradas[nome] = {"sha256": sha, "bytes": caminho.stat().st_size}
        linhas_sha.append(f"{sha}  {nome}")
    manifesto = {
        "versao": ROOT.name,
        "fonte": "https://dadosabertos.tse.jus.br/id/dataset/processual-2026",
        "algoritmo": "SHA-256",
        "nota": "O corte dos atos é 30/09/2026. Os arquivos derivados usam os cinco ZIPs oficiais preservados nesta versão.",
        "arquivos": entradas,
    }
    (ROOT / "manifesto.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (ROOT / "SHA256SUMS.txt").write_text(
        "\n".join(linhas_sha) + "\n", encoding="utf-8"
    )
    print(f"Manifesto público atualizado para {len(entradas)} arquivos.")


if __name__ == "__main__":
    main()
