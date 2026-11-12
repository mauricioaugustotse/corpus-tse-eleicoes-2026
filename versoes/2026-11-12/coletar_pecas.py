"""Coleta retomável do corpus pelo motor local coordenado, sem alterar o Notion."""
import argparse, csv, hashlib, html, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CORTE='2026-10-31'
def carregar(path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default
def salvar(path, obj):
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)
def linhas(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
def alvos():
    ids={r['cnj'] for r in linhas(ROOT/'triagem_confrontos.csv')}
    ids.update(r['NR_PROCESSO'] for r in linhas(ROOT/'acordaos_para_conferencia.csv'))
    ids.update(carregar(ROOT.parent/'2026-10-01/curadoria_confrontos.json',{}))
    return sorted(ids)
def selecionar(processo):
    decisoes={str(d['idProcessoDocumento']):d for d in processo.get('decisoes',[]) if d.get('idProcessoDocumento')}
    for doc in processo.get('documentos',[]):
        if doc.get('documentoSigiloso') or doc.get('publico') is False:continue
        storage=doc.get('documentoStorage') or ''
        if not storage.startswith('tse/'):continue
        tipo=doc.get('tipoDocumento') or ''
        dec=decisoes.get(str(doc.get('idProcessoDocumento')), {})
        data=(dec.get('dataDecisao') or doc.get('dataAssinatura') or doc.get('dataJuntada') or '')[:10]
        if not data or data>CORTE:continue
        if not (dec or tipo.startswith(('Decis','Ac','Sent','Desp')) or ('Certid' in tipo and 'julgamento' in tipo.lower())):continue
        yield {'tipo':tipo,'data_metadata':data,'data_decisao_metadata':dec.get('dataDecisao'),'data_assinatura':doc.get('dataAssinatura'),'data_juntada':doc.get('dataJuntada'),'id_documento':doc.get('idProcessoDocumento'),'storage':storage,'extensao':doc.get('extensaoArquivo') or 'text/html'}
def executar(args):
    sys.path.insert(0,str(args.motor_dir.resolve()))
    import pje_links_motor as motor
    import tse_doc_url as tse
    import requests
    motor.instalar_sinais()
    pasta=ROOT/'coleta_documental';pasta.mkdir(exist_ok=True)
    destino=pasta/'pecas';destino.mkdir(exist_ok=True)
    checkpoint=pasta/'checkpoint.json';estado=carregar(checkpoint,{})
    ids=alvos()
    def recente(cnj):
        bruto=carregar(motor._arquivo_cache(cnj,'TSE'),{})
        return float(bruto.get('instante') or 0)>=datetime(2026,11,11,tzinfo=timezone.utc).timestamp()
    ids.sort(key=lambda cnj:(not recente(cnj),cnj))
    sess=requests.Session();sess.headers.update(tse.HDR)
    def progresso():
        salvar(pasta/'progresso.json',{'atualizado_em':datetime.now(timezone.utc).isoformat(),'total_alvos':len(ids),'consultas_efetuadas':sum(bool(r.get('consulta_efetuada')) for r in estado.values()),'processos_sem_pendencias_de_download':sum(bool(r.get('completo')) for r in estado.values()),'pecas_conferidas':sum(sum(d.get('status')=='conferido' for d in r.get('documentos',[])) for r in estado.values()),'fase':'coleta documental; classificação jurídica pendente'})
    falhas=0;processados=0
    for cnj in ids:
        motor.checar_parada(pasta)
        if estado.get(cnj,{}).get('completo'):continue
        if args.limite and processados>=args.limite:break
        processados+=1;registro=estado.get(cnj,{})
        print(f'CONSULTA {cnj}',flush=True)
        try:
            bruto=carregar(motor._arquivo_cache(cnj,'TSE'),{})
            # Aceita somente inventários obtidos a partir da geração estatística.
            fresco=float(bruto.get('instante') or 0)>=datetime(2026,11,11,tzinfo=timezone.utc).timestamp()
            processos=bruto.get('processos') if fresco else None
            if processos is None:
                processos=motor._post_processos(cnj,sess,pasta,orgao='TSE',pausa=65)
                motor._para_cache(cnj,'TSE',processos)
            falhas=0
            docs=[];antigos={d['url']:d for d in registro.get('documentos',[])}
            for proc in processos:
                if proc.get('instancia')!=3 or proc.get('numeroProcesso')!=cnj:continue
                for doc in selecionar(proc):
                    url=f"{tse.BACKEND}/documento?extensaoArquivo={doc['extensao']}&path={doc['storage']}"
                    anterior=antigos.get(url,{})
                    if anterior.get('status')=='conferido' and (ROOT/anterior['arquivo']).exists():
                        docs.append(anterior);continue
                    entry={**doc,'url':url,'cnj':cnj}
                    try:
                        r=sess.get(url,timeout=60);r.raise_for_status();blob=r.content
                        pdf=tse.extrair_pdf_sjur(blob,r.headers.get('content-type',''))
                        if pdf is not None:
                            import fitz
                            blob=pdf
                            with fitz.open(stream=pdf,filetype='pdf') as f:texto='\n'.join(p.get_text() for p in f)
                            ext='.pdf'
                        else:
                            texto=html.unescape(re.sub('<[^>]+>',' ',r.content.decode('utf-8',errors='replace')));ext='.html'
                        proprio=tse.numero_da_peca(texto)
                        if proprio!=cnj:raise ValueError('cabeçalho não confirma o CNJ solicitado')
                        nome=re.sub(r'\D','',cnj)+'_'+hashlib.sha256(url.encode()).hexdigest()[:16]
                        arq=destino/(nome+ext);arq.write_bytes(blob)
                        (destino/(nome+'.txt')).write_text(texto,encoding='utf-8')
                        entry.update(status='conferido',arquivo=arq.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(blob).hexdigest())
                    except Exception as e:entry.update(status='pendente',erro=str(e)[:240])
                    docs.append(entry)
                    estado[cnj]={'consulta_efetuada':True,'documentos':docs,'completo':False}
                    salvar(checkpoint,estado);progresso()
                    motor.dormir(motor.PAUSA_GET,pasta)
            registro={'consulta_efetuada':True,'consultado_em':datetime.now(timezone.utc).isoformat(),'documentos':docs,'completo':bool(processos) and bool(docs) and all(d['status']=='conferido' for d in docs),'nota':'completo refere-se à coleta; não equivale a curadoria jurídica ou prova de cobertura integral do PJe'}
        except motor.Interrompido:raise
        except Exception as e:
            falhas+=1;registro.update(completo=False,erro_consulta=str(e)[:300])
        estado[cnj]=registro;salvar(checkpoint,estado);progresso()
        print(f"SALVO {cnj}: {len(registro.get('documentos',[]))} peças",flush=True)
        if falhas>=3:raise RuntimeError('três falhas consecutivas; checkpoint preservado')
    progresso()
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--motor-dir',type=Path,required=True);p.add_argument('--limite',type=int,default=0);executar(p.parse_args())
