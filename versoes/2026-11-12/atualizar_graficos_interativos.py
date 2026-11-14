"""Atualiza dados nos modelos visuais preservados, sem trocar CSS/controles/runtime."""
import copy
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELOS = ROOT / 'modelos_graficos'
SAIDA = ROOT / 'graficos_interativos'

def carregar(nome):
    return json.loads((ROOT / nome).read_text(encoding='utf-8'))

def numero(value):
    return f'{value:,}'.replace(',', '.')

def percentual(value):
    return f'{value:.1f}'.replace('.', ',') + '%'

def localizar(texto):
    m = re.search(r'const (spec|panel) = (\{[^\n]+\})', texto)
    if not m: raise ValueError('Modelo sem especificação de dados')
    return m.group(1), json.loads(m.group(2))

def atualizar_modelo(texto, spec, titulo, nota):
    chave, _ = localizar(texto)
    texto = re.sub(r'const '+chave+r' = \{[^\n]+\}', lambda _: 'const '+chave+' = '+json.dumps(spec,ensure_ascii=False,separators=(',',':')), texto, count=1)
    texto = re.sub(r'(commonChartOptions\(options, )"[^\n]*?"(\);)', lambda m: m[1]+json.dumps(nota,ensure_ascii=False)+m[2], texto, count=1)
    texto = re.sub(r'(<div class="figure-title">).*?(</div>)',lambda m:m[1]+html.escape(titulo)+m[2],texto,count=1)
    texto = re.sub(r'(<div class="figure-aside">).*?(</div>)',lambda m:m[1]+html.escape(nota)+m[2],texto,count=1)
    labels=spec['labels']; series=spec['series']
    descricao='. '.join(s['label']+': '+ '; '.join(f'{l}: {s["data"][i]:.2f}'+('%' if s['valueKind']=='percent' else '') for i,l in enumerate(labels)) for s in series)
    texto=re.sub(r'(<p class="sr-only">).*?(</p>)',lambda m:m[1]+html.escape(descricao)+m[2],texto,count=1)
    texto=re.sub(r'(<canvas\b[^>]*aria-label=")[^"]*("[^>]*>).*?(</canvas>)',lambda m:m[1]+html.escape(titulo+'. '+nota+'. '+descricao,quote=True)+m[2]+html.escape(descricao)+m[3],texto,count=1,flags=re.S)
    tabela='<table class="sr-only">\n<caption>'+html.escape(titulo)+'</caption>\n<tr><th>Observação</th>'+''.join('<th>'+html.escape(s['label'])+'</th>' for s in series)+'</tr>\n'
    for i,label in enumerate(labels):
        tabela+='<tr><td>'+html.escape(label)+'</td>'
        for s in series:
            v=s['data'][i]; display=f'{v:.2f}%' if s['valueKind']=='percent' else numero(v)
            tabela+=f'<td data-observation-key="{html.escape(label,quote=True)}" data-series-key="{html.escape(s["label"],quote=True)}" data-raw-value="{v}" data-value-kind="{s["valueKind"]}">{display}</td>'
        tabela+='</tr>\n'
    tabela+='</table>'
    texto=re.sub(r'<table class="sr-only">.*?</table>',lambda _:tabela,texto,count=1,flags=re.S)
    # Recria somente a legenda quando as categorias mudam; conserva os controles.
    m=re.search(r'<div class="legend" data-chart-id="([^"]+)">.*?</div>',texto,re.S)
    if m:
        linha='key-line' in m[0]; entries=[]
        for i,s in enumerate(series):
            color=s.get('color') or f'var({s["colorToken"]})'
            style=('border-top-color' if linha else 'background')+': '+color
            entries.append(f'<span data-series-index="{i}"><span class="'+('key-line' if linha else 'key-sq')+f'" aria-hidden="true" style="{style}"></span>{html.escape(s["label"])}</span>')
        legenda='<div class="legend" data-chart-id="'+m[1]+'">\n'+'\n'.join(entries)+'\n</div>'
        texto=texto[:m.start()]+legenda+texto[m.end():]
    return texto

