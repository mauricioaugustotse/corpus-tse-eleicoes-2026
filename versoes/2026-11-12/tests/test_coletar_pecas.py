import unittest
from coletar_pecas import selecionar

class SelecaoDocumentalTests(unittest.TestCase):
    def doc(self, ident, data, **extra):
        return dict(idProcessoDocumento=ident,tipoDocumento='Decisão',documentoStorage='tse/2026/10/31/hash',dataAssinatura=data,publico=True,**extra)
    def test_corte_inclusivo_e_protecao_de_documentos(self):
        docs=[self.doc(1,'2026-10-31'),self.doc(2,'2026-11-01'),self.doc(3,'2026-10-30',documentoSigiloso=True)]
        self.assertEqual([d['id_documento'] for d in selecionar({'documentos':docs})],[1])
    def test_data_decisao_distingue_juntada_posterior(self):
        proc={'documentos':[self.doc(1,'2026-11-03')],'decisoes':[{'idProcessoDocumento':1,'dataDecisao':'2026-10-31'}]}
        self.assertEqual(next(selecionar(proc))['data_metadata'],'2026-10-31')
    def test_copias_regionais_e_pecas_sem_data_ficam_fora(self):
        doc=self.doc(1,'2026-10-31');doc['documentoStorage']='regional/df/hash'
        self.assertEqual(list(selecionar({'documentos':[doc,self.doc(2,'')]})),[])

    def test_decisoes_nulas_nao_impedem_selecao_de_documento_datado(self):
        proc={'decisoes':None,'documentos':[self.doc(1,'2026-10-31')]}
        self.assertEqual([d['id_documento'] for d in selecionar(proc)],[1])

    def test_documentos_nulos_resultam_selecao_vazia_sem_presumir_decisao(self):
        self.assertEqual(list(selecionar({'decisoes':None,'documentos':None})),[])
