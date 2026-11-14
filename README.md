# Corpus público do TSE para o ciclo das Eleições 2026

Este repositório permite conferir os números do [relatório atualizado no Notion](https://app.notion.com/p/2816527d9bee432da3acce02566b1534). O [pacote com corte em 31/10/2026](versoes/2026-11-12/README.md) corresponde à versão publicada em 14/11/2026. Os cinco arquivos do conjunto [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026) foram gerados em **11/11/2026** e baixados em **12/11/2026**. A consulta documental foi encerrada em **14/11/2026**. O período dos atos selecionados é **03/10/2025 a 31/10/2026**, inclusive.

## Confira sem programar

1. [atos.csv](versoes/2026-11-12/atos.csv): **2.606 atos**, classificados na fonte como 1.893 decisões e 713 acórdãos. Um processo pode ter vários atos.
2. [processos.csv](versoes/2026-11-12/processos.csv): **1.841 processos**, um por CNJ. O filtro de propaganda eleitoral ou direito de resposta reúne **1.005 processos**, contando uma vez os oito presentes nos dois grupos.
3. [confrontos.csv](versoes/2026-11-12/confrontos.csv): **872 candidatos**, divididos em **432 comparáveis, 201 lacunas documentais e 239 demais exclusões**, com motivos individualizados.
4. [relatos.csv](versoes/2026-11-12/relatos.csv): **432 relatos**, com os mesmos CNJs dos confrontos incluídos. A [versão em texto](versoes/2026-11-12/relatos.md) apresenta objeto, medida, etapa e fontes.

No Excel, use **Dados → De Texto/CSV**, escolha **UTF-8** e o separador **ponto e vírgula**. Não conte o cabeçalho. O [dicionário estatístico](versoes/2026-11-12/dicionario.md) e o [dicionário da curadoria](versoes/2026-11-12/dicionario_curadoria.md) explicam as unidades.

| Indicador | Resultado documentado até o corte |
| --- | --- |
| Atos de outubro | 1.669 |
| Confrontos comparáveis | 432: 427 no corpus e 5 em suplemento documental |
| Atendimento à campanha de Lula, total ou parcial | 121 de 218, ou 55,5% |
| Atendimento à campanha de Flávio Bolsonaro, total ou parcial | 69 de 214, ou 32,2% |
| Acórdãos do corpus | 623 unânimes, 89 com divergência e 1 com votação não apurada, entre 713 registros |
| Julgamentos colegiados no recorte presidencial | 296 em 282 processos: 238 unânimes e 58 com divergência |

As autoridades dos totais são [resumo.json](versoes/2026-11-12/resumo.json), [campanha_resumo.json](versoes/2026-11-12/campanha_resumo.json) e [apuracao_colegialidade_resumo.json](versoes/2026-11-12/apuracao_colegialidade_resumo.json). A votação conta julgamentos; o atendimento e a situação da medida contam processos. Liminar não equivale ao julgamento final da ação, e essas taxas não demonstram preferência política do tribunal.

As **1.295 consultas previstas foram concluídas**. Nos 201 casos com lacuna, não foi localizada peça decisória elegível até o corte. Eles não são uma fila de leitura ainda não executada nem prova de ausência de atos; permanecem fora das taxas. Há zero candidatos aguardando revisão nesta rodada, sem eliminar as lacunas de fonte. Os cinco processos suplementares não aumentam as contagens do extrato estatístico.

## Fontes, gráficos e reprodução

Os [cinco ZIPs estatísticos](versoes/2026-11-12/originais) têm geração e hashes em [fontes.json](versoes/2026-11-12/fontes.json). O [inventário documental](versoes/2026-11-12/inventario_documental.json) registra **2.795 entradas por URL distinta**, preservadas em **14 ZIPs**, com caminhos e hashes. Os arquivos estão em [documentos_oficiais](versoes/2026-11-12/documentos_oficiais); extraia-os na pasta da versão, conservando os caminhos internos, para conferir as fontes.

Os [onze gráficos interativos](versoes/2026-11-12/graficos_interativos) preservam os modelos, cores e controles da página. Os HTMLs carregam Chart.js pela internet, e os PNGs foram derivados dos próprios HTMLs. A pasta [graficos](versoes/2026-11-12/graficos) contém as alternativas SVG do coletor. O [guia técnico](REPRODUCAO.md) explica a reprodução dos dados congelados.

O [estado da preparação](versoes/2026-11-12/STATUS.md) registra a consulta encerrada, os limites e os 34 testes aprovados. A atualização editorial das seções 1 a 6 preserva integralmente a seção 7.

## Versão histórica preservada

O [pacote de 1º/10/2026](versoes/2026-10-01/LEIA_PRIMEIRO.md), com corte em **30/09/2026**, conserva 933 atos, 751 processos e 107 confrontos. A [tag histórica](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/tree/v2026-10-01-corte-2026-09-30/versoes/2026-10-01) e a [análise histórica da colegialidade](analises/colegialidade/README.md) mantêm seus próprios arquivos e denominadores.

Na nova extração, o período até setembro contém 937 atos. O [relatório de diferenças](versoes/2026-11-12/relatorio_diferencas.md) separa essa revisão retroativa dos 1.669 atos de outubro. `SQ_DECISAO` não identifica o mesmo documento entre extrações; as versões não devem ser concatenadas.