def configuracoes():
    r=carregar('resumo.json');total=r['total_atos'];processos=r['total_processos']; configs={}
    def modelo(prefixo):
        p=next(MODELOS.glob(prefixo+'*.html'))
        return p,localizar(p.read_text(encoding='utf-8'))[1]
    def guardar(p,s,t,n):configs[p.name]={'spec':s,'titulo':t,'nota':n}
    p,s=modelo('01_');s['labels']=s['tickLabels']=[f'{numero(total)} atos']
    for serie in s['series']:serie['data']=[100*r['atos_por_tipo'][serie['label']]/total]
    guardar(p,s,'Decisões representam '+percentual(100*r['atos_por_tipo']['Decisão']/total)+' dos atos',f"{numero(r['atos_por_tipo']['Decisão'])} decisões e {numero(r['atos_por_tipo']['Acórdão'])} acórdãos até 31/10/2026")
    meses=list(r['atos_por_mes']); nomes=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']; abrevs=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']
    for prefixo in ['02_','03_']:
        p,s=modelo(prefixo);s['labels']=[nomes[int(m[5:])-1].capitalize()+' de '+m[:4] for m in meses];s['tickLabels']=[abrevs[int(m[5:])-1]+'/'+m[2:4] for m in meses]
        for serie in s['series']:
            serie['data']=[r['atos_acumulados_por_mes'][m] if prefixo=='03_' else r['atos_por_mes_tipo'][m][serie['label']] for m in meses]
        if prefixo=='02_':guardar(p,s,'O volume mensal se concentra em outubro',f"Outubro reúne {numero(r['atos_por_mes']['2026-10'])} dos {numero(total)} atos ({percentual(100*r['atos_por_mes']['2026-10']/total)})")
        else:guardar(p,s,f'Os registros alcançam {numero(total)} atos no corte','Acumulado mensal de outubro/2025 a outubro/2026')
    p,s=modelo('04_'); nomes_classes={'Rp':'Representação (Rp)','DR':'Direito de Resposta (DR)','REspEl':'Recurso Especial Eleitoral (REspEl)','RO-El':'Recurso Ordinário Eleitoral (RO-El)','PetCiv':'Petição Cível (PetCiv)'}
    classes=sorted(r['atos_por_classe'],key=lambda k:(-r['atos_por_classe'][k],k))[:5]
    s['labels']=[nomes_classes.get(k,k) for k in classes];s['tickLabels']=classes;s['series'][0]['data']=[r['atos_por_classe'][k] for k in classes]
    guardar(p,s,'As cinco classes com mais atos',f"Cinco classes: {numero(sum(s['series'][0]['data']))} de {numero(total)} atos ({percentual(100*sum(s['series'][0]['data'])/total)})")
    p,s=modelo('05_');autores=sorted(r['atos_por_autor'],key=lambda k:(-r['atos_por_autor'][k],k))[:6]
    s['labels']=autores;s['tickLabels']=[k.title().replace(' De ',' de ').replace(' Da ',' da ').replace('Bôas','Bôas') for k in autores];s['series'][0]['data']=[r['atos_por_autor'][k] for k in autores]
    guardar(p,s,'Os seis autores com mais atos',f"Seis autores: {numero(sum(s['series'][0]['data']))} de {numero(total)} atos ({percentual(100*sum(s['series'][0]['data'])/total)})")
    p,s=modelo('06_');s['labels']=s['tickLabels']=[f'{numero(processos)} processos'];original=s['series'];ambos=copy.deepcopy(original[0]);ambos.update(label='Propaganda e DR',colorToken='--green',colorFallback='#72bc8f')
    s['series']=[original[0],original[1],ambos,original[2]]
    for serie,(label,key) in zip(s['series'],[('Propaganda, sem DR','Propaganda, sem DR'),('DR, sem propaganda','DR, sem propaganda'),('Propaganda e DR','Propaganda e DR'),('Demais assuntos','Demais assuntos')]):
        serie['label']=label;serie['data']=[100*r['processos_por_grupo_comunicacao'][key]/processos]
    guardar(p,s,'Propaganda e direito de resposta no conjunto de processos',f"{numero(r['total_processos_comunicacao'])} de {numero(processos)} processos até 31/10/2026; 8 pertencem aos dois grupos")
    # As cinco figuras jurídicas só são geradas quando a revisão fornecer as entradas.
    arquivo=ROOT/'config_graficos_juridicos.json'
    if arquivo.exists():configs.update(carregar(arquivo.name))
    return configs

def main():
    SAIDA.mkdir(exist_ok=True);config=configuracoes()
    for nome,c in config.items():
        texto=(MODELOS/nome).read_text(encoding='utf-8')
        (SAIDA/nome).write_text(atualizar_modelo(texto,c['spec'],c['titulo'],c['nota']),encoding='utf-8',newline='\n')
    (SAIDA/'dados_graficos.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(config)} gráficos atualizados com os modelos visuais preservados.')

if __name__=='__main__':main()
