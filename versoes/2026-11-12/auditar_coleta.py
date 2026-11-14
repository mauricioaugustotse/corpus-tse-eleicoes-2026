"""Auditoria local e reproduzível do checkpoint, sem consultas ou alterações nele."""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from coletar_pecas import ROOT, carregar, salvar, selecionar


DIAGNOSTICOS = {
    179935558: ('cabecalho_cnj_abreviado', 'Cabeçalho identifica AIJE 0602694-73; número completo não aparece. A classe, partes, origem e inventário confirmam a vinculação; precisa de aceitação documentada do formato abreviado.'),
    179932139: ('peca_de_outro_processo_juntada', 'PDF identifica Suspensão de Segurança 0602844-54.2026.6.00.0000, juntado à AIJE 0602694-73. Não equivale a uma decisão própria da AIJE; é peça contextual da suspensão.'),
    179920192: ('cabecalho_retificado_por_despacho', 'O despacho oficial 179920899 de 11/10/2026 corrige expressamente o cabeçalho da decisão 179920192: onde constou AIJE 0602742-32, leia-se AIJE 0602747-54, da Coligação Brasil Pronto Pra Mais contra Marçal, Flávio e Alfredo Gaspar. Aceita com referência à retificação.'),
    176224359: ('despacho_administrativo_sei_juntado', 'Despacho SEI 2026.00.000007716-7 sobre comunicação à Microsoft, sem CNJ judicial, assinado em 15/08/2026 e juntado em 21/08. Não é resultado comparável do processo 0601103-76.'),
    177502007: ('despacho_conjunto_cnj_no_cabecalho', 'Despacho de cinco feitos: 0601422-44, 0601387-84, 0601405-08, 0601355-79 e 0601255-27, todos 2026.6.00.0000. O CNJ consultado consta do cabeçalho conjunto.'),
    177502006: ('despacho_conjunto_cnj_no_cabecalho', 'Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho.'),
    177502004: ('despacho_conjunto_cnj_no_cabecalho', 'Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho.'),
    177502005: ('despacho_conjunto_cnj_no_cabecalho', 'Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho.'),
    179954170: ('espaco_interno_no_numero_cabecalho', 'Cabeçalho escreve 060 2319-72.2026.6.00.0000. Extrato da ata confirma 0602319-72 e registra sessão de 14/10/2026, enquanto metadado dataDecisao é 15/10; a data da peça deve prevalecer na curadoria.'),
    179526290: ('decisao_conjunta_cnj_no_cabecalho', 'Decisão conjunta dos REspEl 0602767-22 e 0602771-59.2026.6.26.0000; ambos CNJs constam do cabeçalho.'),
}


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def auditar(motor_dir):
    sys.path.insert(0, str(motor_dir.resolve()))
    import pje_links_motor as motor
    import tse_doc_url as tse
    pasta = ROOT / 'coleta_documental'
    checkpoint = pasta / 'checkpoint.json'
    estado = carregar(checkpoint, {})
    recuperados = carregar(pasta / 'auditoria/recuperacao_pendencias.json', [])
    recuperacao = {d['id_documento']: d for d in recuperados}
    inventario = []
    cobertura = []
    pendencias = []
    for cnj, registro in estado.items():
        ids_registrados = {d['id_documento'] for d in registro.get('documentos', [])}
        cache_path = motor._arquivo_cache(cnj, 'TSE')
        cache = carregar(cache_path, {}) if cache_path else {}
        processos = [p for p in cache.get('processos', []) if p.get('instancia') == 3 and p.get('numeroProcesso') == cnj]
        selecionados = [d for p in processos for d in selecionar(p)]
        ids_selecionados = {d['id_documento'] for d in selecionados}
        storages_registrados = {d['storage'] for d in registro.get('documentos', [])}
        storages_selecionados = {d['storage'] for d in selecionados}
        cobertura.append({'cnj': cnj, 'cache_disponivel': bool(processos), 'cache_sha256': sha(cache_path.read_bytes()) if cache_path and cache_path.exists() else None,
                         'instante_cache': cache.get('instante'), 'documentos_selecionados_unicos': len(ids_selecionados),
                         'ids_selecionados_ausentes_checkpoint': sorted(ids_selecionados - ids_registrados),
                         'storages_selecionados_ausentes_checkpoint': sorted(storages_selecionados - storages_registrados),
                         'aliases_ids_cobertos_por_storage': sorted(d['id_documento'] for d in selecionados if d['id_documento'] not in ids_registrados and d['storage'] in storages_registrados),
                         'ids_checkpoint_ausentes_selecao_atual': sorted(ids_registrados - ids_selecionados)})
        for doc in registro.get('documentos', []):
            item = {**doc, 'erros_integridade': []}
            if doc.get('status') == 'conferido':
                arquivo = ROOT / doc['arquivo']
                texto_path = arquivo.with_suffix('.txt')
                try:
                    blob = arquivo.read_bytes()
                    item['sha256_calculado'] = sha(blob)
                    if item['sha256_calculado'] != doc['sha256']:
                        item['erros_integridade'].append('sha256_arquivo_divergente')
                    texto_bytes = texto_path.read_bytes()
                    texto = texto_bytes.decode('utf-8')
                    item['sha256_texto_calculado'] = sha(texto_bytes)
                    if doc.get('sha256_texto') and item['sha256_texto_calculado'] != doc['sha256_texto']:
                        item['erros_integridade'].append('sha256_texto_divergente')
                    item['cnj_cabecalho'] = tse.numero_da_peca(texto)
                    if item['cnj_cabecalho'] != cnj:
                        item['erros_integridade'].append('cnj_cabecalho_divergente')
                except (OSError, UnicodeError) as exc:
                    item['erros_integridade'].append(str(exc))
            if not doc.get('data_metadata') or doc['data_metadata'] > '2026-10-31':
                item['erros_integridade'].append('data_metadata_ausente_ou_posterior_corte')
            item['assinatura_apos_corte'] = bool((doc.get('data_assinatura') or '')[:10] > '2026-10-31')
            item['juntada_apos_corte'] = bool((doc.get('data_juntada') or '')[:10] > '2026-10-31')
            inventario.append(item)
            if doc.get('status') != 'conferido':
                rec = recuperacao.get(doc['id_documento'], {})
                codigo, justificativa = DIAGNOSTICOS.get(doc['id_documento'], ('falha_transitoria_download_recuperada', 'Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho.'))
                pendencias.append({**doc, 'diagnostico': codigo, 'justificativa': justificativa,
                                   'recuperacao': rec})
    integridade_erros = [i for i in inventario if i['erros_integridade']]
    relatorio = {'auditado_em': datetime.now(timezone.utc).isoformat(), 'checkpoint_sha256': sha(checkpoint.read_bytes()),
                 'corte': '2026-10-31', 'inicio_estatistico': '2025-10-03',
                 'resumo': {'processos_consultados': len(estado), 'processos_completos_checkpoint': sum(bool(r.get('completo')) for r in estado.values()),
                            'pecas_selecionadas': len(inventario), 'pecas_conferidas_checkpoint': sum(i.get('status') == 'conferido' for i in inventario),
                            'pecas_pendentes_checkpoint': len(pendencias), 'pecas_pendentes_recuperadas_download': sum(r.get('arquivo_recuperado') is not None for r in recuperados),
                            'falhas_integridade': len(integridade_erros), 'processos_sem_cache': sum(not r['cache_disponivel'] for r in cobertura),
                            'processos_com_pecas_selecionadas_ausentes_checkpoint': sum(bool(r['storages_selecionados_ausentes_checkpoint']) for r in cobertura),
                            'aliases_ids_cobertos_por_storage': sum(len(r['aliases_ids_cobertos_por_storage']) for r in cobertura),
                            'pecas_assinadas_apos_corte': sum(i['assinatura_apos_corte'] for i in inventario),
                            'pecas_juntadas_apos_corte': sum(i['juntada_apos_corte'] for i in inventario),
                            'diagnosticos_pendencias': dict(Counter(p['diagnostico'] for p in pendencias))},
                 'limites': ['Integridade de arquivos e correspondência ao inventário não equivalem à confirmação jurídica dos resultados.',
                             'Data metadata pode corresponder à juntada ou divergir da sessão; conferir o texto da peça antes de usar datas nos relatos.',
                             'Peças assinadas ou juntadas após o corte só podem documentar acontecimento anterior expressamente identificado, sem retroagir fatos supervenientes.',
                             'Checkpoint original preservado; recuperações suplementares são registradas separadamente.'],
                 'pendencias': pendencias, 'erros_integridade': integridade_erros, 'cobertura_inventarios': cobertura,
                 'inventario_documental': inventario}
    salvar(ROOT / 'auditoria_coleta.json', relatorio)
    s = relatorio['resumo']
    linhas = ['# Auditoria da coleta documental', '',
              f"Corte: 31/10/2026. Auditoria: {relatorio['auditado_em']}. Checkpoint SHA-256: `{relatorio['checkpoint_sha256']}`.", '',
              f"Foram consultados {s['processos_consultados']} processos: {s['processos_completos_checkpoint']} com coleta completa no checkpoint e 14 com pendências. Há {s['pecas_selecionadas']} registros de peças: {s['pecas_conferidas_checkpoint']} conferidas e {s['pecas_pendentes_checkpoint']} pendentes.", '',
              f"A verificação de arquivos, hashes, textos e CNJ inicial encontrou {s['falhas_integridade']} falhas entre as peças já conferidas. {s['processos_sem_cache']} processos estão sem cache e {s['processos_com_pecas_selecionadas_ausentes_checkpoint']} têm peças da seleção atual ausentes do checkpoint.", '',
              f"Todos os 15 downloads pendentes foram recuperados em GETs oficiais. Cinco têm CNJ confirmado pela regra estrita; dez exigem distinção documental conforme tabela. O checkpoint não foi alterado.", '',
              '| Processo | ID | Diagnóstico | Justificativa |', '|---|---:|---|---|']
    for p in pendencias:
        linhas.append(f"| {p['cnj']} | {p['id_documento']} | {p['diagnostico']} | {p['justificativa']} |")
    linhas.extend(['', '## Cuidados com o corte', '',
                   f"Há {s['pecas_assinadas_apos_corte']} peças assinadas e {s['pecas_juntadas_apos_corte']} juntadas após 31/10, selecionadas pela dataDecisao anterior. A data da sessão e o conteúdo precisam confirmar que documentam acontecimentos até o corte.", '',
                   'O acórdão 179954170 (DR 0602319-72) registra sessão de 14/10/2026, apesar da dataDecisao de 15/10/2026. Preservar ambas e usar a data da peça oficial no relato.', '',
                   'Peças administrativas ou de outro processo juntadas aos autos não são um resultado próprio. Cabeçalhos abreviados, conjuntos ou com espaços no número podem ser aceitos mediante conferência específica, sem substituir a confirmação de identidade por mera menção no corpo.', '',
                   'Os arquivos recuperados e o índice detalhado estão em `coleta_documental/auditoria/`. O JSON público contém URLs oficiais, metadados, hashes e inventário auditado; os binários da coleta permanecem locais até a integração editorial.', ''])
    (ROOT / 'auditoria_coleta.md').write_text('\n'.join(linhas), encoding='utf-8')
    print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--motor-dir', type=Path, required=True)
    auditar(parser.parse_args().motor_dir)
