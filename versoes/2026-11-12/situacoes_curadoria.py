"""Registra o estágio da medida nos lotes manualmente revistos."""
import json
from pathlib import Path
from revisar_novos_b import MERITO, REVOGADAS

ROOT=Path(__file__).resolve().parent
MERITO_COLEG={'0600976','0601014','0601016','0601315','0601767','0601768','0601788','0601789','0601813','0601838','0601882','0601931','0602025','0602109'}
MERITO_INDIV={'0601773','0601817','0602099'}
MODIFICADAS={'0600950','0600955','0600966','0600973','0601015','0601786','0601806','0601849','0601850','0601862','0602148'}

def main():
    for origem,destino,historico in [('curadoria_historicos_outubro.json','situacoes_historicos.json',True),('curadoria_novos_b.json','situacoes_novos_b.json',False)]:
        dados=json.loads((ROOT/origem).read_text(encoding='utf-8'));situacoes={}
        for cnj,v in dados.items():
            prefixo=cnj[:7];i=v['revisao_outubro'].get('indice_lote_b')
            if not v['incluir']:
                valor='sem resultado comparável';just='Processo excluído do denominador; consultar o motivo documental da curadoria.'
            elif (historico and prefixo in MERITO_COLEG) or (not historico and i in MERITO):
                valor='mérito colegiado';just='O último resultado comparável é de mérito, ou recurso contra esse julgamento, conforme sinopse e peça oficial.'
            elif historico and prefixo in MERITO_INDIV:
                valor='mérito individual';just='Resultado de mérito monocrático; eventual recurso ainda não tem resultado colegiado final documentado até o corte.'
            elif (historico and prefixo in MODIFICADAS) or (not historico and i in REVOGADAS|{65}):
                valor='modificada';just='O Plenário substituiu o resultado cautelar anterior no referendo, nos limites do dispositivo; não se trata necessariamente de mérito.'
            elif historico and prefixo=='0601962':
                valor='modificada individualmente';just='Reconsideração parcial monocrática permite painéis para transmissão do comício, mantendo a remoção do vídeo; não há referendo final comprovado.'
            elif v['tipo_peca'].startswith(('Ac','Certid')):
                valor='mantida';just='O pronunciamento colegiado de referência mantém a tutela ou a negativa cautelar anterior, nos limites do dispositivo.'
            else:
                valor='sem revisão comprovada';just='A medida de referência é monocrática; não foi encontrado resultado colegiado final que a substitua ou referende até o corte.'
            situacoes[cnj]={'colegialidade_situacao':valor,'justificativa':just,'url_peca':v['url_peca'],'data_ato_referencia':v['data_ato_referencia']}
        (ROOT/destino).write_text(json.dumps(situacoes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(destino,len(situacoes))

if __name__=='__main__':main()
