"""Preserva peças públicas em ZIPs reproduzíveis, sem logs, locks ou caches privados."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def main():
    checkpoint=json.loads((ROOT/'coleta_documental/checkpoint.json').read_text(encoding='utf-8'))
    # Espelho público de metadados controlados pelo coletor; sem logs de rede ou credenciais.
    espelho={cnj:{k:v for k,v in r.items() if k in {'consulta_efetuada','consultado_em','completo','sem_pecas_elegiveis','nota','documentos'}} for cnj,r in checkpoint.items()}
    for registro in espelho.values():
        registro['documentos']=[{k:v for k,v in d.items() if k!='erro'} for d in registro.get('documentos',[])]
    (ROOT/'inventario_processos_documentais.json').write_text(json.dumps(espelho,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    docs={d['url']:{'cnj':cnj,**d} for cnj,r in checkpoint.items() for d in r.get('documentos',[]) if d.get('status')=='conferido'}
    suplemento=ROOT/'suplemento_documental_auditoria.json'
    if suplemento.exists():
        extra=json.loads(suplemento.read_text(encoding='utf-8'))
        entradas=extra if isinstance(extra,list) else extra.get('documentos',[])
        for d in entradas:
            if d.get('arquivo') and d.get('url'):docs.setdefault(d['url'],d)
    conexa=ROOT/'curadoria_revisao_conexa.json'
    if conexa.exists():
        for cnj,caso in json.loads(conexa.read_text(encoding='utf-8')).items():
            for d in caso.get('revisao',{}).get('fontes_reconciliacao',[]):
                if d.get('arquivo') and d.get('url') and d.get('sha256'):
                    docs.setdefault(d['url'],{**d,'cnj':d.get('cnj_documento',cnj),'contexto_curadoria':cnj,'status':'fonte contextual verificada; não é novo ato estatístico'})
    pasta=ROOT/'documentos_oficiais';pasta.mkdir(exist_ok=True)
    anterior=ROOT/'inventario_documental.json'
    anterior=json.loads(anterior.read_text(encoding='utf-8')) if anterior.exists() else {'lotes':[],'documentos':[]}
    antigos={d['url']:d for d in anterior['documentos']}
    mapa={}
    for d in antigos.values():
        if d['url'] in docs and d['sha256']==docs[d['url']]['sha256']:
            docs[d['url']]['arquivo']=d['arquivo']
            mapa[d['arquivo']]=d['pacote']
            texto=Path(d['arquivo']).with_suffix('.txt').as_posix()
            mapa[texto]=d['pacote']
    arquivos=sorted({d['arquivo'] for d in docs.values() if d['arquivo'] not in mapa})
    for nome in list(arquivos):
        texto=Path(nome).with_suffix('.txt').as_posix()
        if (ROOT/texto).is_file():arquivos.append(texto)
    lote=[];tamanho=0;numero=len(anterior['lotes'])
    def escrever(nomes):
        nonlocal numero
        numero+=1;nome_zip=f'lote_{numero:03d}.zip';path=pasta/nome_zip
        with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for nome in nomes:
                info=zipfile.ZipInfo(nome,date_time=(2026,11,12,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,(ROOT/nome).read_bytes());mapa[nome]=f'documentos_oficiais/{nome_zip}'
        return {'arquivo':f'documentos_oficiais/{nome_zip}','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'membros':len(nomes)}
    lotes=anterior['lotes'].copy()
    for meta in lotes:
        assert hashlib.sha256((ROOT/meta['arquivo']).read_bytes()).hexdigest()==meta['sha256'],meta['arquivo']
    for nome in sorted(set(arquivos)):
        tam=(ROOT/nome).stat().st_size
        if lote and tamanho+tam>40_000_000:
            lotes.append(escrever(lote));lote=[];tamanho=0
        lote.append(nome);tamanho+=tam
    if lote:lotes.append(escrever(lote))
    inventario=[]
    for url,d in sorted(docs.items()):
        path=ROOT/d['arquivo'];digest=hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest==d['sha256'],d['arquivo']
        inventario.append({**d,'pacote':mapa[d['arquivo']],'membro':d['arquivo']})
    saida={'nota':'Peças oficiais preservadas para conferência. Datas do inventário não substituem a leitura da peça e da data do julgamento. Não atribui resultados jurídicos. Extraia os ZIPs na pasta desta versão para restaurar os caminhos de referência.','total_pecas':len(inventario),'lotes':lotes,'documentos':inventario}
    (ROOT/'inventario_documental.json').write_text(json.dumps(saida,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pecas':len(inventario),'lotes':len(lotes),'bytes_zip':sum(l['bytes'] for l in lotes)},ensure_ascii=False))
if __name__=='__main__':main()
