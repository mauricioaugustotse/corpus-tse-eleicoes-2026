# Corpus público do TSE para o ciclo das Eleições 2026

Este repositório permite conferir os números do [relatório no Notion](https://app.notion.com/p/2816527d9bee432da3acce02566b1534). O [pacote de dados](versoes/2026-10-01/LEIA_PRIMEIRO.md) reúne os cinco arquivos do conjunto [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026) gerados em **1º/10/2026**. Selecionamos os atos com data de **03/10/2025 a 30/09/2026**, inclusive.

## Confira sem programar

1. Abra [atos.csv](versoes/2026-10-01/atos.csv). As **933 linhas de dados** representam registros classificados pelo TSE como Decisão ou Acórdão. Um processo pode ter mais de um ato.
2. Abra [processos.csv](versoes/2026-10-01/processos.csv). São **751 processos**, um por número CNJ. A coluna `FL_RECORTE_COMUNICACAO` marca os **286 processos** com assunto Propaganda Eleitoral ou classe Direito de Resposta. Eles somam **364 atos**.
3. Abra [confrontos.csv](versoes/2026-10-01/confrontos.csv). A lista reúne **132 processos candidatos** com representantes das campanhas de Lula e Flávio Bolsonaro em polos opostos. O motivo de cada inclusão ou exclusão aparece na própria linha.
4. Abra [relatos.csv](versoes/2026-10-01/relatos.csv). Os **107 CNJs relatados** são exatamente os 107 marcados `sim` na coluna `incluir_comparativo` de `confrontos.csv`.

Para abrir os CSVs no Excel, use **Dados → De Texto/CSV**, escolha **UTF-8** e o separador **ponto e vírgula**. Não conte o cabeçalho. O [dicionário](versoes/2026-10-01/dicionario.md) explica as colunas oficiais e o [dicionário da curadoria](versoes/2026-10-01/dicionario_curadoria.md) explica a classificação dos confrontos.

| Número citado | Onde conferir |
| --- | --- |
| 933 atos em 751 processos | [atos.csv](versoes/2026-10-01/atos.csv) e [processos.csv](versoes/2026-10-01/processos.csv) |
| 286 processos no filtro de comunicação e 364 atos | `FL_RECORTE_COMUNICACAO` nos dois CSVs e [resumo.json](versoes/2026-10-01/resumo.json) |
| 107 confrontos com resultado documentado | `incluir_comparativo=sim` em [confrontos.csv](versoes/2026-10-01/confrontos.csv) e 107 linhas em [relatos.csv](versoes/2026-10-01/relatos.csv) |
| Medidas atendidas à campanha de Lula, integral ou parcialmente | 29 de 48 processos classificados, ou 60,4% |
| Medidas atendidas à campanha de Flávio, integral ou parcialmente | 20 de 59 processos classificados, ou 33,9% |

Essas taxas descrevem **apenas os 107 resultados documentados**. Em sete processos com ato em 30/09, a peça ainda não pôde ser lida. Eles constam nominalmente do CSV como pendências e não recebem resultado por suposição. Há outras duas pendências de leitura. Os números podem mudar após essa conferência. O pacote preserva [oito peças examinadas de 30/09](versoes/2026-10-01/pecas/indice_30set.json) com seus hashes. Uma liminar concedida ou negada não significa decisão final da ação.

O filtro de comunicação usa campos oficiais, mas pode deixar outras disputas sobre comunicação fora do grupo. Dos 107 confrontos classificados, **106** integram o corpus de atos. O CNJ **0601315-97.2026.6.00.0000** tem resultado documentado por certidão e aparece só como suplemento documental dos confrontos. Ele não aumenta os 933 atos nem os 751 processos do painel geral.

## Votações e revisão das liminares

A [análise documental da colegialidade](analises/colegialidade) conserva o corte em **30/09/2026** e individualiza as fontes: dos 200 registros de acórdão, **174 têm votação unânime identificada, 15 apresentam divergência e 11 permanecem sem votação apurada**. Nos 107 confrontos presidenciais, há **22 liminares mantidas e quatro modificadas**, entre 26 reexames colegiados comprovados. A planilha separa ainda uma tutela decidida diretamente pelo colegiado, 76 liminares sem revisão colegiada comprovada e quatro decisões individuais de mérito. Ausência de revisão localizada não é prova de pendência processual.

As [planilhas e peças oficiais](analises/colegialidade/README.md) permitem conferir os ministros vencidos e os denominadores. Os [cinco gráficos da colegialidade](analises/colegialidade/graficos) distinguem o universo dos 200 acórdãos e o recorte dos confrontos.

As votações foram apuradas nos extratos das exportações oficiais em CSV do [SJUR](https://jurisprudencia.tse.jus.br/) e nas peças do PJe. A coleta utilizou Python e Playwright para operar a pesquisa e a exportação do portal. O tratamento em Python normalizou os números CNJ, selecionou os registros pertinentes e conciliou as fontes com cada ato do corpus; a classificação jurídica foi conferida na proclamação dos julgamentos. O [guia de reprodução](REPRODUCAO.md#reproduzir-a-apuração-das-votações) explica os programas e como examinar outras exportações do SJUR.

## Arquivos e gráficos

Os [seis gráficos do corpus](versoes/2026-10-01/graficos) apresentam os dados dos dois CSVs oficiais. Os onze HTMLs, contando os cinco da colegialidade, reproduzem os gráficos publicados no Notion e carregam a biblioteca Chart.js pela internet. Os SVGs são alternativas estáticas para abrir sem conexão, com apresentação própria dos programas de reprodução. Os valores exatos estão em [resumo.json](versoes/2026-10-01/resumo.json). Os [cinco ZIPs oficiais](versoes/2026-10-01/originais) foram preservados. [fontes.json](versoes/2026-10-01/fontes.json) registra seus endereços, datas de geração e hashes SHA-256. O [manifesto](versoes/2026-10-01/manifesto.json) permite conferir os demais arquivos.

O [guia técnico](REPRODUCAO.md) ensina a repetir os cálculos e a baixar outra extração. Os 933 registros não são 933 julgamentos definitivos. Alguns atos chamados “Decisão” só dão andamento ao processo, e o portal do TSE pode atualizar seus arquivos.
