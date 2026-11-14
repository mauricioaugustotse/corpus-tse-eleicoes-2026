# Apuração documental da colegialidade — corte de 2026-10-31

## Universo estatístico

São 713 registros de acórdão. Resultado da conciliação: {"total": 713, "votacao": {"unânime": 623, "com divergência": 89, "não apurada": 1}, "ministros_vencidos": {"Floriano de Azevedo Marques": 34, "Estela Aranha": 17, "Dias Toffoli": 19, "André Mendonça": 45, "Nunes Marques": 33, "Antonio Carlos Ferreira": 1, "Sebastião Reis Júnior": 20, "Ricardo Villas Bôas Cueva": 13}}.

São 704 vínculos com acórdão público, oito com proclamação certificada conciliada manualmente e uma lacuna. Os vínculos usam o CNJ confirmado no cabeçalho, espécie, sequência documental e data do ato compatível com assinatura, juntada ou inventário PJe. CNJ e data, isoladamente, não provam a identidade. Os candidatos e a fonte exata permanecem no JSON. Nenhuma certidão foi acrescentada como ato estatístico.

## Pendências de vínculo

- 0601104-61.2026.6.00.0000|4521 — 2026-07-14: conciliação pendente; 2 documento(s) colegiado(s) acessível(is).

## Recorte presidencial

Não é o novo comparativo. A lista dos confrontos finais depende da curadoria de resultados; os mesmos CNJs podem ter mais de um julgamento. Não transportar os 107 históricos como denominador de outubro.

As revisões de tutela precisam da comparação entre a ordem individual e a proclamação. Este programa não transforma expressões como “referendou parcialmente” em manutenção ou reforma sem ler os dois dispositivos.

## Deduplicação e leitura nominal

Certidão e acórdão só são agrupados automaticamente se CNJ, data do inventário e proclamação normalizada forem iguais. Textos diferentes do mesmo dia ficam como candidatos e exigem conciliação antes de somar julgamentos presidenciais. O número de grupos documentais é preparatório, não um total editorial pronto para publicação.

Divergências sem nome resolvido: []

A classificação preserva votação “não apurada” quando não há proclamação ou vínculo suficiente. A soma de ministros vencidos não é o número de julgamentos: um julgamento pode ter vários vencidos.

## Ledger para o recorte presidencial

O campo `ledger_julgamentos` prefere a ata no acórdão. A certidão é fonte complementar quando o núcleo do dispositivo e a votação são compatíveis; nove variantes maiores tiveram leitura paralela registrada no programa. Equivalências não se baseiam só em CNJ e data. Certidões de adiamento ou vista sem proclamação final não contam como julgamento finalizado.

Após gerar `curadoria_confrontos.json`, execute novamente o programa. Ele seleciona os CNJs incluídos e lê `situacoes_*.json` ou o campo `colegialidade_situacao` de cada registro para a classificação da medida. Ausência de classificação manual fica explícita; não se deduz manutenção ou reforma por regex. A votação conta julgamentos; o quadro da situação da medida conta processos.

Correções nominais conferidas: no acórdão de 0602945-91, a referência ao Art. 7º aparece entre os nomes vencidos e não deve cortar Nunes Marques da lista; no acórdão de 0602953-68, a grafia “arRelatora” é lida à luz da relatoria originária expressa de Estela Aranha. O processo suplementar 0601315-97 passou a ter dois acórdãos no inventário documental; cada etapa fica separada no ledger, sem criar atos no ZIP.
