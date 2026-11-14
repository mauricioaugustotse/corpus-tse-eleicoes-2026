# Curadoria documental — corte de 31/10/2026

Esta versão conserva as unidades e regras da curadoria histórica. A extração estatística foi realizada em 12/11/2026, usando arquivos gerados em 11/11. A consulta documental posterior não é apresentada como extração realizada em 1º/11. Enquanto houver consulta complementar, os resultados documentados não constituem apuração exaustiva do corte.

Cada linha de `confrontos.csv` corresponde a um CNJ candidato a confronto. A inclusão exige representantes formais das campanhas de Lula e Flávio Bolsonaro em polos opostos e pronunciamento documentado sobre medida individualizada de comunicação eleitoral. Advogados e terceiros apoiadores não são equiparados automaticamente a representantes formais. Em casos com vários réus, a ordem pode alcançar terceiros ou a plataforma; a presença efetiva da campanha no polo substantivo precisa continuar comprovada. Uma parte expressamente excluída por ilegitimidade não sustenta sozinha o confronto.

O resultado refere-se à campanha autora da medida codificada e ao último resultado comparável documentado até o corte, não à vitória no processo inteiro. Atendimento parcial conta como positivo. Concessão de tutela não é mérito definitivo nem comprovação do cumprimento da ordem. Decisão de emenda, citação, prova, adiamento ou extinção integral sem exame da comunicação não recebe resultado binário. A mera classe, assunto, data ou espécie do ato não determina resultado.

Despacho posterior e extinção de direito de resposta após o pleito não apagam automaticamente uma decisão comparável anterior. O encerramento posterior é descrito no estágio. Negativa decorrente exclusivamente de veiculação já encerrada, sem exame material comparável, fica fora; negativa que também examina a mensagem pode ser comparável, com fundamento misto explicitado. O caso iniciado por `0602712` e os demais anúncios inativos foram revisados independentemente; usar o CNJ completo das planilhas como chave.

As datas de julgamento, assinatura, juntada e registro no inventário são distintas. `data_ato_referencia` conserva a referência documental indicada pelo curador; os JSONs registram, quando disponíveis, as demais datas e a origem da escolha. A sessão virtual pode terminar em data anterior à assinatura do acórdão ou à emissão da certidão. Uma peça posterior não transforma seu conteúdo em acontecimento anterior: a data do julgamento precisa estar documentada.

| Campos | Conteúdo |
| --- | --- |
| `cnj`, `qtd_atos_bulk` | Chave do processo e quantidade de atos no extrato; o CNJ sem ato pode aparecer em suplemento documental. |
| `incluir_comparativo`, `categoria_triagem`, `motivo_inclusao_exclusao` | Inclusão, exclusão ou pendência e sua justificativa. Pendência não é resultado negativo. |
| `campanha_autora`, `polo_ativo_formal`, `polo_passivo_formal` | Lado que formulou a medida codificada e partes oficiais utilizadas para verificar o confronto. |
| `classe_pje`, `assunto_principal_pje`, `assuntos_pje` | Enquadramento cadastral, distinto da classificação jurídica do dispositivo. |
| `objeto_comunicacao`, `pedido_principal_codificado`, `sinopse_curatorial` | Conteúdo e medida individualizados, fundamentos e limites do resultado. |
| `atendido`, `desfecho_medida`, `grau_atendimento`, `status_procedimental` | Resultado codificado e estágio; campo binário vazio nas exclusões ou pendências. |
| `data_ato_referencia`, `url_peca_oficial`, `tipo_peca_oficial` | Peça que fundamenta a classificação. Fontes e hashes adicionais ficam nos JSONs de curadoria. |
| `data_ultima_decisao_pje`, `tipo_ultima_decisao_pje` | Último ato do extrato dentro do corte, que pode ser posterior à medida comparada. |
| `status_fonte`, `fonte_classificacao`, `grau_certeza_triagem`, `geracao_bulk` | Fonte e acesso documental, nível de conferência e geração do extrato. |
| `url_andamento` | Consulta pública do processo, sujeita a desdobramentos posteriores ao corte. |

`relatos.csv` contém exatamente os CNJs incluídos no comparativo. A numeração segue a data da peça de referência em ordem decrescente; empates usam CNJ. Os programas geram tabelas e ordenação a partir da curadoria explícita; não decidem o mérito por palavras isoladas.

A colegialidade conta julgamentos únicos, conciliando certidão e acórdão. Uma ocorrência de voto vencido é contada por ministro e julgamento, inclusive parcialmente vencido. Certidões não são acrescentadas como novos atos a `atos.csv`. A apuração distingue mérito, tutela direta, revisão, manutenção, modificação e ausência de revisão comprovada. Ausência de revisão localizada não prova pendência processual.
