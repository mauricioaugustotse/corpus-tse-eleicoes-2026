"""Individualiza proclamações oficiais, associa acórdãos e preserva lacunas.

Datas distintas: o extrato estatístico frequentemente usa assinatura/juntada,
enquanto a decisão do inventário PJe usa a data da proclamação. O vínculo exige
CNJ no cabeçalho, tipo, data documental, identidade pública e candidato único.
Não classifica mérito nem manutenção de liminar por palavra isolada.
"""
from __future__ import annotations
import argparse
import csv
import difflib
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

MINISTROS = ['André Mendonça', 'Antonio Carlos Ferreira', 'Dias Toffoli',
             'Estela Aranha', 'Floriano de Azevedo Marques', 'Nunes Marques',
             'Ricardo Villas Bôas Cueva', 'Sebastião Reis Júnior',
             'Marco Aurélio Bellizze']

# Conciliação documental manual: o único ato colegiado do extrato nesses
# processos corresponde ao único julgamento com resultado proclamado no
# inventário. Inteiro teor do acórdão não listado; a fonte é a certidão.
CERTIDOES_CONCILIADAS = {
    '0601872-84.2026.6.00.0000': 179848712,
    '0601943-86.2026.6.00.0000': 179848738,
    '0602273-83.2026.6.00.0000': 179848809,
    '0602267-76.2026.6.00.0000': 179916043,
    '0602436-63.2026.6.00.0000': 179914272,
    '0602461-76.2026.6.00.0000': 179916054,
    '0602266-91.2026.6.00.0000': 179916042,
    '0602832-40.2026.6.00.0000': 180170684,
}

# Nove variantes foram lidas lado a lado: diferenças de redação, inversão
# de 'parcialmente deferida' e indicação nominal do relator não são novo ato.
EQUIVALENCIAS_LIDAS = {
    (177397248,177395848), (180172003,180171347),
    (178885541,178879686), (179937176,179936400),
    (178885735,178881653), (178879780,178881686),
    (180177849,180170676),
    (180184889,180168201), (177383637,177380340),
}

def nucleo_proclamacao(texto):
    texto=re.split(r'Acompanharam|Acompanham|Redigir.|Ac.rd.o publicado|N.o integrou|Juntou|Falaram|Aus.ncia|Dispensou',texto,flags=re.I)[0]
    return ''.join(c for c in normalizar(texto) if c.isalnum())

def normalizar(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))

def ler_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def extrair(texto):
    texto = re.sub(r'\s+', ' ', texto).strip()
    atas = list(re.finditer(r'EXTRATO DA ATA', texto, re.I))
    secao = texto[atas[-1].end():] if atas else texto
    sessoes=list(re.finditer(r'SESS.O.{0,120}?(\d{1,2})[ºo]?\.(\d{1,2})\.(\d{4})',secao,re.I))
    sessao_fim=''
    if sessoes:
        dia,mes,ano=sessoes[-1].groups();sessao_fim=f'{ano}-{int(mes):02d}-{int(dia):02d}'
    inicio = list(re.finditer(r'Decis.o\s*:', secao, re.I))
    if inicio:
        trecho = secao[inicio[-1].end():]
    else:
        inicio = list(re.finditer(r'(?:O Tribunal|Prosseguindo com o julgamento, o Tribunal|O presidente do Tribunal)', secao, re.I))
        trecho = secao[inicio[0].start():] if inicio else ''
    trecho = re.split(r'Composi..o\s*:|Presid.ncia\s*:|Vice-Procurador|SESS.O ', trecho, flags=re.I)[0].strip()
    relatores = re.findall(r'Relator(?:\(a\)|a| origin.rio|a origin.ria)?\s*:\s*(?:Ministr(?:[oa]|o\(a\))\s+)?([^.;]+)', secao, re.I)
    relator = ''
    for pessoa in relatores:
        encontrados = [(normalizar(pessoa).find(normalizar(n)), n) for n in MINISTROS if normalizar(n) in normalizar(pessoa)]
        if encontrados: relator = min(encontrados)[1]
        if relator: break
    vencidos = set()
    for m in re.finditer(r'vencid[oa]s?\b', trecho, re.I):
        clausula = trecho[m.end():]
        clausula = re.sub(r'\barRelatora\b', 'a Relatora', clausula)
        clausula = re.split(r'Acompanharam|Acompanham|Redigir.|N.o integrou|Ac.rd.o publicado|Composi..o|Determinou', clausula, flags=re.I)[0]
        clausula = re.split(r'(?<!Art)(?<!art)(?<!Res)(?<!res)\.\s+(?=[A-ZÀ-Ú])', clausula)[0]
        for nome in MINISTROS:
            if normalizar(nome) in normalizar(clausula): vencidos.add(nome)
        if re.search(r'(?:^|[,;]|\be\b)\s*(?:em parte,?\s*)?(?:[oa]s?\s+)?relator(?:a)?\b', clausula, re.I) and relator:
            vencidos.add(relator)
    tn = normalizar(trecho)
    if 'maioria' in tn or 'vencid' in tn:
        votacao = 'com divergência'
    elif 'unanimidade' in tn:
        votacao = 'unânime'
    else:
        votacao = 'não apurada'
    alertas = []
    if votacao == 'com divergência' and not vencidos:
        alertas.append('Divergência sem ministro vencido identificado; exige leitura nominal.')
    if 'unanimidade' in tn and 'vencid' in tn:
        alertas.append('Proclamação usa unanimidade e registra voto parcialmente vencido; classificada com divergência.')
    return dict(extrato=trecho, relator=relator, votacao=votacao,
                vencidos=sorted(vencidos), alertas=alertas,
                data_fim_sessao=sessao_fim,
                secao=secao)

