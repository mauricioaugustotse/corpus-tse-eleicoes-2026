"""Registra a primeira revisão documental do lote A; não publica nem calcula taxas finais.

Os índices abaixo são decisões de leitura humana dos dispositivos, não regras de
classificação por palavras-chave. As regex apenas localizam trechos e datas.
"""
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent

GRUPOS = {
    'deferido': [7,10,14,16,21,23,28,43,73,80,89,97,99,100,117,126,152,158,173,176,180,182,187,190,191,207,208,209,218,224,225],
    'parcial': [9,13,24,27,29,49,67,72,84,92,93,94,95,98,130,163,188,198,199,204,210,211,214,215,216,223,227,228,229],
    'liminar_indeferida': [0,1,2,3,4,5,8,11,12,15,17,25,26,30,38,40,42,45,48,54,55,62,65,70,71,76,96,102,104,105,113,116,123,137,142,146,147,151,156,162,170,184,185,186,189,201,205,206,212,213,222,226],
    'improcedente': [18,19,20,22,32,47,51,52,53,56,58,60,61,63,64,66,68,74,75,79,83,86,87,88,91,101,108,109,111,112,115,119,120,121,124,128,129,131,132,133,134,135,136,139,141,143,144,149,150,154,159,168,169,171,172,177,178,193,194,200],
    'perda_objeto_sem_resultado': [31,33,34,35,36,37,39,41,46,50,57,59,78,81,82,85,90,103,106,107,110,114,118,122,125,127,138,140,145,148,153,155,157,160,161,165,166,175,181,192,202],
    'ilegitimidade_sem_resultado': [167,174,179,183],
    'processual': [6,44,69,77,164,195,196,197,203,217,220,221],
    'fora_confronto': [219],
}

OBJETOS = {
 0: 'Discurso de Lula na II Conferência Nacional do Trabalho e expressão votar em quem tem sorte',
 1: 'Críticas a Flávio Bolsonaro em inauguração de setor do Hospital Federal do Andaraí',
 2: 'Suposto uso eleitoral de eventos institucionais e da inauguração do Hospital do Andaraí',
 3: 'Pronunciamento oficial de Lula na véspera do Dia Internacional da Mulher',
 4: 'Entrevista de Lula no Palácio do Planalto a Brasil247, Fórum e DCM',
 5: 'Vídeos de Flávio Bolsonaro sobre CPI do Banco Master e Partido dos Trabalhadores',
 6: 'Alegado uso de eventos oficiais na Bahia para promoção eleitoral de Lula',
 7: 'Vídeo de Flávio que associa Lula ao PCC e ao Comando Vermelho no debate sobre tarifas e Marco Rubio',
 8: 'Imagem manipulada de Lula agradecendo a Bolsonaro pela criação do PIX',
 9: 'Conjunto de publicações e perfis com conteúdo sintético e propaganda negativa contra Lula',
 10: 'Publicação de Flávio que associa Lula a organizações criminosas',
 11: 'Uso de entrevistas e visitas institucionais de Lula para promoção eleitoral',
 12: 'Discurso de Flávio em Copacabana sobre governo, soberania e crime organizado',
 13: 'Inserção televisiva sem nomes dos candidatos e divulgação de site de propaganda negativa',
 14: 'Vídeo com jingle e fantoches gerados por inteligência artificial contra Lula',
 15: 'Inserção sobre escala 6x1 e sátira da escala 3x4 de Flávio',
 16: 'Inserção de rádio que atribui a Lula desprezo pelos garis',
 17: 'Vídeos nas redes de Flávio, PL e Nikolas sobre fala de Lula a respeito dos garis',
 18: 'Pedido de resposta à inserção sobre escala 6x1 e escala 3x4',
 19: 'Pedido de resposta à inserção sobre escala 6x1 e escala 3x4',
 20: 'Pedido de resposta contra propaganda da campanha Lula',
 21: 'Inserção de rádio com recorte da fala de Lula sobre garis',
 22: 'Pedido de resposta contra propaganda da campanha Lula',
 23: 'Propaganda televisiva com recorte da fala de Lula sobre garis',
 24: 'Impulsionamento pago de propaganda negativa por Flávio e outros representados',
 25: 'Inserção televisiva e emprego da expressão flagrado pela Polícia Federal',
 26: 'Impulsionamento pago de vídeo negativo por Flávio Bolsonaro',
 27: 'Publicações de Flávio, PL e Nikolas com recorte da fala de Lula sobre garis',
 28: 'Reel do PL com recorte da fala de Lula sobre garis',
 29: 'Propaganda eleitoral em site e comunicação do endereço à Justiça Eleitoral',
 30: 'Suposto impulsionamento pago de conteúdo negativo contra Flávio',
 32: 'Crítica à política de segurança pública do governo Bolsonaro',
 38: 'Inserção televisiva e associação de Lula ou de seu partido a organizações criminosas',
 43: 'Inserção de rádio cujo conteúdo foi considerado ofensivo e anti-institucional no referendo',
 44: 'Inserção Eu vou fazer um tesouraço nos impostos e referência a roubalheira do atual governo',
 49: 'Impulsionamento pago de conteúdos negativos contra Flávio em Facebook e Instagram',
 51: 'Vídeos sobre CPMI do INSS, Lula e o Partido dos Trabalhadores',
 53: 'Publicação Sanguessuga do povo sobre arrecadação de tributos pelo governo Lula',
 69: 'Inserção Eu vou fazer um tesouraço nos impostos já suspensa em outro processo',
 77: 'Inserção Eu vou fazer um tesouraço nos impostos já suspensa em outro processo',
 163: 'Propaganda sobre milícias, PIX, salário mínimo e tentativa de golpe',
 164: 'AIJE com pedidos de remoção e restrição de canais sem delimitação suficiente',
 195: 'Tutela antecedente sobre despesas de jantar eleitoral com empresários em São Paulo',
 196: 'Conexão e prevenção em pedido de direito de resposta',
 197: 'Conexão e prevenção em representação sobre publicações relativas à religião',
 203: 'AIJE contra Lula, Alckmin e Janones sobre o canal Exército do Lula',
 217: 'AIJE contra Lula e Alckmin com pedidos de suspensão de perfis e preservação de dados',
 219: 'Medidas de recomendação e moderação aplicadas pela Meta a conteúdos eleitorais',
 220: 'AIJE sobre publicações de Pablo Marçal e projeto Brasil 22 Token',
 221: 'Conexão e prevenção em representação sobre incêndios em universidades',
 227: 'Inserção televisiva Filme 40 – Lula – Nesta eleição, você tem dois lados bem diferentes',
}

