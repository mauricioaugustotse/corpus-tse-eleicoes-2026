#!/usr/bin/env python3
"""Confere a curadoria nominal e reproduz contagens; --graficos usa Matplotlib."""
from pathlib import Path
from collections import Counter
import argparse
import csv
import hashlib
import html
import json

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT.parents[1] / 'versoes' / '2026-10-01'


def ler(nome):
    return json.loads((ROOT / nome).read_text(encoding='utf-8'))


def verificar_e_resumir():
    atos, casos = ler('acordaos.json'), ler('liminares_confrontos.json')
    with (CORPUS / 'atos.csv').open(encoding='utf-8-sig', newline='') as f:
        oficiais = [r for r in csv.DictReader(f, delimiter=';') if r['DS_TIPO_DECISAO'] == 'Acórdão']
    with (CORPUS / 'confrontos.csv').open(encoding='utf-8-sig', newline='') as f:
        confrontos = [r for r in csv.DictReader(f, delimiter=';') if r['incluir_comparativo'] == 'sim']
    assert len(atos) == len({r['chave_ato'] for r in atos}) == 200
    assert {r['chave_ato'] for r in atos} == {r['CHAVE_ATO'] for r in oficiais}
    assert len(casos) == len({r['cnj'] for r in casos}) == 107
    assert {r['cnj'] for r in casos} == {r['cnj'] for r in confrontos}
    for nome, rows in [('acordaos', atos), ('liminares_confrontos', casos)]:
        with (ROOT / (nome + '.csv')).open(encoding='utf-8-sig', newline='') as f:
            csv_rows = list(csv.DictReader(f, delimiter=';'))
        expected = [{k: ' | '.join(v) if isinstance(v, list) else str(v) for k, v in r.items()} for r in rows]
        assert csv_rows == expected, f'CSV e JSON divergem: {nome}'
        for r in rows:
            assert r['votacao'] in {'unânime', 'com divergência', 'não apurada', 'não se aplica'}
            if r['votacao'] == 'com divergência':
                assert 'maioria' in r['extrato'].lower() or 'vencid' in r['extrato'].lower()
                assert r['vencidos'], r['cnj']
            elif r['votacao'] == 'unânime':
                assert 'unanimidade' in r['extrato'].lower()
                assert not r['vencidos']
            if r['arquivo_pje']:
                content = (ROOT / 'fontes_pje' / r['arquivo_pje']).read_bytes()
                assert hashlib.sha256(content).hexdigest() == r['sha256_pje']
                assert r['cnj'].encode() in content, r['cnj']
                assert r['url_peca'].startswith('https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?')
            if r.get('data_ato'):
                assert '2025-10-03' <= r['data_ato'] <= '2026-09-30'
    # Casos que distinguem manutenção, reforma e julgamento direto.
    pc = {r['cnj']: r for r in casos}
    assert pc['0600690-63.2026.6.00.0000']['situacao'] == 'liminar mantida'
    assert pc['0601016-23.2026.6.00.0000']['situacao'] == 'liminar modificada'
    assert pc['0601315-97.2026.6.00.0000']['situacao'] == 'tutela decidida diretamente pelo colegiado'
    assert pc['0600950-43.2026.6.00.0000']['vencidos'] == ['André Mendonça', 'Dias Toffoli']
    assert pc['0601315-97.2026.6.00.0000']['vencidos'] == ['Estela Aranha', 'Floriano de Azevedo Marques', 'Ricardo Villas Bôas Cueva']
    colegiados = [r for r in casos if r['votacao'] in {'unânime', 'com divergência'}]
    status = Counter(r['situacao'] for r in casos)
    reexames = status['liminar mantida'] + status['liminar modificada']
    resumo = {
        'corte': '2026-09-30', 'acordaos_corpus': len(atos),
        'processos_com_acordao': len({r['cnj'] for r in atos}),
        'votacao_corpus': dict(Counter(r['votacao'] for r in atos)),
        'fontes_corpus': dict(Counter(r['fonte'] or 'não localizada' for r in atos)),
        'ministros_vencidos_corpus': dict(Counter(n for r in atos for n in r['vencidos'])),
        'confrontos': len(casos), 'situacao_confrontos': dict(status),
        'colegiados_confrontos': len(colegiados),
        'votacao_confrontos': dict(Counter(r['votacao'] for r in colegiados)),
        'ministros_vencidos_confrontos': dict(Counter(n for r in colegiados for n in r['vencidos'])),
        'reexames_liminares_comprovados': reexames,
        'percentual_mantidas_entre_reexames': round(100 * status['liminar mantida'] / reexames, 1),
        'percentual_modificadas_entre_reexames': round(100 * status['liminar modificada'] / reexames, 1),
        'sem_votacao_apurada': [r['chave_ato'] for r in atos if r['votacao'] == 'não apurada'],
    }
    (ROOT / 'resumo.json').write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return resumo


