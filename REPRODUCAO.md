# Como reproduzir os dados

Este guia é para quem quer executar os programas. O [leia-me](README.md) permite conferir os números sem programação.

## Reproduzir os números do relatório

Instale Python 3.10 ou posterior. Baixe o repositório pelo botão **Code → Download ZIP** do GitHub e descompacte-o. Em um terminal, entre em `versoes/2026-10-01` e execute:

```bash
python verificar_pacote.py
python reproduzir.py
python -m unittest discover -s tests -v
```

No Windows, `py -3` também pode chamar o Python. Os programas usam apenas a biblioteca padrão. A verificação inicial confere os hashes SHA-256, a unicidade de atos e processos e a igualdade dos CNJs dos confrontos com os relatos. `reproduzir.py` recalcula os CSVs, os gráficos SVG, as tabelas de confronto e o relatório técnico. Os HTMLs conservam a apresentação publicada no Notion e não são sobrescritos pelo programa. Ao final, os hashes precisam continuar iguais aos do manifesto.

O comando usa `--data-fim 2026-09-30`. Esse corte é **inclusivo** e foi validado em teste. A extração oficial congelada foi gerada em 1º/10/2026 e tinha 30/09 como última data disponível. O programa recusa um corte posterior à última data encontrada no arquivo.

## Baixar outra extração do TSE

A fonte é o conjunto [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026). Ele oferece os arquivos de Processo Eleitoral, Assuntos, Decisões, Partes e Recursos. Para guardar uma nova rodada, crie **outra pasta vazia** e execute, a partir da raiz do repositório:

```bash
python versoes/2026-10-01/tse_corpus_eleicoes_2026.py --saida nova-extracao --data-fim 2026-09-30
```

O programa baixa os cinco ZIPs, testa integridade, esquema, geração e junções. Um ZIP já existente não é substituído automaticamente. Em uma coleta posterior, o TSE pode ter acrescentado registros com datas antigas. Portanto, a mesma data de corte não garante os mesmos totais deste pacote congelado.

O filtro seleciona `NR_INSTANCIA=3`, `SG_UF_TRIBUNAL=DF`, tipo **Decisão** ou **Acórdão** e `DT_DECISAO` desde 03/10/2025 até o corte. `atos.csv` tem uma linha por `NR_PROCESSO + SQ_DECISAO` na mesma extração. `processos.csv` tem uma linha por CNJ com ao menos um ato selecionado.

## O que depende da leitura das decisões

[gerar_confrontos.py](versoes/2026-10-01/gerar_confrontos.py) junta os campos oficiais à [curadoria documental dos 132 processos](versoes/2026-10-01/curadoria_confrontos.json). [gerar_relatos.py](versoes/2026-10-01/gerar_relatos.py) monta os 107 relatos com os mesmos CNJs dos confrontos incluídos. Os programas reproduzem classificações **já documentadas** e não inferem o mérito a partir da classe, do assunto ou do nome do ato. Para conferir um resultado, abra a peça oficial indicada em `confrontos.csv`.

## Reproduzir a apuração das votações

O [SJUR](https://jurisprudencia.tse.jus.br/) permite pesquisar decisões e exportar os resultados em CSV. As exportações utilizadas foram obtidas pela interface do portal, com filtros de tipo de decisão e data de julgamento. A coleta em Python empregou Playwright para navegar pelas páginas de resultados, selecionar os registros e acionar **Exportar → CSV**. A paginação usada foi de 250 resultados, com consultas por intervalos de datas para respeitar o limite de resultados do portal. A mesma exportação pode ser feita manualmente, sem essa automação.

Os campos utilizados são `siglaTribunalJE`, `origemDecisao`, `numeroProcesso`, `numeroUnico`, `dataDecisao`, `siglaClasse`, `descricaoTipoDecisao`, `relatores`, `textoDecisao` e `textoEmenta`. O CNJ normalizado, com 20 dígitos, permite reunir os registros do SJUR e os atos da base estatística. A data de julgamento do SJUR pode ser diferente da data do ato na base processual; a correspondência foi conferida pela sequência de atos e pelo conteúdo. A votação foi apurada em `textoDecisao`, que registra a proclamação do resultado, e nas peças oficiais do PJe. A ementa não substitui essa conferência.

O repositório preserva os extratos das exportações utilizadas; a conferência não depende da disponibilidade atual do portal. Para selecionar os mesmos processos em um ou mais CSVs exportados do SJUR, execute a partir da raiz:

```bash
python analises/colegialidade/extrair_sjur.py exportacao.csv --saida extratos-selecionados.json --verificar
```

O programa usa a biblioteca padrão do Python, aceita CSV delimitado por vírgula ou ponto e vírgula, filtra acórdãos do TSE e conserva os dez campos oficiais. Por padrão, seleciona os **162 CNJs** cuja fonte de votação é o SJUR em `acordaos.json`. As exportações preservadas contêm **190 registros** desses processos, incluindo variantes cadastrais, associados pela curadoria a **163 atos**. `--verificar` compara o conteúdo selecionado com `extratos_sjur.json`, independentemente da ordem das linhas. Se outra exportação trouxer diferenças, o programa as informa e não altera o espelho nem as classificações publicadas. Registros exatamente iguais são deduplicados; variantes de texto ou de data permanecem distintas.

Para levantar candidatos para todos os **198 processos com acórdão** no corpus, use `--todos-do-corpus` e um nome de saída diferente. Essa opção amplia a seleção documental; não atribui votação nem modifica os resultados. O programa recusa sobrescrever um arquivo existente.

Para conferir as planilhas e refazer as contagens da curadoria, execute:

```bash
python analises/colegialidade/reproduzir.py
```

Esse segundo programa usa `csv` e `json` para verificar a equivalência das tabelas, `hashlib` para conferir as peças oficiais e `collections.Counter` para contar as categorias e as ocorrências de ministros vencidos. A revisão de liminares depende da leitura conjunta da decisão individual e do pronunciamento colegiado. Os programas reproduzem a curadoria registrada, sem decidir essas questões por palavras isoladas.

Os gráficos HTML usam HTML, CSS e JavaScript com Chart.js 4.4.1, carregado do CDN cdnjs, e conservam a apresentação da página do Notion. Precisam de conexão para carregar essa biblioteca. Os SVGs são alternativas estáticas para consulta sem internet, com apresentação distinta. Para gerar os SVGs da colegialidade, instale Matplotlib conforme `analises/colegialidade/requirements-graficos.txt` e execute `python analises/colegialidade/reproduzir.py --graficos`. Essa opção não substitui os HTMLs. Em outra extração, numa pasta vazia, o programa do corpus gera HTMLs simples que incorporam os SVGs.
