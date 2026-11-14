"""Materializa anotações da leitura jurídica dos novos alvos 230:460.

Os conjuntos de resultados abaixo são anotações manuais. Expressões regulares
apenas recortam testemunhos, datas e identificadores para rastreabilidade.
"""
import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
POSITIVOS={1,15,17,18,19,22,27,28,29,31,32,42,45,57,58,59,60,62,63,64,65,67,68,69,70,75,80,84,85,87,90,94,96,97,99,103,105,108,114,115,117,118,120,123,124,132,138,143,145,146,148,149,153,154,161,173,176,178,179,180,181,183,188,197,198,200,202,204,206,213,215,217,218,227}
NEGATIVOS={4,8,10,12,13,14,16,20,21,25,26,30,33,34,35,36,37,38,39,40,46,47,49,51,53,61,71,73,74,77,78,79,81,89,91,92,93,95,102,109,110,111,112,113,116,119,126,127,130,133,136,137,142,150,155,159,170,172,185,187,189,190,192,195,225,226,228}
PARCIAIS={1,18,28,29,42,45,57,60,63,67,69,75,84,85,87,94,96,99,114,118,123,132,146,148,149,153,178,179,180,181,183,197,198,202,227}
MERITO={4,8,10,12,20,21,25,26,33,38,40,46,47,49,73,102}
REVOGADAS={39,89,91,92}
INATIVOS={6,44,55,83,207,208,220,222,223,224}
ADIADOS={66,76,98,163}
DUPLICADOS={100,107,121,141,144,162,175,186,199,205,212,214,216,219}
REFERENCIA={92:1,95:1,110:1,126:1,202:2}

