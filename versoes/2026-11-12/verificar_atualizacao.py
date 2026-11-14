"""Valida o pacote estatístico, seu corte e o manifesto da atualização."""
from pathlib import Path
import csv, hashlib, json
ROOT=Path(__file__).resolve().parent
def rows(name):
    with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))
def verificar():
    fontes=json.loads((ROOT/'fontes.json').read_text(encoding='utf-8'))
    for name, meta in fontes.items():
        candidatos=[p for p in (ROOT/'originais').glob('*.zip') if hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']]
        assert len(candidatos)==1, name
    atos=rows('atos.csv'); processos=rows('processos.csv')
    assert all('2025-10-03'<=r['DT_DECISAO_ISO']<='2026-10-31' for r in atos)
    assert max(r['DT_DECISAO_ISO'] for r in atos)=='2026-10-31'
    assert len(atos)==len({r['CHAVE_ATO'] for r in atos})
    ids={r['NR_PROCESSO'] for r in processos}
    assert len(ids)==len(processos)
    assert ids=={r['NR_PROCESSO'] for r in atos}
    resumo=json.loads((ROOT/'resumo.json').read_text(encoding='utf-8'))
    assert len(atos)==resumo['total_atos']==sum(resumo['atos_por_tipo'].values())==sum(resumo['atos_por_mes'].values())
    assert len(processos)==resumo['total_processos']==sum(int(r['QT_ATOS_RECORTE'])>0 for r in processos)
    assert sum(int(r['QT_ATOS_RECORTE']) for r in processos)==len(atos)
    assert sum(int(r['FL_RECORTE_COMUNICACAO']) for r in processos)==resumo['total_processos_comunicacao']
    alvos=rows('triagem_confrontos.csv')
    assert len(alvos)==len({r['cnj'] for r in alvos})
    assert {r['cnj'] for r in alvos} <= ids
    assert resumo['controle']['atos_posteriores_ao_fim']>0
    for name, digest in json.loads((ROOT/'manifesto_atualizacao.json').read_text(encoding='utf-8')).items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, name
    complemento=''
    if (ROOT/'campanha_resumo.json').exists():
        curadoria=json.loads((ROOT/'campanha_resumo.json').read_text(encoding='utf-8'))
        complemento=f" {curadoria['incluidos_comparativos']} resultados documentados; {curadoria.get('lacunas_documentais',0)} lacunas de fonte."
    print(f'OK: {len(atos)} atos, {len(processos)} processos, {len(alvos)} alvos no extrato.'+complemento)
if __name__=='__main__': verificar()