EXCECOES_FONTE = {170: 180190787, 180: 180190784, 187: 180190783, 189: 180190785, 191: 180190782}


def normalizar(texto):
    return re.sub(r'\s+', ' ', texto)


def main():
    dossies = json.loads((ROOT / 'coleta_documental/auditoria/dossies_novos_a.json').read_text(encoding='utf-8'))
    suplemento = json.loads((ROOT / 'suplemento_documental_auditoria.json').read_text(encoding='utf-8'))
    mapa = {}
    for grupo, indices in GRUPOS.items():
        for indice in indices:
            if indice in mapa:raise ValueError(f'índice repetido {indice}')
            mapa[indice] = grupo
    if set(mapa) != set(range(230)):raise ValueError(f'índices ausentes: {set(range(230))-set(mapa)}')
    saida = {}
    for cnj, r in dossies.items():
        indice = r['indice']; grupo = mapa[indice]
        ref = r['selecionado']
        if indice in EXCECOES_FONTE:
            ref = next(d for d in r['documentos'] if d['id_documento'] == EXCECOES_FONTE[indice])
        if indice == 141:
            ref = next(d for d in suplemento if d['id_documento'] == 179954170)
        if indice == 220:
            ref = next(d for d in suplemento if d['id_documento'] == 179920192)
        texto = normalizar((ROOT / ref['arquivo']).with_suffix('.txt').read_text(encoding='utf-8'))
        marcadores = list(re.finditer(r'Decis.o:\s*O Tribunal|DECIS.O\s+O Tribunal', texto))
        if not marcadores:marcadores = list(re.finditer(r'Ante o exposto|Diante do exposto|Isso posto|Pelo exposto', texto))
        inicio = marcadores[-1].start() if marcadores else max(0, len(texto)-1500)
        evidencia = texto[inicio:inicio+3000]
        fases = {'deferido': ('deferido', True), 'parcial': ('parcial', True),
                 'liminar_indeferida': ('indeferido', False), 'improcedente': ('improcedente', False)}
        incluir = grupo in fases
        grau, atendido = fases.get(grupo, ('sem resultado comparável', None))
        status = {'deferido': 'pedido atendido; conferir extensão na revisão narrativa',
                  'parcial': 'pedido parcialmente atendido',
                  'liminar_indeferida': 'tutela de urgência indeferida ou negativa mantida em referendo',
                  'improcedente': 'pedido rejeitado no julgamento comparável',
                  'perda_objeto_sem_resultado': 'extinção após eleições; sem resultado comparável anterior encontrado',
                  'ilegitimidade_sem_resultado': 'extinção sem mérito por ilegitimidade',
                  'processual': 'ato sem resultado comparável de circulação ou resposta',
                  'fora_confronto': 'campanha contrária não figura em polo oposto; terceiro interessado'}[grupo]
        motivo = status + '.'
        if indice in EXCECOES_FONTE:
            motivo += ' A extinção superveniente por encerramento das eleições não substitui o referendo comparável anterior.'
        if indice in [139,169]:
            motivo = 'Negativa de seguimento fundada no exame material da propaganda: a peça afasta falsidade, ofensa e os pedidos de remoção e multa; resultado negativo comparável.'
        if indice == 6:motivo = 'Extinção sem mérito por inadequação da via; matéria de abuso depende de ação eleitoral própria.'
        if indice == 44:motivo = 'Decadência do direito de resposta; a peça não examina o conteúdo material da propaganda.'
        if indice in [69,77]:motivo = 'Pedido cautelar prejudicado porque a propaganda já fora suspensa no DR0602162-02; não constitui novo resultado autônomo neste CNJ.'
        if indice == 195:motivo = 'Tutela probatória sobre despesas de jantar de campanha; não decide circulação de propaganda ou concessão de resposta.'
        if indice in [196,197,221]:motivo = 'Decisão apenas sobre conexão e prevenção; não aprecia a circulação do conteúdo.'
        if indice in [164,217,220]:motivo = 'Pedidos de urgência reservados até esclarecimentos e delimitação das providências; não há resultado comparável de circulação.'
        if indice == 203:motivo = 'Decisão na AIJE restabelece canal e impõe abstenção de conteúdos já tidos por ilícitos, mas há suspensão presidencial superveniente em processo conexo; resultado agregado exige reconciliação das peças antes de entrar nos percentuais.'
        if indice == 219:motivo = 'Ação da campanha Lula contra Meta; Flávio ingressa somente como terceiro interessado. Não há campanhas em polos processuais opostos.'
        datas = list(re.finditer(r'SESS.O[^.]{0,80}?(\d{1,2})\.(\d{1,2})\.(2026)', texto[-7000:]))
        data_ref = ref['data_metadata']; origem_data = 'metadado; conferência da data escrita pendente'
        if datas:
            m=datas[-1];data_ref=f'{m[3]}-{int(m[2]):02d}-{int(m[1]):02d}';origem_data='data da sessão escrita no extrato da ata'
        if indice==13:data_ref='2026-09-27';origem_data='data escrita no dispositivo da decisão'
        if indice==42:data_ref='2026-10-19';origem_data='data escrita no dispositivo da decisão'
        if indice==45:data_ref='2026-10-13';origem_data='data escrita no dispositivo da decisão'
        if indice==48:data_ref='2026-09-30';origem_data='data escrita no dispositivo da decisão'
        if indice in [69,77]:data_ref='2026-10-14';origem_data='data escrita no dispositivo da decisão'
        if indice==55:data_ref='2026-10-22';origem_data='data escrita no dispositivo da decisão'
        if indice==80:data_ref='2026-10-11';origem_data='data da sessão escrita no extrato da ata'
        if indice==141:data_ref='2026-10-14';origem_data='data da sessão escrita no extrato da ata e certidão'
        if indice==172:data_ref='2026-10-21';origem_data='data escrita no dispositivo da decisão'
        pedido = 'direito de resposta e providências de remoção ou abstenção, conforme peça oficial' if r['triagem']['classe']=='DR' else 'restrição da propaganda ou demais providências descritas na peça oficial'
        objeto = OBJETOS.get(indice, '')
        trecho = re.search(r'Trata-se|Cuida-se|I\. Caso em exame|I\. CASO EM EXAME', texto)
        inicio_obj = trecho.start() if trecho else min(700,len(texto))
        saida[cnj] = {'campanha_autora': 'Flávio' if 'Flávio' in r['triagem']['campanha_ativa_detectada'] else 'Lula',
                      'incluir': incluir, 'categoria': grupo, 'motivo': motivo, 'objeto': objeto,
                      'pedido': pedido, 'sinopse': motivo, 'atendido': atendido, 'grau': grau, 'status': status,
                      'url_peca': ref['url'], 'tipo_peca': ref['tipo'], 'data_ato_referencia': data_ref,
                      'data_metadata': ref['data_metadata'], 'origem_data_referencia': origem_data,
                      'fonte_classificacao': 'peça oficial da Consulta Unificada; dispositivo ou extrato da ata lido',
                      'grau_certeza': 'resultado documentado; revisão narrativa pendente',
                      'status_fonte': 'arquivo íntegro e URL oficial preservados', 'arquivo_peca': ref['arquivo'],
                      'sha256_peca': ref['sha256'], 'id_documento': ref['id_documento'],
                      'evidencia_resultado': evidencia, 'trecho_objeto_para_revisao': texto[inicio_obj:inicio_obj+2400],
                      'revisao': {'estado': 'primeira revisão de dispositivos concluída; revisão integral pendente',
                                  'indice_lote': indice, 'codigo_leitura': grupo,
                                  'pronto_publicacao': False, 'utilizar_em_percentuais_finais': False,
                                  'pendencias': ['Completar e conferir objeto, pedido, fundamento e sinopse narrativa.',
                                                 'Reconciliar todas as peças e datas escritas para confirmar a última referência comparável.',
                                                 'Conferir enquadramento dos representantes formais em campanhas opostas.']}}
    (ROOT/'curadoria_novos_a.json').write_text(json.dumps(saida,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(Counter(r['categoria'] for r in saida.values()))


if __name__ == '__main__':main()
