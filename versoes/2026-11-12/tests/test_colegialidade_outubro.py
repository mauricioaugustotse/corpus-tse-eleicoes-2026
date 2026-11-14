import unittest
from apurar_colegialidade import extrair


class ProclamacaoTests(unittest.TestCase):
    def test_voto_de_precedente_nao_contamina_extrato_proprio(self):
        p = extrair('Precedente: por maioria, vencido André Mendonça. EXTRATO DA ATA Relator: Ministro Dias Toffoli. Decisão: O Tribunal, por unanimidade, rejeitou o pedido. Composição: Ministros...')
        self.assertEqual(p['votacao'], 'unânime')
        self.assertEqual(p['vencidos'], [])

    def test_unanimidade_com_vencidos_parciais_e_divergencia(self):
        p = extrair('EXTRATO DA ATA Relator: Ministro Ricardo Villas Bôas Cueva. Decisão: O Tribunal, por unanimidade, referendou a liminar, vencidos, em parte, os Ministros Sebastião Reis Júnior e André Mendonça. Composição: todos.')
        self.assertEqual(p['votacao'], 'com divergência')
        self.assertEqual(set(p['vencidos']), {'Sebastião Reis Júnior', 'André Mendonça'})

    def test_relator_vencido_nao_confunde_redator_vencedor(self):
        p = extrair('EXTRATO DA ATA Relator: Ministro Nunes Marques. Decisão: O Tribunal, por maioria, não referendou, nos termos do voto divergente do Ministro Dias Toffoli, vencido o relator. Redigirá o acórdão o Ministro Dias Toffoli. Composição: todos.')
        self.assertEqual(p['vencidos'], ['Nunes Marques'])

    def test_referencia_artigo_nao_corta_lista_de_vencidos(self):
        p = extrair('EXTRATO DA ATA Relator: Ministro André Mendonça. Decisão: O Tribunal, por maioria, indeferiu, vencidos o relator, a Ministra Estela Aranha (Art. 7º, § 2º, da Resolução-TSE nº 23.598/2019) e o Ministro Nunes Marques. Redigirá o acórdão o Ministro Sebastião Reis Júnior. Composição: todos.')
        self.assertEqual(set(p['vencidos']), {'André Mendonça', 'Estela Aranha', 'Nunes Marques'})

    def test_certidao_usa_primeiro_tribunal_sem_cortar_objeto_regional(self):
        p = extrair('CERTIDÃO RELATOR(A): MINISTRO(A) NUNES MARQUES PRESIDENTE: MINISTRO NUNES MARQUES DECISÃO O Tribunal, por unanimidade, manteve o acórdão proferido pelo Tribunal Regional Eleitoral. Acompanharam o Relator todos os ministros. Composição: todos.')
        self.assertEqual(p['votacao'], 'unânime')
        self.assertEqual(p['relator'], 'Nunes Marques')

    def test_teses_posteriores_nao_tornam_vencedores_em_vencidos(self):
        p = extrair('EXTRATO DA ATA Relator: Ministro Nunes Marques. Decisão: O Tribunal, por maioria, indeferiu a tutela, vencidos os Ministros Ricardo Villas Bôas Cueva, Floriano de Azevedo Marques e Estela Aranha. Quanto à tese, por maioria, deliberou, nos termos do voto do relator com ajustes do Ministro André Mendonça, vencidos os Ministros Ricardo Villas Bôas Cueva e Floriano de Azevedo Marques. Acompanham integralmente o relator os Ministros André Mendonça, Dias Toffoli e Antonio Carlos Ferreira. Composição: todos.')
        self.assertEqual(set(p['vencidos']), {'Ricardo Villas Bôas Cueva', 'Floriano de Azevedo Marques', 'Estela Aranha'})

    def test_sessao_virtual_entre_meses_usa_data_final(self):
        p=extrair('EXTRATO DA ATA Decisão: O Tribunal, por unanimidade, indeferiu. Composição: todos. SESSÃO VIRTUAL EXTRAORDINÁRIA DE 30.9 A 2.10.2026.')
        self.assertEqual(p['data_fim_sessao'], '2026-10-02')

    def test_primeiro_dia_ordinal_na_data_da_sessao(self):
        p=extrair('EXTRATO DA ATA Decisão: O Tribunal, por unanimidade, indeferiu. Composição: todos. SESSÃO VIRTUAL ORDINÁRIA DE 25.9 A 1º.10.2026.')
        self.assertEqual(p['data_fim_sessao'], '2026-10-01')


if __name__ == '__main__': unittest.main()
