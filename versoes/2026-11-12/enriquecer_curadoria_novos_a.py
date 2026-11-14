"""Acrescenta os estados de colegialidade revistos ao lote A, sem inferir resultados."""
from pathlib import Path
import json
from collections import Counter
from auditar_coleta import DIAGNOSTICOS

ROOT = Path(__file__).resolve().parent


def main():
    path = ROOT/'curadoria_novos_a.json'
    dados = json.loads(path.read_text(encoding='utf-8'))
    modificados = {7,10,14,16,21,23,27,28,43,163,201}
    coleg_merito = {32,51,53,58,64,66,79,80,86,108,109,111,120,121,124,128,131,132,133,141,154,159,171,178,193,194,200}
    merito_positivo = {24,72,92,93,94,95,130,158,227}
    objetos = {
        42:'Publicações que associam Lula a investigações envolvendo Fábio Luís Lula da Silva e Roberta Luchsinger',
        45:'Propaganda televisiva de Flávio sobre desequilíbrio institucional e atuação do governo Lula',
        48:'Vídeo nas redes de Flávio e Alfredo Gaspar sobre atuação do governo Lula',
        54:'Podcast no Alvorada, sanção da política de minerais e encontro religioso no Planalto',
        55:'Vídeo do PL sobre Fábio Luís Lula da Silva, Rafael Nicolau Arbex e investigações',
        58:'Publicação do PL sobre investigações envolvendo filho de Lula e terceiros',
        62:'Propaganda que afirma que os problemas pioraram sob governos do PT e mostra homens armados',
        63:'Propaganda que usa a expressão mesmo DNA para associar Lula a condutas atribuídas a seu filho',
        64:'Vídeo do PL sobre irregularidades investigadas envolvendo familiares de Lula e integrantes do governo',
        65:'Propaganda televisiva negativa contra Lula cuja suspensão cautelar foi pedida',
        66:'Publicação sobre Banco Master, Campos Neto e participação de Flávio em eventos de Vorcaro',
        67:'Vídeo sobre castração química e acusação de estupro de vulnerável contra candidato a vice-presidente',
        70:'Bloco televisivo sobre governos do PT com exibição de indivíduos armados',
        71:'Propaganda televisiva supostamente falsa e descontextualizada contra Lula',
        72:'Impulsionamento de vídeo Quanto tá a picanha na sua cidade com declarações contrastantes de Lula',
        73:'Inserção Eu vou fazer um tesouraço nos impostos',
        76:'Eventos oficiais, estrutura estatal e publicidade institucional em benefício da reeleição',
        79:'Vídeo que atribui a Lula responsabilidade pelo endividamento das famílias',
        80:'Vídeo de inteligência artificial sem identificação acessível do uso da tecnologia',
        83:'Propaganda sobre transferência de renda e emancipação econômica dos beneficiários',
        84:'Carrossel do PL com imagem de Lula e manchetes de 2004, 2005, 2014, 2016 e 2025',
        86:'Vídeo com manchetes Antes do Lula e Depois do Lula e imagens de violência e economia',
        87:'Publicação Um verdadeiro tesouro em dívidas sobre dívida pública',
        88:'Publicação sobre recuperação judicial da rede Habib’s e governo Lula',
        89:'Publicação do PL sobre povo roubado aos poucos e garras sujas do PT',
        91:'Publicação Descaso petista sobre mortes no território Yanomami',
        92:'Impulsionamento do anúncio Meta 937668076055278 contra Lula',
        93:'Impulsionamento do anúncio Meta 1819467069049050 contra Lula',
        94:'Impulsionamento do anúncio Meta 978240255290492 contra Lula',
        95:'Impulsionamento do anúncio Meta 4216142548608182 contra Lula',
        96:'Inserção radiofônica cuja repetição a campanha Lula busca impedir',
        97:'Vídeo Explicando o escândalo master em 30 segundos e alegação de valores recebidos por Flávio',
        98:'Discurso de Lula na Assembleia Geral da ONU e uso eleitoral de sua divulgação',
        99:'Publicação sobre Flávio, Daniel Vorcaro e Banco Master',
        100:'Impulsionamento de três anúncios negativos contra Flávio em Facebook e Instagram',
        102:'Inserção radiofônica que intercala falas de Lula com a palavra Mentira',
        104:'Publicação do PT sobre suposta tentativa de Flávio de impedir medicamentos para emagrecimento no SUS',
        105:'Montagem que associa emenda de Flávio ao homicídio de Marielle Franco',
        108:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        109:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        111:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        112:'Áudio 24 que atribui aos Bolsonaros responsabilidade pela expansão das bets',
        113:'Propaganda de Lula com imagens de aplausos da ONU atribuídos a outro pronunciamento',
        116:'Entrevista de Lula que associa Flávio e sua família a milicianos',
        117:'Reprodução de entrevista de Lula ao SBT pelo perfil do Instituto Lula',
        119:'Propaganda que afirma que Flávio ataca reajuste do Bolsa Família',
        120:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        121:'Inserções que atribuem a Flávio intenção de realizar cortes de despesas públicas',
        123:'Publicação que relaciona aquisição de imóveis da família Bolsonaro a pagamentos em espécie',
        124:'Vídeo colaborativo sobre sigilo de processo envolvendo Flávio e sua capivara',
        126:'Publicações que associam Lula à proteção do PCC e do Comando Vermelho em telegramas diplomáticos',
        128:'Inserções televisivas que atribuem a Flávio responsabilidade pela expansão das bets',
        129:'Inserções televisivas sobre Lula, Flávio, Bolsonaro e a expansão das bets',
        130:'Impulsionamento de três anúncios negativos da campanha Lula contra Flávio',
        134:'Vídeo de Flávio que contrapõe falas de Lula sobre preço da carne',
        135:'Animação produzida por inteligência artificial ambientada em 2036',
        137:'Vídeo do PT que associa escritório de Flávio a empresas vinculadas ao Careca do INSS',
        139:'Publicação colaborativa de Lula com a frase Vamos provar quem é corrupto nesse país',
        141:'Inserções televisivas que atribuem a Flávio responsabilidade pela expansão das bets',
        142:'Vídeo de sabatina sobre fraudes no INSS montadas em 2019 e ressarcimento dos aposentados',
        143:'Reel de Lula que contrapõe projetos de país, democracia e autoritarismo',
        144:'Reel de Lula que contrapõe projetos de país, democracia e autoritarismo',
        146:'Vídeo no Instagram sobre instituição financeira e seu controlador em governos distintos',
        147:'Vídeo que associa Flávio e sua família à submissão a interesses estrangeiros',
        149:'Inserção televisiva que chama o PT de partido do Tigrinho',
        150:'Inserção televisiva que chama o PT de partido do Tigrinho',
        151:'Publicação que associa Lula e seu governo à epidemia das bets e ao endividamento',
        152:'Propaganda radiofônica com trecho de entrevista alegadamente descontextualizado',
        154:'Publicação que associa Lula e seu governo à epidemia das bets e ao endividamento',
        156:'Vídeo de Lula com críticas à atuação de Flávio e à política econômica do governo Bolsonaro',
        158:'Impulsionamento do anúncio Meta 1420886753338283 sobre Flávio e escala 6x1',
        159:'Vídeo do PT que encadeia episódios envolvendo Adriano da Nóbrega, Rodrigo Bacellar e Daniel Vorcaro',
        162:'Publicação colaborativa que associa Flávio a instituição financeira e supostas fraudes',
        168:'Inserção televisiva que chama o PT de partido do Tigrinho',
        169:'Vídeo colaborativo no perfil Brasil com Lula com críticas a Flávio e à sua credibilidade',
        170:'Inserção que atribui aos Bolsonaros responsabilidade pelo crescimento dos jogos de azar',
        171:'Publicação Flávio Bolsobet contra o povo com manchete jornalística',
        172:'Publicação Flávio Bolsobet contra o povo com manchete jornalística',
        173:'Evento Cultura com Lula na Fundição Progresso e alegação de showmício',
        176:'Inserção radiofônica com trecho de entrevista de candidato alegadamente descontextualizado',
        177:'Inserção que chama o PT de partido do Tigrinho e discute cassinos online',
        178:'Nota de repúdio radiofônica sobre críticas de Flávio à CNBB e à Igreja Católica',
        180:'Inserção televisiva que apresenta Flávio como político desonesto e mentiroso',
        182:'Vídeos com fala de Lula sobre câncer de próstata apresentada com conotação sexual envolvendo crianças',
        184:'Vídeo Um Brasil seguro ainda pode renascer que associa Lula e PT ao narcotráfico',
        185:'Montagem negativa contra Lula com associação ao narcotráfico',
        186:'Inserção sobre declarações de Paulo Guedes em 2020 e responsabilidade pelas bets',
        187:'Vídeos com fala de Lula sobre câncer de próstata apresentada com conotação sexual envolvendo crianças',
        188:'Vídeo supostamente manipulado de declaração de candidato, objeto de emenda à inicial',
        189:'Inserção sobre declarações de Paulo Guedes em 2020 e responsabilidade pelas bets',
        190:'Inserção televisiva com fala de Lula sobre saúde apresentada com conotação sexual envolvendo crianças',
        191:'Inserção televisiva com fala de Lula sobre câncer de próstata apresentada com conotação sexual envolvendo crianças',
        193:'Vídeo que relaciona equipe econômica de Flávio à situação econômica e social da Argentina',
        194:'Propaganda que afirma que Flávio nunca trabalhou na vida e o qualifica de mentiroso',
        198:'Vídeo de Lula que atribui crimes a Flávio',
        201:'Vídeo que associa Flávio a apoiadores e reportagens sobre crimes atribuídos a terceiros',
        204:'Impulsionamento de 386 anúncios de vídeo negativo contra Flávio',
        205:'Impulsionamento de conteúdo negativo contra Flávio',
        206:'Impulsionamento de anúncio negativo no Instagram',
        207:'Impulsionamento de vídeo que atribui relações de Flávio com milicianos',
        208:'Impulsionamento de Nota Oficial sobre supostos ataques de Flávio à CNBB e à Igreja Católica',
        209:'Impulsionamento de propaganda sobre Bolsonaro, Paulo Guedes e expansão das bets',
        210:'Impulsionamento de vídeo que associa Flávio à defesa de acusado pela morte de uma criança',
        211:'Impulsionamento de vídeo que associa Flávio à defesa de milícias e organizações criminosas',
        212:'Impulsionamento de 372 anúncios de vídeo negativo contra Flávio',
        213:'Impulsionamento de anúncio negativo no Instagram',
        214:'Impulsionamento de vídeo sobre Flávio e fim da escala 6x1',
        215:'Vídeo que atribui a Flávio propostas de cortes de programas sociais e salário mínimo',
        216:'Vídeo Se Flávio vence, você perde e consequências atribuídas à sua eventual vitória',
        218:'Brasil 22 Token e suposta remuneração de eleitores com criptoativos',
        222:'Inserção televisiva e destaque dos nomes dos candidatos à Presidência e Vice-Presidência',
        223:'Publicações que atribuem a Flávio propostas de extinção de direitos trabalhistas e previdenciários',
        224:'Propaganda com inteligência artificial que associa armas e atuação de Flávio à violência escolar',
        225:'Impulsionamento de propaganda eleitoral negativa e alegada manipulação audiovisual',
        226:'Impulsionamento pago de propaganda eleitoral negativa contra Flávio',
        228:'Impulsionamento de vídeo que associa vitória de Flávio à perda de benefícios sociais e serviços',
        229:'Centenas de anúncios patrocinados que atribuem ligação de Flávio com o crime organizado',
    }
    saida = {}
    for cnj, r in dados.items():
        indice = r['revisao']['indice_lote']
        if indice in objetos:r['objeto']=objetos[indice]
        if r.get('objeto'):r['sinopse']=r['objeto']+'. '+r['motivo']
        if indice in modificados:
            situacao = 'liminar modificada'
            motivo = 'O extrato da ata documenta a não confirmação total ou parcial da tutela individual e a alteração das determinações; ver evidência do resultado.'
        elif indice in coleg_merito:
            situacao = 'decisão colegiada de mérito'
            motivo = 'O extrato da ata decide o pedido principal de resposta ou a representação, não apenas o referendo de tutela provisória.'
        elif r['tipo_peca'].startswith('Ac'):
            situacao = 'liminar mantida'
            motivo = 'O extrato da ata confirma a tutela individual deferida, parcial ou indeferida, conforme a referência indicada.'
        elif r['categoria']=='improcedente' or indice in merito_positivo:
            situacao = 'decisão individual de mérito'
            motivo = 'Dispositivo individual julga o pedido material; não foi identificada decisão colegiada posterior comparável no lote de peças deste CNJ.'
        else:
            situacao = 'sem revisão comprovada'
            motivo = 'Não foi identificado pronunciamento colegiado comparável nas peças consultadas; isso não prova que não tenha havido revisão.'
        if indice in {203,219}:
            situacao = 'pendente'
            motivo = 'Há desdobramentos em processos conexos ou questão de enquadramento como confronto; reconciliar antes de comparar tutela individual e colegiada.'
        r['colegialidade_situacao'] = situacao
        r['colegialidade_justificativa'] = motivo
        saida[cnj] = {'situacao':situacao,'justificativa':motivo,'url_peca':r['url_peca'],
                      'arquivo_peca':r['arquivo_peca'],'id_documento':r['id_documento'],
                      'data_referencia':r['data_ato_referencia'],'evidencia_resultado':r['evidencia_resultado'],
                      'revisao_final_pendente':True}
    path.write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'colegialidade_curadoria_novos_a.json').write_text(json.dumps(saida,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    # Corrige e documenta a recuperação cuja identidade foi esclarecida por despacho.
    audit_path = ROOT/'auditoria_coleta.json'
    auditoria = json.loads(audit_path.read_text(encoding='utf-8'))
    for r in auditoria['pendencias']:
        if r['id_documento']==179920192:r['diagnostico'],r['justificativa']=DIAGNOSTICOS[179920192]
    diagnosticos=auditoria['resumo']['diagnosticos_pendencias']
    diagnosticos.pop('inconsistencia_no_cabecalho_original',None)
    diagnosticos['cabecalho_retificado_por_despacho']=1
    audit_path.write_text(json.dumps(auditoria,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    supl_path=ROOT/'suplemento_documental_auditoria.json'
    supl=json.loads(supl_path.read_text(encoding='utf-8'))
    for r in supl:
        if r['id_documento']==179920192:r['validacao_identidade']=DIAGNOSTICOS[179920192][1]
        elif r['id_documento'] in {179935558,177502007,177502006,177502004,177502005,179954170,179526290}:
            r['validacao_identidade']='Conferência documental manual de cabeçalho abreviado, conjunto ou com espaço; ver auditoria_coleta.json.'
        else:r['validacao_identidade']='CNJ completo no cabeçalho.'
    supl_path.write_text(json.dumps(supl,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=ROOT/'auditoria_coleta.md'
    linhas=md.read_text(encoding='utf-8').splitlines()
    linhas=[linha for linha in linhas if not linha.startswith('O despacho179920899')]
    for i,linha in enumerate(linhas):
        if '| 179920192 |' in linha:
            linhas[i]=f'| 0602747-54.2026.6.00.0000 | 179920192 | {DIAGNOSTICOS[179920192][0]} | {DIAGNOSTICOS[179920192][1]} |'
    linhas.extend(['','O despacho 179920899 de 11/10/2026 corrige expressamente o cabeçalho da decisão 179920192 da AIJE 0602747-54. Essa peça foi incorporada ao suplemento com referência à retificação; 13 das 15 recuperadas são admitidas como peças próprias, permanecendo duas como anexos contextuais.',''])
    md.write_text('\n'.join(linhas),encoding='utf-8')
    print(Counter(r['situacao'] for r in saida.values()))


if __name__=='__main__':main()
