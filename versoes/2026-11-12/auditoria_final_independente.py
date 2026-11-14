"""Conferência independente de contagens, fontes suplementares e pacotes publicados.

Somente lê os artefatos da atualização e escreve seu próprio relatório.
"""
import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import parse_qs,urlparse
import zipfile

ROOT=Path(__file__).resolve().parent
ALVOS=['0602697-28.2026.6.00.0000','0602800-35.2026.6.00.0000',
       '0602824-63.2026.6.00.0000','0602912-04.2026.6.00.0000']


def ler(nome):return json.loads((ROOT/nome).read_text(encoding='utf-8'))
def sha(blob):return hashlib.sha256(blob).hexdigest()
def csv_ler(nome):
    with (ROOT/nome).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))


def main():
    cur=ler('curadoria_confrontos.json');sup=ler('curadoria_suplementares_outubro.json')
    resumo=ler('campanha_resumo.json');triagem=ler('triagem_base_integral.json')
    confrontos=csv_ler('confrontos.csv');relatos=csv_ler('relatos.csv')
    invent=ler('inventario_documental.json');espelho=ler('inventario_processos_documentais.json')
    checkpoint=ler('coleta_documental/checkpoint.json');progresso=ler('coleta_documental/progresso.json')
    coleg=ler('apuracao_colegialidade.json')
    checks=[];erros=[]
    def conferir(nome,condicao,detalhe=None):
        checks.append({'verificacao':nome,'ok':bool(condicao),'detalhe':detalhe})
        if not condicao:erros.append(nome)
    incluidos={c:r for c,r in cur.items() if r.get('incluir')}
    ids_csv=[r['cnj'] for r in confrontos];ids_relatos=[r['cnj'] for r in relatos]
    ids_csv_incl={r['cnj'] for r in confrontos if r['incluir_comparativo']=='sim'}
    conferir('872 confrontos únicos na curadoria e no CSV',len(cur)==len(confrontos)==len(set(ids_csv))==872)
    conferir('Curadoria, triagem integral e CSV cobrem os mesmos CNJs',set(cur)==set(ids_csv)==set(triagem['todos_confrontos_detectados']))
    conferir('432 comparáveis coincidem na curadoria, resumo, CSV e relatos',len(incluidos)==resumo['incluidos_comparativos']==len(relatos)==len(set(ids_relatos))==432 and set(incluidos)==ids_csv_incl==set(ids_relatos))
    conferir('Numeração dos relatos é contínua de 1 a 432',[int(r['numero']) for r in relatos]==list(range(1,433)))
    conferir('Relatos ordenados por data da peça decrescente',[r['data_ato_referencia'] for r in relatos]==sorted((r['data_ato_referencia'] for r in relatos),reverse=True))
    lacunas={c for c,r in cur.items() if r.get('categoria')=='pendência documental; cobertura limitada'}
    conferir('201 lacunas documentais explicitadas e fora dos percentuais',len(lacunas)==resumo.get('lacunas_documentais')==201 and not lacunas.intersection(incluidos))
    conferir('Lacunas não recebem resultado negativo ou positivo',all(cur[c].get('atendido') is None for c in lacunas))
    campanhas={}
    for campanha in ['Lula','Flávio']:
        dados=[r for r in incluidos.values() if r['campanha_autora']==campanha]
        positivos=sum(r['atendido'] is True for r in dados);negativos=sum(r['atendido'] is False for r in dados)
        calc={'pedidos':len(dados),'atendidos':positivos,'nao_atendidos':negativos,'percentual_atendimento':100*positivos/len(dados)}
        campanhas[campanha]=calc;esperado=resumo['campanhas'][campanha]
        conferir(f'Totais e percentual da campanha {campanha}',all(abs(calc[k]-esperado[k])<1e-9 for k in calc),calc)
    conferir('Resultados comparáveis são todos booleanos',sum(r['atendido'] is True or r['atendido'] is False for r in incluidos.values())==432)
    conferir('201 é lacuna de fonte; zero pendências de revisão não significa cobertura integral',resumo.get('pendentes_de_revisao')==0 and resumo.get('lacunas_documentais')==201)
    conferir('1.295 consultas coincidem no checkpoint, espelho e painel',len(checkpoint)==len(espelho)==progresso['total_alvos']==progresso['consultas_efetuadas']==1295 and set(checkpoint)==set(espelho))
    sem_erros={c:{**r,'documentos':[{k:v for k,v in d.items() if k!='erro'} for d in r.get('documentos') or []]} for c,r in checkpoint.items()}
    conferir('Espelho coincide com o checkpoint após sanitização intencional do campo doc.erro',sem_erros==espelho)
    conferidas=sum(d.get('status')=='conferido' for r in checkpoint.values() for d in r.get('documentos') or [])
    completos=sum(bool(r.get('completo')) for r in checkpoint.values())
    conferir('Contagens do painel espelham peças e processos completos',conferidas==progresso['pecas_conferidas'] and completos==progresso['processos_sem_pendencias_de_download'],{'pecas':conferidas,'processos_completos':completos})
    conferir('Nenhum erro de iteração nula permanece no checkpoint',not any(r.get('erro_consulta')=="'NoneType' object is not iterable" for r in checkpoint.values()))

    por_cnj_relatos={r['cnj']:r for r in relatos}
    por_cnj_confrontos={r['cnj']:r for r in confrontos}
    docs_por_url={d['url']:d for d in invent['documentos']}
    conferir('Campos comparativos no CSV correspondem à curadoria',all(
        por_cnj_confrontos[c]['campanha_autora']==r['campanha_autora']
        and por_cnj_confrontos[c]['atendido']==('sim' if r['atendido'] else 'não')
        and por_cnj_confrontos[c]['url_peca_oficial']==r['url_peca']
        and por_cnj_confrontos[c]['data_ato_referencia']==r['data_ato_referencia'] for c,r in incluidos.items()))
    conferir('Datas dos relatos correspondem à referência de cada CNJ',all(por_cnj_relatos[c]['data_ato_referencia']==r['data_ato_referencia'] for c,r in incluidos.items()))
    conferir('Todas as 432 fontes principais estão no inventário publicável',all(r['url_peca'] in docs_por_url for r in incluidos.values()))
    quatro=[]
    for cnj in ALVOS:
        r=sup[cnj];rev=r['revisao_outubro'];ref=rev['fonte_referencia'];ac=rev['fonte_fundamentos']
        fontes=[]
        for papel,fonte in [('certidao_primaria',ref),('acordao_documental_posterior',ac)]:
            arq=ROOT/fonte['arquivo'];blob=arq.read_bytes()
            texto=re.sub(r'\s+',' ',arq.with_suffix('.txt').read_text(encoding='utf-8'))
            primeiro=re.search(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}',texto[:3000])
            cnj_lido=primeiro.group(0) if primeiro else None
            url_hash=Path(parse_qs(urlparse(fonte['url']).query)['path'][0]).name
            fontes.append({'papel':papel,**fonte,'cnj_cabecalho':cnj_lido,'hash_arquivo_conferido':sha(blob)==fonte['sha256'],
                           'hash_na_url_compativel':url_hash==fonte['sha256'],
                           'dispositivo_unanime_improcedente':bool(re.search(r'por unanimidade.{0,150}improcedent',texto,re.I)),
                           'inventariado_para_reproducao':fonte['url'] in docs_por_url})
        conferir(f'CNJ, hash, URL e inventário das duas fontes de {cnj}',all(f['cnj_cabecalho']==cnj and f['hash_arquivo_conferido'] and f['hash_na_url_compativel'] and f['inventariado_para_reproducao'] for f in fontes))
        conferir(f'Certidão anterior ao corte e acórdão posterior de {cnj}',ref['tipo']=='Certidão de julgamento' and ref['data_assinatura'][:10]<='2026-10-31' and ac['tipo']=='Acórdão' and ac['data_assinatura'][:10]>'2026-10-31')
        conferir(f'Improcedência unânime e sessão anterior ao corte de {cnj}',all(f['dispositivo_unanime_improcedente'] for f in fontes) and rev['unanimidade'] is True and rev['data_sessao']<='2026-10-31')
        conferir(f'Fonte principal e cronologia preservadas no relato de {cnj}',r['url_peca']==ref['url'] and ref['url'] in por_cnj_relatos[cnj]['texto'] and rev.get('nota_cronologica') and r['data_julgamento_no_corpo']==rev['data_sessao'])
        conferir(f'CSV incorpora resultado negativo e fonte primária de {cnj}',por_cnj_confrontos[cnj]['atendido']=='não' and por_cnj_confrontos[cnj]['url_peca_oficial']==ref['url'])
        ledger=[a for a in coleg['ledger_julgamentos'] if a['cnj']==cnj]
        conferir(f'Um julgamento documental, sem dupla contagem das duas fontes, de {cnj}',len(ledger)==1 and ledger[0]['votacao']=='unânime' and not ledger[0]['vencidos'] and ledger[0]['data_fim_sessao']==rev['data_sessao'])
        quatro.append({'cnj':cnj,'resultado':'improcedente','votacao':'unânime','data_sessao':rev['data_sessao'],
                       'data_certidao':ref['data_assinatura'][:10],'data_assinatura_acordao':ac['data_assinatura'][:10],
                       'fontes':fontes,'julgamentos_ledger':len(ledger)})

    pacotes=[];mapa_membros={}
    for pacote in invent['lotes']:
        path=ROOT/pacote['arquivo'];blob=path.read_bytes()
        with zipfile.ZipFile(path) as z:
            membros=z.namelist()
        ok_hash=sha(blob)==pacote['sha256'];ok_tamanho=len(blob)==pacote['bytes'];ok_membros=len(membros)==pacote['membros']
        pacotes.append({'arquivo':pacote['arquivo'],'hash_ok':ok_hash,'tamanho_ok':ok_tamanho,'membros_ok':ok_membros,'membros':len(membros)})
        mapa_membros[pacote['arquivo']]=set(membros)
    conferir('Hashes, tamanhos e quantidades de membros dos 14 pacotes',len(pacotes)==14 and all(p['hash_ok'] and p['tamanho_ok'] and p['membros_ok'] for p in pacotes))
    conferir('Inventário declara 2.795 peças documentais',len(invent['documentos'])==invent['total_pecas']==2795)
    conferir('Todos os membros principais inventariados existem nos pacotes',all(d['membro'] in mapa_membros[d['pacote']] for d in invent['documentos']))
    # Confere os bytes arquivados das oito fontes novas, não apenas as cópias locais.
    for novo in quatro:
        for f in novo['fontes']:
            pub=docs_por_url[f['url']]
            with zipfile.ZipFile(ROOT/pub['pacote']) as z:blob=z.read(pub['membro'])
            conferir(f"Fonte arquivada reproduz hash de {novo['cnj']} ({f['papel']})",sha(blob)==f['sha256'])

    saida={'auditado_em':datetime.now(timezone.utc).isoformat(),'aprovado_nestas_verificacoes':not erros,
           'escopo':'Contagens integradas, exclusão das lacunas, espelho de coleta, fontes dos quatro novos comparáveis e pacotes de reprodução. Não substitui a curadoria de cada um dos 872 processos.',
           'totais':{'confrontos':len(cur),'comparaveis':len(incluidos),'relatos':len(relatos),'lacunas_documentais':len(lacunas),'consultas':len(checkpoint),'pecas_checkpoint':conferidas,'pecas_publicadas':len(invent['documentos'])},
           'campanhas':campanhas,'quatro_novos':quatro,'pacotes':pacotes,'verificacoes':checks,'falhas':erros,
           'ressalvas':['As 201 lacunas documentais permanecem excluídas dos percentuais; pendentes_de_revisao=0 não demonstra cobertura integral dos autos.',
                        'Nos quatro novos casos, a referência primária é a certidão assinada em outubro. Os acórdãos assinados em novembro documentam os fundamentos do julgamento anterior; não são novos acontecimentos dentro do corte.',
                        'As 2.787 peças do checkpoint e as 2.795 peças do inventário público têm universos distintos: o inventário inclui complementos e peças contextuais verificadas.',
                        'O espelho público omite intencionalmente apenas o campo doc.erro do diagnóstico operacional; os status e os demais metadados coincidem com o checkpoint.']}
    (ROOT/'relatorio_auditoria_final.json').write_text(json.dumps(saida,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    linhas=['# Auditoria final independente','',f"Resultado: {'APROVADO nas verificações abaixo' if not erros else 'REVISAR: há falhas'}. Auditoria: {saida['auditado_em']}.",'',
            f"Há {len(cur)} confrontos, {len(incluidos)} comparáveis e {len(relatos)} relatos, com os mesmos CNJs entre os incluídos. As {len(lacunas)} lacunas documentais ficam fora dos percentuais. O espelho da coleta contém {len(checkpoint)} processos consultados.",'',
            f"Lula: {campanhas['Lula']['atendidos']}/{campanhas['Lula']['pedidos']} pedidos atendidos ({campanhas['Lula']['percentual_atendimento']:.2f}%). Flávio: {campanhas['Flávio']['atendidos']}/{campanhas['Flávio']['pedidos']} ({campanhas['Flávio']['percentual_atendimento']:.2f}%).",'',
            '## Quatro novos comparáveis','',
            '| CNJ | Sessão | Certidão | Assinatura do acórdão | Resultado |','|---|---|---|---|---|']
    linhas.extend(f"| {r['cnj']} | {r['data_sessao']} | {r['data_certidao']} | {r['data_assinatura_acordao']} | Improcedente por unanimidade |" for r in quatro)
    linhas.extend(['','As certidões são as fontes primárias anteriores ao corte. Os acórdãos posteriores apenas documentam os fundamentos desses julgamentos. As duas fontes foram comparadas e correspondem a um único julgamento no ledger de cada CNJ.','',
                   '## Verificações',''])
    linhas.extend(f"- {'OK' if c['ok'] else 'FALHOU'} — {c['verificacao']}." for c in checks)
    linhas.extend(['','## Limites','']+[f'- {r}' for r in saida['ressalvas']]+[''])
    (ROOT/'relatorio_auditoria_final.md').write_text('\n'.join(linhas),encoding='utf-8')
    print(json.dumps({'aprovado':not erros,'verificacoes':len(checks),'falhas':erros,'totais':saida['totais']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
