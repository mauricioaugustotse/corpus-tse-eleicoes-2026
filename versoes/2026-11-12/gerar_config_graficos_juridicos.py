"""Prepara as cinco figuras jurídicas nos modelos visuais do Notion.

Execute depois da fusão da curadoria e de apurar_colegialidade.py. Não aceita
registros explicitamente marcados como não prontos para publicação.
"""
import argparse
import copy
import json
import math
from pathlib import Path

from atualizar_graficos_interativos import localizar

ROOT=Path(__file__).resolve().parent

def numero(n):return f'{n:,}'.replace(',', '.')

def categoria(s):
    aliases={
        'mantida':'liminar mantida', 'modificada':'liminar modificada',
        'sem revisão comprovada':'sem revisão colegiada comprovada',
        'liminar sem revisão colegiada comprovada':'sem revisão colegiada comprovada',
        'mérito individual':'decisão individual de mérito',
        'mérito colegiado':'decisão colegiada de mérito',
        'tutela colegiada direta':'tutela decidida diretamente pelo colegiado',
        'modificada individualmente':'liminar modificada individualmente',
    }
    return aliases.get(s,s)

def construir(root, resumo, curadoria):
    presid=resumo.get('presidencial')
    if not presid:raise ValueError('Apuração presidencial ausente. Gere a curadoria final e execute apurar_colegialidade.py novamente.')
    pendentes=[]
    for cnj,r in curadoria.items():
        if not r.get('incluir'):continue
        revisao=r.get('revisao',{})
        if revisao.get('pronto_publicacao') is False or revisao.get('utilizar_em_percentuais_finais') is False:
            pendentes.append(cnj)
    if pendentes:raise ValueError(f'{len(pendentes)} registros da curadoria ainda não estão prontos para publicação; configuração não gerada.')
    n=sum(bool(r.get('incluir')) for r in curadoria.values())
    if n!=presid['processos_comparaveis']:raise ValueError('Curadoria e apuração presidencial divergem. Reexecute o apurador.')
    corpus=resumo['corpus']; configs={}
    def modelo(prefixo):
        arquivos=list((root/'modelos_graficos').glob(prefixo+'*.html'))
        if len(arquivos)!=1:raise ValueError(f'Modelo único não localizado: {prefixo}')
        p=arquivos[0]
        return p,copy.deepcopy(localizar(p.read_text(encoding='utf-8'))[1])
    def guardar(p,s,titulo,nota):configs[p.name]={'spec':s,'titulo':titulo,'nota':nota}

    p,s=modelo('07a_'); universos=[corpus,presid]
    s['labels']=s['tickLabels']=[f"Corpus ({numero(corpus['total'])})",f"Confrontos presidenciais ({numero(presid['total'])})"]
    s['axis']['cap']=100
    for serie,key in zip(s['series'],['unânime','com divergência','não apurada']):
        serie['data']=[100*u['votacao'].get(key,0)/u['total'] if u['total'] else 0 for u in universos]
    guardar(p,s,'Votação nos acórdãos do corpus e nos confrontos presidenciais',
            f"{numero(corpus['total'])} registros de acórdão e {numero(presid['total'])} julgamentos dos confrontos até 31/10/2026; votação não apurada permanece no denominador")

    contagens={}
    for key,v in presid['situacao_confrontos'].items():
        key=categoria(key);contagens[key]=contagens.get(key,0)+v
    if sum(contagens.values())!=n:raise ValueError('Situações das medidas não fecham o denominador de processos.')
    p,s=modelo('08a_'); s['labels']=s['tickLabels']=[f'{numero(n)} processos'];s['axis'].pop('cap',None)
    originais=copy.deepcopy(s['series'])
    categorias=[
        ('sem revisão colegiada comprovada','Sem revisão comprovada',originais[0]),
        ('liminar mantida','Liminar mantida',originais[1]),
        ('liminar modificada','Liminar modificada',originais[2]),
        ('decisão individual de mérito','Decisão individual de mérito',originais[3]),
        ('tutela decidida diretamente pelo colegiado','Tutela colegiada direta',originais[4]),
    ]
    merito=copy.deepcopy(originais[3]);merito.update(color='rgba(114, 188, 143, 1)',colorToken='--green',colorFallback='#72bc8f')
    individual=copy.deepcopy(originais[4])
    neutro=copy.deepcopy(originais[0]);neutro.update(color='rgba(112, 112, 112, 1)')
    categorias.extend([
        ('decisão colegiada de mérito','Decisão colegiada de mérito',merito),
        ('liminar modificada individualmente','Liminar modificada individualmente',individual),
    ])
    conhecidas={x[0] for x in categorias};pendente=sum(v for key,v in contagens.items() if key not in conhecidas)
    series=[]
    for key,label,serie in categorias:
        if contagens.get(key,0) or key in {'sem revisão colegiada comprovada','liminar mantida','liminar modificada'}:
            serie.update(label=label,data=[contagens.get(key,0)]);series.append(serie)
    if pendente:
        neutro.update(label='Situação pendente de revisão',data=[pendente]);series.append(neutro)
    s['series']=series
    guardar(p,s,'Situação documentada das medidas nos confrontos presidenciais',
            f"Um registro por processo até 31/10/2026; {numero(pendente)} com situação pendente de revisão. Ausência de revisão localizada não prova pendência processual")

    mantidas=contagens.get('liminar mantida',0);modificadas=contagens.get('liminar modificada',0);reexames=mantidas+modificadas
    p,s=modelo('08b_');s['labels']=s['tickLabels']=[f'{numero(reexames)} reexames documentados'];s['axis']['cap']=100
    for serie,v in zip(s['series'],[mantidas,modificadas]):serie['data']=[100*v/reexames if reexames else 0]
    guardar(p,s,'Manutenção e modificação das liminares pelo colegiado',
            f"{numero(mantidas)} manutenções e {numero(modificadas)} modificações; denominador de {numero(reexames)} processos com reexame cautelar comprovado. Mérito e pendências ficam fora dessa taxa")

    for prefixo,u,qual in [('09a_',corpus,'corpus'),('09b_',presid,'confrontos presidenciais')]:
        p,s=modelo(prefixo)
        nomes=list(s['labels'])
        for nome in ['Sebastião Reis Júnior',*u['ministros_vencidos']]:
            if nome not in nomes:nomes.append(nome)
        valores=[u['ministros_vencidos'].get(nome,0) for nome in nomes]
        s['labels']=s['tickLabels']=nomes;s['series'][0]['data']=valores
        limite=max(5,max(valores or [0])*1.1)
        magnitude=10**math.floor(math.log10(limite))
        s['axis']['cap']=next(v*magnitude for v in [1,2,4,5,8,10] if v*magnitude>=limite)
        guardar(p,s,f'Ministros com votos vencidos nos julgamentos do {qual}' if qual=='corpus' else 'Ministros com votos vencidos nos confrontos presidenciais',
                f"{numero(u['votacao'].get('com divergência',0))} julgamentos com divergência; uma ocorrência por ministro e julgamento, inclusive voto parcialmente vencido")
    return configs

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--corpus',type=Path,default=ROOT);args=parser.parse_args();root=args.corpus
    resumo=json.loads((root/'apuracao_colegialidade_resumo.json').read_text(encoding='utf-8'))
    curadoria=json.loads((root/'curadoria_confrontos.json').read_text(encoding='utf-8'))
    configs=construir(root,resumo,curadoria)
    (root/'config_graficos_juridicos.json').write_text(json.dumps(configs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Cinco configurações jurídicas geradas para os resultados documentados; consulte as pendências da versão.')

if __name__=='__main__':main()
