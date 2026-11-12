"""Protege o trabalho salvo contra pausas, arquivos danificados e duas execuções."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coletar_pecas import arquivo_conferido, preservar_documentos, salvar
from controle_coleta import coletor_ativo, trava_coleta


RAIZ = Path(__file__).resolve().parents[1]


class RetomadaColetaTests(unittest.TestCase):
    def test_retomada_parcial_preserva_pecas_posteriores_ja_salvas(self):
        registro = {
            'documentos': [
                {'url': 'https://oficial/primeira', 'status': 'pendente'},
                {'url': 'https://oficial/segunda', 'status': 'conferido', 'sha256': 'segundo'},
                {'url': 'https://oficial/terceira', 'status': 'conferido', 'sha256': 'terceiro'},
            ]
        }
        primeira = {'url': 'https://oficial/primeira', 'status': 'conferido', 'sha256': 'primeiro'}
        mesclados = preservar_documentos(registro, [primeira])
        por_url = {doc['url']: doc for doc in mesclados}
        self.assertEqual(len(mesclados), 3)
        self.assertEqual(por_url[primeira['url']], primeira)
        self.assertEqual(por_url['https://oficial/segunda'], registro['documentos'][1])
        self.assertEqual(por_url['https://oficial/terceira'], registro['documentos'][2])

    def test_mescla_inclui_nova_peca_sem_duplicar_url(self):
        antigo = {'url': 'https://oficial/a', 'status': 'pendente'}
        novo = {'url': antigo['url'], 'status': 'conferido'}
        adicional = {'url': 'https://oficial/b', 'status': 'conferido'}
        mesclados = preservar_documentos({'documentos': [antigo]}, [novo, adicional])
        self.assertEqual({d['url']: d for d in mesclados}, {novo['url']: novo, adicional['url']: adicional})
        self.assertEqual(len(mesclados), 2)

    def test_arquivo_conferido_exige_bytes_integros_e_texto_preservado(self):
        with tempfile.TemporaryDirectory() as pasta:
            root = Path(pasta)
            arquivo = root / 'pecas' / 'decisao.html'
            arquivo.parent.mkdir()
            conteudo = '<p>Decisão oficial</p>'.encode('utf-8')
            doc = {'status': 'conferido', 'arquivo': 'pecas/decisao.html',
                   'sha256': hashlib.sha256(conteudo).hexdigest()}
            self.assertFalse(arquivo_conferido(root, doc))
            arquivo.write_bytes(conteudo)
            self.assertFalse(arquivo_conferido(root, doc))
            arquivo.with_suffix('.txt').write_text('Decisão oficial', encoding='utf-8')
            self.assertTrue(arquivo_conferido(root, doc))
            arquivo.write_bytes(b'arquivo incompleto')
            self.assertFalse(arquivo_conferido(root, doc))

    def test_salvar_preserva_json_completo_e_unicode(self):
        with tempfile.TemporaryDirectory() as pasta:
            path = Path(pasta) / 'checkpoint.json'
            dados = {'processo': {'documentos': [{'tipo': 'Acórdão', 'status': 'conferido'}]}}
            salvar(path, dados)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), dados)
            dados['outro'] = {'documentos': [], 'completo': False}
            salvar(path, dados)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), dados)

    def test_falha_na_troca_atomica_preserva_checkpoint_anterior(self):
        with tempfile.TemporaryDirectory() as pasta:
            path = Path(pasta) / 'checkpoint.json'
            anterior = {'processo': {'documentos': [{'url': 'https://oficial/salvo'}]}}
            salvar(path, anterior)
            bytes_anteriores = path.read_bytes()
            with patch.object(Path, 'replace', side_effect=OSError('troca indisponível')):
                with self.assertRaises(OSError):
                    salvar(path, {'processo': {'documentos': []}})
            self.assertEqual(path.read_bytes(), bytes_anteriores)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')), anterior)

    def test_trava_impede_segundo_processo_e_libera_ao_terminar(self):
        with tempfile.TemporaryDirectory() as pasta:
            root = Path(pasta)
            self.assertFalse(coletor_ativo(root))
            with trava_coleta(root):
                self.assertTrue(coletor_ativo(root))
                codigo = (
                    'from pathlib import Path\n'
                    'from controle_coleta import trava_coleta\n'
                    'import sys\n'
                    'try:\n'
                    '    with trava_coleta(Path(sys.argv[1])):\n'
                    '        print("adquiriu")\n'
                    'except RuntimeError:\n'
                    '    print("bloqueado")\n'
                )
                resultado = subprocess.run(
                    [sys.executable, '-c', codigo, str(root)], cwd=RAIZ,
                    capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(resultado.returncode, 0, resultado.stderr)
                self.assertEqual(resultado.stdout.strip(), 'bloqueado')
            self.assertFalse(coletor_ativo(root))
            with trava_coleta(root):
                self.assertTrue(coletor_ativo(root))

    def test_trava_e_liberada_mesmo_quando_coleta_falha(self):
        with tempfile.TemporaryDirectory() as pasta:
            root = Path(pasta)
            with self.assertRaisesRegex(ValueError, 'falha simulada'):
                with trava_coleta(root):
                    raise ValueError('falha simulada')
            self.assertFalse(coletor_ativo(root))


if __name__ == '__main__':
    unittest.main()
