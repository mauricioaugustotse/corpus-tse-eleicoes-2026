"""Confere polos em toda a base oficial, inclusive processos sem ato no recorte."""
import csv
import io
import json
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def normal(t):
    return ''.join(c for c in unicodedata.normalize('NFKD',t.upper()) if not unicodedata.combining(c))
def rows(stem):
    with zipfile.ZipFile(ROOT/'originais'/(stem+'.zip')) as z:
        with z.open(stem+'.csv') as f:
            yield from csv.DictReader(io.TextIOWrapper(f,encoding='latin1'),delimiter=';')
def campanha(t):
    t=normal(t);resultado=set()
    if any(x in t for x in ['LUIZ INACIO LULA DA SILVA','GERALDO JOSE RODRIGUES ALCKMIN FILHO','COLIGACAO BRASIL PRONTO PRA MAIS','FEDERACAO BRASIL DA ESPERANCA','PARTIDO DOS TRABALHADORES (PT) - NACIONAL']):resultado.add('Lula')
    if any(x in t for x in ['FLAVIO NANTES BOLSONARO','PARTIDO LIBERAL (PL) - NACIONAL']):resultado.add('Flávio')
    return resultado
def main():
    polos=defaultdict(lambda:defaultdict(list))
    for p in rows('processos_eleitorais_partes_2026'):
        if p['NR_INSTANCIA']=='3' and p['SG_UF_TRIBUNAL']=='DF' and p['TP_PARTE'] not in ['ADVOGADO','FISCAL DA LEI']:
            polos[p['NR_PROCESSO']][normal(p['DS_POLO'])].append(p['NM_PARTE'])
    coletados=json.loads((ROOT/'coleta_documental/checkpoint.json').read_text(encoding='utf-8'))
    novos=[];todos=[];total=0
    for p in rows('processo_eleitoral_2026'):
        if p['NR_INSTANCIA']!='3' or p['SG_UF_TRIBUNAL']!='DF':continue
        total+=1;pp=polos[p['NR_PROCESSO']]
        a=campanha(' | '.join(pp['POLO ATIVO']));b=campanha(' | '.join(pp['POLO PASSIVO']))
        if ('Lula' in a and 'Flávio' in b) or ('Flávio' in a and 'Lula' in b):
            todos.append(p['NR_PROCESSO'])
            if p['NR_PROCESSO'] not in coletados:
                novos.append({'cnj':p['NR_PROCESSO'],'classe':p['SG_CLASSE'],'autuacao':p['DT_AUTUACAO'],'ultima':p['DT_ULTIMA_DECISAO'],'tipo':p['TP_ULTIMA_DECISAO'],'ativo':pp['POLO ATIVO'],'passivo':pp['POLO PASSIVO']})
    rel={'total_processos_base':total,'total_confrontos_detectados':len(todos),'todos_confrontos_detectados':todos,'sem_coleta':novos,'nota':'Detecção por nomes formais do dicionário; não equivale a resultado comparável nem presume atos anteriores ao corte.'}
    (ROOT/'triagem_base_integral.json').write_text(json.dumps(rel,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'total_base':total,'confrontos':len(todos),'sem_coleta':len(novos),'amostra':novos[:8]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
