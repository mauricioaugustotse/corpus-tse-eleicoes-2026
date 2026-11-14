# Atualização até 31/10/2026 — ponto de retomada de 14/11

A atualização permanece em preparação. Não publicar os percentuais desta etapa como apuração final de outubro. A página do Notion ainda conserva a versão anterior; a seção 7, “Bruno”, está preservada.

## Concluído e salvo

- Extração estatística: 2.606 atos em 1.841 processos; 713 registros de acórdão. Os cinco ZIPs oficiais foram gerados em 11/11 e baixados em 12/11. Corte inclusivo de 31/10, fonte com atos até 10/11.
- Auditoria da coleta inicial: 1.015 consultas e 2.689 peças íntegras. Das 15 peças pendentes, 13 foram admitidas após recuperação e conferência; duas são anexos contextuais, não peças próprias do CNJ em que foram juntadas.
- Leitura dos 132 alvos históricos e 460 novos alvos do extrato. Os lotes estão em `curadoria_historicos_outubro.json`, `curadoria_novos_a.json` e `curadoria_novos_b.json`. As exceções e pendências estão documentadas; não inferir resultado por metadados.
- A integração atual tem 428 resultados comparáveis documentados, 164 exclusões fundamentadas e 280 alvos em consulta complementar. O caso conexo da AIJE 0602694-73 foi reconciliado em `curadoria_revisao_conexa.json`, com limites explicitados em `auditoria_conexa.md`.
- Apuração geral das votações: 623 unânimes, 89 divergentes e 1 sem vínculo documental seguro entre os 713 registros. A lacuna é `0601104-61.2026.6.00.0000|4521`. Votos vencidos contados por ministro e julgamento.
- Onze gráficos interativos atualizados nos modelos da página, com PNGs derivados dos próprios HTMLs. O recorte presidencial ainda poderá mudar com o complemento.
- Substituições editoriais estatísticas preparadas em `alteracoes_estatisticas.json`; relatos documentados em `relatos.csv/md`. Ainda faltam a integração editorial final e a publicação no Notion.
- Fontes públicas preservadas nos ZIPs de `documentos_oficiais/`, com índice e hashes em `inventario_documental.json`. Não adicionar ao Git os caches gerais do motor, logs ou URLs assinadas do backup do Notion.

## Coleta complementar em execução

A primeira seleção documental cobriu o corpus de atos, os processos com acórdão e os alvos antigos, mas não todos os confrontos dos polos da base integral. A varredura de 4.354 processos encontrou 872 candidatos a confronto, incluindo 280 fora daquela seleção. Isso não significa 872 resultados comparáveis. `triagem_base_integral.json` discrimina os casos; um deles foi autuado depois do corte e não pode gerar acontecimento anterior a ele.

O coletor foi ampliado para 1.295 alvos e retomado no mesmo diretório, com os mesmos controles de pausa e reaproveitamento. O processo continua em segundo plano, sem depender de manter esta conversa aberta. Consultar o estado atual pelo painel da Área de Trabalho ou por `python controle_coleta.py status`; não usar este texto como contador em tempo real.

Depois da consulta, os novos processos precisam de curadoria jurídica. Entradas sem leitura suficiente ficam explicitamente fora dos denominadores. Escrever essa revisão em `curadoria_suplementares_outubro.json`; `consolidar_curadoria.py` a incorpora por CNJ sem perder os três lotes anteriores. Eventuais revisões de processos conexos ficam em `curadoria_revisao_conexa.json`.

## Retomar a análise e reproduzir

1. Conferir `controle_coleta.py status`, checkpoint e pendências; não iniciar coletor duplicado. O painel continua permitindo Pausar e Retomar.
2. Ler os documentos dos 280 alvos complementares até o corte e registrar fontes, datas, pedidos, resultados e situações de colegialidade. Excluir os acontecimentos posteriores ao corte. Não substituir resultado comparável por mero despacho ou extinção posterior sem exame da comunicação.
3. Integrar os lotes e recalcular: `python consolidar_curadoria.py`, `python gerar_confrontos.py`, `python apurar_colegialidade.py`, `python gerar_config_graficos_juridicos.py`, `python atualizar_graficos_interativos.py`, `python renderizar_graficos.py`.
4. Atualizar a redação das seções 1 a 6, todas as tabelas e listas nominais, os relatos em ordem da peça oficial e os onze anexos. Conservar a seção 7 exatamente. Não reaproveitar os números de setembro para outubro.
5. Exportar novas peças com `python exportar_documentos.py`; esse programa preserva os ZIPs anteriores e acrescenta lotes. Atualizar o manifesto e executar o verificador, os testes e a conferência visual. Os ZIPs contêm os caminhos originais para extração nesta pasta. O apurador aceita `inventario_processos_documentais.json` quando não existe checkpoint local.
6. Publicar a versão completa no branch `atualizacao-corte-2026-10-31` e na mesma página do Notion. O PR 1 permanece como rascunho até a conclusão. A alteração da página já está autorizada; não pedir nova permissão de rotina.

Página: https://app.notion.com/p/2816527d9bee432da3acce02566b1534

PR: https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/pull/1