def graficos(s):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    matplotlib.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none', 'svg.hashsalt': 'tse-colegialidade', 'font.size': 11})
    dest = ROOT / 'graficos'
    dest.mkdir(exist_ok=True)

    def svg(nome, title, subtitle, labels, values, colors, note, denominator=None):
        fig, ax = plt.subplots(figsize=(10.5, 1.9 + .48 * len(labels)))
        fig.patch.set_facecolor('white')
        fig.subplots_adjust(left=.40, right=.89, top=.72, bottom=.20)
        ax.barh(range(len(labels)), values, color=colors, height=.6)
        ax.set_yticks(range(len(labels)), labels)
        ax.invert_yaxis()
        limit = max(values or [1]) * 1.27
        ax.set_xlim(0, limit)
        for i, v in enumerate(values):
            pct = (' · ' + f'{100*v/denominator:.1f}'.replace('.', ',') + '%') if denominator else ''
            ax.text(v + limit * .015, i, str(v) + pct, va='center', fontsize=11, color='#172b3a')
        ax.tick_params(axis='both', length=0)
        ax.set_xticks([])
        for spine in ax.spines.values(): spine.set_visible(False)
        fig.text(.04, .93, title, fontsize=17, weight='bold', color='#172b3a')
        fig.text(.04, .855, subtitle, fontsize=10.5, color='#475569')
        fig.text(.04, .045, note, fontsize=9, color='#475569')
        buf = io.StringIO()
        fig.savefig(buf, format='svg', metadata={'Date': None, 'Creator': 'Corpus TSE — colegialidade'})
        plt.close(fig)
        body = buf.getvalue().replace("font-family: 'DejaVu Sans'", "font-family: Arial, 'DejaVu Sans', sans-serif")
        (dest / (nome + '.svg')).write_text(body, encoding='utf-8')
        return body[body.index('<svg'):]

    blue, orange, gray = '#155e75', '#b45309', '#64748b'
    votes = []
    for key, n, subtitle in [('corpus', 200, '200 registros de acórdão do corpus · Corte em 30/09/2026'), ('confrontos', 27, '27 julgamentos colegiados nos confrontos presidenciais · Inclui certidões')]:
        counts = s['votacao_' + key]
        votes.append(svg('votacao_' + key, 'Como o TSE votou', subtitle,
                         ['Unânimes', 'Com divergência', 'Votação não apurada'],
                         [counts.get(x, 0) for x in ['unânime', 'com divergência', 'não apurada']],
                         [blue, orange, gray], 'Unidade: julgamento. Divergência parcial também conta como divergência.', n))
    situations = ['liminar sem revisão colegiada comprovada', 'liminar mantida', 'liminar modificada', 'decisão individual de mérito', 'tutela decidida diretamente pelo colegiado']
    situations_svg = svg('situacao_liminares', 'O que ocorreu com as medidas', '107 confrontos presidenciais · Situação documentada até 30/09/2026',
                         ['Sem revisão colegiada comprovada', 'Liminar mantida pelo colegiado', 'Liminar modificada pelo colegiado', 'Decisão individual de mérito', 'Tutela decidida direto pelo colegiado'],
                         [s['situacao_confrontos'][x] for x in situations],
                         [gray, blue, orange, '#76858f', '#537780'],
                         'Dos 26 reexames comprovados: 22 mantiveram (84,6%) e 4 modificaram (15,4%).\nAusência de revisão localizada não prova pendência processual. Unidade: processo.', 107)
    names = ['André Mendonça', 'Floriano de Azevedo Marques', 'Estela Aranha', 'Nunes Marques', 'Dias Toffoli', 'Antonio Carlos Ferreira', 'Ricardo Villas Bôas Cueva']
    minister = []
    for key, subtitle in [('corpus', '15 acórdãos com divergência identificada no corpus'), ('confrontos', '8 julgamentos com divergência nos confrontos presidenciais')]:
        count = s['ministros_vencidos_' + key]
        minister.append(svg('vencidos_' + key, 'Ministros com votos vencidos', subtitle, names, [count.get(n, 0) for n in names], [orange] * len(names),
                            'Uma ocorrência por ministro e julgamento, inclusive voto parcialmente vencido.\nVários ministros podem ficar vencidos no mesmo julgamento.'))

    def html_chart(filename, panels, labels):
        tabs = ''.join(f'<button type="button" aria-pressed="{str(i==0).lower()}" onclick="selectPanel({i})">{html.escape(t)}</button>' for i, t in enumerate(labels)) if len(panels) > 1 else ''
        items = ''.join(f'<section id="panel-{i}" {"hidden" if i else ""}>{v}</section>' for i, v in enumerate(panels))
        content = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Co legialidade no TSE</title><style>body{margin:0;padding:12px;background:#f8fafc;font-family:Arial,sans-serif}main{max-width:1120px;margin:auto;background:white;border:1px solid #e2e8f0;border-radius:8px;overflow:hidden}nav{display:flex;gap:8px;flex-wrap:wrap;padding:14px 20px 0}button{font:14px Arial;padding:9px 14px;cursor:pointer;border:1px solid #94a3b8;border-radius:6px;background:white;color:#334155}button[aria-pressed=true]{background:#155e75;color:white;border-color:#155e75}svg{display:block;width:100%;height:auto}section[hidden]{display:none}</style><main><nav>''' + tabs + '</nav>' + items + '''</main><script>function selectPanel(i){document.querySelectorAll('section').forEach((x,j)=>x.hidden=i!==j);document.querySelectorAll('button').forEach((x,j)=>x.setAttribute('aria-pressed',i===j))}</script></html>'''
        content = content.replace('Co legialidade', 'Colegialidade')
        (dest / filename).write_text(content, encoding='utf-8')
    html_chart('07_votacao.html', votes, ['Acórdãos do corpus (200)', 'Colegiados nos confrontos (27)'])
    html_chart('08_liminares.html', [situations_svg], [])
    html_chart('09_ministros_vencidos.html', minister, ['Acórdãos do corpus', 'Confrontos presidenciais'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--graficos', action='store_true')
    args = parser.parse_args()
    s = verificar_e_resumir()
    if args.graficos: graficos(s)
    print(json.dumps(s, ensure_ascii=False, indent=2))
