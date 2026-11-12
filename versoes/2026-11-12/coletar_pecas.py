"""Coleta retomável do corpus pelo motor local coordenado, sem alterar o Notion."""
import argparse, csv, hashlib, html, json, re, sys, time, os, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CORTE='2026-10-31'
def carregar(path, default):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default
def salvar(path, obj):
    salvar_bytes(path,json.dumps(obj,ensure_ascii=False,indent=2).encode('utf-8'))
def salvar_bytes(path, blob):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as f:
        temp=Path(f.name);f.write(blob);f.flush();os.fsync(f.fileno())
    try:
        # No Windows, uma leitura concorrente pode bloquear a troca por instantes.
        for tentativa in range(8):
            try:
                temp.replace(path)
                break
            except PermissionError:
                if tentativa == 7:raise
                time.sleep(min(0.05 * 2**tentativa, 1.0))
    finally:temp.unlink(missing_ok=True)
def preservar_documentos(registro, novos):
    docs={d['url']:d for d in registro.get('documentos',[])}
    docs.update({d['url']:d for d in novos})
    return list(docs.values())
def arquivo_conferido(root, doc):
    if doc.get('status')!='conferido' or not doc.get('arquivo') or not doc.get('sha256'):return False
    arquivo=root/doc['arquivo'];texto=arquivo.with_suffix('.txt')
    try:
        return (hashlib.sha256(arquivo.read_bytes()).hexdigest()==doc['sha256'] and texto.is_file()
                and (not doc.get('sha256_texto') or hashlib.sha256(texto.read_bytes()).hexdigest()==doc['sha256_texto']))
    except OSError:return False
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
    for registro in estado.values():
        registro['documentos']=preservar_documentos(registro,[])
    salvar(checkpoint,estado)
    ids=alvos()
    def recente(cnj):
        bruto=carregar(motor._arquivo_cache(cnj,'TSE'),{})
        return float(bruto.get('instante') or 0)>=datetime(2026,11,11,tzinfo=timezone.utc).timestamp()
    ids.sort(key=lambda cnj:(not recente(cnj),cnj))
    sess=requests.Session();sess.headers.update(tse.HDR)
    locais={r['url']:r for r in carregar(ROOT/'inventario_documental_parcial.json',[]) if r.get('sha256')}
    def progresso():
        salvar(pasta/'progresso.json',{'estado_execucao':'em_execucao','atualizado_em':datetime.now(timezone.utc).isoformat(),'total_alvos':len(ids),'consultas_efetuadas':sum(bool(r.get('consulta_efetuada')) for r in estado.values()),'processos_sem_pendencias_de_download':sum(bool(r.get('completo')) for r in estado.values()),'pecas_conferidas':sum(sum(d.get('status')=='conferido' for d in r.get('documentos',[])) for r in estado.values()),'fase':'coleta documental; classificação jurídica pendente'})
    progresso()
    falhas=0;processados=0
    for cnj in ids:
        motor.checar_parada(pasta)
        salvo=estado.get(cnj,{})
        if salvo.get('completo') and salvo.get('documentos') and all(arquivo_conferido(ROOT,d) for d in salvo['documentos']):continue
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
            docs=[];vistos=set();antigos={d['url']:d for d in registro.get('documentos',[])}
            for proc in processos:
                if proc.get('instancia')!=3 or proc.get('numeroProcesso')!=cnj:continue
                for doc in selecionar(proc):
                    motor.checar_parada(pasta)
                    url=f"{tse.BACKEND}/documento?extensaoArquivo={doc['extensao']}&path={doc['storage']}"
                    if url in vistos:continue
                    vistos.add(url)
                    anterior=antigos.get(url,{})
                    if arquivo_conferido(ROOT,anterior):
                        docs.append(anterior);continue
                    entry={**doc,'url':url,'cnj':cnj}
                    try:
                        local=anterior if anterior.get('sha256') else locais.get(url,{})
                        caminho=ROOT/local['arquivo'] if local.get('arquivo') else None
                        blob=caminho.read_bytes() if caminho and caminho.is_file() else b''
                        reutilizado=bool(blob and hashlib.sha256(blob).hexdigest()==local.get('sha256'))
                        content_type='text/html'
                        if not reutilizado:
                            r=sess.get(url,timeout=60);r.raise_for_status();blob=r.content;content_type=r.headers.get('content-type','')
                        pdf=tse.extrair_pdf_sjur(blob,content_type)
                        if pdf is not None:
                            import fitz
                            blob=pdf
                            with fitz.open(stream=pdf,filetype='pdf') as f:texto='\n'.join(p.get_text() for p in f)
                            ext='.pdf'
                        else:
                            texto=html.unescape(re.sub('<[^>]+>',' ',blob.decode('utf-8',errors='replace')));ext='.html'
                        proprio=tse.numero_da_peca(texto)
                        if proprio!=cnj:raise ValueError('cabeçalho não confirma o CNJ solicitado')
                        nome=re.sub(r'\D','',cnj)+'_'+hashlib.sha256(url.encode()).hexdigest()[:16]
                        arq=destino/(nome+ext);salvar_bytes(arq,blob)
                        texto_bytes=texto.encode('utf-8')
                        salvar_bytes(destino/(nome+'.txt'),texto_bytes)
                        entry.update(status='conferido',arquivo=arq.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(blob).hexdigest(),sha256_texto=hashlib.sha256(texto_bytes).hexdigest(),reaproveitado=reutilizado)
                    except motor.Interrompido:raise
                    except Exception as e:entry.update(status='pendente',erro=str(e)[:240])
                    docs.append(entry)
                    registro={**registro,'consulta_efetuada':True,'documentos':preservar_documentos(registro,[entry]),'completo':False}
                    estado[cnj]=registro
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
    if args.limite:return 'parcial'
    return 'concluida' if all(estado.get(cnj,{}).get('completo') for cnj in ids) else 'finalizada_com_pendencias'

def rodar(args):
    from controle_coleta import trava_coleta
    sys.path.insert(0,str(args.motor_dir.resolve()))
    import pje_links_motor as motor
    pasta=ROOT/'coleta_documental'
    def status(valor, erro=None):
        path=pasta/'progresso.json';dados=carregar(path,{})
        dados.update(estado_execucao=valor,atualizado_em=datetime.now(timezone.utc).isoformat())
        if erro:dados['ultimo_erro']=erro
        else:dados.pop('ultimo_erro',None)
        salvar(path,dados)
    try:
        with trava_coleta(pasta):
            try:
                resultado=executar(args);status(resultado);return 0
            except motor.Interrompido:
                status('pausada');print('PAUSADA: progresso preservado.',flush=True);return 0
            except Exception as exc:
                status('erro',str(exc));print(f'ERRO: {exc}',file=sys.stderr,flush=True);return 1
    except RuntimeError as exc:
        print(str(exc),file=sys.stderr);return 2
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--motor-dir',type=Path,required=True);p.add_argument('--limite',type=int,default=0);sys.exit(rodar(p.parse_args()))