TITULOS={
4:'Cortes orçamentários e programas sociais em propaganda televisiva',
8:'Cortes orçamentários e programas sociais em propaganda de rádio',
10:'Cortes orçamentários e política de armas em propaganda de TV',
12:'Política de armas e organizações criminosas em inserções de rádio',
13:'“Tesouraço”, Farmácia Popular, câncer e habitação na TV',
14:'“Tesouraço”, combate ao câncer e habitação no rádio',
16:'Acesso a armas e violência em propaganda de rádio',
20:'“O Brasil tá sem presidente”: bloco da tarde de 09/10',
21:'“O Brasil tá sem presidente”: bloco noturno de 09/10',
25:'Cortes orçamentários e programas sociais em inserções de rádio',
26:'Política de armas e violência em inserções de rádio',
33:'“O Brasil tá sem presidente”: bloco de TV de 10/10',
40:'“Tesouraço” e programas sociais nas redes sociais',
46:'Cortes orçamentários e programas sociais no rádio',
47:'Cortes orçamentários e programas sociais em nova propaganda de rádio',
49:'Política de flexibilização de armas e criminalidade no rádio',
73:'“Tesouraço” e programas sociais em inserções televisivas',
1:'Vídeo pago “Com Flávio Bolsonaro, você perde” e segurança de crianças',
15:'Inserção de Flávio sem identificação do vice',17:'Outra inserção de Flávio sem identificação do vice',
18:'Programa de TV de 09/10: vice, ajuste fiscal e inteligência artificial',19:'Identificação do vice em propaganda de Flávio',
22:'“Lula prometeu picanha, mas entregou a fila do osso”: inserção de 10/10',
24:'Vídeo de Pablo Marçal sobre Lula e religiosidade',27:'Inserção sem nome do vice de Flávio',
28:'Impulsionamento de conteúdo negativo contra Flávio',29:'Programa de TV de 10/10: vice, programas sociais e IA',
30:'Vídeo sobre governos do PT com imagens de indivíduos armados',31:'Montagem de declarações de Lula nas redes sociais',
32:'“Vem com Flávio”: vice e tempo de apoiadores em inserção',
34:'Programa noturno de TV de 10/10 contestado pela coligação de Lula',
35:'“O Brasil está sem presidente” e identificação do vice',36:'Programa de TV de 10/10 contestado pela coligação de Lula',
37:'Publicação crítica a Lula nas redes sociais',
38:'Inserção de rádio com interjeições “Mentira!”',39:'Crítica ao “tesouraço”: retirada revogada no referendo',
42:'Publicação do PT sobre corte de R$ 250 bilhões',45:'Publicações sobre a Marcha pela Democracia na Avenida Paulista',
51:'Montagem com tesoura e Farmácia Popular',53:'Vídeo de Flávio apontado como desinformativo',
57:'“Votar em Flávio” e “milícia no poder” em publicação colaborativa',58:'Publicação que atribuía a Lula intenção de fechar igrejas',
59:'Anúncio pago que atribuía a Lula o abandono do País',60:'Outro anúncio pago sobre o abandono do País',
61:'Pedido de resposta a vídeo com indivíduos armados',62:'“Fila do osso”: inserção de 11/10',
63:'Nome do vice em propaganda de Flávio',64:'Inserção “Vem com Flávio” de 11/10',
65:'Alegação de R$ 7 bilhões em viagens de Lula e da primeira-dama',
67:'Vídeo com crianças em encenação no Dia das Crianças',68:'“Lula prometeu picanha”: inserções televisivas',
69:'Identificação do vice em propaganda televisiva',70:'“Vem com Flávio”: inserção de 12/10',
71:'Crítica ao “tesouraço” em propaganda de rádio',74:'Publicação negativa contra Lula',
75:'Imagem sintética de mulher limpando a estação Trianon-Masp',
77:'Pedido de resposta ao programa noturno de TV de 12/10',78:'Programa noturno de TV de 12/10',
79:'“Brasil sem presidente”, saída temporária e nome do vice',80:'Vídeo que associa Flávio a milícias',
81:'Pedido de resposta ao bloco de TV sobre presidente e saída temporária',
82:'Estrutura de comunicação de sindicatos, estudantes e movimentos sociais',
84:'“Lembre-se do Miguel” e “Tal pai, tal filho” em anúncios pagos',
85:'Afirmação de que Lula representa e protege integrantes do PCC',
87:'Publicação colaborativa de Freixo: Vorcaro, milícia e Trump',
89:'Publicação sobre o fim da escala 6x1: remoção revogada',90:'“Fila do osso” nos perfis de Flávio e do PL',
91:'Vídeo sobre endividamento, inflação e renda: liminar revogada',
92:'Propaganda que associa Lula à criminalidade: liminar não referendada',
93:'Pedido de resposta a inserção televisiva crítica à gestão',94:'Bloco televisivo: vice e informações jornalísticas',
95:'Outro pedido de resposta a propaganda televisiva crítica',96:'Outro bloco de TV com identificação inadequada do vice',
97:'“Vem com Flávio”: inserção de 13/10',99:'Identificação do vice na propaganda de Flávio',
102:'Escala 6x1 e propostas trabalhistas em inserções televisivas',
103:'Maçã em putrefação e nome do vice em programa de 14/10',105:'Vídeo “mural de investigação” no canal Tropa do Flávio',
108:'“Flávio Bolsonaro é duas caras”: inserção sobre escala 6x1',
109:'Propaganda de rádio sobre a Marcha pela Democracia',
110:'Pedido de resposta à propaganda sobre INSS e familiares de Lula',
111:'Pedido de resposta ao programa de TV de 14/10',112:'Inserção de rádio com crítica à gestão e notícias',
113:'Inserção televisiva apontada como desinformativa',114:'Nome do vice em propaganda de Flávio',
115:'Montagem de falas de Lula com imagens de violência explícita',
116:'Bloco de TV da campanha de Lula contestado por Flávio',117:'Impulsionamento de “Com Flávio Bolsonaro, você perde”',
118:'Anúncio Meta ID 852704987899762',119:'Peça de rádio de 16/10 contestada por Flávio',
120:'“A lobista do careca do INSS”: inserções de 15/10',
123:'Programa de 15/10: vice e Marcha pela Democracia',124:'“A campanha do Lula esconde quem é o verdadeiro Lula”',
126:'Pedido de resposta a inserções de TV',127:'Informações jornalísticas em inserções de rádio de 15/10',
130:'Críticas à gestão em inserções de rádio de 15/10',
132:'Maçã apodrecida e defesa de acusado de homicídio na propaganda de Lula',
133:'Propaganda da campanha de Lula no horário eleitoral gratuito',136:'Inserções de TV de 16/10 contestadas por Lula',
137:'Pedido de resposta às inserções de TV de 16/10',
138:'“Lula sempre foi a favor da saidinha dos presos”: rádio',142:'Inserções de TV de 16/10 com críticas à gestão',
143:'“A lobista do careca do INSS”: inserções de 16/10',145:'Nome do vice na propaganda de Flávio',
146:'“Flávio já está preparando um golpe”: escala 6x1',
148:'“Preste atenção nessas informações oficiais”: milícia e escala 6x1',
149:'Recomendação de conteúdos dos perfis de Nikolas Ferreira e Pablo Marçal',
150:'Inserção radiofônica da campanha de Lula',153:'Vídeo sintético “Pegadinha do Lulão”',
154:'Montagem de falas de Lula com imagens de crime real',155:'Publicação contestada pela campanha de Lula',
159:'Críticas à gestão em inserções de rádio de 17/10',161:'“Lula sempre foi a favor da saidinha dos presos”: rádio',
166:'Promessa de emendas a municípios no encontro Missão Flávio MS',
170:'Críticas à gestão em inserções de TV de 18/10',172:'Críticas à gestão em inserções de rádio de 18/10',
173:'“Lula sempre foi a favor da saidinha dos presos”: rádio',
176:'“Sou filho do Presidente. Quer me dar?”: extensão à republicação na internet',
178:'“O Bolsa Família está ameaçado” em impulsionamentos pagos',179:'Impulsionamento de “Flávio defendeu assassino de criança”',
180:'“Abra seu sigilo bancário, Flávio Bolsonaro” em anúncios pagos',181:'Anúncio Meta ID 1833720587771128',
183:'“O Brasil precisa de pacificação, não de revanchismo”',185:'Críticas à gestão em inserções de TV de 19/10',
187:'Pedido de resposta a vídeo de Flávio publicado em 18/10',188:'“Lula sempre foi a favor da saidinha dos presos”: rádio',
189:'Vídeo de Flávio publicado no Instagram e Facebook em 18/10',190:'Críticas à gestão em inserções de rádio de 19/10',
192:'Comunicações Gov.br/WhatsApp e marca “União e Reconstrução”',195:'Sítio flaviometro.com',
197:'Desafio dos sigilos: Vorcaro, INSS e mansão em inserção de rádio',
198:'Canal Exército do Lula: liminar em mandado de segurança',200:'“A lobista do careca do INSS”: nova inserção televisiva',
202:'Amplificação de perfis e vídeo “Flavinho de Papai”',204:'“Lula sempre foi a favor da saidinha dos presos”: rádio de 20/10',
206:'Imagens de detidos em Piracicaba com camisetas de Lula',210:'Mandado de segurança sobre inclusão em pauta de direitos de resposta',
213:'Fala de Lula sobre saída temporária associada a manchetes de crimes',
215:'Saída temporária e manchetes de crimes: bloco de TV da tarde',
217:'Saída temporária e manchetes de crimes: bloco de TV da noite',218:'“Lula sempre foi a favor da saidinha dos presos”: rádio',
225:'Programa Alô Alô Brasil e uso da estrutura da Rádio Nacional',
226:'Comunicação digital da campanha de Lula: anúncios, conteúdos e coordenação',
227:'Canal Tropa do Flávio e áudio sobre supostos votos de mesários',
228:'Manifesto e formulário foraflavio.com.br e anúncios de terceiros',
}

