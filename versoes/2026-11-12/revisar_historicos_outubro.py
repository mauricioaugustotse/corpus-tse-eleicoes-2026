"""Materializa a revisão documental dos 132 alvos históricos (anotações manuais)."""
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Resultados escolhidos após leitura dos dispositivos e peças oficiais, não por palavras-chave.
ALTERACOES = {
    '0600318': (True, True, 'integral na medida cautelar', 'tutela provisória deferida', 'A relatora determinou a remoção do vídeo sintético “Alô Brasília: novo sucesso da bandidagem” e proibiu nova difusão, em 22/10, após a emenda da inicial. A tutela decorre do realismo da manipulação por inteligência artificial; não constitui julgamento definitivo.'),
    '0600947': (True, False, 'não atendido', 'tutela provisória indeferida', 'A decisão, datada no corpo em 26/09 e registrada em 28/09, negou a suspensão e a remoção da campanha institucional sobre o fim da escala 6x1. O relator não identificou probabilidade de uso eleitoral ilícito dos recursos públicos, sem antecipar o mérito. A exclusão anterior por falta de inteiro teor foi superada.'),
    '0600958': (True, False, 'não atendido', 'tutela provisória indeferida; instrução em curso', 'A decisão de corpo datado de 07/07, registrada em 28/07, negou a remoção dos vídeos de eventos oficiais individualizados e as demais cautelares. Considerou necessária a reconstrução integral dos pronunciamentos e dos fatos. O despacho posterior trata de prova e não modifica a negativa da medida comunicacional.'),
    '0600955': (True, True, 'atendimento documentado, extensão não discriminada', 'tutela provisória deferida no referendo', 'Em 08/10, o Plenário, por unanimidade, não referendou a negativa liminar e determinou a remoção das três postagens. Para as duas últimas, também proibiu a republicação. O resultado substitui a negativa anterior, ainda em cognição provisória.'),
    '0600966': (True, False, 'não atendido', 'tutela provisória cassada no referendo', 'No julgamento encerrado em 02/10 e documentado em 03/10, o Plenário, por maioria, não referendou a tutela e determinou o restabelecimento das publicações sobre Flávio e o tarifaço. Ficaram vencidos o relator, André Mendonça e Floriano de Azevedo Marques. O mérito permaneceu sujeito ao contraditório.'),
    '0600976': (True, True, 'parcial', 'mérito parcialmente procedente; tutela confirmada', 'Em 23/10, o Plenário, por unanimidade, confirmou definitivamente a vedação ao impulsionamento pago do conteúdo negativo, preservou a circulação orgânica e aplicou multa de R$ 5 mil ao PL. Os demais pedidos sancionatórios foram rejeitados. O acórdão e a certidão foram registrados em 24/10.'),
    '0601014': (True, False, 'não atendido', 'improcedência mantida em recurso', 'Em 23/10, o Plenário, por unanimidade, negou o recurso e manteve a improcedência da representação sobre vídeo exibido na Festa do Peão de Americana. Não foram demonstrados pedido de voto nem uso ilícito da estrutura do evento pelo pré-candidato. O acórdão foi registrado em 29/10.'),
    '0601016': (True, True, 'parcial', 'mérito parcialmente procedente mantido em recurso', 'A decisão de mérito confirmou a retirada do vídeo e a proibição de associar pessoalmente Lula ao PCC e ao Comando Vermelho sem substrato fático mínimo, com multa de R$ 5 mil. Em 22/10, o Plenário negou os recursos de ambas as partes, vencido em parte Dias Toffoli. O acórdão foi registrado em 29/10; a confirmação de mérito é parcial.'),
    '0601315': (True, False, 'não atendido', 'mérito improcedente', 'Em 23/10, o Plenário, por unanimidade, julgou improcedentes os pedidos sobre o vídeo sintético de Jair Bolsonaro exibido na convenção e prejudicados os embargos contra a tutela. A nova alegação sobre regras da convenção não foi conhecida. O acórdão foi registrado em 24/10; a negativa agora se apoia em julgamento de mérito.'),
    '0601767': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 12/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre a propaganda que relacionava Flávio ao Banco Master. Reconheceu substrato factual e crítica política, sem imputação criminosa apta a justificar a resposta. A peça foi registrada em 13/10.'),
    '0601768': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta relativo à inserção sobre Flávio e o Banco Master. O acórdão de 11/10 distingue crítica política e juízo de valor de falsidade manifesta ou ofensa juridicamente qualificada.'),
    '0601786': (True, False, 'não atendido', 'tutela provisória cassada no referendo', 'No julgamento encerrado em 02/10, o Plenário, por maioria, cassou os efeitos da liminar que suspendia a peça de rádio “Foi o Flávio Bolsonaro”. Prevaleceu a divergência de Sebastião Reis Júnior, que considerou a crítica amparada pelo debate eleitoral; ficaram vencidos o relator, André Mendonça e Dias Toffoli.'),
    '0601788': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 12/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre inserção que contrapõe entrevista de Flávio a áudio sobre patrocínio de filme pelo controlador do Banco Master. Entendeu presentes substrato factual e juízos de valor, sem falsidade manifesta. O acórdão de 13/10 supera a pendência documental anterior.'),
    '0601789': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre propaganda na internet que relacionava Flávio ao Banco Master. O pedido de tutela ficou prejudicado pelo exame do mérito. O acórdão de 11/10 supera a pendência documental anterior.'),
    '0601806': (True, False, 'não atendido', 'tutela provisória cassada no referendo', 'No julgamento encerrado em 02/10, o Plenário, por maioria, não referendou a parte concessiva da tutela que restringia publicação do PT sobre Flávio, milícia e corrupção. Prevaleceu o voto de Dias Toffoli; ficaram vencidos o relator, André Mendonça e Floriano de Azevedo Marques. O resultado substitui a concessão parcial anterior.'),
    '0601811': (True, True, 'parcial', 'tutela provisória parcialmente deferida e referendada', 'Após a instrução inicial, a decisão de 06/10 suspendeu novas veiculações das peças específicas enquanto não fosse incluído o nome do vice com legibilidade e proporção legais. Em 10/10, o Plenário referendou a tutela parcial por unanimidade. A regra prospectiva genérica e a multa ficaram fora desse deferimento cautelar.'),
    '0601813': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre inserção televisiva relativa a Flávio e ao Banco Master; considerou prejudicada a tutela. O acórdão de 11/10 supera a falta de individualização documental anterior.'),
    '0601838': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre inserção televisiva que aproximava Flávio de fatos relativos ao Banco Master. Considerou existente substrato factual para a crítica e prejudicou o exame da tutela. A peça de 11/10 supera a pendência documental anterior.'),
    '0601849': (True, True, 'integral na medida cautelar', 'tutela provisória deferida no referendo; mérito em curso', 'No julgamento encerrado em 02/10, o Plenário, por maioria, substituiu a negativa por ordem de retirada da propaganda com vídeo do portal Dia Dia Notícia e proibição de nova divulgação. Dias Toffoli redigiu o acórdão; Nunes Marques e André Mendonça ficaram vencidos. A certidão de 20/10 registra retirada de pauta para reexame, sem novo resultado de mérito.'),
    '0601850': (True, True, 'integral na medida cautelar', 'tutela provisória deferida no referendo', 'No julgamento encerrado em 02/10, o Plenário, por maioria, determinou a remoção da propaganda nas redes sociais com vídeo do portal Dia Dia Notícias e proibiu nova difusão. Vencidos Nunes Marques e André Mendonça. A remoção cautelar não equivale à concessão definitiva de resposta.'),
    '0601862': (True, True, 'integral na medida cautelar', 'tutela provisória deferida no referendo', 'No julgamento encerrado em 02/10, o Plenário, por maioria, determinou a remoção da propaganda televisiva com vídeo do portal Dia Dia Notícia e proibiu nova difusão. Vencidos Nunes Marques e André Mendonça. A remoção cautelar não equivale à concessão definitiva de resposta.'),
    '0601882': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário afastou a preliminar de ilegitimidade e julgou improcedente, por unanimidade, o direito de resposta sobre críticas à educação e à pandemia no governo Jair Bolsonaro, com comparação entre pai e filho. O mérito negativo substitui a etapa apenas liminar.'),
    '0601931': (True, False, 'não atendido', 'direito de resposta improcedente', 'Em 10/10, o Plenário julgou improcedente, por unanimidade, o direito de resposta sobre inserção televisiva relativa ao Banco Master. A omissão de autoria da propaganda foi considerada matéria de via própria; as demais expressões foram tratadas como crítica política com substrato factual. O acórdão de 11/10 supera a pendência anterior.'),
    '0601962': (True, True, 'parcial', 'tutela provisória parcialmente reconsiderada', 'Em 01/10, o relator permitiu o uso dos painéis exclusivamente para transmitir o comício ao público presente, com condições e vedação de publicidade autônoma. Manteve a remoção do vídeo no YouTube e as demais ordens compatíveis. O atendimento permanece positivo, com alcance cautelar reduzido.'),
    '0602025': (True, True, 'parcial', 'mérito parcialmente procedente mantido em recurso', 'No julgamento encerrado em 08/10, o Plenário, por unanimidade, negou o recurso contra a procedência parcial por impulsionamento negativo, mantendo a restrição e a multa. A peça mantém resultado de mérito, sem transformar a negativa do recurso em derrota da campanha autora da representação.'),
    '0602099': (True, False, 'não atendido', 'direito de resposta improcedente', 'A decisão de 07/10 julgou improcedente o direito de resposta e a remoção das publicações “Enquanto o futuro deles é a Suíça”. O relator entendeu inexistentes imputação inequívoca de crime a Lula e falsidade manifesta; a tutela ficou prejudicada pelo mérito. A pendência documental anterior foi superada.'),
    '0602109': (True, False, 'não atendido', 'direito de resposta e remoção definitiva improcedentes', 'Em 22/10, o Plenário, por maioria, julgou improcedentes os pedidos de resposta e remoção definitiva do conteúdo, vencido Floriano de Azevedo Marques. O acórdão de 23/10 substitui a referência apenas à negativa liminar, sem alterar o resultado negativo.'),
    '0602148': (True, True, 'integral na medida cautelar', 'tutela provisória deferida no referendo', 'No julgamento encerrado em 08/10, o Plenário, por maioria, substituiu a negativa por tutela que proíbe nova veiculação do bloco ou conteúdo substancialmente idêntico até o mérito. Vencidos o relator e André Mendonça e, em parte, Floriano de Azevedo Marques. A preservação da gravação também foi determinada.'),
    '0602263': (True, True, 'integral na medida cautelar', 'tutela provisória deferida e referendada', 'No julgamento encerrado em 08/10, o Plenário referendou, por unanimidade, a suspensão do impulsionamento e a remoção do anúncio Meta ID 1400264218224285, que direcionava ao portal Direita Já. O inteiro teor individualiza o anúncio e supera a pendência anterior.'),
    '0602265': (True, True, 'integral na medida cautelar', 'tutela provisória deferida e referendada', 'No julgamento encerrado em 08/10, o Plenário referendou, por unanimidade, a suspensão do impulsionamento e a remoção do anúncio Meta ID 1072087735422852, que direcionava ao portal Direita Já. O inteiro teor individualiza o anúncio e supera a pendência anterior.'),
}

