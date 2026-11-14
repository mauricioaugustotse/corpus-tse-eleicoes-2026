"""Integra lotes revisados e registra, sem resultado presumido, as consultas pendentes."""
import json
from pathlib import Path
from triagem_base_integral import campanha

ROOT=Path(__file__).resolve().parent
def ler(nome):return json.loads((ROOT/nome).read_text(encoding='utf-8'))
def main():
    resultado={}
    for nome in ['curadoria_historicos_outubro.json','curadoria_novos_a.json','curadoria_novos_b.json']:
        lote=ler(nome)
        assert not (set(resultado)&set(lote)),nome
        resultado.update(lote)
    if (ROOT/'curadoria_revisao_conexa.json').exists():resultado.update(ler('curadoria_revisao_conexa.json'))
    for r in ler('triagem_base_integral.json')['sem_coleta']:
        autor='Lula' if 'Lula' in campanha(' | '.join(r['ativo'])) else 'Flávio'
        resultado.setdefault(r['cnj'],{'campanha_autora':autor,'incluir':False,'atendido':None,'categoria':'consulta complementar e curadoria pendentes','motivo':'Processo identificado nos polos de toda a base oficial, fora da seleção documental inicial. Aguarda consulta e análise; não recebe resultado por metadados.','objeto':'','pedido':'','sinopse':'Sem resultado atribuído. A inclusão ou exclusão substantiva depende da leitura das peças até 31/10/2026.','grau':'sem resultado documentado nesta revisão','status':'consulta complementar e curadoria pendentes','url_peca':'','tipo_peca':'','data_ato_referencia':'','fonte_classificacao':'metadados oficiais dos processos e partes; não equivalem à leitura da decisão','grau_certeza':'pendente','status_fonte':'inventário e peças em consulta complementar','revisao':{'pronto_publicacao':False,'utilizar_em_percentuais_finais':False,'pendencias':['Obter e analisar peças oficiais até o corte.']}})
    extra=ROOT/'curadoria_suplementares_outubro.json'
    if extra.exists():resultado.update(ler(extra.name))
    for cnj,r in resultado.items():
        if r.get('incluir') and (r.get('revisao',{}).get('pronto_publicacao') is False or r.get('revisao',{}).get('utilizar_em_percentuais_finais') is False):
            raise ValueError(f'Processo não revisado marcado para entrar no comparativo: {cnj}')
    (ROOT/'curadoria_confrontos.json').write_text(json.dumps(dict(sorted(resultado.items())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(resultado)} alvos; {sum(bool(r["incluir"]) for r in resultado.values())} resultados comparáveis documentados. Lacunas e exclusões permanecem explícitas nos registros.')
if __name__=='__main__':main()
