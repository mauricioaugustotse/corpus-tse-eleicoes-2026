"""Audita os caches afetados por decisoes=null, sem rede ou mutações na coleta."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
CORTE='2026-10-31'


def contar(itens):
    return dict(Counter(itens))


def main(motor_dir):
    sys.path.insert(0,str(motor_dir.resolve()))
    import pje_links_motor as motor
    fontes=json.loads((ROOT/'auditoria_caches_149_alvos.json').read_text(encoding='utf-8'))
    processos=[]
    todos_elegiveis=[]
    for cnj in fontes['cnjs']:
        path=motor._arquivo_cache(cnj,'TSE')
        bruto=json.loads(path.read_text(encoding='utf-8')) if path and path.exists() else {}
        lista=bruto.get('processos') or []
        fontes_encontradas=[];elegiveis=[];descartes=Counter();tipos_publicos=Counter();outras_origens=[]
        for proc in lista:
            if not isinstance(proc,dict):
                descartes['processo_com_tipo_inesperado']+=1
                continue
            fontes_encontradas.append({'cnj':proc.get('numeroProcesso'),'instancia':proc.get('instancia'),
                                      'orgao':proc.get('orgao'),'documentos_tipo':type(proc.get('documentos')).__name__,
                                      'decisoes_tipo':type(proc.get('decisoes')).__name__,
                                      'quantidade_documentos':len(proc.get('documentos') or []),
                                      'quantidade_decisoes':len(proc.get('decisoes') or [])})
            if proc.get('instancia')!=3 or proc.get('numeroProcesso')!=cnj:
                descartes['instancia_ou_cnj_diverso']+=len(proc.get('documentos') or [])
                continue
            decisoes={str(d['idProcessoDocumento']):d for d in (proc.get('decisoes') or []) if d.get('idProcessoDocumento')}
            for doc in (proc.get('documentos') or []):
                if doc.get('documentoSigiloso') or doc.get('publico') is False:
                    descartes['sigiloso_ou_nao_publico']+=1;continue
                storage=doc.get('documentoStorage') or ''
                if not storage.startswith('tse/'):
                    outras_origens.append({'id_documento':doc.get('idProcessoDocumento'),'tipo':doc.get('tipoDocumento'),
                                            'storage':storage,'data_assinatura':doc.get('dataAssinatura'),
                                            'data_juntada':doc.get('dataJuntada')})
                    descartes['storage_ausente_ou_nao_tse']+=1;continue
                tipo=doc.get('tipoDocumento') or ''
                tipos_publicos[tipo]+=1
                dec=decisoes.get(str(doc.get('idProcessoDocumento')), {})
                data=(dec.get('dataDecisao') or doc.get('dataAssinatura') or doc.get('dataJuntada') or '')[:10]
                if not data:
                    descartes['data_ausente']+=1;continue
                if data>CORTE:
                    descartes['data_posterior_corte']+=1;continue
                if not (dec or tipo.startswith(('Decis','Ac','Sent','Desp')) or ('Certid' in tipo and 'julgamento' in tipo.lower())):
                    descartes['tipo_fora_selecao']+=1;continue
                extensao=doc.get('extensaoArquivo') or 'text/html'
                elegiveis.append({'cnj':cnj,'instancia':proc.get('instancia'),'orgao':proc.get('orgao'),
                                  'tipo':tipo,'data_metadata':data,'data_assinatura':doc.get('dataAssinatura'),
                                  'data_juntada':doc.get('dataJuntada'),'id_documento':doc.get('idProcessoDocumento'),
                                  'storage':storage,'extensao':extensao,
                                  'url':f'https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo={extensao}&path={storage}'})
        unicos={r['url']:r for r in elegiveis}
        processo={'cnj':cnj,'cache_disponivel':bool(bruto),'cache_sha256':hashlib.sha256(path.read_bytes()).hexdigest() if path and path.exists() else None,
                  'cache_instante':bruto.get('instante'),'tipo_processos':type(bruto.get('processos')).__name__,
                  'fontes_encontradas':fontes_encontradas,'documentos_elegiveis_registros':len(elegiveis),
                  'documentos_elegiveis_urls_unicas':len(unicos),'tipos_elegiveis_urls_unicas':contar(r['tipo'] for r in unicos.values()),
                  'tipos_publicos_tse_registros':dict(tipos_publicos),'descartes_selecao':dict(descartes),
                  'documentos_outra_origem':outras_origens,
                  'documentos_elegiveis':list(unicos.values()),
                  'conclusao_cobertura':'há peças elegíveis no cache, apesar de decisoes=null' if unicos else 'nenhuma peça elegível encontrada neste inventário; isso não prova ausência de atos no processo'}
        processos.append(processo);todos_elegiveis.extend(unicos.values())
    resumo={'processos_auditados':len(processos),'caches_disponiveis':sum(p['cache_disponivel'] for p in processos),
            'processos_com_fonte_instancia3_cnj_exato':sum(any(f['instancia']==3 and f['cnj']==p['cnj'] for f in p['fontes_encontradas']) for p in processos),
            'processos_com_decisoes_nulas':sum(any(f['decisoes_tipo']=='NoneType' for f in p['fontes_encontradas']) for p in processos),
            'processos_com_documentos_elegiveis':sum(bool(p['documentos_elegiveis_urls_unicas']) for p in processos),
            'processos_com_algum_documento_no_cache':sum(any(f['quantidade_documentos'] for f in p['fontes_encontradas']) for p in processos),
            'processos_com_documentos_lista_vazia':sum(not any(f['quantidade_documentos'] for f in p['fontes_encontradas']) for p in processos),
            'total_documentos_no_cache':sum(sum(f['quantidade_documentos'] for f in p['fontes_encontradas']) for p in processos),
            'tipos_publicos_tse_nao_elegiveis':dict(sum((Counter(p['tipos_publicos_tse_registros']) for p in processos),Counter())),
            'tipos_documentos_outra_origem':contar(d['tipo'] for p in processos for d in p['documentos_outra_origem']),
            'processos_sem_documentos_elegiveis_neste_inventario':sum(not p['documentos_elegiveis_urls_unicas'] for p in processos),
            'documentos_elegiveis_urls_unicas_por_processo':len(todos_elegiveis),
            'documentos_elegiveis_urls_unicas_globais':len({r['url'] for r in todos_elegiveis}),
            'tipos_elegiveis':contar(r['tipo'] for r in todos_elegiveis),
            'primeira_data_elegivel':min((r['data_metadata'] for r in todos_elegiveis),default=None),
            'ultima_data_elegivel':max((r['data_metadata'] for r in todos_elegiveis),default=None)}
    resultado={'auditado_em':datetime.now(timezone.utc).isoformat(),'corte':CORTE,
               'checkpoint_sha256_no_diagnostico':fontes['checkpoint_sha256_no_diagnostico'],
               'resumo':resumo,'limite':'decisoes=null não equivale a ausência de atos. A seleção usa documentos públicos da instância 3, CNJ exato, storage TSE e data de assinatura/juntada até o corte. Nenhuma consulta POST ou GET foi realizada; nenhum checkpoint foi alterado.',
               'processos':processos}
    (ROOT/'auditoria_caches_149.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    linhas=['# Auditoria dos caches com decisões nulas','',f"Foram auditados {resumo['processos_auditados']} caches relativos à falha de iteração sobre `decisoes=null`. Nenhuma lista nula foi tratada como ausência de atos.",'',
            f"Há {resumo['processos_com_documentos_elegiveis']} processos com peças elegíveis e {resumo['processos_sem_documentos_elegiveis_neste_inventario']} sem peças elegíveis neste inventário. Os elegíveis totalizam {resumo['documentos_elegiveis_urls_unicas_por_processo']} URLs distintas por processo ({resumo['documentos_elegiveis_urls_unicas_globais']} globalmente), com os seguintes tipos: `{json.dumps(resumo['tipos_elegiveis'],ensure_ascii=False)}`.",'',
            f"Em {resumo['processos_com_fonte_instancia3_cnj_exato']} casos, a fonte confirma instância 3 e CNJ exato. As datas elegíveis vão de {resumo['primeira_data_elegivel']} a {resumo['ultima_data_elegivel']}.",'',
            'O diagnóstico não atribui resultados jurídicos. A ausência de peça elegível neste inventário não comprova inexistência de atos no processo. Listas de tipos, descartes, identificação de origem e links oficiais estão no JSON.','',
            f"Dos 149 caches, {resumo['processos_com_algum_documento_no_cache']} possuem algum documento visível, somando {resumo['total_documentos_no_cache']} registros; {resumo['processos_com_documentos_lista_vazia']} têm lista de documentos vazia. Os tipos com storage TSE são: `{json.dumps(resumo['tipos_publicos_tse_nao_elegiveis'],ensure_ascii=False)}`. Os cinco registros da origem RS incluem duas decisões, um despacho e duas intimações com storage regional/rs ou pje1g/rs; não foram confundidos com atos próprios do TSE, embora o contêiner do processo informe órgão TSE e instância 3.",'',
            '| CNJ | Peças elegíveis únicas | Tipos |','|---|---:|---|']
    linhas.extend(f"| {p['cnj']} | {p['documentos_elegiveis_urls_unicas']} | {json.dumps(p['tipos_elegiveis_urls_unicas'],ensure_ascii=False)} |" for p in processos)
    (ROOT/'auditoria_caches_149.md').write_text('\n'.join(linhas)+'\n',encoding='utf-8')
    print(json.dumps(resumo,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--motor-dir',type=Path,required=True)
    main(parser.parse_args().motor_dir)
