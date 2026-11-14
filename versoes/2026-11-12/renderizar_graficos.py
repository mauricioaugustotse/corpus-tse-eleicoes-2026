"""Confere os dados no canvas e exporta PNGs a partir dos próprios HTMLs."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
def main():
    pasta=ROOT/'graficos_interativos';config=json.loads((pasta/'dados_graficos.json').read_text(encoding='utf-8'));relatorio=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1200,'height':650},device_scale_factor=1,color_scheme='light')
        for nome,c in config.items():
            erros=[]
            def registrar(exc):erros.append(str(exc))
            page.on('pageerror',registrar)
            page.goto((pasta/nome).as_uri(),wait_until='networkidle',timeout=60000)
            page.wait_for_function('typeof Chart !== "undefined" && Chart.getChart(document.querySelector("canvas")) !== undefined',timeout=15000)
            dados=page.evaluate('''() => {const c=Chart.getChart(document.querySelector('canvas'));return {labels:c.data.labels,series:c.data.datasets.filter(s=>!s.auxiliary).map(s=>({label:s.label,data:s.data})),titulo:document.querySelector('.figure-title').textContent,canvas:!!c.width&&!!c.height}}''')
            esperado=[{'label':s['label'],'data':s['data']} for s in c['spec']['series']]
            assert dados['series']==esperado,(nome,dados['series'],esperado)
            assert dados['labels']==c['spec']['labels'] and dados['titulo']==c['titulo'] and dados['canvas'],nome
            assert not erros,(nome,erros)
            # Valida os controles de legenda antes de retornar ao estado inicial.
            legenda=page.locator('.legend [data-series-index="0"]')
            if legenda.count():legenda.click();legenda.click()
            page.wait_for_timeout(500)
            page.locator('.chart-figure').screenshot(path=str(pasta/(Path(nome).stem+'.png')))
            page.remove_listener('pageerror',registrar)
            relatorio.append({'arquivo':nome,'dados_renderizados_conferidos':True,'erros_javascript':erros,'largura_exportacao':1200})
            print(nome+': OK',flush=True)
        browser.close()
    (pasta/'verificacao_renderizacao.json').write_text(json.dumps(relatorio,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
