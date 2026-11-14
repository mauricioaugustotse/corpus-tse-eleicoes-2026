"""Envia um arquivo pelo endereço temporário fornecido pela integração Notion."""
import json
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parent
PASTA=ROOT/'coleta_documental/publicacao'
def main():
    cfg=json.loads((PASTA/'upload_atual.json').read_text(encoding='utf-8'))
    path=ROOT/'graficos_interativos'/cfg['filename']
    assert path.resolve().is_relative_to((ROOT/'graficos_interativos').resolve())
    assert cfg.get('upload_method','POST')=='POST' and cfg.get('upload_form_field','file')=='file'
    with path.open('rb') as f:
        resposta=requests.post(cfg['upload_url'],headers=cfg['upload_headers'],files={'file':(path.name,f,cfg['content_type'])},timeout=90,allow_redirects=False)
    resposta.raise_for_status();dados=resposta.json()
    (PASTA/'resultado_ultimo.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert dados.get('markdown_source'), 'Resposta sem referência para anexar o arquivo'
    indice=PASTA/'uploads_notion.json';lista=json.loads(indice.read_text(encoding='utf-8')) if indice.exists() else []
    lista=[r for r in lista if r['filename']!=path.name]
    lista.append({'filename':path.name,'file_upload_id':cfg['file_upload_id'],'markdown_source':dados['markdown_source']})
    indice.write_text(json.dumps(lista,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'filename':path.name,'enviado':True,'total_anexos':len(lista)},ensure_ascii=False))
if __name__=='__main__':main()
