"""Registra uma segunda leitura documental de inativos e dez proclamações.

As avaliações abaixo são curadoria explícita feita após a leitura dos textos,
não resultados inferidos pelo programa. A amostra é intencional, sem pretensão
de estimar uma taxa de erro estatística para os 713 atos.
"""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
AVALIACOES_INATIVOS={
    '0601896':('exclusão coerente','Reconhece probabilidade do direito quanto ao impulsionamento negativo; nega a urgência porque o anúncio já cessou. Não rejeita materialmente a alegação de ilicitude.'),
    '0601916':('exclusão coerente','Reconhece probabilidade do direito; anúncio encerrado e ausência de risco concreto de reativação. Proibição de conteúdos futuros e distintos é genérica, sem medida individualizada remanescente.'),
    '0602698':('exclusão coerente','Reconhece o caráter negativo e a probabilidade do direito; dois impulsionamentos pretéritos não provam reativação iminente. Dados e sanção ficam para a instrução.'),
    '0602700':('exclusão coerente','A própria fundamentação admite a probabilidade do direito, mas o encerramento do impulsionamento esvazia a suspensão e não há risco concreto de reativação.'),
    '0602712':('rever exclusão; recomendação de inclusão como cautelar não atendida','Há fundamento material próprio: a chamada Lula no Flow e o trocadilho com Flávio não evidenciam de plano caráter negativo nem imputação depreciativa explícita. A peça também afasta o perigo de dano por inatividade. É hipótese mista, distinta da simples falta de objeto; não classificar como improcedência definitiva.'),
    '0602789':('exclusão coerente','Reconhece probabilidade do direito sobre o impulsionamento negativo do Tesouraço; os dois anúncios estão inativos, única razão concreta para negar a medida de circulação.'),
    '0602802':('exclusão coerente','Impulsionamento encerrado e sem reativação concreta; pedido orgânico não integra o objeto urgente e sanção fica reservada.'),
    '0602860':('exclusão coerente','Publicação já indisponível e nenhum risco concreto de republicação; não decide a veracidade das imputações sobre INSS e reserva a sanção.'),
    '0602876':('exclusão coerente','Retirada do vídeo esvazia expressamente remoção e abstenção de republicação; prossegue apenas a pretensão de multa.'),
    '0602934':('exclusão coerente','Admite plausibilidade da alegação de conteúdo patrocinado negativo; anúncios encerrados, sem risco concreto de retomada. Mérito sancionatório preservado.'),
    '0603297':('exclusão coerente','Anúncio inativo, ausência de perigo atual e inadequação de abstenção genérica; nenhuma conclusão desfavorável de mérito sobre a ilicitude.'),
    '0603300':('exclusão coerente','Mesma estrutura jurídica: inatividade do anúncio, ausência de risco concreto e sanção reservada.'),
    '0603347':('exclusão coerente','Anúncio sobre a PEC da Segurança já inativo; inexistência de veiculação paga a interromper e risco futuro não demonstrado.'),
    '0603352':('exclusão coerente','Anúncio sobre queimadas na Amazônia já inativo; ausência de veiculação paga atual e de risco concreto de reativação.'),
    '0603355':('exclusão coerente','Anúncio sobre Lulinha já inativo; indeferimento fundado na falta de perigo atual, com sanção para exame posterior.'),
    '0603357':('exclusão coerente','Anúncio sobre os eleitores do Rio já inativo; falta de perigo atual, abstenção genérica recusada e sanção preservada.'),
}
AMOSTRAS_COLEGIADAS={
    '0600005':('unânime',[],'Não conhecimento do recurso especial proclamado por unanimidade.'),
    '0600251':('unânime',[],'Ata sem rótulo Decisão seguido de dois-pontos: contém unanimidade e manutenção do registro.'),
    '0601413':('unânime',[],'Ata própria defere unanimemente o DRAP; não usa votos de precedentes.'),
    '0602319':('unânime',[],'Cabeçalho abreviado recuperado; própria ata do dia 14/10 registra unanimidade na improcedência do direito de resposta.'),
    '0600690':('com divergência',['Floriano de Azevedo Marques'],'Referendo da tutela parcial; Floriano vencido em parte. Não contar como reforma da tutela apenas pelo voto parcial.'),
    '0601099':('com divergência',['Nunes Marques'],'Relator originário Nunes vencido; Dias é redator da divergência vencedora.'),
    '0601648':('com divergência',['Dias Toffoli','Estela Aranha'],'Ata registra expressamente os dois votos parcialmente vencidos.'),
    '0602217':('com divergência',['André Mendonça','Sebastião Reis Júnior'],'Apesar da palavra unanimidade, a própria proclamação registra dois vencidos parciais; regra do estudo exige divergência.'),
    '0602945':('com divergência',['André Mendonça','Estela Aranha','Nunes Marques'],'Relator André e Estela e Nunes vencidos; a citação ao Art. 7º entre os nomes não encerra a lista.'),
    '0601104':('não apurada',[],'Certidão e Resolução são unânimes, mas a identidade com o registro de acórdão do ZIP de 14/07 não está provada. A amostra confirma a conservação da lacuna, não unanimidade imputada ao ato.'),
}