OBJETOS_NOVOS = {
    '0600947': ('Campanha institucional sobre o fim da escala 6x1', 'suspensão e remoção dos conteúdos institucionais sobre a escala 6x1'),
    '0600958': ('Vídeos de solenidades oficiais apontados como promoção eleitoral', 'remoção dos vídeos dos eventos oficiais individualizados na inicial'),
    '0601788': ('Inserção sobre Flávio, patrocínio de filme e Banco Master', 'direito de resposta à inserção televisiva e sua suspensão cautelar'),
    '0601789': ('Propaganda na internet sobre Flávio e Banco Master', 'direito de resposta à propaganda na internet'),
    '0601813': ('Inserção de TV sobre Flávio e Banco Master', 'direito de resposta à inserção televisiva'),
    '0601838': ('Inserção de TV sobre Flávio e Banco Master', 'direito de resposta à inserção televisiva'),
    '0601931': ('Inserção de 08/09 sobre Flávio e Banco Master', 'direito de resposta à inserção e suspensão cautelar'),
    '0602099': ('Publicações “Enquanto o futuro deles é a Suíça”', 'direito de resposta e remoção das publicações'),
    '0602263': ('Anúncio Meta ID 1400264218224285 e portal Direita Já', 'suspensão do impulsionamento e remoção do anúncio negativo'),
    '0602265': ('Anúncio Meta ID 1072087735422852 e portal Direita Já', 'suspensão do impulsionamento e remoção do anúncio negativo'),
}

