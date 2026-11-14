"""Confere denominadores, rastreabilidade pública e dados dos gráficos desta etapa."""
import csv
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def ler(nome):return json.loads((ROOT/nome).read_text(encoding='utf-8'))
def csvs(nome):
    with (ROOT/nome).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def main():
    curadoria=ler('curadoria_confrontos.json');confrontos=csvs('confrontos.csv');relatos=csvs('relatos.csv');resumo=ler('campanha_resumo.json')
    assert len(confrontos)==len(curadoria)==len({r['cnj'] for r in confrontos})
    incluidos={k for k,v in curadoria.items() if v['incluir']}
    assert incluidos=={r['cnj'] for r in confrontos if r['incluir_comparativo']=='sim'}=={r['cnj'] for r in relatos}
    assert len(relatos)==len(incluidos)==resumo['incluidos_comparativos']
    assert [int(r['numero']) for r in relatos]==list(range(1,len(relatos)+1))
    assert all(r['data_ato_referencia']<='2026-10-31' for r in relatos)
    assert sum(v['pedidos'] for v in resumo['campanhas'].values())==len(incluidos)
    for r in confrontos:
        assert r['atendido'] in ['sim','não'] if r['incluir_comparativo']=='sim' else r['atendido']==''
    inventario=ler('inventario_documental.json');docs={d['url']:d for d in inventario['documentos']}
    for meta in inventario['lotes']:
        path=ROOT/meta['arquivo'];assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'],path
        with zipfile.ZipFile(path) as z:assert z.testzip() is None,path
    for cnj in incluidos:
        r=curadoria[cnj];assert r['url_peca'] in docs,(cnj,'fonte não preservada')
        ref=docs[r['url_peca']];p=ROOT/ref['arquivo']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==ref['sha256'],cnj
        assert not r.get('revisao',{}).get('pronto_publicacao') is False,cnj
    apuracao=ler('apuracao_colegialidade_resumo.json')
    for nome in ['corpus','presidencial']:
        a=apuracao[nome];assert sum(a['votacao'].values())==a['total'],nome
    assert apuracao['presidencial']['processos_comparaveis']==len(incluidos)
    assert sum(apuracao['presidencial']['situacao_confrontos'].values())==len(incluidos)
    configs=ler('graficos_interativos/dados_graficos.json');assert len(configs)==11
    for nome,c in configs.items():
        s=c['spec'];assert all(len(v['data'])==len(s['labels']) for v in s['series']),nome
        if s.get('mode')=='stacked-percent':
            for i in range(len(s['labels'])):assert abs(sum(v['data'][i] for v in s['series'])-100)<1e-6,nome
    print(f'OK: {len(curadoria)} alvos, {len(incluidos)} resultados documentados, {resumo.get("lacunas_documentais",0)} lacunas de fonte; 11 gráficos e fontes preservadas.')
if __name__=='__main__':main()
