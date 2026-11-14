"""Extrai datas escritas e confronta referências do lote A para revisão humana."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MESES={'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}


def data_escrita(doc):
    t=re.sub(r'\s+',' ',(ROOT/doc['arquivo']).with_suffix('.txt').read_text(encoding='utf-8'))
    sessoes=list(re.finditer(r'SESS.O[^.]{0,80}?(\d{1,2})\.(\d{1,2})\.(2026)',t[-7000:]))
    if sessoes:
        m=sessoes[-1]
        return f'{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}',m[0],'sessão escrita no extrato da ata'
    bras=list(re.finditer(r'Bras[ií]lia\s*(?:\(DF\)|/DF)?\s*,\s*(\d{1,2})\s*(?:º|°)?\s+de\s+(\w+)\s+de\s+(2026)',t,re.I))
    bras=[m for m in bras if m[2].lower() in MESES]
    if bras:
        m=bras[-1]
        return f'{m[3]}-{MESES[m[2].lower()]:02d}-{int(m[1]):02d}',m[0],'data escrita na peça'
    ass=(doc.get('data_assinatura') or '')[:10]
    return ass or doc['data_metadata'],ass or doc['data_metadata'],'assinatura do documento no inventário oficial' if ass else 'dataDecisao no inventário oficial'


def main():
    dados=json.loads((ROOT/'curadoria_novos_a.json').read_text(encoding='utf-8'))
    dossies=json.loads((ROOT/'coleta_documental/auditoria/dossies_novos_a.json').read_text(encoding='utf-8'))
    supl=json.loads((ROOT/'suplemento_documental_auditoria.json').read_text(encoding='utf-8'))
    revisoes={}
    for cnj,r in dados.items():
        docs=dossies[cnj]['documentos']+[s for s in supl if s['cnj']==cnj]
        ref=next(d for d in docs if d['id_documento']==r['id_documento'])
        dt,trecho,origem=data_escrita(ref)
        candidatos=[]
        for d in docs:
            if d['tipo'].startswith('Desp') or 'Certid' in d['tipo']:continue
            data,evid,fonte=data_escrita(d)
            if data>dt and data<='2026-10-31':candidatos.append({'id_documento':d['id_documento'],'tipo':d['tipo'],'data':data,'evidencia':evid})
        revisoes[cnj]={'indice':r['revisao']['indice_lote'],'id_referencia':r['id_documento'],'data_escrita':dt,'evidencia_data':trecho,'origem_data':origem,'candidatos_posteriores':candidatos}
        if candidatos:print(r['revisao']['indice_lote'],cnj,'referencia',dt,'OUTROS',candidatos)
    (ROOT/'coleta_documental/auditoria/datas_lote_a.json').write_text(json.dumps(revisoes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
