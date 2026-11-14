"""Reproduz tabelas e relatos da curadoria explícita; não infere resultados do texto."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from triagem_base_integral import rows, normal, campanha

ROOT=Path(__file__).resolve().parent
def ler(nome):
    return json.loads((ROOT/nome).read_text(encoding='utf-8'))
def ler_csv(nome):
    with (ROOT/nome).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f,delimiter=';'))
def gravar_csv(nome, dados, campos=None):
    with (ROOT/nome).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=campos or list(dados[0]),delimiter=';',lineterminator='\n')
        w.writeheader();w.writerows(dados)
def main():
    curadoria=ler('curadoria_confrontos.json');resumo=ler('resumo.json');corte=resumo['fim_decisao']
    processos={r['NR_PROCESSO']:r for r in rows('processo_eleitoral_2026') if r['NR_INSTANCIA']=='3' and r['SG_UF_TRIBUNAL']=='DF'}
    polos=defaultdict(lambda:defaultdict(list));assuntos=defaultdict(set)
    for r in rows('processos_eleitorais_partes_2026'):
        if r['NR_INSTANCIA']=='3' and r['SG_UF_TRIBUNAL']=='DF' and r['TP_PARTE'] not in ['ADVOGADO','FISCAL DA LEI']:
            polos[r['NR_PROCESSO']][normal(r['DS_POLO'])].append(r['NM_PARTE'])
    for r in rows('processos_eleitorais_assuntos_2026'):
        if r['NR_INSTANCIA']=='3' and r['SG_UF_TRIBUNAL']=='DF':assuntos[r['NR_PROCESSO']].add(r['DS_ASSUNTO'])
    atos=defaultdict(list)
    for a in ler_csv('atos.csv'):atos[a['NR_PROCESSO']].append(a)
    registros=[];relatos=[]
    for cnj,s in sorted(curadoria.items()):
        assert cnj in processos,cnj
        p=processos[cnj];ativo=polos[cnj]['POLO ATIVO'];passivo=polos[cnj]['POLO PASSIVO'];ca=campanha(' | '.join(ativo));cp=campanha(' | '.join(passivo))
        assert (('Lula' in ca and 'Flávio' in cp) or ('Flávio' in ca and 'Lula' in cp)),cnj
        incluir=s['incluir'];atendido=s.get('atendido');data=s.get('data_ato_referencia','')
        assert not data or data<=corte,(cnj,data)
        if incluir:
            assert isinstance(atendido,bool),(cnj,'resultado não documentado')
            assert s.get('url_peca') and data,(cnj,'fonte ou data ausente')
        else:assert atendido is None,(cnj,'excluído com resultado binário')
        ultimo=max(atos[cnj],key=lambda a:a['DT_DECISAO_ISO']) if atos[cnj] else {}
        registro={'cnj':cnj,'incluir_comparativo':'sim' if incluir else 'não','motivo_inclusao_exclusao':s['motivo'],'categoria_triagem':s['categoria'],'campanha_autora':s['campanha_autora'],'polo_ativo_formal':' | '.join(ativo),'polo_passivo_formal':' | '.join(passivo),'classe_pje':p['SG_CLASSE'],'assunto_principal_pje':p['DS_ASSUNTO_PRINCIPAL'],'assuntos_pje':' | '.join(sorted(assuntos[cnj])),'objeto_comunicacao':s.get('objeto',''),'pedido_principal_codificado':s.get('pedido',''),'desfecho_medida':('atendido' if atendido else 'não atendido') if incluir else 'sem resultado comparável','atendido':('sim' if atendido else 'não') if incluir else '','grau_atendimento':s.get('grau',''),'status_procedimental':s.get('status',''),'data_ultima_decisao_pje':ultimo.get('DT_DECISAO_ISO',''),'tipo_ultima_decisao_pje':ultimo.get('DS_TIPO_DECISAO',''),'qtd_atos_bulk':len(atos[cnj]),'data_ato_referencia':data,'url_peca_oficial':s.get('url_peca',''),'tipo_peca_oficial':s.get('tipo_peca',''),'status_fonte':s.get('status_fonte',''),'url_andamento':p['DS_URL_PROCESSO'],'sinopse_curatorial':s.get('sinopse',''),'geracao_bulk':resumo['geracao_oficial'],'fonte_classificacao':s.get('fonte_classificacao',''),'grau_certeza_triagem':s.get('grau_certeza','')}
        registros.append(registro)
        if incluir:
            relato=s.get('relato',{})
            # A sinopse revista é a fonte da nova narrativa; texto antigo requer revisão.
            texto=relato.get('texto') if relato and not relato.get('requer_atualizacao') else None
            if not texto:
                texto=f"Em [**{cnj}**]({p['DS_URL_PROCESSO']}), {s['sinopse']} Fonte — [({s.get('tipo_peca','peça oficial').lower()})]({s['url_peca']})."
            relatos.append({'numero':0,'cnj':cnj,'titulo':s.get('objeto') or relato.get('titulo') or cnj,'texto':texto,'data_ato_referencia':data})
    relatos.sort(key=lambda r:(r['data_ato_referencia'],r['cnj']),reverse=True)
    for i,r in enumerate(relatos,1):r['numero']=i
    assert {r['cnj'] for r in relatos}=={r['cnj'] for r in registros if r['incluir_comparativo']=='sim'}
    gravar_csv('confrontos.csv',registros);gravar_csv('relatos.csv',relatos,campos=['numero','cnj','titulo','texto','data_ato_referencia'])
    selecionados=[r for r in registros if r['incluir_comparativo']=='sim'];counts=Counter((r['campanha_autora'],r['atendido']) for r in selecionados)
    resumo_c={'data_corte':corte,'status':'resultados documentados; quadro em ampliação pela consulta complementar','total_triagem':len(registros),'incluidos_comparativos':len(selecionados),'excluidos_ou_pendentes':len(registros)-len(selecionados),'pendentes_de_revisao':sum(s.get('revisao',{}).get('pronto_publicacao') is False for s in curadoria.values()),'processos_no_corpus':sum(bool(atos[r['cnj']]) for r in selecionados),'suplemento_documental':[r['cnj'] for r in selecionados if not atos[r['cnj']]],'campanhas':{}}
    for autor in ['Lula','Flávio']:
        total=sum(counts[autor,x] for x in ['sim','não']);pos=counts[autor,'sim']
        resumo_c['campanhas'][autor]={'pedidos':total,'atendidos':pos,'nao_atendidos':counts[autor,'não'],'percentual_atendimento':100*pos/total if total else None}
    (ROOT/'campanha_resumo.json').write_text(json.dumps(resumo_c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'relatos.md').write_text('\n\n'.join(f"### {r['numero']}. {r['titulo']}\n\n{r['texto']}" for r in relatos)+'\n',encoding='utf-8')
    print(json.dumps(resumo_c,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