MESES={n:i for i,n in enumerate(['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'],1)}

def texto(doc):
    return re.sub(r'\s+',' ',(ROOT/doc['arquivo']).with_suffix('.txt').read_text(encoding='utf-8')).strip() if doc.get('arquivo') else ''

def main():
    old=json.loads((ROOT.parent/'2026-10-01/curadoria_confrontos.json').read_text(encoding='utf-8'))
    cp=json.loads((ROOT/'coleta_documental/checkpoint.json').read_text(encoding='utf-8'))
    with (ROOT/'triagem_confrontos.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
    novos=sorted([r for r in rows if r['cnj'] not in old],key=lambda r:r['cnj'])[230:460]
    resultado={}
    for i,r in enumerate(novos):
        cnj=r['cnj'];docs=cp[cnj]['documentos'];ref=docs[REFERENCIA.get(i,0)];t=texto(ref)
        incluir=i in POSITIVOS or i in NEGATIVOS;atendido=i in POSITIVOS if incluir else None
        objeto=TITULOS.get(i,'Pedido de resposta à propaganda eleitoral sem resultado comunicacional autônomo')
        pedido='remoção, suspensão ou abstenção da comunicação eleitoral individualizada'
        categoria='comparável' if incluir else 'sem resultado comparável'
        grau='parcial' if i in PARCIAIS else 'atendimento documentado, extensão não discriminada' if atendido else 'não atendido' if incluir else 'sem resultado comparável'
        status='tutela provisória deferida' if atendido else 'tutela provisória indeferida' if incluir else 'encerramento sem resultado comparável documentado'
        if i in MERITO:
            status='pedido de direito de resposta improcedente';pedido='direito de resposta à comunicação eleitoral individualizada'
            justificativa='O Plenário examinou o conteúdo e julgou improcedente o pedido de direito de resposta. O julgamento não afirma a veracidade de toda a mensagem; afasta os pressupostos excepcionais da resposta.'
        elif i in REVOGADAS:
            status='tutela concessiva não referendada; efeitos afastados'
            justificativa='O Plenário não referendou a tutela concessiva; prevalece o resultado negativo mais recente, sem convertê-lo em improcedência definitiva.'
        elif incluir:
            justificativa=('A medida comunicacional individualizada foi acolhida '+('parcialmente' if i in PARCIAIS else 'na extensão documentada')+'. A ordem tem natureza cautelar e não equivale à procedência definitiva de todo o processo.' if atendido else 'O pedido de restrição da comunicação individualizada foi indeferido na etapa cautelar, por ausência dos requisitos de intervenção, sem conclusão definitiva do mérito.')
            if ref['tipo'].startswith(('Ac','Certid')):status+=' e referendada'
        elif i in INATIVOS:
            categoria='perda de objeto; publicação ou anúncio inativo'
            justificativa='A única medida de circulação ficou esvaziada pela retirada ou inatividade integral do conteúdo, sem risco concreto de reiteração. O rótulo de indeferimento não é convertido em resultado negativo comparável; a pretensão sancionatória pode prosseguir.'
        elif i in ADIADOS:
            categoria='tutela reservada; contraditório inicial'
            justificativa='O juízo reservou o exame da tutela para depois do contraditório. Não há concessão nem negativa material da medida comunicacional até o corte.'
            status='exame da tutela adiado'
        elif i in DUPLICADOS:
            categoria='tutela prejudicada por duplicidade; resposta extinta após pleito'
            justificativa='A tutela reproduzia providência examinada em outra representação e foi julgada prejudicada neste CNJ; a resposta foi posteriormente extinta após o segundo turno. O resultado do outro processo não é transplantado para este.'
        elif i==11:
            categoria='extinção sem mérito; litispendência';justificativa='O Plenário reconheceu litispendência com o DR 0602806-42 e extinguiu o processo sem exame do mérito.'
        elif i==24:
            categoria='fora do confronto formal após exclusão do candidato'
            justificativa='Flávio foi excluído por ilegitimidade passiva. A remoção do vídeo e o bloqueio de cópias atingem o terceiro Pablo Marçal; o atendimento não é atribuído à campanha adversária no comparativo.'
        elif i in {82,166}:
            categoria='tutela abstrata e instrução; sem medida comunicacional individualizada'
            justificativa='A decisão recebe a AIJE e indefere providências prospectivas ou instrutórias, sem decidir retirada ou manutenção de comunicação individualizada no recorte. Os fatos de abuso permanecem sob apuração.'
        elif i==122:
            categoria='extinção sem mérito; desistência para eliminar duplicidade'
            justificativa='O relator homologou a desistência para eliminar duplicidade, sem examinar o conteúdo da propaganda.'
        elif i==210:
            categoria='processual; pauta e perda superveniente de objeto'
            justificativa='O mandado tratava de inclusão de direitos de resposta em pauta e foi encerrado por perda superveniente do objeto, sem resultado material autônomo sobre circulação.'
        else:
            categoria='extinção sem mérito após o pleito'
            justificativa='O inventário contém apenas extinção do pedido de resposta após o segundo turno, sem resultado comparável anterior documentado neste CNJ. Não é contado como indeferimento ou improcedência.'
        if i==149:
            justificativa='A decisão de 23/10 impõe aplicação da política de não recomendação a publicações eleitorais de perfis individualizados e tutela inibitória parcial até o encerramento do segundo turno; nega a exclusão integral dos perfis das recomendações. Há candidatos da campanha adversária no polo passivo.'
        if i==192:justificativa='A reconsideração de 24/10 mantém a negativa de suspensão das comunicações governamentais individualizadas pelos canais Gov.br/WhatsApp e de retirada da marca de gestão; a instrução e a preservação de prova permanecem autônomas.'
        if i==195:justificativa='O relator nega a indisponibilização integral de flaviometro.com e defere apenas preservação e obtenção de dados. Essas diligências não contam como atendimento da medida de retirada do sítio.'
        if i==198:
            justificativa='A liminar de 23/10 suspende medidas de restrição do canal Exército do Lula em procedimentos administrativos, até decisão jurisdicional competente. A coligação impetrante tem Flávio como litisconsorte passivo formal; os demais pedidos são indeferidos.'
            status='liminar parcialmente deferida em mandado de segurança';pedido='suspensão de medidas que impedem o funcionamento do canal Exército do Lula'
        if i==202:justificativa='A decisão de 24/10 veda favorecimento algorítmico excepcional de perfis individualizados e determina revisão humana do vídeo Flavinho de Papai, com restabelecimento condicionado ao resultado dessa revisão. O restabelecimento judicial imediato e outros pedidos ficam reservados.'
        if i==225:justificativa='A decisão de 24/10 recebe a AIJE e nega a tutela que restringiria o programa Alô Alô Brasil e a utilização da Rádio Nacional nos termos requeridos; não julga o mérito do alegado uso da estrutura pública.'
        if i==226:justificativa='A decisão de 24/10 nega medidas de retirada de conteúdos descritos na inicial, suspensão de anúncios e ordens coordenadas por insuficiência de suporte probatório. O recebimento da AIJE não significa reconhecimento da ilicitude ou do abuso.'
        if i==227:justificativa='A decisão de 23/10 nega a suspensão integral do canal Tropa do Flávio, mas proíbe republicações de conteúdos já delimitados e determina a retirada do áudio sobre supostos votos lançados por mesários em nome de ausentes. O atendimento é parcial e cautelar.'
        if i==228:justificativa='A decisão de 24/10 nega a suspensão do manifesto/formulário foraflavio.com.br e as medidas de retirada ou abstenção remanescentes; não conhece do pedido sobre anúncios já submetidos a outra representação. Falta demonstração de utilização efetiva dos dados em favor dos candidatos.'
        data_julgamento=None
        if ref['tipo'].startswith('Ac'):
            m=re.search(r'Brasília, (\d{1,2}) de (\w+) de (2026)',t)
            if m and m[2].lower() in MESES:data_julgamento=f'2026-{MESES[m[2].lower()]:02d}-{int(m[1]):02d}'
        testemunho=''
        m=list(re.finditer(r'Decisão:',t))
        if m:testemunho=t[m[-1].start():m[-1].start()+1600]
        else:
            m=list(re.finditer(r'Ante o exposto|Diante do exposto|Desse modo, indefiro',t,re.I))
            testemunho=t[m[-1].start():m[-1].start()+2200] if m else t[-2400:]
        encerramentos=[d for d in docs if 'julgo extinto o pedido de direito de resposta' in texto(d) or 'perda superveniente do objeto desta ação' in texto(d)]
        sinopse=f"{objeto}. {justificativa} Peça oficial registrada em {ref['data_metadata'][8:10]}/{ref['data_metadata'][5:7]}; corte em 31/10/2026."
        if data_julgamento and data_julgamento!=ref['data_metadata']:sinopse+=f" O julgamento é datado no corpo em {data_julgamento[8:10]}/{data_julgamento[5:7]}, distinto do registro da peça."
        if incluir and encerramentos:
            sinopse+=' O pedido de resposta foi posteriormente extinto após o pleito, sem novo exame da medida comunicacional anterior.'
            status+='; resposta extinta após o pleito'
        resultado[cnj]={'campanha_autora':'Lula' if 'Lula' in r['campanha_ativa_detectada'] else 'Flávio',
            'incluir':incluir,'atendido':atendido,'categoria':categoria,'motivo':justificativa,
            'objeto':objeto,'pedido':pedido,'sinopse':sinopse,'grau':grau,'status':status,
            'url_peca':ref['url'],'tipo_peca':ref['tipo'],'data_ato_referencia':ref['data_metadata'],
            'data_julgamento_no_corpo':data_julgamento,
            'fonte_classificacao':'leitura documental da peça oficial; classificação jurídica manual',
            'grau_certeza':'alto','status_fonte':'inteiro teor oficial salvo; URL e hash identificados',
            'revisao_outubro':{'status':'verificado','corte':'2026-10-31','indice_lote_b':i,
                'testemunho_dispositivo':testemunho,
                'fonte_referencia':{'arquivo':ref['arquivo'],'sha256':ref['sha256'],'url':ref['url']},
                'inventario_documental':[{'arquivo':d.get('arquivo'),'url':d['url'],'data_metadata':d['data_metadata'],'tipo':d['tipo']} for d in docs]},
            'relato':{'titulo':objeto,'texto':sinopse,'requer_atualizacao':True}}
    assert len(resultado)==230
    (ROOT/'curadoria_novos_b.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('230 alvos;',sum(v['incluir'] for v in resultado.values()),'comparáveis;',sum(v['atendido'] is True for v in resultado.values()),'positivos')

if __name__=='__main__':main()