def texto(doc):
    if not doc.get('arquivo'):return ''
    return re.sub(r'\s+', ' ', (ROOT/doc['arquivo']).with_suffix('.txt').read_text(encoding='utf-8')).strip()

def main():
    antigos=json.loads((ROOT.parent/'2026-10-01/curadoria_confrontos.json').read_text(encoding='utf-8'))
    checkpoint=json.loads((ROOT/'coleta_documental/checkpoint.json').read_text(encoding='utf-8'))
    resultado={}
    for cnj,original in antigos.items():
        v=copy.deepcopy(original);prefixo=cnj[:7]
        docs=checkpoint[cnj]['documentos']
        # Exceções documentais revisadas: atos processuais não substituem tutela anterior.
        escolhidos=[d for d in docs if d.get('arquivo') and not (
            'julgo extinto o pedido de direito de resposta' in texto(d)
            or (d['tipo'].startswith('Certid') and ('retirado' in texto(d) or 'pediu vista' in texto(d)))
        )]
        if prefixo=='0600958':escolhidos=[docs[1]]
        if prefixo=='0601303':escolhidos=[d for d in escolhidos if d['data_metadata']<'2026-10-01']
        if prefixo=='0601091':escolhidos=[]
        ref=escolhidos[0] if escolhidos else None
        alteracao=ALTERACOES.get(prefixo)
        if alteracao:
            incluir,atendido,grau,status,sinopse=alteracao
            v.update(incluir=incluir,atendido=atendido,grau=grau,status=status,sinopse=sinopse,
                     categoria='comparável',motivo='Resultado de medida comunicacional individualizada verificado na peça oficial até o corte.')
        elif ref and ref['data_metadata']>='2026-10-01' and v['incluir']:
            t=texto(ref)
            if 'referendou' in t:
                resumo='O pronunciamento colegiado de outubro manteve o resultado cautelar documentado, conforme o dispositivo da peça de referência.'
                v['status']='tutela provisória referendada; alcance conforme a peça'
                v['sinopse']=v['sinopse']+' Atualização até 31/10: '+resumo
        if prefixo in OBJETOS_NOVOS:
            v['objeto'],v['pedido']=OBJETOS_NOVOS[prefixo]
        if prefixo=='0602230':
            v.update(incluir=False,atendido=None,categoria='processual; tutela genérica e prova',
                     motivo='As remoções individualizadas não foram conhecidas por repetirem pedidos apresentados a outros relatores. O indeferimento remanescente recai sobre ordem abstrata e preservação de prova, sem resultado comparável autônomo sobre uma comunicação.',
                     status='AIJE em curso; cautelares não conhecidas ou indeferidas',
                     sinopse='Em 16/10, a Corregedoria não conheceu das remoções que reproduziam pedidos de outros processos, julgou prejudicada providência já abrangida, negou a ordem prospectiva abstrata e a preservação probatória residual. Os episódios permanecem na causa de pedir da AIJE, sem resultado comparável autônomo de comunicação nesta peça.')
        encerramentos=[d for d in docs if 'julgo extinto o pedido de direito de resposta' in texto(d)]
        if encerramentos:
            v['encerramento_sem_merito']={'data_metadata':encerramentos[0]['data_metadata'],'url':encerramentos[0]['url'],'motivo':'perda superveniente do objeto após segundo turno; não equivale a improcedência ou revogação expressa da tutela'}
            v['status']+='; direito de resposta extinto após o pleito em 29/10'
            v['sinopse']+=' Em 29/10, o pedido de resposta foi extinto após o segundo turno, sem novo exame da medida comunicacional. A classificação conserva o resultado comparável anterior; não afirma concessão definitiva de resposta.'
        if ref:
            v.update(url_peca=ref['url'],tipo_peca=ref['tipo'],data_ato_referencia=ref['data_metadata'],
                     fonte_classificacao='leitura documental do inteiro teor oficial (coleta de novembro; corte 31/10/2026)',
                     grau_certeza='alto',status_fonte='peça oficial salva e vinculada; datas metadata e julgamento distinguidas na revisão')
        if not ref and original.get('url_peca'):
            v['url_peca']=original['url_peca']
        revisados=[d for d in docs if d.get('arquivo') and (d['data_metadata']>='2026-10-01' or d==ref)]
        v['revisao_outubro']={'status':'verificado','corte':'2026-10-31',
            'inclusao_alterada':v['incluir']!=original['incluir'],
            'resultado_alterado':v['atendido']!=original['atendido'],
            'documentos_revisados':[{'url':d['url'],'arquivo':d['arquivo'],'sha256':d.get('sha256'),'data_metadata':d['data_metadata'],'tipo':d['tipo']} for d in revisados],
            'pendencias_download':[{'url':d['url'],'erro':d.get('erro')} for d in docs if not d.get('arquivo')],
            'nota':'Ementa/dispositivo e contexto pertinentes lidos; classificação jurídica manual. Ausência de novo resultado é limitada ao inventário coletado.'}
        # O relato antigo deve ser editado a partir da sinopse atual, nunca publicá-lo como se já revisado.
        if v.get('relato'):v['relato']['requer_atualizacao']=True
        resultado[cnj]=v
    destino=ROOT/'curadoria_historicos_outubro.json'
    destino.write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    linhas=['# Revisão dos 132 alvos históricos até 31/10/2026','',
        'Revisão documental manual de ementas/dispositivos, contexto e peças relevantes; os metadados foram usados para localizar documentos, nunca para inferir resultados. As datas de referência abaixo seguem o registro da peça; as datas de julgamento identificadas no corpo constam das sinopses. O pacote permite rever cada conclusão por URL e hash.', '',
        f"Dos {len(resultado)} alvos, {sum(v['incluir'] for v in resultado.values())} possuem resultado comparável. Há {sum(v['revisao_outubro']['inclusao_alterada'] for v in resultado.values())} inclusões novas entre os antigos excluídos.",'',
        'A extinção posterior do direito de resposta, por término do pleito, é registrada separadamente. Não apaga a decisão cautelar anterior sobre retirada ou manutenção de propaganda. Pedidos que nunca tiveram medida comunicacional examinada permanecem fora do denominador.', '',
        'Os relatos históricos ainda requerem revisão editorial; o campo `relato.requer_atualizacao` impede confundi-los com texto pronto. As sinopses contêm os resultados atuais.', '',
        '| CNJ | Incluído | Atendido | Referência | Estágio |','|---|---|---|---|---|']
    for cnj,v in resultado.items():linhas.append(f"| {cnj} | {'sim' if v['incluir'] else 'não'} | {v['atendido']} | {v.get('data_ato_referencia','')} | {v['status']} |")
    (ROOT/'auditoria_historicos.md').write_text('\n'.join(linhas)+'\n',encoding='utf-8')
    print(len(resultado),sum(v['incluir'] for v in resultado.values()))

if __name__=='__main__':main()
