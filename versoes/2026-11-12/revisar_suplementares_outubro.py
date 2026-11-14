"""Materializa a revisão manual dos 280 alvos suplementares, sem rede nem mutações no coletor.

Os quatro méritos e as particularidades processuais abaixo decorrem da leitura
das peças salvas. A enumeração do cache serve para documentar cobertura, nunca
para atribuir resultado jurídico a partir do tipo do documento.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CACHE = ROOT.parents[3] / 'pje_links_work' / '_cache_pje'
CORTE = '2026-10-31'


def ler(path):
    return json.loads(path.read_text(encoding='utf-8'))


def gravar(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def texto(doc):
    return re.sub(r'\s+', ' ', (ROOT / doc['arquivo']).with_suffix('.txt').read_text(encoding='utf-8')).strip()


def fonte(doc):
    path = ROOT / doc['arquivo']
    assert sha(path) == doc['sha256'], doc['arquivo']
    return {k: doc.get(k) for k in (
        'arquivo', 'sha256', 'url', 'id_documento', 'tipo', 'data_metadata',
        'data_decisao_metadata', 'data_assinatura', 'data_juntada')}


def inventario_cache(alvo):
    cnj = alvo['cnj']
    path = CACHE / (re.sub(r'\D', '', cnj) + '_TSE.json')
    raw = ler(path)
    procs = [p for p in raw.get('processos', [])
             if p.get('numeroProcesso') == cnj and p.get('instancia') == 3]
    assert procs, cnj
    docs, motivos = [], Counter()
    for proc in procs:
        decs = {str(d['idProcessoDocumento']): d for d in (proc.get('decisoes') or [])
                if d.get('idProcessoDocumento')}
        for d in (proc.get('documentos') or []):
            dec = decs.get(str(d.get('idProcessoDocumento')), {})
            data = (dec.get('dataDecisao') or d.get('dataAssinatura') or d.get('dataJuntada') or '')[:10]
            tipo = d.get('tipoDocumento') or ''
            storage = d.get('documentoStorage') or ''
            if d.get('documentoSigiloso') or d.get('publico') is False:
                motivo = 'documento não público no inventário'
            elif not storage.startswith('tse/'):
                motivo = 'arquivo de outra origem; não selecionado como peça TSE'
            elif not data:
                motivo = 'data não informada'
            elif data > CORTE:
                motivo = 'data posterior ao corte'
            elif not (dec or tipo.startswith(('Decis', 'Ac', 'Sent', 'Desp')) or ('Certid' in tipo and 'julgamento' in tipo.lower())):
                motivo = 'tipo fora da seleção documental'
            else:
                motivo = 'elegível para leitura, sem classificação automática'
            motivos[motivo] += 1
            docs.append({
                'id_documento': d.get('idProcessoDocumento'), 'tipo': tipo,
                'data_selecao': data, 'data_decisao_metadata': dec.get('dataDecisao'),
                'data_assinatura': d.get('dataAssinatura'), 'data_juntada': d.get('dataJuntada'),
                'storage': storage, 'motivo_selecao': motivo,
            })
    return {
        'cnj': cnj, 'cache_arquivo_original': 'pje_links_work/_cache_pje/' + path.name,
        'cache_sha256': sha(path),
        'cache_extraido_em': datetime.fromtimestamp(raw['instante'], timezone.utc).isoformat(),
        'instancia_confirmada': 3, 'fontes_cnj_exato': len(procs),
        'decisoes_nulas': any(p.get('decisoes') is None for p in procs),
        'documentos_inventariados': len(docs), 'contagens_selecao': dict(motivos),
        'objeto_cadastral': next((p.get('objeto') for p in procs if p.get('objeto')), None),
        'documentos': docs,
        'limite': 'Inventário oficial consultado posteriormente ao corte. Não comprova cobertura integral do PJe nem permite inferir resultado de pedido sem a respectiva peça.'
    }


# Leitura jurídica manual: os quatro julgamentos de mérito documentados.
MERITOS = {
    '0602697-28': {
        'objeto': 'Quatorze impulsionamentos sobre a extinção da escala 6x1 e a posição política de Flávio Bolsonaro',
        'pedido': 'Interromper os impulsionamentos apontados como propaganda negativa e reconhecer a infração eleitoral',
        'data_julgamento': '2026-10-23',
        'fundamento': 'O vídeo apresentava exclusivamente proposta de governo; a referência ao adversário estava na legenda, como contraponto político com respaldo temporal. A manifestação e o voto favoráveis posteriores de Flávio não tornavam retroativamente falsa a publicidade anterior.',
        'sinopse': 'Flávio Bolsonaro questionou quatorze anúncios patrocinados de Lula e da Coligação Brasil Pronto pra Mais sobre o fim da escala 6x1, cuja legenda lhe atribuía atuação contrária à mudança. Requereu a interrupção dos impulsionamentos e o reconhecimento de propaganda negativa irregular. O Tribunal distinguiu o vídeo exclusivamente propositivo da referência comparativa na legenda e ressaltou que a manifestação e o voto favoráveis posteriores de Flávio, em 14 de outubro, não demonstravam falsidade retroativa dos anúncios anteriores. Na sessão de 23 de outubro, julgou os pedidos improcedentes por unanimidade, com resolução do mérito e prejuízo da tutela de urgência.',
    },
    '0602800-35': {
        'objeto': 'Direito de resposta a trinta anúncios no Facebook sobre o “tesouraço” e os efeitos do programa econômico de Flávio',
        'pedido': 'Conceder direito de resposta à propaganda impulsionada sobre cortes em programas sociais e aposentadorias',
        'data_julgamento': '2026-10-21',
        'fundamento': 'A propaganda utilizava comentários jornalísticos e prognósticos críticos sobre o plano econômico, sem falsidade objetiva reconhecível de plano. A instrução permitia o julgamento de mérito favorável aos requeridos, apesar da ausência do texto da resposta.',
        'sinopse': 'Flávio Bolsonaro pediu direito de resposta a trinta anúncios de Lula e da Coligação Brasil Pronto pra Mais no Facebook, que combinavam recortes de comentários jornalísticos, imagens do candidato e prognósticos de cortes em programas sociais e aposentadorias sob a expressão “tesouraço”. O Tribunal reconheceu que a identidade dos anúncios permitia examinar o mérito mesmo com cópias de apenas duas páginas e afastou a preliminar de inépcia. Considerou o conteúdo uma interpretação crítica do plano econômico, sem falsidade objetiva que justificasse a resposta. Na sessão de 21 de outubro, o pedido foi julgado improcedente por unanimidade.',
    },
    '0602824-63': {
        'objeto': 'Direito de resposta à inserção televisiva que comparava o “tesouraço” de Flávio a cortes no governo Jair Bolsonaro',
        'pedido': 'Conceder direito de resposta às inserções televisivas de 10 de outubro e fixar multa para eventual descumprimento',
        'data_julgamento': '2026-10-21',
        'fundamento': 'A justaposição de proposta de redução de gastos com cortes orçamentários históricos constituía prognóstico político desfavorável. Não houve imputação categórica de uma proposta de extinguir benefícios sociais nem falsidade objetiva que autorizasse resposta.',
        'sinopse': 'Flávio Bolsonaro pediu direito de resposta a inserções televisivas de Lula e da Coligação Brasil Pronto pra Mais veiculadas em 10 de outubro. A propaganda ligava sua proposta de “tesouraço” a manchetes sobre cortes em Farmácia Popular, combate ao câncer e financiamento habitacional durante o governo Jair Bolsonaro. O Tribunal distinguiu essa comparação histórica e o prognóstico eleitoral desfavorável da atribuição categórica de uma proposta de extinguir benefícios, preservando a crítica política. Na sessão de 21 de outubro, rejeitou a preliminar de inépcia e julgou o pedido improcedente por unanimidade; a multa para eventual descumprimento ficou prejudicada.',
    },
    '0602912-04': {
        'objeto': 'Direito de resposta à propaganda de rádio sobre armas, violência e organizações criminosas',
        'pedido': 'Veicular resposta nas inserções e blocos de audiência indicados, pelo tempo mínimo de um minuto, com multa em caso de descumprimento',
        'data_julgamento': '2026-10-21',
        'fundamento': 'A mensagem criticava os resultados da política de ampliação do acesso a armas, apoiada em dados e reportagens, sem imputar a Flávio participação pessoal em crimes. A redução de homicídios e a linguagem dramática não demonstravam, por si, falsidade manifesta ou ofensa pessoal grave.',
        'sinopse': 'Flávio Bolsonaro pediu direito de resposta a propaganda de Lula e da Coligação Brasil Pronto pra Mais transmitida em 12 de outubro, em 32 inserções de rádio. A mensagem relacionava a ampliação do acesso a armas e munições à violência e à circulação de armamentos entre milícias e organizações criminosas, com efeitos sonoros de tiros e sirenes. O Tribunal entendeu que se tratava de crítica a uma política pública com substrato em dados e reportagens, sem imputação individualizada de participação do candidato em atividades ilícitas. Na sessão de 21 de outubro, julgou o pedido improcedente por unanimidade.',
    },
}


# Exceções aos despachos usuais de contraditório: lidas e anotadas individualmente.
PROCESSUAIS = {
    '0600291-34': ('Emenda da inicial e esclarecimento da autoria das publicações',
        'O despacho de 22 de outubro exigiu correção da inicial e demonstração da vinculação dos demais representados à publicação “Samba da Esbanja”, cuja URL apontava apenas para o PL. Não apreciou a tutela sobre o conteúdo.'),
    '0601336-73': ('Encerramento do plantão e remessa à relatoria',
        'A Presidência deixou de examinar a tutela sobre vídeo sintético de Flávio como piloto de caça porque se encerrava o plantão, remetendo o pedido à relatora no expediente seguinte. Esse ato não equivale a indeferimento da retirada.'),
    '0601378-25': ('Apensamento e tutela examinada em outro processo',
        'Os despachos determinaram o apensamento à Rp 0601357-49 e registraram que a tutela de objeto coincidente já fora examinada e atendida naquele processo. Sem peça de julgamento material autônomo neste CNJ, o resultado alheio não é transplantado nem contado em duplicidade.'),
    '0601684-91': ('Contraditório e inclusão de litisconsorte em representação especial',
        'Os atos reservam a tutela ao contraditório, admitem Geraldo Alckmin como litisconsorte facultativo e abrem vista à Procuradoria-Geral Eleitoral. Não há nas peças selecionadas decisão comparável sobre uma comunicação eleitoral individualizada.'),
    '0601743-79': ('Identificação de perfil e citação, com tutela reservada',
        'Os cinco despachos tratam da identificação do perfil @pesquisas_elige, dados dos provedores e citação, inclusive por edital. A tutela sobre o vídeo impugnado foi postergada; as diligências de identificação não constituem concessão ou indeferimento de remoção.'),
    '0601954-18': ('Citação e vista à Procuradoria-Geral Eleitoral',
        'As peças selecionadas determinam a citação e posterior vista à Procuradoria-Geral Eleitoral. Não documentam resultado sobre medida comunicacional ou julgamento material da pretensão.'),
    '0601967-17': ('Citação e parecer ministerial antes de exame do pedido',
        'O despacho determina a citação dos representados e vista à Procuradoria-Geral Eleitoral, sem decisão material sobre a comunicação impugnada.'),
    '0602229-64': ('Emenda do direito de resposta; tutela coincidente examinada em outro CNJ',
        'O despacho de 11 de outubro registra que tutela idêntica fora apreciada na Rp 0602232-19; o de 17 de outubro exige o texto da resposta em 24 horas, sob pena de indeferimento da inicial. Nenhum dos dois fornece resultado comunicacional autônomo neste CNJ; não se presume extinção pelo simples prazo nem se duplica o resultado da representação conexa.'),
    '0602240-93': ('Juntada do texto da resposta',
        'A relatora determinou a apresentação do texto da resposta em 24 horas e, depois, contraditório. A advertência de eventual extinção não é decisão de extinção nem julgamento de mérito.'),
    '0602627-11': ('Juntada do texto da resposta',
        'A Presidência exigiu o texto da resposta e manifestação dos requeridos antes de julgamento. A peça tem registro em 17 de outubro e data redacional de 12 de outubro; não contém resultado comparável sobre o vídeo questionado.'),
    '0602830-70': ('Regularização do pedido de resposta',
        'O despacho exige a apresentação do texto da resposta em 24 horas. Não decide a veracidade da propaganda impulsionada nem concede ou rejeita o direito de resposta.'),
    '0602837-62': ('Regularização do pedido de resposta',
        'O despacho exige de Flávio e Alfredo Gaspar o texto da resposta à propaganda televisiva de 10 de outubro. A regularização processual não resolve o pedido de resposta.'),
    '0602880-96': ('Emenda da inicial de direito de resposta',
        'A Presidência determina a apresentação do conteúdo da resposta e o contraditório, sob advertência de eventual indeferimento da inicial. Não decide a pretensão comunicacional. Registro da peça em 21 de outubro; data redacional de 20 de outubro.'),
    '0602931-10': ('Defesa e instrução sobre possível uso de inteligência artificial',
        'A peça informa expressamente a ausência de pedido de tutela de urgência e determina defesa e esclarecimentos sobre imagens produzidas por inteligência artificial na propaganda televisiva. Não há julgamento de mérito do direito de resposta nas peças selecionadas.'),
    '0603044-61': ('Juntada do texto da resposta',
        'A Presidência exige o texto da resposta à propaganda televisiva de 15 de outubro e, depois, manifestação dos requeridos. Não aprecia a pretensão comunicacional.'),
    '0603170-14': ('Juntada do texto da resposta',
        'O despacho exige o texto da resposta à propaganda em bloco de rádio de 19 de outubro, para permitir contraditório e controle de proporcionalidade. Não concede nem indefere o pedido de resposta.'),
    '0603214-33': ('Instrução técnica de pedido administrativo sobre o canal Exército do Lula',
        'O ato solicita esclarecimentos técnicos a provedores, relatórios e preservação de registros sobre o canal Exército do Lula e eventual amplificação coordenada, com posterior contraditório. Os demais pedidos e preliminares ficam expressamente postergados. A preservação de dados e a solicitação de informações não equivalem à suspensão do canal ou à remoção da comunicação impugnada.'),
}


def main():
    alvos = sorted(ler(ROOT / 'triagem_base_integral.json')['sem_coleta'], key=lambda r: r['cnj'])
    cp_path = ROOT / 'coleta_documental/checkpoint.json'
    cp = ler(cp_path)
    assert len(alvos) == len({a['cnj'] for a in alvos}) == 280
    inventarios, resultado, situacoes = {}, {}, {}
    for alvo in alvos:
        cnj = alvo['cnj']; prefixo = cnj[:10]
        reg = cp[cnj]
        assert reg.get('consulta_efetuada') is True, cnj
        inv = inventario_cache(alvo); inventarios[cnj] = inv
        docs = reg.get('documentos') or []
        assert all(d.get('status') == 'conferido' for d in docs), cnj
        fontes = [fonte(d) for d in docs]
        ativo = ' '.join(alvo['ativo']).upper()
        autora = 'Flávio' if 'FLAVIO' in ativo or 'FLÁVIO' in ativo or 'ALFREDO GASPAR' in ativo or 'PARTIDO LIBERAL' in ativo else 'Lula'
        base = {
            'campanha_autora': autora, 'incluir': False, 'atendido': None,
            'categoria': 'pendência documental; cobertura limitada',
            'motivo': 'Nenhuma peça decisória pública elegível ao corte foi selecionada no inventário consultado. Isso não demonstra inexistência de outros atos no PJe nem autoriza classificar o pedido como negado.',
            'objeto': 'Pretensão sem resultado comparável documentalmente acessível no inventário selecionado',
            'pedido': 'Não classificado sem peça judicial pertinente ao corte',
            'sinopse': '', 'grau': 'sem resultado comparável',
            'status': 'fora dos percentuais; pendência documental',
            'url_peca': None, 'tipo_peca': None, 'arquivo_peca': None, 'sha256_peca': None,
            'data_ato_referencia': None, 'data_julgamento_no_corpo': None,
            'fonte_classificacao': 'inventário oficial armazenado; nenhuma inferência de resultado a partir de metadados',
            'grau_certeza': 'limitado quanto ao resultado; alto quanto ao inventário observado',
            'status_fonte': 'inventário consultado; sem peça judicial elegível para classificar resultado',
            'polos_cadastrais': {'ativo': alvo['ativo'], 'passivo': alvo['passivo']},
            'classe': alvo['classe'], 'data_autuacao': datetime.strptime(alvo['autuacao'], '%d/%m/%Y').date().isoformat(),
            'revisao_outubro': {
                'status': 'pendente documental', 'corte': CORTE,
                'fonte_referencia': None, 'inventario_documental': fontes,
                'fonte_inventario': {
                    'arquivo': 'inventario_suplementares_cache.json',
                    'chave': cnj, 'cache_sha256': inv['cache_sha256'],
                    'extraido_em': inv['cache_extraido_em'],
                },
                'cobertura': 'Limitada ao inventário oficial consultado e às peças públicas selecionáveis por tipo, origem e corte. Não se presume acesso integral aos autos.',
            },
        }
        primary = None
        situacao = 'sem resultado comparável'
        justificativa = base['motivo']
        if base['data_autuacao'] > CORTE:
            base.update({
                'categoria': 'fora do corte; autuação posterior',
                'motivo': 'Processo autuado em 03/11/2026, após o corte de 31/10/2026. Não integra os resultados do período.',
                'objeto': 'Processo autuado após o corte temporal',
                'status': 'excluído pelo corte temporal', 'grau_certeza': 'alto para a exclusão temporal',
            })
            base['revisao_outubro']['status'] = 'verificado quanto ao corte temporal'
        elif prefixo in MERITOS:
            m = MERITOS[prefixo]
            cert = next(d for d in docs if d['tipo'].startswith('Cert'))
            acord = next(d for d in docs if d['tipo'].startswith('Ac'))
            primary = cert
            base.update({
                'incluir': True, 'atendido': False, 'categoria': 'comparável',
                'motivo': 'Julgamento de mérito improcedente, comprovado por certidão contemporânea e inteiro teor do acórdão.',
                'objeto': m['objeto'], 'pedido': m['pedido'], 'sinopse': m['sinopse'],
                'grau': 'não atendido', 'status': 'mérito colegiado; improcedência',
                'data_julgamento_no_corpo': m['data_julgamento'],
                'fundamento_classificacao': m['fundamento'],
                'fonte_classificacao': 'leitura manual da certidão oficial e do acórdão; resultado comprovado até o corte',
                'grau_certeza': 'alto', 'status_fonte': 'certidão contemporânea e inteiro teor oficial salvos, com URLs e hashes',
            })
            base['revisao_outubro'].update({
                'status': 'verificado', 'unanimidade': True,
                'data_sessao': m['data_julgamento'],
                'testemunho_dispositivo': texto(cert)[texto(cert).find('DECISÃO'):],
                'fonte_fundamentos': fonte(acord),
                'nota_cronologica': 'O resultado é comprovado pela certidão assinada em outubro. O inteiro teor do acórdão foi assinado/juntado em novembro e é utilizado para documentar os fundamentos do julgamento anterior, não como novo acontecimento no período.',
            })
            situacao = 'mérito colegiado'
            justificativa = 'Improcedência unânime na sessão de ' + m['data_julgamento'] + ', comprovada por certidão anterior ao corte; sem resultado de tutela autônoma a substituir o mérito.'
        elif prefixo == '0600701-92':
            primary = next(d for d in docs if d['tipo'].startswith('Cert'))
            base.update({
                'categoria': 'extinção sem mérito; inadequação da via pré-convencional',
                'motivo': 'Na sessão de 23/10/2026, o Tribunal extinguiu o direito de resposta sem resolução do mérito, porque ajuizado em 17 de abril, antes do marco legal da escolha de candidatos em convenção. A tutela ficou prejudicada; não houve julgamento da veracidade ou ilicitude das publicações.',
                'objeto': 'Pedido de resposta a publicações que associavam PT, Lula e lideranças a organizações criminosas',
                'pedido': 'Remover as publicações e veicular direito de resposta',
                'status': 'extinção sem resultado comunicacional comparável',
                'data_julgamento_no_corpo': '2026-10-23',
            })
            base['revisao_outubro'].update({
                'status': 'verificado', 'unanimidade': True, 'data_sessao': '2026-10-23',
                'nota_cronologica': 'Extinção comprovada pela certidão de 24/10. O acórdão, assinado em 03/11, documenta o julgamento de 23/10, sem transformar a extinção processual em resultado negativo de mérito.',
            })
        elif docs:
            primary = max(docs, key=lambda d: (d['data_metadata'], d.get('id_documento') or 0))
            titulo, motivo = PROCESSUAIS.get(prefixo, (
                'Tutela reservada ao contraditório',
                'A peça determina citação ou manifestação dos requeridos e vista à Procuradoria-Geral Eleitoral antes da apreciação da tutela. Não contém concessão ou indeferimento de medida sobre a comunicação impugnada; o pedido permanece sem resultado comparável documentado neste inventário.'
            ))
            base.update({
                'categoria': 'processual; sem resultado comparável documentado',
                'motivo': motivo, 'objeto': titulo,
                'pedido': 'Pretensão comunicacional sem julgamento material na documentação selecionada',
                'status': 'fora dos percentuais; ato processual sem resultado comparável',
            })
            base['revisao_outubro'].update({
                'status': 'verificado',
                'testemunho_dispositivo': texto(primary)[-2400:],
            })
        if primary:
            f = fonte(primary)
            base.update({
                'url_peca': primary['url'], 'tipo_peca': primary['tipo'],
                'arquivo_peca': primary['arquivo'], 'sha256_peca': primary['sha256'],
                'data_ato_referencia': primary['data_metadata'],
                'fonte_classificacao': 'leitura documental manual da peça oficial, com ressalva expressa da cobertura do inventário',
                'grau_certeza': 'alto quanto ao conteúdo da peça; cobertura dos autos limitada',
                'status_fonte': 'peça oficial salva; URL, data e hash identificados',
            })
            base['revisao_outubro']['fonte_referencia'] = f
            if not base['incluir']:
                justificativa = base['motivo']
        else:
            base['revisao_outubro']['contagens_inventario'] = inv['contagens_selecao']
            if not inv['documentos_inventariados']:
                base['motivo'] += ' A resposta de documentos deste inventário está vazia; decisões nulas ou lista vazia não são prova de ausência de pronunciamentos.'
            elif inv['decisoes_nulas']:
                base['motivo'] += ' O campo de decisões veio nulo; a lista de documentos foi examinada separadamente, sem peça elegível segundo os filtros.'
            base['revisao_outubro']['status'] = ('verificado quanto ao corte temporal' if base['data_autuacao'] > CORTE else 'pendente documental')
            justificativa = base['motivo']
        if not base['sinopse']:
            base['sinopse'] = base['objeto'] + '. ' + base['motivo']
        base['relato'] = {'titulo': base['objeto'], 'texto': base['sinopse'], 'requer_atualizacao': True}
        base['colegialidade_situacao'] = situacao
        resultado[cnj] = base
        situacoes[cnj] = {
            'colegialidade_situacao': situacao, 'justificativa': justificativa,
            'url_peca': base['url_peca'], 'data_ato_referencia': base['data_ato_referencia'],
            'data_julgamento_no_corpo': base['data_julgamento_no_corpo'],
            'fonte_referencia': base['revisao_outubro']['fonte_referencia'],
        }
    gravar(ROOT / 'inventario_suplementares_cache.json', {
        'corte': CORTE, 'checkpoint_sha256': sha(cp_path),
        'nota': 'Inventários consultados em novembro; contagens de seleção não são resultados judiciais. Nenhuma requisição de rede foi feita por este programa.',
        'processos': inventarios,
    })
    gravar(ROOT / 'curadoria_suplementares_outubro.json', resultado)
    gravar(ROOT / 'situacoes_suplementares.json', situacoes)
    resumo = {
        'total': len(resultado), 'comparaveis': sum(r['incluir'] for r in resultado.values()),
        'positivos': sum(r['incluir'] and r['atendido'] is True for r in resultado.values()),
        'negativos': sum(r['incluir'] and r['atendido'] is False for r in resultado.values()),
        'categorias': dict(Counter(r['categoria'] for r in resultado.values())),
        'status_revisao': dict(Counter(r['revisao_outubro']['status'] for r in resultado.values())),
        'pecas_lidas': sum(len(cp[a['cnj']].get('documentos') or []) for a in alvos),
        'inventarios_decisoes_nulas': sum(i['decisoes_nulas'] for i in inventarios.values()),
    }
    assert resumo['comparaveis'] == resumo['negativos'] == 4 and resumo['positivos'] == 0
    assert len(resultado) == len(situacoes) == 280
    gravar(ROOT / 'resumo_suplementares_outubro.json', resumo)
    (ROOT / 'auditoria_suplementares.md').write_text(
        '# Auditoria dos 280 alvos suplementares\n\n'
        'Corte dos acontecimentos: **31/10/2026**. Inventários consultados em novembro; nenhuma nova consulta de rede foi feita nesta revisão. '
        'A extração posterior não é apresentada como extração de 1º de novembro.\n\n'
        '**Resultado:** 4 processos comparáveis, todos com pedido não atendido por julgamento de mérito colegiado unânime. '
        'Outros 276 permanecem fora dos percentuais: 73 com atos apenas processuais, 1 extinto sem mérito, 201 com pendência documental/cobertura limitada e 1 autuado após o corte.\n\n'
        '## Julgamentos acrescentados\n\n'
        '| CNJ | Sessão | Pretensão e fundamento | Resultado |\n'
        '| --- | --- | --- | --- |\n'
        '| 0602697-28 | 23/10 | 14 impulsionamentos sobre escala 6x1: proposta de governo e comparação contextual, sem propaganda negativa autônoma | Improcedência unânime |\n'
        '| 0602800-35 | 21/10 | Resposta a 30 anúncios no Facebook sobre tesouraço: comentários jornalísticos e prognósticos críticos do programa econômico | Improcedência unânime |\n'
        '| 0602824-63 | 21/10 | Resposta a inserção de TV sobre tesouraço: comparação com cortes históricos, sem imputação categórica de extinção de benefícios | Improcedência unânime |\n'
        '| 0602912-04 | 21/10 | Resposta a inserções de rádio sobre armas e violência: crítica a política pública, sem imputação pessoal de crime | Improcedência unânime |\n\n'
        'As quatro classificações usam como fonte principal as certidões de 22 ou 24 de outubro, contemporâneas ao período. '
        'Os acórdãos foram assinados/juntados em novembro e documentam os fundamentos dos julgamentos de outubro, comprovados nas certidões. '
        'As datas de sessão, metadado, assinatura e juntada estão separadas; nenhum resultado ocorrido depois do corte foi antecipado.\n\n'
        '## Exclusões e limites\n\n'
        'O DR 0600701-92, ajuizado antes da escolha convencional de candidatos, foi extinto sem mérito na sessão de 23/10, '
        'com tutela prejudicada. Não é improcedência nem negativa de mérito. '
        'O processo 0602285-10.2026.6.14.0000 foi autuado em 03/11 e está excluído por data.\n\n'
        'Em 73 processos, as peças selecionadas contêm apenas citação, emenda, instrução, preservação de registros ou postergação da tutela. '
        'O simples rótulo Despacho não determinou a exclusão: a leitura do conteúdo verificou a ausência de concessão/indeferimento de medida comunicacional comparável. '
        'A PetCiv 0603214-33 exige esclarecimentos técnicos dos provedores e preservação de registros, deixando os demais pedidos postergados. '
        'A Rp 0601743-79 trata de identificação de perfil e citação; não é decisão de remoção. '
        'A Rp 0601378-25 e o DR 0602229-64 mencionam tutela de processo conexo, sem resultado autônomo a transplantar ou duplicar.\n\n'
        'Nos 202 processos sem peça elegível (incluindo o autuado após o corte), o inventário bruto foi examinado por CNJ exato e instância 3. '
        'Há respostas vazias, decisões nulas, documentos de outros tipos/origens e atos posteriores ao corte. '
        'Isso não prova inexistência de outros atos nos autos, ausência de tutela ou rejeição do pedido. '
        'Os 201 processos anteriores ao corte sem fonte suficiente estão expressamente marcados como pendência documental e fora dos percentuais.\n\n'
        '## Rastreabilidade e validação\n\n'
        'O JSON contém os 280 CNJs únicos, polos, motivo, objeto, estágio, cobertura e fontes por processo. '
        'As 93 peças selecionadas foram conferidas por leitura e hash; certidões e acórdãos do mesmo julgamento não geram dois resultados. '
        'O inventário de cache registra hashes, data real de consulta, filtros e documentos, sem atribuir-lhes resultado por metadados. '
        'Os arquivos de fonte principal têm SHA-256 conferido; os quatro resultados possuem certidão anterior ao corte. '
        'A classificação foi materializada por `revisar_suplementares_outubro.py`, sem modificar checkpoint, coletor, histórico ou arquivos dos lotes A/B.\n',
        encoding='utf-8')
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
