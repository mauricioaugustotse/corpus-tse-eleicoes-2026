# Corpus oficial — corte em 31/10/2026

**Pacote publicado no Notion; consulta documental encerrada em 14/11/2026.** Foram concluídas as 1.295 consultas previstas. A curadoria reúne **872 candidatos: 432 comparáveis, 201 lacunas documentais e 239 demais exclusões**, sem candidatos aguardando revisão nesta rodada. [STATUS.md](STATUS.md) registra resultados e limites; [registro_publicacao_notion.json](registro_publicacao_notion.json) documenta a conferência da página efetivamente salva.

## Dados e corte temporal

Fonte primária: [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026), Secretaria Judiciária, sistema PJe. Os cinco arquivos foram gerados em **11/11/2026** e baixados em **12/11/2026**. O corte inclusivo de `DT_DECISAO` é **03/10/2025 a 31/10/2026**. A fonte contém atos até 10/11; os 456 posteriores ao corte foram excluídos.

- [atos.csv](atos.csv): **2.606 registros**, sendo 1.893 decisões e 713 acórdãos, uma linha por `NR_PROCESSO + SQ_DECISAO` nesta extração.
- [processos.csv](processos.csv): **1.841 CNJs** com ato selecionado.
- Filtro de comunicação: **1.005 processos**, união de 671 apenas com propaganda eleitoral, 326 apenas de Direito de Resposta e oito em ambos os grupos.
- [confrontos.csv](confrontos.csv) e [relatos.csv](relatos.csv): **432 CNJs comparáveis**, sendo 427 do corpus e cinco suplementares, com um relato por confronto incluído.

Os filtros são `NR_INSTANCIA=3`, `SG_UF_TRIBUNAL=DF` e tipo Decisão ou Acórdão. Os CSVs usam UTF-8 com BOM e ponto e vírgula. Em `atos.csv`, as colunas oficiais do processo recebem o prefixo `PROCESSO_`. Os ZIPs completos e LEIAMEs estão em [originais](originais), com geração e hashes em [fontes.json](fontes.json).

## Curadoria e limites

[campanha_resumo.json](campanha_resumo.json) registra **121/218 (55,5%)** de atendimento à campanha de Lula e **69/214 (32,2%)** à de Flávio Bolsonaro. Atendimento parcial integra o numerador. O resultado é o da medida comparável documentada até o corte; despacho posterior não reclassifica automaticamente o mérito.

Os **201 casos com lacuna documental** foram consultados, mas não tiveram peça decisória elegível localizada até o corte. Não são pendências de leitura humana nem prova de ausência de atos. Ficam sem resultado binário e fora das taxas, com motivos registrados, assim como as 239 demais exclusões.

[apuracao_colegialidade_resumo.json](apuracao_colegialidade_resumo.json) registra **623 votações unânimes, 89 com divergência e uma não apurada** entre os 713 acórdãos. O vínculo documental não resolvido é `0601104-61.2026.6.00.0000|4521`. No recorte presidencial, são **296 julgamentos em 282 processos**, sendo 238 unânimes e 58 divergentes. A situação da medida conta cada CNJ uma vez.

Data do extrato, sessão, assinatura e juntada são distintas. O autor do ato não é necessariamente o relator atual; o rótulo Decisão pode designar materialmente um despacho. A leitura da peça, sua identidade e seu alcance sustentam a classificação. Liminar não equivale ao resultado definitivo ou ao trânsito em julgado.

## Fontes e apresentação

O [inventário documental](inventario_documental.json) preserva **2.795 entradas por URL distinta em 14 ZIPs** de [documentos_oficiais](documentos_oficiais), com caminhos e hashes. O total público inclui a coleta, o suplemento de auditoria e fonte contextual. O contador operacional de 2.787 peças usa registros por CNJ e pode conter URLs compartilhadas: não tem a mesma unidade do inventário público e não deve ser somado às entradas do suplemento.

Os **onze HTMLs de [graficos_interativos](graficos_interativos)** preservam a apresentação do Notion, com Chart.js e PNGs derivados. A pasta [graficos](graficos) contém alternativas SVG do coletor. Os dados estão em [dados_graficos.json](graficos_interativos/dados_graficos.json), e a conferência visual em [verificacao_renderizacao.json](graficos_interativos/verificacao_renderizacao.json).

[pagina_proposta.md](pagina_proposta.md) reúne as seções 1 a 6, os 432 relatos e as referências gráficas; a seção 7 permanece integralmente preservada. O [relatório de diferenças](relatorio_diferencas.md) explica a comparação com a versão histórica.

## Reprodução

Extraia os 14 ZIPs de `documentos_oficiais/` nesta pasta, preservando os caminhos internos. O [guia técnico](../../REPRODUCAO.md) contém a sequência completa. A apuração com `--inventario-publico` usa o espelho congelado, independentemente de checkpoints locais.

```bash
python verificar_atualizacao.py
python consolidar_curadoria.py
python gerar_confrontos.py
python apurar_colegialidade.py --inventario-publico
python gerar_config_graficos_juridicos.py
python atualizar_graficos_interativos.py
python verificar_curadoria.py
python -m unittest discover -s tests -v
```

A preparação registrou **34 testes aprovados**. `python renderizar_graficos.py` exige Playwright e Chromium. A reprodução estatística usa `python tse_corpus_eleicoes_2026.py --saida . --offline --data-fim 2026-10-31`; esse coletor também regenera documentação básica, que deve ser comparada com a documentação editorial desta versão. Os ZIPs congelados não são substituídos automaticamente.
