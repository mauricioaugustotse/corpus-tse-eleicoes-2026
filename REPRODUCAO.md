# Como reproduzir os dados

Este guia é para quem quer executar os programas. O [leia-me](README.md) permite conferir os números sem programação.

## Reproduzir os números do relatório

Instale Python 3.10 ou posterior. Baixe o repositório pelo botão **Code → Download ZIP** do GitHub e descompacte-o. Em um terminal, entre em `versoes/2026-10-01` e execute:

```bash
python verificar_pacote.py
python reproduzir.py
python -m unittest discover -s tests -v
```

No Windows, `py -3` também pode chamar o Python. Os programas usam apenas a biblioteca padrão. A verificação inicial confere os hashes SHA-256, a unicidade de atos e processos e a igualdade dos CNJs dos confrontos com os relatos. `reproduzir.py` recalcula os CSVs, os seis gráficos, as tabelas de confronto e o relatório técnico. Ao final, os hashes precisam continuar iguais aos do manifesto.

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
