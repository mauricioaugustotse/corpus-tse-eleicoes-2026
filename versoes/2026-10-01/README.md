# Corpus oficial — atos do TSE no ciclo das Eleições 2026

Fonte primária: https://dadosabertos.tse.jus.br/id/dataset/processual-2026 (Secretaria Judiciária do TSE, sistema PJe).

Recorte de `DT_DECISAO`: **2025-10-03 a 2026-09-30**, inclusive. A data final foi informada em `--data-fim`; a última data disponível nos ZIPs é **2026-09-30**. Geração dos arquivos e SHA-256: `fontes.json`.

`atos.csv` tem uma linha por `NR_PROCESSO + SQ_DECISAO` da instância 3, `SG_UF_TRIBUNAL=DF`, e inclui apenas `DS_TIPO_DECISAO` igual a `Decisão` ou `Acórdão`. `processos.csv` tem uma linha por CNJ com ao menos um ato selecionado. Os dois CSVs usam UTF-8 com BOM e ponto e vírgula. As colunas originais do arquivo de decisões ficam sem prefixo em `atos.csv`; as de processo recebem `PROCESSO_`. Em `processos.csv`, os campos originais de processo ficam sem prefixo. Os arquivos oficiais completos, inclusive LEIAME em PDF, estão em `originais/`.

Os gráficos em `graficos/` usam somente estas duas tabelas. Cada HTML contém seu SVG e abre sem internet; o SVG também é fornecido separadamente. `resumo.json` contém os valores usados nos gráficos. A classe DR e os assuntos oficiais que contêm `Propaganda Eleitoral` formam um recorte objetivo de comunicação; o grupo não mede procedência, remoção, favorecimento ou resultado de mérito.

**Limites:** `DT_DECISAO` é a data do ato no arquivo PJe; data de sessão e data de publicação são fatos diferentes. `NM_AUTOR_DECISAO` é o autor do ato, não necessariamente o relator do processo. O rótulo oficial `DS_TIPO_DECISAO=Decisão` pode incluir peça materialmente intitulada despacho; a qualificação do teor exige conferência individual. O catálogo processual não fornece dispositivo ou URL direta de cada peça. A seleção por processo não substitui exame jurídico individual.

Reprodução offline: `python tse_corpus_eleicoes_2026.py --saida <esta-pasta> --offline`. Os ZIPs congelados nunca são sobrescritos automaticamente.
