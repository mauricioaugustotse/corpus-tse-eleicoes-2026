import unittest
from pathlib import Path
from gerar_config_graficos_juridicos import construir

ROOT=Path(__file__).resolve().parents[1]

class ConfigJuridicosTests(unittest.TestCase):
    def dados(self):
        base={'total':20,'votacao':{'unânime':15,'com divergência':4,'não apurada':1},'ministros_vencidos':{'André Mendonça':19,'Sebastião Reis Júnior':8}}
        presid={'total':4,'votacao':{'unânime':3,'com divergência':1},'ministros_vencidos':{'Sebastião Reis Júnior':1},'processos_comparaveis':4,'situacao_confrontos':{'liminar mantida':2,'liminar modificada':1,'pendente':1}}
        return {'corpus':base,'presidencial':presid},{str(i):{'incluir':True} for i in range(4)}

    def test_config_preserva_pendente_e_inclui_sebastiao_sem_cortar_eixo(self):
        resumo,curadoria=self.dados();configs=construir(ROOT,resumo,curadoria)
        self.assertEqual(len(configs),5)
        for nome,c in configs.items():
            s=c['spec'];self.assertTrue(all(len(t['data'])==len(s['labels']) for t in s['series']))
            if nome.startswith('08a_'):
                self.assertEqual(sum(x['data'][0] for x in s['series']),4)
                self.assertIn('Situação pendente de revisão',[x['label'] for x in s['series']])
            if nome.startswith('09a_'):
                self.assertIn('Sebastião Reis Júnior',s['labels'])
                self.assertGreater(s['axis']['cap'],19)
            if nome.startswith('08b_'):
                self.assertAlmostEqual(sum(x['data'][0] for x in s['series']),100)

    def test_curadoria_marcada_nao_pronta_impede_geracao(self):
        resumo,curadoria=self.dados();curadoria['0']['revisao']={'pronto_publicacao':False}
        with self.assertRaisesRegex(ValueError,'não estão prontos'):construir(ROOT,resumo,curadoria)

    def test_curadoria_e_resumo_diferentes_impedem_geracao(self):
        resumo,curadoria=self.dados();curadoria['0']['incluir']=False
        with self.assertRaisesRegex(ValueError,'divergem'):construir(ROOT,resumo,curadoria)

    def test_lacuna_documental_excluida_nao_entra_nos_percentuais(self):
        resumo,curadoria=self.dados()
        curadoria['lacuna']={'incluir':False,'revisao':{'pronto_publicacao':False,'utilizar_em_percentuais_finais':False}}
        configs=construir(ROOT,resumo,curadoria)
        figura=next(c for nome,c in configs.items() if nome.startswith('08a_'))
        self.assertEqual(sum(s['data'][0] for s in figura['spec']['series']),4)

if __name__=='__main__':unittest.main()
