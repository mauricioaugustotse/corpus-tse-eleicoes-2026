# Verificação do pacote

- Os cinco ZIPs oficiais passaram por verificação CRC, SHA-256, esquema, geração na mesma rodada e junções por CNJ, tribunal e instância.
- `atos.csv` contém **933 chaves únicas** `NR_PROCESSO + SQ_DECISAO`. `processos.csv` contém **751 CNJs únicos**. O corte inclusivo de `DT_DECISAO` termina em **30/09/2026**, última data disponível no extrato gerado em 1º/10.
- Os seis gráficos reproduzem tipo de ato, mês e tipo, acumulado, classe, autor e recorte de comunicação. Os cinco primeiros usam 933 atos; o sexto usa 751 processos. Os valores estão em `resumo.json`.
- O recorte oficial de comunicação soma **286 processos e 364 atos**. Ele não classifica resultados dos pedidos.
- O inventário documental contém **132 CNJs** com campanhas opostas. **107** entram no comparativo e aparecem exatamente uma vez em `relatos.csv`. Os outros **25** constam de `confrontos.csv` com motivo de exclusão ou pendência.
- Entre os 15 CNJs examinados com ato em 30/09, **oito decisões** foram lidas no PJe. Sete concederam a liminar pedida, duas delas parcialmente, e uma a negou. Em todos os oito, o PJe mostrou apenas intimações posteriores no próprio dia 30/09. Os outros sete não recebem resultado inferido do ZIP.
- As taxas entre os casos classificados são **29/48 (60,4%)** para medidas pedidas pela campanha de Lula e **20/59 (33,9%)** para a de Flávio. São resultados de medidas documentadas, muitas cautelares. Há **nove triagens sem inteiro teor**, das quais sete com ato em 30/09. A amostra não é declarada exaustiva.
- Cinco resultados colegiados permanecem documentados por certidão oficial sem acórdão no ZIP. O CNJ 0601315-97 não tem ato no corpus e entra apenas como suplemento documental do comparativo.

`python reproduzir.py` verifica os hashes, recalcula os derivados e volta a verificar o manifesto. Os cinco testes do gerador oficial cobrem filtros, chaves, esquema, gráficos e a inclusão de 30/09 no corte. A leitura jurídica das peças está documentada nas fontes do CSV de confronto e não é substituída por testes de código.