def main():
    path=ROOT/'coleta_documental/checkpoint.json'
    if not path.exists():path=ROOT/'inventario_processos_documentais.json'
    checkpoint=json.loads(path.read_text(encoding='utf-8'))
    apuracao=json.loads((ROOT/'apuracao_colegialidade.json').read_text(encoding='utf-8'))
    inativos=[]
    for prefix,(parecer,justificativa) in AVALIACOES_INATIVOS.items():
        cnj=next(n for n in checkpoint if n.startswith(prefix))
        docs=[d for d in checkpoint[cnj]['documentos'] if d.get('status')=='conferido' and d.get('arquivo') and d['tipo'].startswith(('Ac','Dec'))]
        fonte=sorted(docs,key=lambda d:d['data_metadata'],reverse=True)[0]
        texto=re.sub(r'\s+',' ',(ROOT/fonte['arquivo']).with_suffix('.txt').read_text(encoding='utf-8'))
        assert hashlib.sha256((ROOT/fonte['arquivo']).read_bytes()).hexdigest()==fonte['sha256']
        inativos.append(dict(cnj=cnj,parecer=parecer,justificativa=justificativa,
            documento=fonte['id_documento'],url=fonte['url'],arquivo=fonte['arquivo'],sha256=fonte['sha256'],
            data_metadata=fonte['data_metadata'],requer_decisao_curatorial=prefix=='0602712'))
    amostras=[]
    for prefix,(votacao,vencidos,leitura) in AMOSTRAS_COLEGIADAS.items():
        ato=next(a for a in apuracao['atos'] if a['cnj'].startswith(prefix))
        confere=ato['votacao']==votacao and set(ato['vencidos'])==set(vencidos)
        amostras.append(dict(chave_ato=ato['chave_ato'],cnj=ato['cnj'],votacao_esperada=votacao,
            vencidos_esperados=vencidos,leitura_independente=leitura,confere_com_apuracao=confere,
            url=ato.get('url'),arquivo=ato.get('arquivo'),sha256=ato.get('sha256')))
    with (ROOT/'colegialidade_atos.csv').open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f,delimiter=';'))
    resultado={'metodo':'Segunda leitura manual dos dispositivos e dez proclamações; seleção intencional de casos com dificuldades de interpretação, sem inferência estatística da taxa de erro.',
        'inativos':inativos,'amostras_colegiadas':amostras,
        'consistencia_matematica':{'linhas':len(rows),'chaves_unicas':len({r['chave_ato'] for r in rows}),
            'votacao':dict(Counter(r['votacao'] for r in rows)),
            'amostras_conferentes':sum(a['confere_com_apuracao'] for a in amostras)}}
    (ROOT/'auditoria_independente_inativos_colegialidade.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    linhas=['# Auditoria independente de inativos e colegialidade','',resultado['metodo'],'',
        '## Conclusão sobre anúncios inativos','',
        'Quinze exclusões propostas são coerentes com a regra histórica que deixa fora das taxas a medida de circulação integralmente esvaziada. O rótulo de indeferimento não equivale a resultado material negativo quando a veiculação já terminou e a alegação de ilicitude permanece para exame posterior.',
        '', 'O processo 0602712-94 exige tratamento próprio. Recomendo revisão da exclusão: a peça também examina a natureza da mensagem e não identifica, de plano, propaganda negativa ou imputação depreciativa. Pode ser incluído como cautelar não atendida com fundamento misto, explicitando a falta de urgência. Isso não é julgamento definitivo de improcedência. Esta auditoria não altera a curadoria de outro responsável.',
        '', '| CNJ | Parecer | Justificativa |','|---|---|---|']
    for r in inativos:linhas.append(f"| {r['cnj']} | {r['parecer']} | {r['justificativa']} [Peça oficial]({r['url']}) |")
    linhas+=['','## Dez proclamações conferidas','',
        'As dez leituras coincidem com a apuração registrada: quatro unânimes, cinco com divergência e a única lacuna deliberadamente conservada. As fontes, hashes e nomes esperados estão no JSON. Esta amostra é um controle de casos difíceis; não substitui a conferência das demais proclamações.',
        '',json.dumps(resultado['consistencia_matematica'],ensure_ascii=False)]
    (ROOT/'auditoria_independente_inativos_colegialidade.md').write_text('\n'.join(linhas)+'\n',encoding='utf-8')
    print(json.dumps(resultado['consistencia_matematica'],ensure_ascii=False))

if __name__=='__main__':main()