def main(root, corte, inventario_publico=False):
    checkpoint_path=root/('inventario_processos_documentais.json' if inventario_publico else 'coleta_documental/checkpoint.json')
    if not checkpoint_path.exists():checkpoint_path=root/'inventario_processos_documentais.json'
    checkpoint = ler_json(checkpoint_path)
    suplemento_path = root/'suplemento_documental_auditoria.json'
    if suplemento_path.exists():
        for d in ler_json(suplemento_path):
            registro = checkpoint.setdefault(d['cnj'], {'documentos':[]})
            anteriores = {x['url']:x for x in registro['documentos']}
            anteriores[d['url']] = d
            registro['documentos'] = list(anteriores.values())
    with (root/'acordaos_para_conferencia.csv').open(encoding='utf-8-sig', newline='') as f:
        atos = list(csv.DictReader(f, delimiter=';'))
    documentos = []
    por_cnj = defaultdict(list)
    for cnj, registro in checkpoint.items():
        for d in registro.get('documentos', []):
            if d.get('status') != 'conferido' or not d.get('arquivo'): continue
            if not (d.get('tipo', '').startswith('Ac') or d.get('tipo', '').startswith('Certid') or d.get('tipo') == 'Resolução'): continue
            if d.get('data_metadata', '') > corte: continue
            path = root/d['arquivo']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == d['sha256'], path
            texto = path.with_suffix('.txt').read_text(encoding='utf-8')
            # A peça deve confirmar o CNJ antes de qualquer citação de precedentes.
            assert cnj in re.sub(r'\s+', '', texto[:5500]), (cnj, d['arquivo'])
            apurado = extrair(texto)
            secao = apurado.pop('secao')
            id_julgamento = f"{cnj}|{d['data_metadata']}|{hashlib.sha256(normalizar(apurado['extrato']).encode()).hexdigest()[:16]}"
            r = dict(cnj=cnj, id_documento=d['id_documento'], tipo=d['tipo'],
                     data_metadata=d['data_metadata'], data_assinatura=d.get('data_assinatura'),
                     data_juntada=d.get('data_juntada'), url=d['url'], arquivo=d['arquivo'],
                     sha256=d['sha256'], id_julgamento=id_julgamento,
                     secao_ata=secao, **apurado)
            documentos.append(r); por_cnj[cnj].append(r)
    # Um documento público só pode fundamentar uma linha estatística.
    usados = set(); associacoes = []
    for ato in atos:
        cnj, data = ato['NR_PROCESSO'], ato['DT_DECISAO_ISO']
        candidatos = [r for r in por_cnj[cnj] if r['tipo'].startswith('Ac') and any(
            (r.get(k) or '')[:10] == data for k in ('data_metadata', 'data_assinatura', 'data_juntada'))]
        r = dict(chave_ato=ato['CHAVE_ATO'], cnj=cnj, data_ato=data,
                 autor_bulk=ato['NM_AUTOR_DECISAO'], votacao='não apurada', vencidos=[],
                 candidatos=[d['id_documento'] for d in candidatos])
        certidao_conciliada = False
        if not candidatos and cnj in CERTIDOES_CONCILIADAS:
            candidatos = [r for r in por_cnj[cnj] if r['id_documento']==CERTIDOES_CONCILIADAS[cnj]]
            assert sum(a['NR_PROCESSO']==cnj for a in atos)==1, cnj
            assert len(candidatos)==1 and candidatos[0]['votacao']=='unânime', cnj
            certidao_conciliada = True
        if len(candidatos) == 1 and candidatos[0]['id_documento'] not in usados:
            doc = candidatos[0]
            r.update(documento=doc['id_documento'], url=doc['url'], arquivo=doc['arquivo'],
                     sha256=doc['sha256'], extrato=doc['extrato'], relator=doc['relator'],
                     votacao=doc['votacao'], vencidos=doc['vencidos'], alertas=doc['alertas'],
                     vinculo='CNJ confirmado no cabeçalho; Acórdão público único; data do ato compatível com assinatura, juntada ou inventário; sequência sem reaproveitamento de documento',
                     data_julgamento_metadata=doc['data_metadata'])
            if certidao_conciliada:
                r['vinculo']='Conciliação documental manual: único registro de acórdão do processo e único resultado colegiado certificado antes do ato; CNJ, etapa e sequência conferidos. Fonte: certidão de julgamento; inteiro teor do acórdão ausente do inventário.'
            r['tipo_fonte']=doc['tipo']
            usados.add(doc['id_documento'])
        else:
            r.update(vinculo='pendente de conciliação documental',
                     documentos_disponiveis=[{'id_documento':d['id_documento'], 'tipo':d['tipo'],
                         'data_metadata':d['data_metadata'], 'url':d['url'],
                         'extrato':d['extrato']} for d in por_cnj[cnj]])
        associacoes.append(r)
    # Não somar certidão e acórdão do mesmo resultado: equivalência exige
    # mesma data do inventário e proclamação normalizada idêntica. Se o texto
    # difere, preservar candidatos em vez de presumir equivalência.
    grupos = defaultdict(list)
    for doc in documentos: grupos[doc['id_julgamento']].append(doc)
    julgamentos = []
    for ident, docs in grupos.items():
        preferido = sorted(docs, key=lambda r:not r['tipo'].startswith('Ac'))[0]
        julgamentos.append(dict(id_julgamento=ident, cnj=preferido['cnj'],
                data_metadata=preferido['data_metadata'], votacao=preferido['votacao'],
                vencidos=preferido['vencidos'], relator=preferido['relator'],
                extrato=preferido['extrato'], fonte_preferencial=preferido['url'],
                documentos=[d['id_documento'] for d in docs],
                duplicidade_resolvida=len(docs)>1, alertas=preferido['alertas']))
    # Ledger de julgamentos: a ata no acórdão é a fonte preferencial. Uma
    # certidão com mesma data/etapa e votação é fonte complementar, não novo
    # julgamento. Sem acórdão, preserva a certidão com resultado proclamado.
    por_sessao = defaultdict(list)
    for doc in documentos:
        por_sessao[(doc['cnj'],doc['data_fim_sessao'] or doc['data_metadata'])].append(doc)
    ledger = []
    for chave, docs in sorted(por_sessao.items()):
        acordaos = [d for d in docs if d['tipo'].startswith('Ac')]
        certidoes = [d for d in docs if d['tipo'].startswith('Certid') and d['votacao']!='não apurada']
        principais = acordaos or certidoes
        if not principais:continue
        if len(principais)>1:
            # Não presumir que certidões distintas do mesmo dia sejam um
            # julgamento. A deduplicação exige proclamação normalizada igual.
            unicos = {normalizar(d['extrato']):d for d in principais}
            principais=list(unicos.values())
        for doc in principais:
            outros_principais={d['id_documento'] for d in principais if d['id_documento']!=doc['id_documento']}
            complementares = [d for d in docs if d['id_documento']!=doc['id_documento'] and d['id_documento'] not in outros_principais]
            equivalencias=[]
            for outro in complementares:
                similaridade=difflib.SequenceMatcher(None,nucleo_proclamacao(doc['extrato']),nucleo_proclamacao(outro['extrato'])).ratio()
                lida=(doc['id_documento'],outro['id_documento']) in EQUIVALENCIAS_LIDAS
                inacabada=outro['votacao']=='não apurada'
                equivalencias.append(dict(documento=outro['id_documento'],
                    nucleo_similaridade=round(similaridade,4),
                    resultado_compativel=outro['votacao']==doc['votacao'] and set(outro['vencidos'])==set(doc['vencidos']),
                    leitura_paralela=lida,
                    status='ato de sessão sem proclamação final' if inacabada else
                           'variante textual conferida manualmente' if lida else
                           'mesmo núcleo proclamado e votação' if similaridade>=.95 else
                           'equivalência pendente de revisão'))
            divergencias = [d['id_documento'] for d in complementares if
                d['votacao']!='não apurada' and (d['votacao']!=doc['votacao'] or set(d['vencidos'])!=set(doc['vencidos']))]
            ledger.append(dict(cnj=doc['cnj'], data_metadata=doc['data_metadata'],
                id_julgamento=f"{doc['cnj']}|{doc['id_documento']}", documento_principal=doc['id_documento'],
                tipo_fonte=doc['tipo'], url=doc['url'], arquivo=doc['arquivo'],
                data_fim_sessao=doc['data_fim_sessao'],
                votacao=doc['votacao'], vencidos=doc['vencidos'], extrato=doc['extrato'],
                documentos_complementares=[d['id_documento'] for d in complementares],
                equivalencia_documental=equivalencias,
                divergencias_entre_fontes=divergencias,
                nota='Acórdão preferencial e certidões da mesma data documental/etapa, com resultado comparado; decisões de vista ou adiamento não somadas. Pendências nominais entre fontes preservadas.'))
    antigas = ler_json(root.parent/'2026-10-01/curadoria_confrontos.json')
    antigos_incluidos = {cnj for cnj,r in antigas.items() if r.get('incluir')}
    candidatos_presidenciais = set()
    with (root/'triagem_confrontos.csv').open(encoding='utf-8-sig',newline='') as f:
        candidatos_presidenciais.update(r['cnj'] for r in csv.DictReader(f, delimiter=';'))
    def resumir(rows):
        return {'total':len(rows),'votacao':dict(Counter(r['votacao'] for r in rows)),
                'ministros_vencidos':dict(Counter(n for r in rows for n in set(r['vencidos'])))}
    resultado = {
        'corte':corte,
        'metodo':'Proclamação isolada do EXTRATO DA ATA ou certidão. Voto parcialmente vencido conta como divergência. Uma ocorrência por ministro e julgamento. Vínculos ambíguos não recebem votação por aproximação.',
        'corpus':resumir(associacoes),
        'documentos_por_tipo':dict(Counter(d['tipo'] for d in documentos)),
        'julgamentos_documentais':resumir(julgamentos),
        'confrontos_historicos_apenas_documental':resumir([r for r in julgamentos if r['cnj'] in antigos_incluidos]),
        'aviso_recorte_presidencial':'Não é o novo comparativo. A lista dos confrontos finais depende da curadoria de resultados; os mesmos CNJs podem ter mais de um julgamento. Não transportar os 107 históricos como denominador de outubro.',
        'atos':associacoes,
        'julgamentos':julgamentos,
        'ledger_julgamentos':ledger,
        'documentos':documentos,
        'pendencias_vinculo':[r['chave_ato'] for r in associacoes if not r.get('documento')],
        'divergencias_sem_nome':[r['id_documento'] for r in documentos if r['votacao']=='com divergência' and not r['vencidos']],
    }
    curadoria_path=root/'curadoria_confrontos.json'
    if curadoria_path.exists():
        curadoria=ler_json(curadoria_path)
        incluidos={cnj:r for cnj,r in curadoria.items() if r.get('incluir')}
        votos_presidenciais=[r for r in ledger if r['cnj'] in incluidos]
        situacoes={}
        paths=set(root.glob('situacoes_*.json'))|set(root.glob('colegialidade_curadoria_*.json'))
        for path in sorted(paths):
            situacoes.update(ler_json(path))
        casos=[]
        for cnj,r in sorted(incluidos.items()):
            revisao=situacoes.get(cnj,{})
            if isinstance(revisao,str):revisao={'situacao':revisao}
            situacao=r.get('colegialidade_situacao') or revisao.get('colegialidade_situacao') or revisao.get('situacao') or 'situação da medida pendente de curadoria'
            casos.append(dict(cnj=cnj,situacao=situacao,justificativa=r.get('colegialidade_justificativa') or revisao.get('justificativa',''),
                fonte_resultado=r.get('url_peca',''),status_curatorial=r.get('status',''),
                fonte_situacao=revisao, julgamentos=[v['id_julgamento'] for v in votos_presidenciais if v['cnj']==cnj]))
        status=Counter(r['situacao'] for r in casos)
        resultado['presidencial']={**resumir(votos_presidenciais),
            'processos_comparaveis':len(incluidos),'processos_com_julgamento_colegiado':len({r['cnj'] for r in votos_presidenciais}),
            'situacao_confrontos':dict(status),'casos':casos,'julgamentos':votos_presidenciais,
            'aviso':'Votação conta julgamentos únicos documentados dos CNJs incluídos; situação da medida conta um CNJ. Um processo pode ter vários julgamentos. Pendências de situação ficam explícitas.'}
    (root/'apuracao_colegialidade.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    resumo={k:resultado[k] for k in ['corte','metodo','corpus','pendencias_vinculo','divergencias_sem_nome']}
    if 'presidencial' in resultado:
        resumo['presidencial']={k:v for k,v in resultado['presidencial'].items() if k not in {'casos','julgamentos'}}
    (root/'apuracao_colegialidade_resumo.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (root/'colegialidade_atos.csv').open('w',encoding='utf-8-sig',newline='') as f:
        campos=['chave_ato','cnj','data_ato','votacao','vencidos','documento','relator','url','extrato','vinculo']
        writer=csv.DictWriter(f,fieldnames=campos,delimiter=';',extrasaction='ignore');writer.writeheader()
        for r in associacoes:writer.writerow({**r,'vencidos':' | '.join(r['vencidos'])})
    linhas=['# Apuração documental da colegialidade — corte de '+corte,
            '', '## Universo estatístico', '',
            f"São {len(atos)} registros de acórdão. Resultado da conciliação: {json.dumps(resultado['corpus'],ensure_ascii=False)}.",
            '', 'São 704 vínculos com acórdão público, oito com proclamação certificada conciliada manualmente e uma lacuna. Os vínculos usam o CNJ confirmado no cabeçalho, espécie, sequência documental e data do ato compatível com assinatura, juntada ou inventário PJe. CNJ e data, isoladamente, não provam a identidade. Os candidatos e a fonte exata permanecem no JSON. Nenhuma certidão foi acrescentada como ato estatístico.',
            '', '## Pendências de vínculo', '']
    for r in associacoes:
        if not r.get('documento'):
            linhas.append(f"- {r['chave_ato']} — {r['data_ato']}: conciliação pendente; {len(r.get('documentos_disponiveis',[]))} documento(s) colegiado(s) acessível(is).")
    linhas += ['', '## Recorte presidencial', '', resultado['aviso_recorte_presidencial'],
               '', 'As revisões de tutela precisam da comparação entre a ordem individual e a proclamação. Este programa não transforma expressões como “referendou parcialmente” em manutenção ou reforma sem ler os dois dispositivos.',
               '', '## Deduplicação e leitura nominal', '',
               'Certidão e acórdão só são agrupados automaticamente se CNJ, data do inventário e proclamação normalizada forem iguais. Textos diferentes do mesmo dia ficam como candidatos e exigem conciliação antes de somar julgamentos presidenciais. O número de grupos documentais é preparatório, não um total editorial pronto para publicação.',
               '', f"Divergências sem nome resolvido: {resultado['divergencias_sem_nome']}",
               '', 'A classificação preserva votação “não apurada” quando não há proclamação ou vínculo suficiente. A soma de ministros vencidos não é o número de julgamentos: um julgamento pode ter vários vencidos.']
    linhas += ['', '## Ledger para o recorte presidencial', '',
               'O campo `ledger_julgamentos` prefere a ata no acórdão. A certidão é fonte complementar quando o núcleo do dispositivo e a votação são compatíveis; nove variantes maiores tiveram leitura paralela registrada no programa. Equivalências não se baseiam só em CNJ e data. Certidões de adiamento ou vista sem proclamação final não contam como julgamento finalizado.',
               '', 'Após gerar `curadoria_confrontos.json`, execute novamente o programa. Ele seleciona os CNJs incluídos e lê `situacoes_*.json` ou o campo `colegialidade_situacao` de cada registro para a classificação da medida. Ausência de classificação manual fica explícita; não se deduz manutenção ou reforma por regex. A votação conta julgamentos; o quadro da situação da medida conta processos.',
               '', 'Correções nominais conferidas: no acórdão de 0602945-91, a referência ao Art. 7º aparece entre os nomes vencidos e não deve cortar Nunes Marques da lista; no acórdão de 0602953-68, a grafia “arRelatora” é lida à luz da relatoria originária expressa de Estela Aranha. O processo suplementar 0601315-97 passou a ter dois acórdãos no inventário documental; cada etapa fica separada no ledger, sem criar atos no ZIP.']
    (root/'apuracao_colegialidade.md').write_text('\n'.join(linhas)+'\n',encoding='utf-8')
    print(json.dumps({k:resultado[k] for k in ['corpus','documentos_por_tipo','julgamentos_documentais','pendencias_vinculo','divergencias_sem_nome']},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--corte',default='2026-10-31')
    parser.add_argument('--inventario-publico',action='store_true',help='Reproduz o espelho congelado, mesmo com coleta local em andamento.')
    args=parser.parse_args();main(args.corpus,args.corte,args.inventario_publico)

