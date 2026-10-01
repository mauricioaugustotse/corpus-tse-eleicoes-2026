#!/usr/bin/env python3
"""Seleciona acórdãos em exportações CSV oficiais do SJUR, sem atribuir votação."""

import argparse
import csv
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
FIELDS = (
    'siglaTribunalJE', 'origemDecisao', 'numeroProcesso', 'numeroUnico',
    'dataDecisao', 'siglaClasse', 'descricaoTipoDecisao', 'relatores',
    'textoDecisao', 'textoEmenta',
)


def cnj_digits(value):
    return re.sub(r'[^0-9]', '', value)


def row_key(row):
    """Compara os dez campos, conservando espaços e variantes do texto oficial."""
    return tuple(row[field] for field in FIELDS)


def selected_cnjs(all_corpus=False):
    rows = json.loads((ROOT / 'acordaos.json').read_text(encoding='utf-8'))
    return {
        cnj_digits(row['cnj']) for row in rows
        if all_corpus or row['fonte'].startswith('SJUR')
    }


def select_exports(paths, cnjs):
    # Ementas extensas excedem o limite padrão do leitor CSV. O ajuste também
    # funciona em plataformas cujo C long é menor que o inteiro de Python.
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            break
        except OverflowError:
            limit //= 10

    selected = []
    seen = set()
    for path in paths:
        with path.open(encoding='utf-8-sig', newline='') as stream:
            header = stream.readline()
            stream.seek(0)
            dialect = csv.Sniffer().sniff(header, delimiters=',;')
            reader = csv.DictReader(stream, dialect=dialect)
            missing = set(FIELDS) - set(reader.fieldnames or ())
            if missing:
                raise ValueError(f'{path.name}: campos ausentes: {", ".join(sorted(missing))}')
            for row in reader:
                if row['siglaTribunalJE'] != 'TSE' or row['descricaoTipoDecisao'] != 'Acórdão':
                    continue
                if cnj_digits(row['numeroUnico'] or '') not in cnjs:
                    continue
                if any(row[field] is None for field in FIELDS):
                    raise ValueError(f'{path.name}: registro incompleto na linha {reader.line_num}')
                candidate = {field: row[field] for field in FIELDS}
                key = row_key(candidate)
                if key not in seen:
                    seen.add(key)
                    selected.append(candidate)
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csvs', nargs='+', type=Path, help='CSV(s) exportado(s) do SJUR')
    parser.add_argument('--saida', required=True, type=Path, help='JSON de saída, que não pode existir')
    parser.add_argument('--todos-do-corpus', action='store_true',
                        help='seleciona os 198 CNJs com acórdão, inclusive os apurados por PJe ou pendentes')
    parser.add_argument('--verificar', action='store_true',
                        help='confere igualdade de conteúdo com extratos_sjur.json antes de salvar')
    args = parser.parse_args()
    if args.verificar and args.todos_do_corpus:
        parser.error('--verificar compara o espelho dos CNJs com fonte SJUR; não combine com --todos-do-corpus')
    if args.saida.exists():
        parser.error('o arquivo de saída já existe; escolha outro nome')
    try:
        cnjs = selected_cnjs(args.todos_do_corpus)
        rows = select_exports(args.csvs, cnjs)
        if args.verificar:
            reference = json.loads((ROOT / 'extratos_sjur.json').read_text(encoding='utf-8'))
            expected = {row_key(row) for row in reference}
            actual = {row_key(row) for row in rows}
            if actual != expected:
                raise ValueError(
                    f'exportação difere do espelho: {len(expected - actual)} registros ausentes; '
                    f'{len(actual - expected)} registros adicionais ou diferentes. Nenhum arquivo foi salvo.'
                )
        with args.saida.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))
    found_cnjs = {cnj_digits(row['numeroUnico']) for row in rows}
    print(f'{len(rows)} registros; {len(found_cnjs)} de {len(cnjs)} CNJs selecionados; saída: {args.saida}')
    if args.verificar:
        print('Conteúdo igual ao espelho extratos_sjur.json, independentemente da ordem das linhas.')


if __name__ == '__main__':
    main()
