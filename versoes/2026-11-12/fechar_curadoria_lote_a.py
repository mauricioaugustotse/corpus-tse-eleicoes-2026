"""Consolida decisões de revisão documental do lote A com fontes e ressalvas."""
import json
import re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parent


def main():
    path=ROOT/'curadoria_novos_a.json'
    dados=json.loads(path.read_text(encoding='utf-8'))
    datas=json.loads((ROOT/'coleta_documental/auditoria/datas_lote_a.json').read_text(encoding='utf-8'))
    objetos={
        20:'Inserção sobre Flávio, escala 6x1 e sátira da escala 3x4',
        22:'Inserção sobre Flávio, escala 6x1 e sátira da escala 3x4',
        40:'Live eleitoral de Lula realizada no Palácio da Alvorada com participação de terceiros',
        47:'Vídeo de inteligência artificial que apresenta Lula como DJ com frases sobre carne e ovos',
        52:'Publicação do PL sobre investigação de Fábio Luís Lula da Silva e referências ao talento de família',
        56:'Publicação que atribui a Lula oferta de cargo à lobista Roberta Luchsinger',
        60:'Publicação sobre suposto plano de R$ 626 milhões envolvendo Lulinha, Careca do INSS e gabinete presidencial',
        61:'Publicação que contrapõe promessa de picanha à frase de Lula sobre comer ovos',
        68:'Inserção radiofônica segundo a qual o partido de Flávio tentou barrar o reajuste do Bolsa Família',
        74:'Inserção radiofônica segundo a qual o partido de Flávio tentou barrar o reajuste do Bolsa Família',
        75:'Inserção radiofônica segundo a qual o partido de Flávio tentou barrar o reajuste do Bolsa Família',
        101:'Inserção radiofônica segundo a qual o partido de Flávio tentou barrar o reajuste do Bolsa Família',
        115:'Publicação do PT sobre críticas de Flávio ao reajuste do Bolsa Família e referência à fila do osso',
        131:'Inserção radiofônica que atribui a Flávio responsabilidade pela expansão das apostas online',
        132:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        133:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        136:'Vídeo de inteligência artificial ambientado em 2036 que associa o terceiro mandato de Lula a facções',
        152:'Propaganda de rádio Você acredita no que o Lula promete com fala sobre mentir retirada de entrevista ao Flow',
        176:'Inserção de rádio Você acredita no que o Lula promete com fala sobre mentir retirada de entrevista ao Flow',
        199:'Montagem de vídeos de artistas de campanha sanitária da Covid-19 transformados em mensagem eleitoral',
        200:'Vídeo Bolsonaristas, os falsos defensores da família com reportagens sobre crimes atribuídos a terceiros',
        225:'Impulsionamento do vídeo Com Flávio Bolsonaro, você perde com recortes de discurso e imagens negativas',
        80:'Vídeo com inteligência artificial, figuras antropomórficas e grave descontextualização de falas',
    }
    impulsionamento={24,49,72,92,93,94,95,100,130,158,204,207,208,209,210,211,214,225,228,229}
    fundamento_pessoal={
        7:'A referência a integrantes do PCC e do Comando Vermelho como criminosos dele foi considerada associação pessoal de Lula a facções, sem suporte fático mínimo.',
        8:'O conteúdo foi considerado crítica satírica, sem o realismo necessário à configuração de deepfake ou ilicitude manifesta que justificasse remoção cautelar.',
        9:'A decisão preserva sátira e crítica, mas afasta imputações de crimes, associação a facções, fabricação de imagens e falas com aparência de autenticidade e representação de violência contra o candidato.',
        10:'A edição seletiva e as referências ao PCC e ao Comando Vermelho foram consideradas associação ilícita de Lula a organizações criminosas; o relator reajustou seu voto.',
        13:'A versão televisiva não identificava de modo claro e legível os nomes dos integrantes da chapa; a ordem fica limitada à correção dessa identificação.',
        14:'A restrição decorre do conteúdo ofensivo e da associação do governo a criminosos sem lastro mínimo, não da mera utilização de fantoches ou de inteligência artificial.',
        16:'O recorte transformou uma manifestação de valorização dos garis em mensagem de menosprezo à categoria.',
        21:'A supressão do contexto modificou o sentido da fala de Lula e a converteu em preconceito contra profissionais da limpeza urbana.',
        23:'O colegiado considerou gravemente descontextualizada a apresentação da fala como deboche dos garis.',
        27:'O colegiado diferenciou as versões dos vídeos e restringiu seis publicações; o atendimento foi parcial, conforme o voto prevalecente.',
        28:'O recorte da manifestação de Lula foi considerado manipulação de sentido capaz de produzir falsa mensagem de preconceito contra os garis.',
        29:'A propaganda na internet deve observar a comunicação do endereço e as demais exigências aplicáveis; a liminar foi confirmada somente nos pontos deferidos.',
        43:'A maioria considerou plausível a ofensa e a veiculação de mensagem de forte caráter anti-institucional, restringindo a repetição da inserção.',
        47:'A montagem foi examinada como sátira e crítica ao custo de vida; não se reconheceu falsidade manifesta ou descontextualização apta a gerar resposta.',
        52:'A linguagem depreciativa e a associação familiar foram consideradas insuficientes para caracterizar hipótese excepcional de direito de resposta; quanto a Flávio, reconheceu-se ilegitimidade passiva, prosseguindo o exame material contra o PL.',
        53:'A maioria considerou a publicação sobre arrecadação tributária crítica política fundada em informação jornalística, apesar da divergência sobre o caráter ofensivo da expressão sanguessuga.',
        56:'O texto foi examinado em conjunto com a legenda que atribui a informação a terceira pessoa; não se reconheceu falsidade manifesta ou ofensa pessoal qualificada.',
        60:'As referências à investigação e a pessoas próximas ao presidente foram consideradas interpretação crítica de fatos de interesse público, sem falsidade manifesta que autorizasse resposta.',
        61:'A frase é autêntica e a contraposição à promessa de picanha foi considerada crítica política sobre custo de vida, sem descontextualização juridicamente suficiente para resposta.',
        63:'A peça foi apreciada em seu conjunto e a associação retórica entre pai e filho não foi considerada imputação factual pessoal apta a justificar direito de resposta.',
        64:'O pedido relativo a Flávio foi extinto por ilegitimidade; em relação ao PL, a crítica política e o substrato jornalístico afastaram a concessão de resposta.',
        66:'As referências ao Banco Master, ao Banco Central e a eventos foram consideradas interpretação crítica de fatos públicos, sem falsidade objetiva manifesta.',
        67:'A tutela foi confirmada apenas na extensão parcialmente deferida; preservar a distinção entre o debate sobre castração química e a imputação dirigida ao candidato a vice-presidente.',
        68:'A propaganda tem substrato na iniciativa judicial de parlamentar filiado ao PL; a simplificação da autoria institucional foi considerada crítica política, não falsidade sabida.',
        74:'A iniciativa judicial de parlamentar do PL constitui substrato para a síntese política da propaganda; não se reconheceu falsidade manifesta.',
        75:'A iniciativa judicial de parlamentar do PL constitui substrato para a síntese política da propaganda; não se reconheceu falsidade manifesta.',
        80:'O recurso amplia a restrição ao reconhecer grave descontextualização e criação de estados emocionais sem relação com a verdade dos fatos, além de aplicar multa individual; a decisão prevalecente não se limita ao aviso de uso de inteligência artificial.',
        84:'A justaposição de manchetes de períodos e contextos diferentes, com omissão de informações relevantes, foi considerada apta a distorcer a mensagem sobre o candidato.',
        86:'As incorreções de datas e de fonte não alteravam substancialmente as notícias nem os períodos políticos comparados; prevaleceu a crítica política.',
        89:'O colegiado manteve a liminar contra a mensagem ofensiva do PL; o voto individual contrário à confirmação não constitui resultado do julgamento.',
        97:'A afirmação de recebimento pessoal de quase R$ 70 milhões por Flávio foi considerada imputação concreta, sem lastro mínimo; operações envolvendo terceiros não comprovam recebimento pelo candidato.',
        98:'A tutela ficou limitada ao segmento do pronunciamento na ONU que ingressou diretamente na disputa eleitoral; outros registros de atuação institucional foram preservados.',
        99:'A mensagem sobre Banco Master e Flávio foi considerada merecedora de restrição cautelar, sem antecipar o julgamento principal do pedido de resposta.',
        101:'A simplificação política da iniciativa de parlamentar do PL não foi considerada informação sabidamente inverídica; prevaleceu o contradiscurso.',
        104:'A publicação parte de ação judicial efetivamente proposta; a caracterização política de seus efeitos e a expressão hostil foram consideradas crítica protegida.',
        108:'A intenção de cortar despesas públicas foi considerada tema legítimo do debate eleitoral; divergência interpretativa não basta para resposta.',
        109:'A intenção de cortar despesas públicas foi considerada tema legítimo do debate eleitoral; divergência interpretativa não basta para resposta.',
        111:'A intenção de cortar despesas públicas foi considerada tema legítimo do debate eleitoral; divergência interpretativa não basta para resposta.',
        113:'A relatora não reconheceu ilicitude manifesta em grau suficiente para medida cautelar, preservando o exame aprofundado após o contraditório.',
        115:'A crítica sobre o reajuste e as expressões irônicas foram consideradas propaganda adversarial protegida; não se reconheceu falsidade manifesta ou ofensa pessoal qualificada.',
        116:'A fala sobre relações políticas com milicianos foi considerada, no exame preliminar, predominantemente opinativa e sem imputação individualizada de fato criminoso determinado.',
        119:'A crítica do candidato ao momento e à legalidade do reajuste forneceu substrato para a síntese política da propaganda.',
        120:'A intenção de cortar despesas públicas foi considerada tema legítimo do debate eleitoral; divergência interpretativa não basta para resposta.',
        121:'A intenção de cortar despesas públicas foi considerada tema legítimo do debate eleitoral; divergência interpretativa não basta para resposta.',
        126:'A associação de Lula à proteção do PCC e do Comando Vermelho, sem suporte idôneo, ultrapassou a crítica política e justificou a retirada cautelar.',
        128:'O debate sobre a regulação das apostas e suas etapas legislativas fornece substrato à atribuição de responsabilidade política; não se reconheceu falsidade manifesta.',
        131:'O debate sobre a regulação das apostas e suas etapas legislativas fornece substrato à atribuição de responsabilidade política; não se reconheceu falsidade manifesta.',
        132:'A atribuição de intenção de realizar ajustes no orçamento foi considerada crítica política, sem distorção evidente apta a justificar resposta.',
        133:'A atribuição de intenção de realizar ajustes no orçamento foi considerada crítica política, sem distorção evidente apta a justificar resposta.',
        141:'As etapas de regulação das apostas fornecem substrato factual ao debate sobre responsabilidade política; a crítica não foi considerada falsidade objetiva manifesta.',
        163:'A tutela foi preservada quanto à associação a milícias e afastada quanto ao PIX, entendido como prognóstico político; a modificação reduziu o alcance da ordem sem eliminar todo atendimento.',
        173:'A presença de apresentações artísticas ao vivo para animar evento eleitoral atrai a vedação de showmício; discursos e manifestações de apoio de artistas foram ressalvados.',
        199:'Falhas e mensagens autênticas de campanha sanitária foram retiradas de seu contexto e transformadas em recomendação eleitoral; a ordem recai nas publicações de terceiros, permanecendo Flávio no polo passivo.',
        200:'O vídeo foi considerado crítica à coerência entre discurso de defesa da família e condutas de apoiadores, sem atribuir pessoalmente ao requerente os crimes noticiados.',
        201:'A maioria afastou a restrição cautelar e o bloqueio por hash por não reconhecer, no exame provisório, a ilicitude necessária, preservando a apreciação definitiva após contraditório.',
        215:'O vídeo atribui propostas inexistentes e descontextualiza as manifestações do candidato, justificando remoção delimitada e preservação de registros.',
        223:'A tutela ficou limitada à publicação identificada, sem ordem genérica sobre links ou conteúdos ainda não examinados.',
        224:'A tutela aplica a vedação ao uso de conteúdo sintético manipulado para prejudicar candidatura, conforme o contexto de armas e violência escolar examinado na peça.',
        227:'O julgamento de mérito torna definitiva a suspensão da inserção e da referência ao pedido de investigação por estupro de vulnerável contra Alfredo Gaspar, com atendimento parcial e sanção.',
    }
    inativos={26,30,205,206,226}
    for cnj,r in dados.items():
        i=r['revisao']['indice_lote']
        if i in objetos:r['objeto']=objetos[i]
        if i==213:
            r.update(incluir=True,atendido=False,grau='indeferido',categoria='liminar_indeferida',status='tutela indeferida e negativa mantida em referendo')
            r['objeto']='Anúncios que divulgam participação de Lula no Flow e empregam trocadilho com o nome de Flávio'
            fundamento_pessoal[i]='O colegiado examinou a natureza da mensagem: a chamada para entrevista e o trocadilho humorístico não evidenciavam propaganda negativa, imputação de crime ou depreciação manifesta. Subsidiariamente, a inatividade dos anúncios também afastava o perigo de dano. A negativa é materialmente comparável, com fundamento misto.'
        dt=datas[cnj]
        r['data_ato_referencia']=dt['data_escrita']
        r['origem_data_referencia']=dt['origem_data']
        r['evidencia_data']=dt['evidencia_data']
        if i==218:r['grau']='parcial';r['categoria']='parcial';r['status']='tutela parcialmente deferida e mantida em referendo'
        if i in inativos:
            r.update(incluir=False,atendido=None,grau='sem resultado comparável',categoria='impulsionamento já encerrado',status='tutela indeferida por anúncios inativos')
            r['motivo']='Os anúncios patrocinados já estavam inativos e o pedido cautelar foi rejeitado por ausência de dano atual. Não se trata de autorização material da propaganda nem de derrota comparável sobre circulação ativa.'
            if i==213:r['motivo']+=' A peça também contém apreciação subsidiária do caráter negativo não evidenciado de plano; a exclusão preserva a mesma regra aplicada aos demais anúncios inativos.'
        if r['incluir']:
            if i in fundamento_pessoal:fund=fundamento_pessoal[i]
            elif i in impulsionamento:fund='O impulsionamento pago é admitido para promover candidatura própria e vedado para amplificar conteúdo negativo contra adversário; a restrição recai sobre o patrocínio, sem confundir eventual crítica orgânica lícita com publicidade remunerada.'
            elif r['atendido']:fund='A peça reconhece falsidade ou descontextualização suficiente para impor a medida comunicacional delimitada no dispositivo, preservando os demais pontos não acolhidos.'
            elif r['categoria']=='liminar_indeferida':fund='No exame provisório, não se reconheceu falsidade objetiva ou excesso em grau suficiente para restringir a comunicação, preservando o contraditório e o exame posterior do mérito.'
            else:fund='A peça considerou o conteúdo crítica ou interpretação política de fatos públicos e não reconheceu falsidade manifesta ou ofensa pessoal qualificada que justificasse a resposta ou a retirada pretendida.'
            if i in {24,72,92,93,94,95,130,158}:fund+=' O dispositivo reconhece a irregularidade do patrocínio e a sanção ou restrição correspondente; não declara ilícita toda circulação orgânica do conteúdo.'
            r['fundamento']=fund
            tipo=r['tipo_peca']
            if r['atendido']:
                resultado='O pedido obteve atendimento parcial.' if r['grau']=='parcial' else 'O pedido obteve atendimento na extensão descrita na peça.'
                if r['colegialidade_situacao']=='liminar modificada':resultado+=' O colegiado modificou a tutela individual.'
                elif r['colegialidade_situacao']=='liminar mantida':resultado+=' O colegiado manteve a tutela individual.'
            else:
                resultado='O pedido de tutela de urgência foi indeferido.' if r['categoria']=='liminar_indeferida' else 'O pedido foi rejeitado no julgamento material.'
                if r['colegialidade_situacao']=='liminar mantida':resultado+=' O indeferimento foi mantido no referendo.'
            r['pedido']='restrição do impulsionamento pago e demais providências delimitadas na peça' if i in impulsionamento else ('direito de resposta e medidas de suspensão ou remoção descritas na peça' if 'direito de resposta' in r['pedido'] else 'suspensão, remoção ou abstenção de veiculação do conteúdo descrito')
            r['sinopse']=r['objeto']+'. '+resultado+' '+fund
            r['motivo']=fund
            if i in {170,180,187,189,191}:
                nota=' A extinção superveniente após as eleições não substitui o resultado comparável do referendo anterior, documentado na peça de referência.'
                r['motivo']+=nota;r['sinopse']+=nota
            pronto=bool(r['objeto']) and r['data_ato_referencia']<='2026-10-31'
            r['revisao'].update(estado='objeto, resultado, fundamento e data conferidos nas peças disponíveis' if pronto else 'pendência documental de objeto ou data',pronto_publicacao=pronto,utilizar_em_percentuais_finais=pronto,pendencias=[] if pronto else ['Completar a identificação documental do objeto ou da data.'])
            r['grau_certeza']='alto' if pronto else 'pendente'
        else:
            r['fundamento']=r['motivo']
            if not r['objeto']:
                r['objeto']='Pedido sem resultado comparável de circulação ou resposta documentado até o corte'
            r['sinopse']=r['objeto']+'. '+r['motivo']
            r['revisao'].update(estado='exclusão documentada; fora dos percentuais',pronto_publicacao=True,utilizar_em_percentuais_finais=False,pendencias=[])
        if i==203:
            r['revisao'].update(estado='pendente de reconciliação com suspensão presidencial em processo conexo',pronto_publicacao=False,utilizar_em_percentuais_finais=False,pendencias=['Reconciliar a decisão da AIJE com a Suspensão de Segurança 0602844-54 e as peças da PetCiv 0602791-73, sem atribuir o ato de outro processo à AIJE.'])
        r['unidade_classificacao']='CNJ e pedido da campanha autora; atendimento parcial positivo; não atribui responsabilidade pessoal a todos os representados'
        r['revisao']['polos_formais']='Campanha autora e campanha oposta identificadas nos polos da peça/inventário; o ingresso somente como terceiro interessado não conta como polo oposto.'
        if i==219:r['revisao']['polos_formais']='Flávio admitido somente como terceiro interessado em ação contra Meta; excluído do confronto.'
    path.write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coleg_path=ROOT/'colegialidade_curadoria_novos_a.json'
    coleg=json.loads(coleg_path.read_text(encoding='utf-8'))
    for cnj,r in dados.items():
        coleg[cnj].update(data_referencia=r['data_ato_referencia'],revisao_final_pendente=not r['revisao']['pronto_publicacao'])
    coleg_path.write_text(json.dumps(coleg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Categorias:',Counter(r['categoria'] for r in dados.values()))
    print('Incluídos:',sum(r['incluir'] for r in dados.values()))
    print('Prontos:',sum(r['revisao']['pronto_publicacao'] for r in dados.values()))


if __name__=='__main__':main()
