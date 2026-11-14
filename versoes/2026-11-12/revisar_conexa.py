"""Reconcilia a AIJE 0602694-73 com traslados e pronunciamentos conexos."""
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CNJ='0602694-73.2026.6.00.0000'

def fonte(doc,arquivo=None,cnj_documento=None):
    p=ROOT/(arquivo or doc['arquivo'])
    return {'url':doc['url'],'arquivo':p.relative_to(ROOT).as_posix(),
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'data_metadata':doc['data_metadata'],
        'id_documento_no_inventario':doc.get('id_documento'),
        'cnj_documento':cnj_documento or doc.get('cnj') or CNJ}

def main():
    cp=json.loads((ROOT/'coleta_documental/checkpoint.json').read_text(encoding='utf-8'))
    antigo=json.loads((ROOT/'curadoria_novos_a.json').read_text(encoding='utf-8'))[CNJ]
    ds={d['id_documento']:d for d in cp[CNJ]['documentos']}
    f11=fonte(ds[179921442]);f10=fonte(ds[179917788]);f28=fonte(ds[180256195])
    fss=fonte(ds[179932139],'coleta_documental/auditoria/179932139.pdf','0602844-54.2026.6.00.0000')
    fss['id_documento_originario']=179926797
    fss['nota']='Traslado juntado à AIJE; o cabeçalho original é SS-Ele 0602844-54. A própria peça determina seu traslado à AIJE. Não contar como novo ato estatístico nem como decisão emitida na AIJE.'
    f13=fonte(ds[179935558],'coleta_documental/auditoria/179935558.html')
    ms=cp['0603256-82.2026.6.00.0000']['documentos'][0];fms=fonte(ms,cnj_documento='0603256-82.2026.6.00.0000')
    v=copy.deepcopy(antigo)
    motivo=('A decisão de 11/10 não acolhe a suspensão integral do canal, mas impõe aos seus responsáveis abstenção de divulgar conteúdos cuja ilicitude já foi reconhecida pelo TSE, nos limites das respectivas decisões. A SS-Ele de 13/10 susta exclusivamente o item b (restabelecimento) e preserva expressamente o item c (abstenção). A ordem parcial sobre o canal e esse conjunto objetivamente delimitado de conteúdos satisfaz a regra de atendimento parcial positivo; não se conta como concessão da suspensão integral.')
    sinopse=('Flávio ajuizou AIJE contra Janones e a chapa de Lula sobre o canal Exército do Lula, pedindo suspensão, restrição de publicações e retirada de conteúdos. Em 11/10, a Corregedoria considerou insuficiente a prova para suspender todo o canal e determinou seu restabelecimento, mas impôs aos responsáveis abstenção de reproduzir conteúdos já declarados ilícitos pelo TSE, nos limites das decisões anteriores. Em 13/10, a Presidência sustou apenas a ordem de restabelecimento na SS-Ele 0602844-54, preservando expressamente a abstenção; o atendimento codificado é parcial por essa restrição remanescente, sem afirmar suspensão integral deferida na AIJE. A decisão posterior na própria AIJE apenas pediu referendo urgente, e o despacho de 28/10 tratou do interesse nos pedidos ainda pendentes. O mandado de segurança de 23/10 suspendeu medidas administrativas em nível de canal e expressamente distinguiu a SS-Ele, sem julgamento final do mérito ou do referendo da AIJE documentado até o corte.')
    v.update(incluir=True,atendido=True,categoria='comparável',motivo=motivo,fundamento=motivo,
        objeto='Canal Exército do Lula: suspensão integral e restrição de conteúdos previamente declarados ilícitos',
        pedido='suspensão do canal e, subsidiariamente, restrição das publicações e conteúdos ilícitos nele difundidos',
        sinopse=sinopse,grau='parcial',status='ordem cautelar parcial; restabelecimento sustado em contracautela; mérito e referendo não concluídos na documentação',
        url_peca=f11['url'],tipo_peca='Decisão',data_ato_referencia='2026-10-11',data_metadata='2026-10-11',
        origem_data_referencia='assinatura da decisão de referência; efeito do item c confirmado pela contracautela de 13/10',
        grau_certeza='alto quanto ao teor dos dispositivos; enquadramento curatorial explicitado',
        status_fonte='decisão própria da AIJE e traslado da SS-Ele lidos; pronunciamentos posteriores reconciliados',
        fonte_classificacao='leitura das decisões oficiais da AIJE, traslado da SS-Ele e decisão contextual do MSCiv',
        colegialidade_situacao='sem revisão comprovada',
        colegialidade_justificativa='A contracautela é monocrática em processo conexo e não equivale a referendo pelo Plenário. O exame colegiado foi solicitado, mas não há conclusão documentada até o corte.',
        evidencia_data='2026-10-11',
        relato={'titulo':'Canal Exército do Lula: restrição parcial preservada e conflito entre procedimentos','texto':sinopse,'requer_atualizacao':True},
        revisao={'estado':'reconciliado por leitura dos dispositivos e delimitação do objeto comparado',
            'indice_lote':antigo.get('revisao',{}).get('indice_lote',203),
            'codigo_leitura':'parcial',
            'polos_formais':antigo.get('revisao',{}).get('polos_formais'),
            'pronto_publicacao':True,'utilizar_em_percentuais_finais':True,'pendencias':[],
            'limites':['O funcionamento efetivo do canal não é usado como resultado da AIJE.',
                'A contracautela não é convertida em concessão da suspensão integral na AIJE.',
                'A ordem de abstenção alcança conteúdos já identificados em pronunciamentos anteriores, no canal individualizado; não se codifica proibição geral de toda crítica futura.',
                'A SS-Ele não foi impugnada no MSCiv 0603256-82; sua revogação não é inferida da liminar contra atos administrativos.'],
            'fontes_reconciliacao':[f10,f11,fss,f13,fms,f28]})
    (ROOT/'curadoria_revisao_conexa.json').write_text(json.dumps({CNJ:v},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Revisão conexa materializada: atendimento parcial, sem confundir procedimentos.')

if __name__=='__main__':main()
