# Dicionário da curadoria de confrontos

Este dicionário complementa `dicionario.md`, que descreve os campos extraídos dos arquivos estatísticos oficiais. `confrontos.csv` e `relatos.csv` são tabelas de **análise documental por processo**. Os resultados dos pedidos não são campos fornecidos no ZIP de decisões do TSE. Esta versão usa o extrato gerado em 01/10/2026, com atos datados até 30/09/2026.

## Unidade e regra de inclusão

Cada linha de `confrontos.csv` corresponde a um CNJ candidato a confronto entre representantes formais das campanhas de Lula e Flávio Bolsonaro em polos opostos. `incluir_comparativo=sim` exige um pronunciamento documentado que tenha examinado medida individualizada de comunicação eleitoral, como remoção, abstenção, impulsionamento ou direito de resposta. Pedidos apenas instruídos, medida integralmente sem objeto e extinção integral sem exame da comunicação não recebem resultado binário. A presença das partes no processo, da classe `Rp` ou `DR`, ou do assunto propaganda não basta, isoladamente, para classificar o resultado. Linhas `não` registram exclusões ou pendências de triagem; seu motivo e o nível de prova devem ser lidos em conjunto.

Nos 107 processos incluídos nesta versão, o resultado é atribuído à **campanha autora da medida codificada**. `atendido=sim` inclui atendimento total ou parcial da medida identificada. `atendido=não` indica que ela não foi deferida na etapa documentada. Negativa de liminar não significa improcedência definitiva, e concessão de resposta não prova veiculação. O resultado comparável pode continuar válido apesar de um despacho posterior. A maior data do processo ou o último rótulo do ZIP não reclassifica automaticamente o mérito.

## Identificação das campanhas nos polos

O gerador normaliza caixa e acentos dos nomes oficiais. No lado de Lula reconhece Luiz Inácio Lula da Silva, Geraldo José Rodrigues Alckmin Filho, Coligação Brasil Pronto pra Mais, Federação Brasil da Esperança e PT nacional. No lado de Flávio reconhece Flávio Nantes Bolsonaro e PL nacional. Exige os lados em polos opostos, excluindo advogados do pareamento. O dicionário explícito está na função `campaign` de `gerar_confrontos.py`; a regra não transforma qualquer terceiro apoiador em representante formal da campanha.

## Campos de `confrontos.csv`

| Campo | Significado e limite |
|---|---|
| `cnj` | Número único do processo; chave para `processos.csv`, `atos.csv` e `relatos.csv`. |
| `incluir_comparativo` | `sim` integra os 107 processos do quadro de atendimento; `não` fica fora da taxa. |
| `motivo_inclusao_exclusao` | Justificativa textual da triagem; uma justificativa baseada só em metadados é provisória até conferência da peça. |
| `categoria_triagem` | Rótulo de controle da inclusão ou do motivo de exclusão, como `comparável`, `processual`, `extinção sem mérito`, `perda de objeto` ou `triagem pendente de inteiro teor`. O texto da peça determina o alcance jurídico. |
| `campanha_autora` | Lado que formulou a medida comparada (`Lula` ou `Flávio`), conforme os polos formais e a peça analisada; não designa o vencedor da eleição ou do processo inteiro. |
| `polo_ativo_formal`, `polo_passivo_formal` | Partes usadas para verificar o confronto formal. Nomes de coligações, federações e partidos podem representar a campanha. |
| `classe_pje`, `assunto_principal_pje`, `assuntos_pje` | Classe e assuntos registrados no PJe/extratos oficiais; descrevem o enquadramento administrativo e não o dispositivo da peça. |
| `objeto_comunicacao` | Conteúdo, meio ou conduta comunicacional individualizada na triagem; texto descritivo, não categoria estatística independente. |
| `pedido_principal_codificado` | Medida tomada como referência para o resultado. É descrição curatorial, não extração automática ou taxonomia exaustiva dos pedidos do processo. |
| `desfecho_medida` | Síntese `atendido`, `não atendido` ou `sem resultado comparável` da medida codificada. |
| `atendido` | Campo para o cálculo: `sim`, `não` ou vazio se a linha for excluída. O cálculo conta processos, nunca atos nem pedidos individuais. |
| `grau_atendimento` | Pode indicar `parcial`, `integral na medida cautelar`, `não atendido`, `sem resultado comparável` ou `atendimento documentado, extensão não discriminada`. O último valor **não autoriza inferir atendimento integral**. |
| `status_procedimental` | Estado da medida na peça de referência ou anotação curatorial. O valor genérico `efeito da decisão de referência; ver sinopse para estado do mérito` não equivale a trânsito em julgado nem à situação processual atual. |
| `data_ultima_decisao_pje`, `tipo_ultima_decisao_pje` | Data e tipo do registro mais recente disponível nos metadados do processo PJe, quando informados. Pode ser um despacho posterior à medida comparada; não define automaticamente `atendido`. |
| `qtd_atos_bulk` | Quantos atos daquele CNJ constam do `atos.csv` congelado. Zero identifica processo sem ato no corpus; valores positivos não provam que o desfecho curatorial esteja no ZIP. |
| `data_ato_referencia` | Data da peça ou do resultado documental usado na classificação, distinta da última data administrativa do processo e, às vezes, da `DT_DECISAO` do extrato. Deve ser lida com `url_peca_oficial` e a sinopse. |
| `url_peca_oficial`, `tipo_peca_oficial` | Endereço e espécie da peça que fundamenta a classificação, quando verificada. Certidão de julgamento, decisão, despacho e acórdão são espécies diferentes. Campo vazio indica que não há peça direta documentada nesta coleta. |
| `status_fonte` | Descrição da fonte e do acesso à peça. Pode indicar inteiro teor HTML da Consulta Unificada, texto integral da exportação oficial de jurisprudência TSE/PJe ou certidão PJe. A ausência de URL direta em algumas linhas **não significa ausência de leitura**, se o texto integral da exportação oficial foi consultado. A indicação de metadados sem inteiro teor identifica triagem provisória e não sustenta conclusão sobre o resultado. |
| `fonte_classificacao` | Fonte usada para a classificação: codificação editorial com fonte oficial indicada, texto integral da exportação oficial de jurisprudência, HTML da Consulta Unificada ou somente metadados do ZIP. Diferencia a análise documental da triagem provisória por metadados. |
| `grau_certeza_triagem` | `alto` quando o teor da peça foi examinado nesta conferência; `codificação editorial com fonte oficial indicada` quando há classificação documentada e peça oficial vinculada; `provisório` quando o inteiro teor ainda não foi obtido. O grau descreve a evidência da triagem, não a probabilidade de êxito jurídico. |
| `url_andamento` | Página do processo na Consulta Unificada PJe; permite acompanhar mudanças posteriores ao corte. |
| `sinopse_curatorial` | Resumo do objeto, medida e estágio documentado; deve conservar limitações de liminar, certidão ou decisão sem mérito. |
| `geracao_bulk` | Data e hora declaradas pelo arquivo estatístico oficial utilizado, não data do julgamento. |

