# Corpus oficial — atos do TSE no ciclo das Eleições 2026

**Versão em preparação.** O estado atual e as instruções de continuação estão em [RETOMADA.md](RETOMADA.md). Os resultados comparáveis já documentados estão em `confrontos.csv` e `relatos.csv`, mas a consulta complementar de 280 candidatos ainda pode ampliar o quadro. Pendências não recebem resultado por suposição. Os onze gráficos que preservam a apresentação do Notion estão em `graficos_interativos/`; `graficos/` contém as alternativas SVG do coletor.

Fonte primária: https://dadosabertos.tse.jus.br/id/dataset/processual-2026 (Secretaria Judiciária do TSE, sistema PJe).

Recorte de `DT_DECISAO`: **2025-10-03 a 2026-10-31**, inclusive. A data final foi informada em `--data-fim`; a última data disponível nos ZIPs é **2026-11-10**. Geração dos arquivos e SHA-256: `fontes.json`.

`atos.csv` tem uma linha por `NR_PROCESSO + SQ_DECISAO` da instância 3, `SG_UF_TRIBUNAL=DF`, e inclui apenas `DS_TIPO_DECISAO` igual a `Decisão` ou `Acórdão`. `processos.csv` tem uma linha por CNJ com ao menos um ato selecionado. Os dois CSVs usam UTF-8 com BOM e ponto e vírgula. As colunas originais do arquivo de decisões ficam sem prefixo em `atos.csv`; as de processo recebem `PROCESSO_`. Em `processos.csv`, os campos originais de processo ficam sem prefixo. Os arquivos oficiais completos, inclusive LEIAME em PDF, estão em `originais/`.

Os gráficos em `graficos/` usam somente estas duas tabelas. Os HTMLs publicados conservam os estilos e controles da página do estudo, com Chart.js 4.4.1 carregado pela internet; os SVGs são representações estáticas independentes, disponíveis sem conexão. A reprodução recalcula os SVGs e preserva os HTMLs existentes. Uma extração em pasta vazia recebe HTMLs simples com SVG incorporado. `resumo.json` contém os valores usados nos gráficos. A classe DR e os assuntos oficiais que contêm `Propaganda Eleitoral` formam um recorte objetivo de comunicação; o grupo não mede procedência, remoção, favorecimento ou resultado de mérito.

**Limites:** `DT_DECISAO` é a data do ato no arquivo PJe; data de sessão e data de publicação são fatos diferentes. `NM_AUTOR_DECISAO` é o autor do ato, não necessariamente o relator do processo. O rótulo oficial `DS_TIPO_DECISAO=Decisão` pode incluir peça materialmente intitulada despacho; a qualificação do teor exige conferência individual. O catálogo processual não fornece dispositivo ou URL direta de cada peça. A seleção por processo não substitui exame jurídico individual.

Reprodução estatística offline: `python tse_corpus_eleicoes_2026.py --saida <esta-pasta> --offline --data-fim 2026-10-31`. Os ZIPs congelados nunca são sobrescritos automaticamente.

Para reproduzir a curadoria e a colegialidade, extraia os ZIPs de `documentos_oficiais/` nesta pasta, conservando seus caminhos internos. Execute `python consolidar_curadoria.py`, `python gerar_confrontos.py` e `python apurar_colegialidade.py --inventario-publico`. O último comando usa o espelho documental congelado mesmo que exista outra coleta local em andamento. As classificações jurídicas permanecem explícitas nos JSONs; o programa não as infere automaticamente.

Execute `python gerar_config_graficos_juridicos.py` e `python atualizar_graficos_interativos.py` para reconstruir os onze HTMLs. A exportação PNG e a conferência dos controles usam `python renderizar_graficos.py`, com Playwright e Chromium disponíveis. `python verificar_atualizacao.py` confere o manifesto e a base estatística; `python verificar_curadoria.py` confere denominadores, fontes e gráficos; `python -m unittest discover -s tests -v` executa os testes. O relatório `graficos_interativos/verificacao_renderizacao.json` registra a conferência dos onze canvases renderizados.
