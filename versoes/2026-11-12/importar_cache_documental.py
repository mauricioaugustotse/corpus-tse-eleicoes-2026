"""Reaproveita links públicos conhecidos; não descobre peças nem consulta CAPTCHA."""
import argparse, csv, hashlib, json, re, urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent
def executar(cache):
    with (ROOT/'triagem_confrontos.csv').open(encoding='utf-8-sig') as f:
        ids={re.sub(r'\D','',r['cnj']) for r in csv.DictReader(f,delimiter=';')}
    inventory=[]
    for p in sorted(cache.glob('*.json')):
        if p.name.split('_')[0] not in ids: continue
        o=json.loads(p.read_text(encoding='utf-8'))
        for proc in o.get('processos',[]):
            for d in proc.get('documentos',[]):
                tipo=d.get('tipoDocumento') or ''
                dt=(d.get('dataAssinatura') or d.get('dataJuntada') or '')[:10]
                storage=d.get('documentoStorage') or ''
                if not storage.startswith('tse/') or not dt or dt>'2026-10-31': continue
                if d.get('documentoSigiloso') or d.get('publico') is False: continue
                if not (tipo.startswith(('Decis','Ac','Sent')) or ('Certid' in tipo and 'julgamento' in tipo.lower())): continue
                url='https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo='+d['extensaoArquivo']+'&path='+storage
                inventory.append({'cnj':o['cnj'],'tipo':tipo,'data_assinatura_ou_juntada':dt,'url':url,'cache_obtido_epoch':o.get('instante'),'nota':'inventário parcial de cache; data do ato e resultado dependem da peça'})
    unique={r['url']:r for r in inventory};inventory=list(unique.values())
    out=ROOT/'pecas_cache';out.mkdir(exist_ok=True)
    def baixar(r):
        dest=out/(re.sub(r'\D','',r['cnj'])+'_'+hashlib.sha256(r['url'].encode()).hexdigest()[:16]+'.html')
        try:
            if not dest.exists():
                with urllib.request.urlopen(r['url'],timeout=30) as response: body=response.read()
                if body.lstrip().startswith(b'{') or b'captcha' in body[:3000].lower(): raise ValueError('resposta sem peça verificável')
                dest.write_bytes(body)
            r.update(arquivo=dest.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),status='baixada; leitura jurídica pendente')
        except Exception as e: r.update(status='indisponível',erro=type(e).__name__)
        return r
    with ThreadPoolExecutor(max_workers=3) as pool: inventory=list(pool.map(baixar,inventory))
    (ROOT/'inventario_documental_parcial.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'links':len(inventory),'processos':len({r['cnj'] for r in inventory}),'baixadas':sum('sha256' in r for r in inventory)},ensure_ascii=True))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path,required=True);executar(p.parse_args().cache)
