# Dicionário do corpus

O significado integral das colunas originais consta nos PDFs LEIAME de cada ZIP em `originais/`. A grafia dos campos oficiais foi conservada.

| Coluna | Arquivo | Definição |
|---|---|---|
| `NR_PROCESSO` | ambos | Número CNJ; chave do processo. |
| `SQ_DECISAO` | atos | Sequencial oficial do ato no arquivo de decisões. Pode mudar em outra extração. |
| `CHAVE_ATO` | atos | `NR_PROCESSO|SQ_DECISAO`; chave única nesta extração. |
| `DT_DECISAO` | atos | Data do ato no PJe, formato original `dd/mm/aaaa`. |
| `DT_DECISAO_ISO` | atos | Mesma data, em `aaaa-mm-dd`. |
| `DS_TIPO_DECISAO` | atos | Categoria fornecida pelo TSE: Decisão ou Acórdão. |
| `NM_AUTOR_DECISAO` | atos | Autor do ato segundo o TSE; não é a relatoria. |
| `PROCESSO_*` | atos | Cópia literal do campo `*` do arquivo oficial Processo Eleitoral. |
| `CD_ASSUNTOS_OFICIAIS`, `DS_ASSUNTOS_OFICIAIS` | processos | União ordenada dos assuntos da tabela oficial Assuntos e do assunto principal do processo; separador ` | `. |
| `PARTES_POLO_ATIVO`, `PARTES_POLO_PASSIVO`, `PARTES_INTERESSADAS` | processos | `TP_PARTE: NM_PARTE`, provenientes do arquivo oficial Partes; advogados e fiscais da lei omitidos. |
| `QT_ATOS_RECORTE` | processos | Quantidade de atos presentes em `atos.csv` para o CNJ. |
| `DT_PRIMEIRO_ATO_ISO`, `DT_ULTIMO_ATO_ISO` | processos | Primeira e última `DT_DECISAO` selecionadas. |
| `FL_PROPAGANDA_OFICIAL` | ambos | 1 se qualquer assunto oficial, inclusive principal, contém `Propaganda Eleitoral`; senão 0. |
| `FL_DIREITO_RESPOSTA` | ambos | 1 se `SG_CLASSE=DR`; senão 0. |
| `FL_RECORTE_COMUNICACAO` | ambos | União lógica das duas bandeiras anteriores. |

`#NULO#` e outros vazios dos arquivos oficiais não são inferidos nem preenchidos nos campos originais. `fontes.json` registra URL, hash, esquema, geração e totais de cada um dos cinco ZIPs. A chave identifica registros dentro deste pacote, mas não substitui a leitura das peças ao analisar o resultado de um processo.
