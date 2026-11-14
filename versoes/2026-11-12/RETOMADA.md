# Atualização até 31/10/2026 — registro da entrega

**Estado em 14/11/2026: consulta encerrada e página do Notion publicada e conferida.** As 1.295 consultas foram concluídas, e o complemento foi incorporado à curadoria. Não reiniciar a coleta para cumprir instruções antigas da preparação. O conteúdo efetivamente publicado está em `pagina_publicada.md`; o registro de conferência está em `registro_publicacao_notion.json`. As 201 lacunas de fonte são limites documentais explicitados, não consultas ou leituras ainda aguardando execução.

## Ponto de referência

- `resumo.json`: 2.606 atos, 1.841 processos, 713 acórdãos e 1.005 processos no filtro de comunicação.
- `campanha_resumo.json`: 872 candidatos, 432 comparáveis, 201 lacunas documentais, 239 demais exclusões e zero pendências de revisão. Os 432 se dividem em 427 processos do corpus e cinco suplementares.
- `apuracao_colegialidade_resumo.json`: 623 acórdãos unânimes, 89 divergentes e um sem votação apurada; no recorte presidencial, 296 julgamentos em 282 processos, sendo 238 unânimes e 58 divergentes.
- `inventario_documental.json`: 2.795 entradas por URL distinta em 14 ZIPs, com caminhos e hashes; referência pública para restaurar as fontes.
- `confrontos.csv`, `relatos.csv` e `relatos.md`: 432 resultados e relatos, com igualdade dos CNJs incluídos.
- `graficos_interativos/`: onze HTMLs, PNGs derivados e relatório de renderização; `pagina_proposta.md`: atualização editorial com a seção 7 preservada.

Os 201 casos com lacuna já foram consultados; não foi localizada peça decisória elegível até o corte. Essa categoria não prova ausência de atos nem constitui fila de leitura humana. A outra lacuna expressa é o vínculo do acórdão `0601104-61.2026.6.00.0000|4521`. Nenhuma recebe classificação por suposição.

## Conferir e entregar

1. Usar os três resumos como autoridade. O complemento está em `curadoria_suplementares_outubro.json`, e a reconciliação de processos conexos em `curadoria_revisao_conexa.json`. Não transportar os números intermediários de 428 comparáveis ou 280 consultas abertas.
2. Para reprodução documental, extrair os 14 ZIPs nesta pasta e executar `python consolidar_curadoria.py`, `python gerar_confrontos.py` e `python apurar_colegialidade.py --inventario-publico`. O parâmetro usa o espelho congelado, independentemente dos checkpoints.
3. Recalcular gráficos somente se os dados mudarem: `python gerar_config_graficos_juridicos.py`, `python atualizar_graficos_interativos.py` e `python renderizar_graficos.py`. A última etapa exige Playwright e Chromium. Conferir títulos, datas, totais, tooltips e PNGs.
4. Conferir as seções 1 a 6, os 432 relatos e a identidade da seção 7 com a referência. Publicar os anexos e atualizar a mesma página do Notion por alterações dirigidas; confirmar o resultado salvo e os gráficos.
5. Consolidar o manifesto e executar `python verificar_atualizacao.py`, `python verificar_curadoria.py` e `python -m unittest discover -s tests -v`. A preparação registrou 34 testes aprovados; alterações posteriores devem receber as verificações correspondentes.
6. Entregar o branch `atualizacao-corte-2026-10-31` pelo PR existente e registrar a revisão publicada. Preservar a versão histórica, sua tag e `analises/colegialidade`. Não adicionar caches gerais do motor, logs particulares, backups de acesso ou URLs assinadas do Notion ao repositório público.

O [relatório de diferenças](relatorio_diferencas.md) separa a ampliação temporal das revisões retroativas. Uma futura atualização deve criar nova versão; não concatenar extrações usando `SQ_DECISAO` como identificador documental estável.

Página: https://app.notion.com/p/2816527d9bee432da3acce02566b1534

PR: https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/pull/1
