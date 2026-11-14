"""Monta proposta editorial local com as lacunas explícitas; não escreve no Notion."""
import csv
import html
import json
import re
from collections import Counter
from pathlib import Path
from gerar_config_graficos_juridicos import categoria

ROOT=Path(__file__).resolve().parent
def ler(nome):return json.loads((ROOT/nome).read_text(encoding='utf-8'))
def n(v):return f'{v:,}'.replace(',','.')
def pct(v,t):return f'{100*v/t:.1f}'.replace('.',',')+'%'
def link(cnj):return f'[{cnj[:10]}](https://consultaunificadapje.tse.jus.br/#/public/resultado/{cnj})'
def tabela(headers,rows):
    def celula(v):return '<td>\n'+str(v)+'\n</td>'
    return '<table fit-page-width="true" header-row="true">\n'+''.join('<tr>\n'+''.join(celula(v) for v in row)+'\n</tr>\n' for row in [headers,*rows])+'</table>'
def main():
    referencia=(ROOT/'pagina_referencia_notion.md').read_text(encoding='utf-8')
    texto=referencia.split('<content>\n',1)[1].rsplit('</content>',1)[0].rstrip('\n')
    texto_original=texto
    secao7=texto[re.search(r'^## 7\.',texto,re.M).start():]
    for a in ler('alteracoes_estatisticas.json')['alteracoes']:
        assert texto.count(a['old_str'])==1,a['old_str'][:60]
        texto=texto.replace(a['old_str'],a['new_str'])
    a=ler('apuracao_colegialidade.json');cg=a['corpus'];p=a['presidencial'];c=ler('campanha_resumo.json');cur=ler('curadoria_confrontos.json');q=c['incluidos_comparativos']
    situacoes=Counter()
    for k,v in p['situacao_confrontos'].items():situacoes[categoria(k)]+=v
    mant=situacoes['liminar mantida'];mod=situacoes['liminar modificada'];reex=mant+mod
    def par(inicio,novo):
        nonlocal texto
        ps=[p for p in texto.split('\n\n') if p.startswith(inicio)]
        assert len(ps)==1,(inicio,len(ps))
        texto=texto.replace(ps[0],novo,1)
    par('Um acórdão pode decidir',f'Um acórdão pode decidir uma etapa do processo ou apenas revisar uma liminar, sem encerrar o mérito. A leitura das peças oficiais permitiu identificar, nos <b>{n(cg["total"])} registros de acórdão</b>, <b>{n(cg["votacao"]["unânime"])} julgamentos unânimes ({pct(cg["votacao"]["unânime"],cg["total"])})</b> e <b>{n(cg["votacao"]["com divergência"])} com divergência ({pct(cg["votacao"]["com divergência"],cg["total"])})</b>; <b>1 registro ({pct(1,cg["total"])})</b> permanece sem votação conciliada com segurança. A lacuna é o ato de 14/07 do processo 0601104-61: há resolução e certidão, mas o vínculo com o registro de acórdão do extrato não foi suficientemente comprovado.')
    par('Nos confrontos judiciais relativos',f'Nos confrontos judiciais relativos à propaganda presidencial já documentados, o colegiado <b>manteve {mant} das {reex} liminares</b> cujo reexame está comprovado <b>({pct(mant,reex)})</b> e modificou <b>{mod} ({pct(mod,reex)})</b>. A atuação foi predominantemente confirmatória nesse subconjunto. O julgamento de mérito e os casos sem revisão comprovada ficam fora desse denominador. As [planilhas, peças e critérios de classificação](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/tree/atualizacao-corte-2026-10-31/versoes/2026-11-12) permitem conferir cada resultado.')
    nomes_situacoes={'sem revisão colegiada comprovada':'liminares sem revisão colegiada comprovada','liminar mantida':'liminares mantidas','liminar modificada':'liminares modificadas','decisão individual de mérito':'decisões individuais de mérito','decisão colegiada de mérito':'decisões colegiadas de mérito','liminar modificada individualmente':'liminar modificada individualmente','tutela decidida diretamente pelo colegiado':'tutelas decididas diretamente pelo colegiado'}
    distribuicao='; '.join(f'{n(v)} {nomes_situacoes.get(k,k)}' for k,v in situacoes.items() if v)
    par('Para examinar a situação das medidas',f'Para examinar a situação das medidas nos confrontos presidenciais, o gráfico seguinte organiza os <b>{q} processos com resultado documentado</b> pela etapa mais recente comparável: {distribuicao}. A ausência de revisão localizada não prova pendência processual. A classificação distingue o reexame cautelar do julgamento de mérito.')
    par('Quanto ao conjunto das liminares',f'Quanto às liminares reexaminadas pelo Plenário nesses confrontos, a <b>taxa de manutenção</b> considera os {reex} processos com reexame cautelar comprovado: {mant} medidas mantidas e {mod} modificadas.')
    nominal=next(x for x in texto.split('\n\n') if x.startswith('| Ministro | Corpus'))
    nomes=list(cg['ministros_vencidos']);nomes.sort(key=lambda k:-cg['ministros_vencidos'][k])
    novo='| Ministro | Corpus ('+str(cg['votacao']['com divergência'])+' acórdãos) | Confrontos ('+str(p['votacao'].get('com divergência',0))+' julgamentos) |\n| --- | --- | --- |\n'+'\n'.join(f'| {nome} | {cg["ministros_vencidos"].get(nome,0)} | {p["ministros_vencidos"].get(nome,0)} |' for nome in nomes)
    if nominal.rstrip().endswith('</toggle>'):novo+='\n</toggle>'
    texto=texto.replace(nominal,novo)
    par('<b>Situação dos 107 confrontos',f'<b>Situação dos {q} confrontos presidenciais documentados.</b> {distribuicao}. Pendência de referendo não se confunde com pendência do mérito. A consulta complementar ainda pode ampliar o conjunto, que não representa a totalidade de processos ajuizados.')
    vencidos='; '.join(f'{nome}: {v}' for nome,v in sorted(p['ministros_vencidos'].items(),key=lambda x:-x[1]))
    par('<b>Unanimidade e divergência',f'<b>Unanimidade e divergência nas disputas presidenciais.</b> Os {p["total"]} julgamentos colegiados documentados nos processos incluídos se dividem em {p["votacao"].get("unânime",0)} unânimes ({pct(p["votacao"].get("unânime",0),p["total"])}) e {p["votacao"].get("com divergência",0)} com divergência ({pct(p["votacao"].get("com divergência",0),p["total"]) }). As ocorrências de voto vencido nesse recorte são: {vencidos}. Conta-se uma ocorrência por ministro e julgamento, inclusive divergência parcial; vários ministros podem ficar vencidos no mesmo julgamento. Esses números são próprios dos confrontos presidenciais e se distinguem dos valores do corpus geral.')
    reformados=[x['cnj'] for x in p['casos'] if categoria(x['situacao'])=='liminar modificada']
    par('<b>Alcance das reformas',f'<b>Alcance das reformas de decisões liminares.</b> Foram documentadas modificações em {mod} processos: '+', '.join(link(x) for x in reformados)+'. A modificação pode ampliar ou reduzir a medida e não equivale, por si só, ao julgamento definitivo do processo. Referendo de tutela já parcialmente deferida é manutenção; referendo que efetivamente restringe ou amplia o dispositivo exige classificação própria, após a comparação das duas peças.')
    divergentes=[j for j in p['julgamentos'] if j['votacao']=='com divergência']
    linhas=[]
    for j in sorted(divergentes,key=lambda j:(j.get('data_fim_sessao') or j['data_metadata'],j['cnj']),reverse=True):
        data=j.get('data_fim_sessao') or j['data_metadata']
        linhas.append([link(j['cnj'])+' — '+data,html.escape(j['extrato'][:350])+('…' if len(j['extrato'])>350 else ''),', '.join(j['vencidos']),f'[(peça oficial)]({j["url"]})'])
    patron=r'(Julgamentos com divergência nos confrontos presidenciais[^\n]*\n\n)<table.*?</table>'
    texto,quant=re.subn(patron,lambda m:m[1]+tabela(['Processo e data do julgamento','Resultado proclamado (trecho)','Ministros vencidos','Fonte oficial'],linhas),texto,count=1,flags=re.S);assert quant==1
    inicio=texto.index('### 3.3');fim=texto.index('### 3.4');secao=texto[inicio:fim]
    rows=[['Decisão ou Acórdão no extrato oficial do TSE','Ato identificado no arquivo','2.606'],['Processos com ao menos um desses atos','CNJ único','1.841'],['Assunto Propaganda Eleitoral ou classe Direito de Resposta','CNJ único do corpus','1.005'],['Confrontos presidenciais com resultado comparável documentado','CNJ único, com exame documental',f'{q} ({c["processos_no_corpus"]} no corpus e {len(c["suplemento_documental"])} em suplemento)']]
    secao=re.sub(r'<table.*?</table>',lambda _:tabela(['Recorte','Unidade','Quantidade'],rows),secao,count=1,flags=re.S)
    texto=texto[:inicio]+secao+texto[fim:]
    par('O suplemento documental encontrado',f'O suplemento documental mantém o [processo 0601315-97](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000), sem ato no extrato selecionado. O inventário documental passou a conter acórdãos de suas etapas, que foram conciliados com as certidões sem criar linhas novas em atos.csv. Entre os {q} resultados comparáveis documentados, {c["processos_no_corpus"]} pertencem ao corpus estatístico e {len(c["suplemento_documental"])} ao suplemento. A inclusão documental não aumenta os 2.606 atos nem os 1.841 processos do painel geral.')
    inicio=texto.index('### 4.2');fim=texto.index('## 5.')
    titulo=texto[inicio:].split('\n',1)[0]
    corpo=[titulo,f'Como destacado nas seções anteriores, o quadro compara <b>{q} processos com resultado comparável documentado</b>, com representantes formais das campanhas presidenciais em polos opostos. Atendimento <b>parcial</b> conta como positivo. Casos sem resultado comparável ou sem documentação suficiente ficam fora dos percentuais.',f'<b>Casos em conferência.</b> A varredura de toda a base identificou {c["total_triagem"]} candidatos a confronto. Há {q} resultados comparáveis documentados, {c["excluidos_ou_pendentes"]-c["pendentes_de_revisao"]} exclusões fundamentadas e {c["pendentes_de_revisao"]} alvos em consulta ou revisão complementar. As pendências estão discriminadas em confrontos.csv e não recebem resultado por metadados. Estes totais descrevem a etapa atual da curadoria, que ainda pode ser ampliada.']
    linhas=[]
    for autor,v in c['campanhas'].items():linhas.append([autor+' e representantes formais',v['pedidos'],v['atendidos'],v['nao_atendidos'],pct(v['atendidos'],v['pedidos'])])
    corpo+=[tabela(['Campanha autora','Processos','Atendido, total ou parcialmente','Não atendido','Taxa de atendimento'],linhas),'A unidade é o processo, mesmo quando contém mais de uma decisão. As taxas descrevem apenas o conjunto documentado e não medem o resultado final da ação, a execução da medida, a correção de cada propaganda ou o êxito eleitoral das campanhas.']
    listas=[]
    for autor in ['Lula','Flávio']:
        for resultado in [True,False]:
            ids=sorted(k for k,v in cur.items() if v['incluir'] and v['campanha_autora']==autor and v['atendido'] is resultado)
            listas.append(f'- <b>{autor}, pedidos '+('atendidos' if resultado else 'não atendidos')+f' ({len(ids)}).</b> '+', '.join(link(x) for x in ids)+'.')
    categorias_excluidas=Counter(v['categoria'] for v in cur.values() if not v['incluir'])
    rotulos={'perda_objeto_sem_resultado':'perda de objeto sem resultado comparável','ilegitimidade_sem_resultado':'ilegitimidade sem resultado comparável','fora_confronto':'fora do confronto presidencial'}
    categorias_excluidas={rotulos.get(k,k):v for k,v in categorias_excluidas.items()}
    corpo+=['<toggle>\nProcessos incluídos — listas nominais por campanha e resultado\n\n'+'\n'.join(listas)+'\n</toggle>','<toggle>\nExclusões e pendências — motivos por processo\n\n'+tabela(['Categoria','Processos'],[[html.escape(k),v] for k,v in sorted(categorias_excluidas.items(),key=lambda x:-x[1])])+'\n\nA [planilha nominal de confrontos](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/blob/atualizacao-corte-2026-10-31/versoes/2026-11-12/confrontos.csv) identifica cada processo, o motivo, a fonte e o estágio. As pendências documentais não recebem resultado negativo.\n</toggle>']
    texto=texto[:inicio]+'\n\n'.join(corpo)+'\n\n'+texto[fim:]
    relatos=(ROOT/'relatos.md').read_text(encoding='utf-8')
    bloco=f'## 5. {q} confrontos presidenciais com resultado documentado\n\nOs relatos estão ordenados pela data da peça de referência, em ordem decrescente. Distinguem a medida comparada, os desdobramentos e o estágio até 31/10/2026. O conjunto ainda pode ser ampliado após a consulta complementar.\n\n'+relatos.rstrip()+'\n\n'
    texto,quant=re.subn(r'^## 5\..*?(?=^## 6\.)',lambda _:bloco,texto,count=1,flags=re.S|re.M);assert quant==1
    # Os anexos locais são referências do rascunho; a publicação usará uploads do Notion.
    texto=re.sub(r'notion-file-block://[^"\n]+&name=([^"\n]+)',lambda m:'graficos_interativos/'+('01_tipos_ato_restaurado_notion_agent_chart.png' if m[1].endswith('.png') else m[1]),texto)
    # Mantém acessíveis as fontes já citadas, inclusive quando o relato passou
    # a adotar uma peça posterior como referência principal.
    links_antigos={url:label for label,url in re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',texto_original)}
    faltantes={url:label for url,label in links_antigos.items() if url not in texto}
    por_url={};secao5=re.search(r'^## 5\..*?(?=^## 6\.)',texto_original,re.S|re.M)[0]
    historias=list(re.finditer(r'^### \d+\. ',secao5,re.M))
    for i,m in enumerate(historias):
        bloco=secao5[m.start():historias[i+1].start() if i+1<len(historias) else len(secao5)]
        cnj=re.search(r'\d{7}-\d{2}\.\d{4}\.6\.\d{2}\.\d{4}',bloco)
        if cnj:
            for url in re.findall(r'\]\((https?://[^)]+)\)',bloco):por_url[url]=cnj[0]
    grupos={}
    for url,label in faltantes.items():
        chave=por_url.get(url,'Demais referências')
        rotulo=re.sub(r'<[^>]+>|\*','',label).strip('() ') or 'peça oficial'
        grupos.setdefault(chave,[]).append(f'[({rotulo})]({url})')
    arquivo=''
    if grupos:
        arquivo='<toggle>\nPeças e referências citadas na versão de setembro\n\nEstas referências foram citadas na versão com corte em 30/09/2026. Os relatos acima trazem a classificação atualizada.\n\n'+tabela(['Processo','Referências preservadas'],[[link(k) if k!='Demais referências' else k,' '.join(v)] for k,v in sorted(grupos.items())])+'\n</toggle>'
        texto=texto.replace('## 6. Outros eixos em torno da disputa',arquivo+'\n\n## 6. Outros eixos em torno da disputa',1)
    destino=ROOT/'coleta_documental/publicacao';destino.mkdir(parents=True,exist_ok=True)
    (destino/'arquivo_fontes_historicas.json').write_text(json.dumps({'old_str':'## 6. Outros eixos em torno da disputa','new_str':arquivo+'\n\n## 6. Outros eixos em torno da disputa','links_preservados':len(faltantes)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert texto[re.search(r'^## 7\.',texto,re.M).start():]==secao7,'Seção 7 alterada'
    assert len(re.findall(r'^### \d+\. ',texto,re.M))==q,'Quantidade de relatos incorreta'
    assert len(re.findall(r'^## [1-7]\. ',texto,re.M))==7,'Seções principais duplicadas ou ausentes'
    assert texto.count('<embed ')==11 and texto.count('<image ')==1,'Anexos ausentes ou duplicados'
    pilha=[]
    for m in re.finditer(r'<(/?)(toggle|table|tr|td|th)\b[^>]*>',texto):
        if m[1]:
            assert pilha and pilha.pop()==m[2],f'Fechamento de bloco inválido: {m[0]}'
        elif not m[0].endswith('/>'):pilha.append(m[2])
    assert not pilha,f'Blocos sem fechamento: {pilha}'
    aviso='> Rascunho local em preparação. Consulta complementar e revisão editorial final pendentes; anexos ainda precisam ser enviados ao Notion.\n\n'
    if c.get('etapa_complementar_integrada'):
        lacunas=c.get('lacunas_documentais',c['pendentes_de_revisao'])
        par('Na comparação entre os confrontos', 'Na comparação entre os confrontos das campanhas presidenciais, os resultados registrados em <code>confrontos.csv</code> foram classificados após a leitura das peças indicadas. A consulta documental foi realizada de 12 a 14/11/2026, preservando o corte dos acontecimentos em 31/10. O arquivo estatístico do TSE não informa o resultado de cada pedido. Portanto, a classificação qualitativa depende da análise das peças, com as fontes, as datas e os limites explicitados na seção 5.')
        texto=texto.replace('A consulta complementar ainda pode ampliar o conjunto, que não representa a totalidade de processos ajuizados.','O conjunto contém somente resultados documentados e não representa todos os processos ajuizados ou todas as decisões eventualmente proferidas.')
        par('O suplemento documental mantém',f'O suplemento documental reúne {len(c["suplemento_documental"])} processos com resultado comparável e sem ato no extrato selecionado: '+', '.join(link(k) for k in c['suplemento_documental'])+f'. Entre os {q} resultados documentados, {c["processos_no_corpus"]} pertencem ao corpus estatístico e {len(c["suplemento_documental"])} ao suplemento. As fontes distinguem certidões emitidas até o corte de acórdãos assinados depois que documentam julgamentos anteriores. A inclusão documental não aumenta os 2.606 atos nem os 1.841 processos do painel geral.')
        par('<b>Casos em conferência.</b>',f'<b>Cobertura documental e lacunas.</b> A varredura dos polos da base integral identificou {c["total_triagem"]} candidatos a confronto. Há {q} resultados comparáveis documentados, {c["excluidos_ou_pendentes"]-lacunas} exclusões fundamentadas e {lacunas} processos sem documentação decisória elegível suficiente neste inventário. Todas as consultas foram efetuadas. A ausência de peça elegível não comprova inexistência de atos. Os motivos de exclusão e as lacunas aparecem nominalmente em confrontos.csv; nenhum desses processos recebe resultado por metadados. Um candidato autuado em 03/11 foi excluído pelo corte temporal.')
        texto=texto.replace('O conjunto ainda pode ser ampliado após a consulta complementar.','Casos sem resultado comparável documentado ficam fora destes relatos e dos percentuais.')
        aviso='> Proposta editorial conferida. Anexos locais serão substituídos pelos arquivos enviados ao Notion na publicação.\n\n'
    (ROOT/'pagina_proposta.md').write_text(aviso+texto+'\n',encoding='utf-8')
    (ROOT/'auditoria_rascunho.json').write_text(json.dumps({'status':'rascunho; não publicado','confrontos_relatados':q,'pendencias_consulta_revisao':c['pendentes_de_revisao'],'julgamentos_divergentes_na_tabela':len(divergentes),'secao7_identica':True,'anexos_interativos':texto.count('<embed '),'versoes_estaticas':texto.count('<image ')},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Proposta preparada: {q} relatos; seção 7 idêntica; referências gráficas locais prontas para envio.')
if __name__=='__main__':main()
