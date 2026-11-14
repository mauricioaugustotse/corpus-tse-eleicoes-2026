"""Prepara substituições pontuais verificáveis; não publica o rascunho no Notion."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def n(v):return f'{v:,}'.replace(',','.')
def pct(v,d):return f'{100*v/d:.1f}'.replace('.',',')+'%'
def main():
    fonte=ROOT/'pagina_referencia_notion.md'
    original=fonte.read_text(encoding='utf-8');r=json.loads((ROOT/'resumo.json').read_text(encoding='utf-8'))
    with (ROOT/'atos.csv').open(encoding='utf-8-sig') as f:atos=list(csv.DictReader(f,delimiter=';'))
    with (ROOT/'processos.csv').open(encoding='utf-8-sig') as f:processos=list(csv.DictReader(f,delimiter=';'))
    alteracoes=[]
    def par(inicio,novo):
        candidatos=[p for p in original.split('\n\n') if p.startswith(inicio)]
        if inicio=='A base de dados reúne':candidatos=[p for p in candidatos if '933 atos' in p]
        if len(candidatos)!=1:raise ValueError((inicio,len(candidatos)))
        alteracoes.append({'old_str':candidatos[0],'new_str':novo})
    total=r['total_atos'];np=r['total_processos']
    par('A base de dados reúne',f'A base de dados reúne <b>{n(total)} atos em {n(np)} processos distintos</b>, entre <date start="2025-10-03" end="2026-10-31" />. Um processo pode ter mais de um ato. Por isso, os {n(total)} contam registros classificados como Decisão ou Acórdão, enquanto os {n(np)} contam processos apenas pelo número único do CNJ. Nenhuma dessas contagens indica, por si só, que o processo terminou ou teve julgamento de mérito.')
    par('Na base de dados, <b>',f'Na base de dados, <b>{n(r["atos_por_tipo"]["Decisão"])} atos aparecem como Decisão ({pct(r["atos_por_tipo"]["Decisão"],total)})</b> e <b>{n(r["atos_por_tipo"]["Acórdão"])} como Acórdão ({pct(r["atos_por_tipo"]["Acórdão"],total)})</b>. Para saber o que foi decidido em cada caso, é preciso ler a peça. O nome do ato não mostra se houve liminar, providência processual simples (despacho) ou julgamento de mérito, o que será analisado com enfoque específico na seção 5.')
    par('<b>Setembro de 2026 teve',f'<b>Outubro de 2026 teve o maior volume</b>, com {n(r["atos_por_mes"]["2026-10"])} atos, ou {pct(r["atos_por_mes"]["2026-10"],total)} do <i>corpus empiricus</i> desta pesquisa. Os gráficos usam a data registrada no sistema oficial.')
    par('A curva abaixo mostra','A curva abaixo mostra o crescimento dos registros até a data de corte em 31 de outubro de 2026.')
    par('As classes processuais registradas',f'As classes processuais registradas nos <b>{n(total)} atos</b> se distribuem assim.')
    classes=sorted(r['atos_por_classe'],key=lambda k:-r['atos_por_classe'][k]);top=classes[:5]
    bloco=next(p for p in original.split('\n\n') if p.startswith('- <b>Rp</b>'))
    novo='\n'.join(f'- <b>{k}</b> — {n(r["atos_por_classe"][k])} atos ({pct(r["atos_por_classe"][k],total)}).' for k in top)
    outros=total-sum(r['atos_por_classe'][k] for k in top)
    novo+=f'\n- <b>Demais classes</b> — {n(outros)} atos ({pct(outros,total)}).'
    alteracoes.append({'old_str':bloco,'new_str':novo})
    tabela=next(p for p in original.split('\n\n') if p.startswith('| Classe ou grupo de classes'))
    linhas=['| Classe ou grupo de classes | Atos |','| --- | --- |']+[f'| {k} | {n(r["atos_por_classe"][k])} |' for k in classes[:8]]+[f'| Demais classes (fora das oito discriminadas) | {n(total-sum(r["atos_por_classe"][k] for k in classes[:8]))} |',f'| <b>Total</b> | <b>{n(total)}</b> |']
    alteracoes.append({'old_str':tabela,'new_str':'\n'.join(linhas)})
    autores=sorted(r['atos_por_autor'],key=lambda k:-r['atos_por_autor'][k]);top3=sum(r['atos_por_autor'][k] for k in autores[:3])
    par('O gráfico abaixo mostra o <b>ministro autor',f'O gráfico abaixo mostra o <b>ministro autor de cada ato</b>, conforme a base de dados do TSE. Esse nome pode ser diferente do relator atual do processo. Nunes Marques ({n(r["atos_por_autor"]["NUNES MARQUES"])}), André Mendonça ({n(r["atos_por_autor"]["ANDRÉ MENDONÇA"])}) e Estela Aranha ({n(r["atos_por_autor"]["ESTELA ARANHA"])}) assinam, juntos, {n(top3)} atos (ou {pct(top3,total)}) no período avaliado.')
    tabela=next(p for p in original.split('\n\n') if p.startswith('| Autor do ato'))
    linhas=['| Autor do ato | Atos |','| --- | --- |']+[f'| {k.title().replace(" De "," de ").replace(" Da "," da ")} | {n(r["atos_por_autor"][k])} |' for k in autores]+[f'| <b>Total</b> | <b>{n(total)}</b> |']
    alteracoes.append({'old_str':tabela,'new_str':'\n'.join(linhas)})
    par('Os registros foram obtidos no conjunto', 'Os registros foram obtidos no conjunto [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026), formado a partir de dados do Portal de Dados Abertos da Justiça Eleitoral. Esta versão utiliza os cinco arquivos oficiais gerados em <b>11/11/2026</b>, extraídos em <b>12/11/2026</b>, preservados com suas datas e seus <i>hashes</i> — códigos digitais que permitem conferir a integridade dos arquivos. A [versão histórica de 1º/10/2026](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/tree/v2026-10-01-corte-2026-09-30/versoes/2026-10-01) mantém os dados anteriores. O novo pacote conserva o corte em 31/10/2026, embora a fonte contenha atos até 10/11; a data da extração não se confunde com a data de corte.')
    par('O período dos atos selecionados', 'O período dos atos selecionados vai de <b>03/10/2025 a 31/10/2026</b>, inclusive. A última data encontrada no arquivo oficial é 10/11/2026; os atos posteriores ao corte foram excluídos. O ano da eleição indica o pleito a que o processo se refere. Ele não precisa coincidir com o ano do processo nem com o do julgamento. Por isso, a base inclui <b>3 atos de 2025</b>, e o recorte começa antes do início formal da campanha.')
    par('Essa possibilidade de conferência não elimina', 'Essa possibilidade de conferência não elimina os limites da fonte. O TSE pode atualizar os arquivos e alguns resultados anunciados em sessão ainda não aparecem no extrato. Os totais descrevem, assim, a extração de <b>12/11/2026</b>, formada por arquivos gerados em <b>11/11/2026</b>, com atos judiciais datados até <b>31/10/2026</b>. A nova extração também revisou registros anteriores: há 937 atos até setembro, contra 933 na versão histórica; as duas extrações não foram concatenadas.')
    propaganda=sum(p['FL_PROPAGANDA_OFICIAL']=='1' for p in processos);dr=sum(p['FL_DIREITO_RESPOSTA']=='1' for p in processos);comatos=sum(a['FL_RECORTE_COMUNICACAO']=='1' for a in atos)
    par('No cadastro, o <b>assunto</b>',f'No cadastro, o <b>assunto</b> indica o tema e a <b>classe</b> identifica o tipo de processo. O gráfico reúne <b>{n(propaganda)} processos</b> cujo assunto menciona <b>Propaganda Eleitoral</b> e <b>{n(dr)}</b> da classe <b>Direito de Resposta</b>. Há <b>8 processos em ambos os grupos</b>: são {n(propaganda-8)} apenas de propaganda e {n(dr-8)} apenas de direito de resposta. A união, sem dupla contagem, soma <b>{n(r["total_processos_comunicacao"])} processos e {n(comatos)} atos.</b>')
    par('<b>Registros de candidatura.</b>', '<b>Registros de candidatura.</b> O corpus tem <b>60 atos em 41 processos da classe RCand</b>. Os recursos sobre registros têm classes próprias e também ajudam a compreender esse eixo. No caso de José Roberto Arruda, o TSE, por maioria, manteve o indeferimento do registro de candidatura ao governo do Distrito Federal em razão das condenações por improbidade. O mesmo julgamento afastou, por unanimidade, multa aplicada a outro recorrente. Floriano de Azevedo Marques e Estela Aranha ficaram vencidos em parte. A decisão foi proferida em 24/09 e aparece no extrato como ato de 13/10; essas datas não designam dois julgamentos [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/10/13/18/41/51/b51fc76dd4088d63cd0793a0825370cf51c5dcaabf034d52a433b7830ec51131).')
    par('A base de dados reúne <b>92 atos',next(p for p in original.split('\n\n') if p.startswith('A base de dados reúne <b>92 atos')).replace('<b>92 atos em 82 petições cíveis</b>','<b>126 atos em 107 petições cíveis</b>'))
    par('O corpus tem <b>53 atos',next(p for p in original.split('\n\n') if p.startswith('O corpus tem <b>53 atos')).replace('<b>53 atos em 38 processos','<b>67 atos em 48 processos'))
    for a in alteracoes:
        assert original.count(a['old_str'])==1,a['old_str'][:60]
    (ROOT/'alteracoes_estatisticas.json').write_text(json.dumps({'status':'preparado; aguarda integração da curadoria e das fontes gráficas para publicação conjunta','alteracoes':alteracoes,'secao7_preservar':'## 7. Conclusão / outros tópicos (texto livre)\n\nBruno'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(alteracoes)} substituições editoriais preparadas; comunicação: {comatos} atos.')
if __name__=='__main__':main()
