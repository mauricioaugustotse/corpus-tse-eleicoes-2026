# Auditoria da coleta documental

Corte: 31/10/2026. Auditoria: 2026-11-14T12:39:14.961231+00:00. Checkpoint SHA-256: `72e4408e772d5ebc2350e5e4a51717326a04386abee7e2333817622964a61034`.

Foram consultados 1015 processos: 1001 com coleta completa no checkpoint e 14 com pendências. Há 2704 registros de peças: 2689 conferidas e 15 pendentes.

A verificação de arquivos, hashes, textos e CNJ inicial encontrou 0 falhas entre as peças já conferidas. 0 processos estão sem cache e 0 têm peças da seleção atual ausentes do checkpoint.

Todos os 15 downloads pendentes foram recuperados em GETs oficiais. Cinco têm CNJ confirmado pela regra estrita; dez exigem distinção documental conforme tabela. O checkpoint não foi alterado.

| Processo | ID | Diagnóstico | Justificativa |
|---|---:|---|---|
| 0602694-73.2026.6.00.0000 | 179935558 | cabecalho_cnj_abreviado | Cabeçalho identifica AIJE 0602694-73; número completo não aparece. A classe, partes, origem e inventário confirmam a vinculação; precisa de aceitação documentada do formato abreviado. |
| 0602694-73.2026.6.00.0000 | 179932139 | peca_de_outro_processo_juntada | PDF identifica Suspensão de Segurança 0602844-54.2026.6.00.0000, juntado à AIJE 0602694-73. Não equivale a uma decisão própria da AIJE; é peça contextual da suspensão. |
| 0602747-54.2026.6.00.0000 | 179920192 | cabecalho_retificado_por_despacho | O despacho oficial 179920899 de 11/10/2026 corrige expressamente o cabeçalho da decisão 179920192: onde constou AIJE 0602742-32, leia-se AIJE 0602747-54, da Coligação Brasil Pronto Pra Mais contra Marçal, Flávio e Alfredo Gaspar. Aceita com referência à retificação. |
| 0601103-76.2026.6.00.0000 | 176224359 | despacho_administrativo_sei_juntado | Despacho SEI 2026.00.000007716-7 sobre comunicação à Microsoft, sem CNJ judicial, assinado em 15/08/2026 e juntado em 21/08. Não é resultado comparável do processo 0601103-76. |
| 0601255-27.2026.6.00.0000 | 177502007 | despacho_conjunto_cnj_no_cabecalho | Despacho de cinco feitos: 0601422-44, 0601387-84, 0601405-08, 0601355-79 e 0601255-27, todos 2026.6.00.0000. O CNJ consultado consta do cabeçalho conjunto. |
| 0601355-79.2026.6.00.0000 | 177502006 | despacho_conjunto_cnj_no_cabecalho | Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho. |
| 0601383-47.2026.6.00.0000 | 178881658 | falha_transitoria_download_recuperada | Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho. |
| 0601387-84.2026.6.00.0000 | 177502004 | despacho_conjunto_cnj_no_cabecalho | Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho. |
| 0601405-08.2026.6.00.0000 | 177502005 | despacho_conjunto_cnj_no_cabecalho | Mesmo despacho conjunto de cinco feitos, com o CNJ consultado no cabeçalho. |
| 0601894-45.2026.6.00.0000 | 179857611 | falha_transitoria_download_recuperada | Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho. |
| 0601912-66.2026.6.00.0000 | 179848730 | falha_transitoria_download_recuperada | Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho. |
| 0601973-24.2026.6.00.0000 | 179935112 | falha_transitoria_download_recuperada | Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho. |
| 0602115-28.2026.6.00.0000 | 179536454 | falha_transitoria_download_recuperada | Nova requisição GET oficial recuperou a peça e confirmou CNJ no cabeçalho. |
| 0602319-72.2026.6.00.0000 | 179954170 | espaco_interno_no_numero_cabecalho | Cabeçalho escreve 060 2319-72.2026.6.00.0000. Extrato da ata confirma 0602319-72 e registra sessão de 14/10/2026, enquanto metadado dataDecisao é 15/10; a data da peça deve prevalecer na curadoria. |
| 0602771-59.2026.6.26.0000 | 179526290 | decisao_conjunta_cnj_no_cabecalho | Decisão conjunta dos REspEl 0602767-22 e 0602771-59.2026.6.26.0000; ambos CNJs constam do cabeçalho. |

## Cuidados com o corte

Há 15 peças assinadas e 15 juntadas após 31/10, selecionadas pela dataDecisao anterior. A data da sessão e o conteúdo precisam confirmar que documentam acontecimentos até o corte.

O acórdão 179954170 (DR 0602319-72) registra sessão de 14/10/2026, apesar da dataDecisao de 15/10/2026. Preservar ambas e usar a data da peça oficial no relato.

Peças administrativas ou de outro processo juntadas aos autos não são um resultado próprio. Cabeçalhos abreviados, conjuntos ou com espaços no número podem ser aceitos mediante conferência específica, sem substituir a confirmação de identidade por mera menção no corpo.

Os arquivos recuperados e o índice detalhado estão em `coleta_documental/auditoria/`. O JSON público contém URLs oficiais, metadados, hashes e inventário auditado; os binários da coleta permanecem locais até a integração editorial.


O despacho 179920899 de 11/10/2026 corrige expressamente o cabeçalho da decisão 179920192 da AIJE 0602747-54. Essa peça foi incorporada ao suplemento com referência à retificação; 13 das 15 recuperadas são admitidas como peças próprias, permanecendo duas como anexos contextuais.

O despacho 179920899 de 11/10/2026 corrige expressamente o cabeçalho da decisão 179920192 da AIJE 0602747-54. Essa peça foi incorporada ao suplemento com referência à retificação; 13 das 15 recuperadas são admitidas como peças próprias, permanecendo duas como anexos contextuais.
