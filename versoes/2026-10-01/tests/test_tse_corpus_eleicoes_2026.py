import csv
import io
import tempfile
import unittest
import zipfile
from datetime import date
from pathlib import Path

import tse_corpus_eleicoes_2026 as corpus


CNJ_RP = "0600001-00.2026.6.00.0000"
CNJ_DR = "0600002-00.2026.6.00.0000"


def processo(cnj, classe, assunto, relator="RELATOR DO PROCESSO"):
    return {"NR_PROCESSO": cnj, "NR_INSTANCIA": "3", "SG_UF_TRIBUNAL": "DF",
            "SG_CLASSE": classe, "DS_ASSUNTO_PRINCIPAL": assunto,
            "NM_RELATOR": relator, "DS_URL_PROCESSO": f"https://oficial/{cnj}"}


def ato(cnj, sequencial, data, tipo, autor="AUTOR DO ATO"):
    return {"NR_PROCESSO": cnj, "SQ_DECISAO": sequencial, "DT_DECISAO": data,
            "DS_TIPO_DECISAO": tipo, "NM_AUTOR_DECISAO": autor,
            "NR_INSTANCIA": "3", "SG_UF_TRIBUNAL": "DF"}


class CorpusTests(unittest.TestCase):
    def fontes(self):
        return {
            "processos": [processo(CNJ_RP, "Rp", "Outro assunto"),
                           processo(CNJ_DR, "DR", "Direito de Resposta")],
            "assuntos": [{"NR_PROCESSO": CNJ_RP, "NR_INSTANCIA": "3", "SG_UF_TRIBUNAL": "DF",
                          "CD_ASSUNTO": "1", "DS_ASSUNTO": "Propaganda Política - Propaganda Eleitoral - Redes Sociais"}],
            "partes": [{"NR_PROCESSO": CNJ_RP, "NR_INSTANCIA": "3", "SG_UF_TRIBUNAL": "DF",
                        "DS_POLO": "Pólo ativo", "TP_PARTE": "REPRESENTANTE", "NM_PARTE": "CAMPANHA"},
                       {"NR_PROCESSO": CNJ_RP, "NR_INSTANCIA": "3", "SG_UF_TRIBUNAL": "DF",
                        "DS_POLO": "Pólo ativo", "TP_PARTE": "ADVOGADO", "NM_PARTE": "NÃO É PARTE"}],
            "decisoes": [ato(CNJ_RP, "100", "03/10/2025", "Decisão"),
                         ato(CNJ_RP, "101", "03/10/2025", "Acórdão"),
                         ato(CNJ_DR, "102", "04/10/2025", "Decisão"),
                         ato(CNJ_DR, "103", "02/10/2025", "Decisão"),
                         ato(CNJ_DR, "104", "04/10/2025", "Despacho")],
        }

    def test_chave_de_ato_recorte_tematico_e_autoria_sao_distintos_da_relatoria(self):
        atos, casos, controle = corpus.construir_corpus(self.fontes())
        self.assertEqual(len(atos), 3)
        self.assertEqual(len(casos), 2)
        self.assertEqual(len({a["CHAVE_ATO"] for a in atos}), 3)
        self.assertEqual(controle["atos_anteriores_ao_inicio"], 1)
        self.assertEqual({c["NR_PROCESSO"]: c["FL_RECORTE_COMUNICACAO"] for c in casos},
                         {CNJ_RP: 1, CNJ_DR: 1})
        rp = next(c for c in casos if c["NR_PROCESSO"] == CNJ_RP)
        self.assertEqual(rp["FL_PROPAGANDA_OFICIAL"], 1)
        self.assertEqual(rp["FL_DIREITO_RESPOSTA"], 0)
        self.assertIn("REPRESENTANTE: CAMPANHA", rp["PARTES_POLO_ATIVO"])
        self.assertNotIn("NÃO É PARTE", rp["PARTES_POLO_ATIVO"])
        resumo = corpus.resumir(atos, casos, controle)
        self.assertEqual(resumo["atos_por_tipo"], {"Acórdão": 1, "Decisão": 2})
        self.assertEqual(resumo["atos_por_mes_tipo"]["2025-10"], {"Decisão": 2, "Acórdão": 1})
        self.assertEqual(resumo["atos_por_autor"], {"AUTOR DO ATO": 3})
        self.assertNotIn("RELATOR DO PROCESSO", resumo["atos_por_autor"])

    def test_rejeita_sequencial_repetido_no_mesmo_processo(self):
        fontes = self.fontes()
        fontes["decisoes"].append(ato(CNJ_RP, "100", "05/10/2025", "Decisão"))
        with self.assertRaisesRegex(ValueError, "chave de ato repetida"):
            corpus.construir_corpus(fontes)

    def test_corte_inclusivo_de_30set_e_rejeicao_de_data_futura(self):
        fontes = self.fontes()
        fontes["decisoes"].append(ato(CNJ_RP, "105", "30/09/2026", "Decisão"))
        atos_29, _, _ = corpus.construir_corpus(fontes, data_fim=date(2026, 9, 29))
        atos_30, _, controle = corpus.construir_corpus(fontes, data_fim=date(2026, 9, 30))
        self.assertEqual((len(atos_29), len(atos_30)), (3, 4))
        self.assertEqual(controle["ultima_data_disponivel"], "2026-09-30")
        self.assertEqual(controle["data_fim_parametrizada"], "2026-09-30")
        with self.assertRaisesRegex(ValueError, "posterior à última data disponível"):
            corpus.construir_corpus(fontes, data_fim=date(2026, 10, 1))

    def test_csv_oficial_exige_esquema_exato_e_geracao_uniforme(self):
        def zip_decisoes(path, geracoes, colunas=corpus.SCHEMAS["decisoes"]):
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=colunas, delimiter=";", lineterminator="\n")
            writer.writeheader()
            for i, (dia, hora) in enumerate(geracoes):
                linha = {campo: "" for campo in colunas}
                valores = dict(DT_GERACAO=dia, HH_GERACAO=hora, ANO_ELEICAO="2026",
                               NR_PROCESSO=CNJ_RP, SG_UF_TRIBUNAL="DF", NR_INSTANCIA="3",
                               SQ_DECISAO=str(i), DT_DECISAO="29/09/2026", DS_TIPO_DECISAO="Decisão")
                linha.update({campo: valor for campo, valor in valores.items() if campo in colunas})
                writer.writerow(linha)
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("decisoes.csv", buffer.getvalue().encode("latin-1"))

        with tempfile.TemporaryDirectory() as pasta:
            path = Path(pasta) / "decisoes.zip"
            zip_decisoes(path, [("30/09/2026", "06:00:00")])
            linhas, meta = corpus._ler_fonte(path, "decisoes")
            self.assertEqual((len(linhas), meta["linhas_nacionais"]), (1, 1))
            zip_decisoes(path, [("30/09/2026", "06:00:00"), ("30/09/2026", "07:00:00")])
            with self.assertRaisesRegex(ValueError, "mais de uma geração"):
                corpus._ler_fonte(path, "decisoes")
            zip_decisoes(path, [("30/09/2026", "06:00:00")], colunas=corpus.SCHEMAS["decisoes"][:-1])
            with self.assertRaisesRegex(ValueError, "schema inesperado"):
                corpus._ler_fonte(path, "decisoes")

    def test_graficos_html_contem_svg_e_tipos_mensais(self):
        atos, casos, controle = corpus.construir_corpus(self.fontes())
        resumo = corpus.resumir(atos, casos, controle)
        with tempfile.TemporaryDirectory() as pasta:
            nomes = corpus.gerar_graficos(Path(pasta), resumo)
            self.assertEqual(len(nomes), 6)
            svg = (Path(pasta) / "02_atos_por_mes.svg").read_text(encoding="utf-8")
            pagina = (Path(pasta) / "02_atos_por_mes.html").read_text(encoding="utf-8")
            self.assertIn("Decisão", svg)
            self.assertIn("Acórdão", svg)
            self.assertIn("out/25", svg)
            self.assertIn("n=3 atos", svg)
            self.assertIn("<svg", pagina)


if __name__ == "__main__":
    unittest.main()