## Datas e resultados fora do ZIP de decisões

Há **cinco resultados colegiados documentados por certidões de julgamento, sem acórdão correspondente no ZIP congelado**. O CNJ `0600950-43.2026.6.00.0000` integra os 751 processos por decisão anterior de 04/08, mas a remoção determinada pelo Plenário na sessão virtual de 04 a 08/09 é documentada pela certidão emitida em 09/09. O CNJ `0601315-97.2026.6.00.0000` não tem ato no extrato e figura como suplemento documental, com resultado também certificado. As certidões de 09/09 dos CNJs `0601303-83.2026.6.00.0000`, `0601767-10.2026.6.00.0000` e `0601768-92.2026.6.00.0000` documentam, respectivamente, referendo por maioria da tutela parcial e dois referendos unânimes de indeferimentos. O ZIP contém apenas uma `Decisão` anterior de 01/09 para cada um desses três CNJs. Não há link de acórdão confirmado para esses três no pacote; os resultados se apoiam nas certidões verificadas. Portanto, quatro dos cinco CNJs pertencem ao corpus por ato anterior, e apenas `0601315-97` é processo suplementar. Nenhuma certidão é acrescentada como nova linha a `atos.csv`.

O ZIP identifica atos por `NR_PROCESSO` e `SQ_DECISAO`, mas não fornece o texto ou ID público da peça. A associação entre a narrativa e um ato do ZIP deve ser conferida pela peça oficial. Coincidência de CNJ, tipo e data, isoladamente, não prova que sejam a mesma peça. Certidões não são somadas como linhas novas a `atos.csv`.

As exclusões `0600947-88.2026.6.00.0000` e `0600958-20.2026.6.00.0000` permanecem **provisórias**. Há atos no ZIP, mas o inteiro teor não foi acessado. Outros **sete processos com ato em 30/09** e campanhas opostas também aguardam leitura da peça. Seu assunto ou classe não permite inferir atendimento nem afastar a possibilidade de medida comunicacional. As outras 16 exclusões têm classificação apoiada em texto integral oficial ou HTML PJe, conforme as colunas de fonte, embora nem todas disponham de URL direta da peça nesta coleta.

## Confrontos com ato em 30/09

Entre os processos examinados com ato em 30/09, **15** têm as campanhas em polos opostos. Oito peças dessa data foram lidas no PJe. Em sete, a liminar pedida foi atendida, duas delas parcialmente. Em uma, a retirada cautelar foi negada. O PJe mostrou apenas intimações posteriores nessa data para esses oito CNJs. Os sete restantes constam nominalmente em `curadoria_confrontos.json` e em `confrontos.csv`, sem resultado codificado. Essas pendências tornam provisórias as taxas calculadas apenas sobre os 107 resultados já documentados.

## Campos de `relatos.csv`

`numero` é a ordem de apresentação na seção 5, sem significado cronológico ou probatório. `cnj` vincula o relato a uma única linha `incluir_comparativo=sim` de `confrontos.csv`. `titulo` resume o objeto. `texto` traz os fatos, o alcance e a etapa do pronunciamento, com links diretos às peças e ao andamento quando disponíveis. Os 107 CNJs de `relatos.csv` devem coincidir exatamente com os 107 incluídos em `confrontos.csv`. `tse_relatorio_corpus.py` verifica essa igualdade ao gerar o relatório.
