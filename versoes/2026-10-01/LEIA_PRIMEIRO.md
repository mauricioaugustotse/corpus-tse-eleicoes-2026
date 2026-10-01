# Leia-me do pacote gerado em 1º/10/2026

O [guia principal](../../README.md) mostra como conferir o relatório com uma planilha. O [guia técnico](../../REPRODUCAO.md) explica a execução dos programas.

Esta pasta guarda cinco ZIPs oficiais do TSE gerados em **01/10/2026**. O filtro por data do ato vai de **03/10/2025 a 30/09/2026**, inclusive. Ele produz **933 atos em 751 processos**. O filtro por assunto Propaganda Eleitoral ou classe Direito de Resposta reúne **286 processos e 364 atos**. Os seis gráficos usam apenas esses campos oficiais.

A tabela `confrontos.csv` examina **132 processos** com representantes das campanhas presidenciais em polos opostos. Em **107** deles, foi possível documentar o resultado de uma medida de comunicação eleitoral. Esses mesmos CNJs aparecem, uma vez cada, em `relatos.csv`. O arquivo `curadoria_confrontos.json` guarda as informações documentais usadas para gerar as duas tabelas. Entre 15 processos examinados com ato em 30/09, **oito** tiveram as decisões conferidas e **sete** ainda aguardam leitura do inteiro teor. Há outras duas pendências de leitura. Assim, as taxas se referem apenas aos processos classificados e podem mudar.

Para conferir este pacote, execute `python verificar_pacote.py`. Para recriar os derivados dos ZIPs congelados, execute `python reproduzir.py`. O arquivo `relatorio.md` é uma saída técnica. A página do Notion pode receber edição de linguagem posterior, mas seus números devem corresponder aos CSVs deste pacote.

Um ato classificado como Decisão pode ser apenas uma providência processual. Os 933 registros não são uma contagem de julgamentos finais. Uma nova extração do TSE também pode trazer outros números para o mesmo corte.
