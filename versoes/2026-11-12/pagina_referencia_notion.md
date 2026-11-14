Here is the result of "fetch" for the Page with URL https://app.notion.com/p/2816527d9bee432da3acce02566b1534 as of 2026-11-12T12:41:10.637Z:
<page url="https://app.notion.com/p/2816527d9bee432da3acce02566b1534" icon="🗳️">
<ancestor-path></ancestor-path>
<properties>
{"title":"Bastidores da campanha presidencial 2026: perfil do contencioso eleitoral no TSE"}
</properties>
<iconMetadata>{"type":"emoji","emoji":"🗳️"}</iconMetadata>
<content>
## 1. Introdução

Este estudo acompanha os atos do TSE no <b>ciclo das Eleições 2026</b>, com atenção especial às disputas de comunicação social entre as campanhas presidenciais (propaganda). Os gráficos mostram os registros obtidos no [Portal de Dados Abertos](https://dadosabertos.tse.jus.br/id/dataset/processual-2026).

A base de dados reúne <b>933 atos em 751 processos distintos</b>, entre <date start="2025-10-03" end="2026-09-30" />. Um processo pode ter mais de um ato. Por isso, os 933 contam registros classificados como Decisão ou Acórdão, enquanto os 751 contam processos apenas pelo número único do CNJ. Nenhuma dessas contagens indica, por si só, que o processo terminou ou teve julgamento de mérito.

Na base de dados, <b>733 atos aparecem como Decisão (78,6%)</b> e <b>200 como Acórdão (21,4%)</b>. Para saber o que foi decidido em cada caso, é preciso ler a peça. O nome do ato não mostra se houve liminar, providência processual simples (despacho) ou julgamento de mérito, o que será analisado com enfoque específico na seção 5.

<embed source="notion-file-block://e9fe1bf6-7b3b-4f5f-a694-082d325d1a45/c0bc4d15-9209-4a23-970f-8c0900d54d73?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=01_tipos_ato_restaurado_notion_agent_chart.html" />

<toggle>
Versão estática — tipos de ato

<image source="notion-file-block://2959e929-0b9a-4469-b4e2-25dafed19978/4a56a5c3-eb25-45fc-9b32-844ebd8b25ce?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=01_tipos_ato_versao_estatica.png" />
</toggle>

<b>Setembro de 2026 teve o maior volume</b>, com 603 atos, ou 64,6% do <i>corpus empiricus</i> desta pesquisa. Os gráficos usam a data registrada no sistema oficial.

<embed source="notion-file-block://cb2e667f-1a2f-4ec9-82fd-155ab6081e00/6db06a51-e4e2-448b-8d6e-8923f0b295bf?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=02_atos_por_mes_notion_agent_chart.html" />

A curva abaixo mostra o crescimento dos registros até a data de corte em 30 de setembro de 2026.

<embed source="notion-file-block://b548fb2a-2df6-4a56-97da-bf7a35d74bd2/f67d1beb-2972-4df1-a7e5-37fd8a178ceb?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=03_ritmo_acumulado_notion_agent_chart.html" />

## 2. Volume, classes e autoria dos atos

As classes processuais registradas nos <b>933 atos</b> se distribuem assim.

- <b>Rp</b> — 310 atos (33,2%).
- <b>REspEl</b> — 107 atos (11,5%).
- <b>PetCiv</b> — 92 atos (9,9%).
- <b>DR</b> — 71 atos (7,6%).
- <b>RO-El</b> — 65 atos (7,0%).
- <b>Demais classes</b> — 288 atos (30,9%).

<embed source="notion-file-block://0fc62d49-9408-4b79-85ec-eb631ced9d83/75b7494f-f91f-4388-843b-06373cff2c25?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=04_classes_por_ato_notion_agent_chart.html" />

<toggle>
Dados completos — classes dos atos

| Classe ou grupo de classes | Atos |
| --- | --- |
| Rp | 310 |
| REspEl | 107 |
| PetCiv | 92 |
| DR | 71 |
| RO-El | 65 |
| RCand | 59 |
| MSCiv | 54 |
| PA | 53 |
| Demais classes (fora das oito discriminadas) | 122 |
| <b>Total</b> | <b>933</b> |
</toggle>

<b>Classe e assunto são informações distintas</b>. Um processo da classe Representação pode tratar de vários temas. Para uma análise qualitativa, usamos um filtro de propaganda e de direito de resposta explicado nas seções 3 e 4.

O gráfico abaixo mostra o <b>ministro autor de cada ato</b>, conforme a base de dados do TSE. Esse nome pode ser diferente do relator atual do processo. Nunes Marques (297), André Mendonça (239) e Estela Aranha (131) assinam, juntos, 667 atos (ou 71,5%) no período avaliado.

<embed source="notion-file-block://dca9103b-b5c8-40f7-b40a-c0e4ce8a0e81/a399844a-ba5e-44f0-ad60-2a2479d8aaa4?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=05_autores_dos_atos_notion_agent_chart.html" />

<toggle>
Dados completos — ministros autores dos atos

| Autor do ato | Atos |
| --- | --- |
| Nunes Marques | 297 |
| André Mendonça | 239 |
| Estela Aranha | 131 |
| Dias Toffoli | 76 |
| Antonio Carlos Ferreira | 65 |
| Ricardo Villas Bôas Cueva | 58 |
| Floriano de Azevedo Marques | 43 |
| Sebastião Reis Junior | 23 |
| Cármen Lúcia | 1 |
| <b>Total</b> | <b>933</b> |
</toggle>

Um acórdão pode decidir uma etapa do processo ou apenas revisar uma liminar, sem encerrar o mérito. A leitura dos extratos oficiais do sistemas da Justiça Eleitoral permitiu identificar, nos <b>200 registros de acórdão</b>, <b>174 julgamentos unânimes (87,0%)</b> e <b>15 com divergência (7,5%)</b>; os <b>11 restantes (5,5%)</b> permanecem com votação não apurada.

Nos confrontos judiciais relativos à propaganda presidencial, o colegiado <b>manteve 22 das 26 liminares </b>cujo reexame foi levado a Plenário <b>(84,6%)</b> e modificou <b>quatro (15,4%)</b>. A atuação foi, portanto, predominantemente confirmatória nesse subconjunto. As [planilhas nominais, peças oficiais e critérios de classificação](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/tree/main/analises/colegialidade) permitem conferir cada resultado.

<embed source="notion-file-block://d413bbd8-ab48-4fdb-9526-e72d9d230e7d/bdd9664e-8035-4034-9000-06ccdb5e01a8?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=07a_individual_notion_agent_chart.html" />

Para examinar a situação das medidas liminares nos confrontos presidenciais, o gráfico seguinte organiza os 107 processos conforme a situação da decisão. Predominam os <b>76 processos</b> com liminares sem revisão colegiada comprovada até a data de corte. Em outros <b>26</b>, houve reexame pelo Plenário, que <b>manteve 22 </b>medidas e modificou quatro. Completam o conjunto um processo em que a tutela foi decidida diretamente pelo colegiado e <b>4 </b>com decisões individuais de mérito. A distribuição evidencia, assim, o predomínio de medidas liminares ainda sem revisão colegiada comprovada.

<embed source="notion-file-block://f57d735b-1e62-4b62-b025-b6a506b2d0de/c2d71fd3-c711-4d06-9846-b13591072721?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=08a_individual_notion_agent_chart.html" />

Quanto ao conjunto das liminares reexaminadas pelo Plenário nas disputas de propaganda eleitoral na campanha presidencial, a <b>taxa de manutenção </b>abaixo discriminada considera os 26 reexames: 22 medidas mantidas e 4 modificadas:

<embed source="notion-file-block://abcb7ae6-1bc6-48c1-b8f0-432370a15ce5/8d4fb2f0-36dc-43df-8ea4-158c10c59a2f?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=08b_individual_notion_agent_chart.html" />

A predominância de manutenções de medidas liminares não significa ausência de divergência durante as votações. O próximo gráfico identifica os ministros que ficaram vencidos, inclusive parcialmente. Conta-se uma ocorrência por ministro e por julgamento.

<embed source="notion-file-block://9f7500da-d2f5-405f-b470-76f959187252/237fa34d-cbde-41ed-b440-72e1366c3d81?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=09a_individual_notion_agent_chart.html" />

O recorte da campanha presidencial exige uma leitura própria: o gráfico seguinte evidencia as ocorrências de voto vencido nesses confrontos, mantendo a unidade de contagem por ministro e julgamento.

<embed source="notion-file-block://9ed01021-b1c3-41ab-8b22-c2af18bcc769/235ca1ae-c51d-4a07-b472-eaf3cc28640b?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=09b_individual_notion_agent_chart.html" />

<toggle>
Dados completos — ocorrências de voto vencido

| Ministro | Corpus (15 acórdãos) | Confrontos (8 julgamentos) |
| --- | --- | --- |
| André Mendonça | 8 | 5 |
| Floriano de Azevedo Marques | 7 | 3 |
| Estela Aranha | 4 | 3 |
| Nunes Marques | 3 | 2 |
| Dias Toffoli | 1 | 1 |
| Antonio Carlos Ferreira | 1 | 0 |
| Ricardo Villas Bôas Cueva | 0 | 1 |
</toggle>

<b>Situação dos 107 confrontos presidenciais.</b> Além das 22 manutenções e 4 modificações, há 1 tutela decidida diretamente pelo colegiado, 76 liminares sem revisão colegiada comprovada até a data de corte (30/09/2026) e 4 decisões individuais de mérito. Outro detalhe importante é que a pendência de referendo não se confunde com pendência do mérito.

<b>Unanimidade e divergência nas disputas presidenciais.</b> Os 27 julgamentos colegiados se dividem em 19 unânimes (70,4%) e 8 com divergência (29,6%). Os votos vencidos ocorreram em <b>8 </b>julgamentos para <b>André Mendonça</b>, <b>7 </b>para <b>Floriano de Azevedo Marques</b>, <b>4 </b>para <b>Estela Aranha</b>, <b>3 </b>para <b>Nunes Marques </b>e <b>1 </b>para <b>Dias Toffoli </b>e <b>Antonio Carlos Ferreira</b>, cada. Conta-se uma ocorrência por ministro e julgamento, inclusive divergência parcial; vários ministros podem ficar vencidos no mesmo julgamento. Os gráficos apresentam separadamente as ocorrências de voto vencido no <i>corpus empiricus </i>do ciclo eleitoral de 2026 e nos confrontos presidenciais.

<b>Alcance das reformas de decisões liminares.</b> Nos 4 confrontos em que houve modificação — [0600950-43](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600950-43.2026.6.00.0000), [0600973-86](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600973-86.2026.6.00.0000), [0601015-38](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601015-38.2026.6.00.0000) e [0601016-23](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601016-23.2026.6.00.0000) — o Plenário alterou negativas anteriores de tutela e determinou a remoção de conteúdo. Isso não encerrou o mérito das representações. Já a expressão “referendou a liminar parcialmente deferida” foi contada como manutenção da decisão. No caso do vídeo do PT sobre Flávio e o Pix, por exemplo, a medida foi mantida por maioria, embora Floriano de Azevedo Marques tenha ficado vencido em parte por admitir a circulação sem impulsionamento.

<toggle>
Julgamentos com divergência nos confrontos presidenciais — resultado, ministros vencidos e fonte

<table fit-page-width="true" header-row="true">
<tr>
<td>
Processo
</td>
<td>
Efeito sobre a medida
</td>
<td>
Ministros vencidos
</td>
<td>
Fonte oficial
</td>
</tr>
<tr>
<td>
[0600468-95.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600468-95.2026.6.00.0000)
</td>
<td>
liminar mantida
</td>
<td>
André Mendonça
</td>
<td>
[(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/18/35/52/ef38ba9b753579025484a79dac886d3235cc53650c4829b3e53b2a56f67563be)
</td>
</tr>
<tr>
<td>
[0600690-63.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600690-63.2026.6.00.0000)
</td>
<td>
liminar mantida
</td>
<td>
Floriano de Azevedo Marques (em parte)
</td>
<td>
[(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/37/f985a29dbfbb483e899994bbcb0bdb4a5aff4225bcd0f033e8b8f1e8807b5156)
</td>
</tr>
<tr>
<td>
[0600950-43.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600950-43.2026.6.00.0000)
</td>
<td>
liminar modificada
</td>
<td>
André Mendonça, Dias Toffoli
</td>
<td>
[(certidão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/25/13/288f0f99aa8b3d4ef8d3bd8fcff41adf3a380012e6a4cf822a2ba056e04d9e4a)
</td>
</tr>
<tr>
<td>
[0600973-86.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600973-86.2026.6.00.0000)
</td>
<td>
liminar modificada
</td>
<td>
André Mendonça, Estela Aranha, Nunes Marques
</td>
<td>
[(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/30/7/48cf5eb1efd7140745dc8d6b525d4de40b0ac7f621dcbf1688f1b9715fbea644)
</td>
</tr>
<tr>
<td>
[0601015-38.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601015-38.2026.6.00.0000)
</td>
<td>
liminar modificada
</td>
<td>
André Mendonça
</td>
<td>
[(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/26/18/15/12/11d1357487a1cdead5b3772912df571170b8703f9a860c65783ff07a9f5056f6)
</td>
</tr>
<tr>
<td>
[0601016-23.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601016-23.2026.6.00.0000)
</td>
<td>
liminar modificada
</td>
<td>
André Mendonça, Nunes Marques
</td>
<td>
[(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/24/17/59/20/71c70ea9c630e73023fc2fbdbddbd289e697dd5ca6dc70a1cab269ff86f1ef7f)
</td>
</tr>
<tr>
<td>
[0601303-83.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601303-83.2026.6.00.0000)
</td>
<td>
liminar mantida
</td>
<td>
Estela Aranha, Floriano de Azevedo Marques
</td>
<td>
[(certidão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/25/48/26241ed77fbe34599c955b261083ae1ccfe66407a12dc784944e050071b532dc)
</td>
</tr>
<tr>
<td>
[0601315-97.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000)
</td>
<td>
Tutela indeferida diretamente pelo colegiado
</td>
<td>
Estela Aranha, Floriano de Azevedo Marques, Ricardo Villas Bôas Cueva
</td>
<td>
[(certidão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/22/26/17/976befd03bfb522f74b25d240f808158818419a60d96ba7363c590c3a2f926df)
</td>
</tr>
</table>
</toggle>

## 3. Metodologia: construção e conferência da base de dados

A pesquisa distingue duas tarefas: contar os atos e processos registrados na fonte oficial e identificar o resultado dos pedidos. A primeira utiliza o extrato estatístico do TSE; a segunda exige a leitura das peças processuais. Essa separação orienta a organização da base de dados e a interpretação dos números.

### 3.1 Origem dos dados e corte temporal

Os registros foram obtidos no conjunto [Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026), formado a partir de dados do Portal de Dados Abertos da Justiça Eleitoral. Esta versão utiliza os cinco arquivos oficiais gerados em <b>01/10/2026</b>, preservados com suas datas e seus <i>hashes </i>— códigos digitais que permitem conferir a integridade dos arquivos. A [versão congelada de 1º/10/2026](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026/tree/v2026-10-01-corte-2026-09-30/versoes/2026-10-01) mantém exatamente os dados usados neste estudo, mesmo que o TSE atualize o conjunto posteriormente.

O período dos atos selecionados vai de <b>03/10/2025 a 30/09/2026</b>, última data disponível nessa extração. O ano da eleição indica o pleito a que o processo se refere. Ele não precisa coincidir com o ano do processo nem com o do julgamento. Por isso, a base inclui <b>3 atos de 2025</b>, e o recorte começa antes do início formal da campanha.

### 3.2 Critérios de seleção e unidades de contagem

Foram incluídos somente os registros que atendem, simultaneamente, aos seguintes critérios do arquivo oficial:

- <code>NR_INSTANCIA=3</code>: atos da instância do TSE;
- <code>SG_UF_TRIBUNAL=DF</code>: tribunal identificado pela sigla DF;
- <code>DS_TIPO_DECISAO</code>: classificação como Decisão ou Acórdão.

A contagem distingue <b>atos</b> de <b>processos</b>. Em <code>atos.csv</code>, cada linha combina o número CNJ do processo com <code>SQ_DECISAO</code>, um sequencial do arquivo. Em <code>processos.csv</code>, cada número CNJ aparece uma única vez. Assim, um processo com vários atos judiciais gera vários registros na contagem de atos, mas é contado apenas uma vez na relação de processos.

### 3.3 Análise e classificação dos resultados

O quadro abaixo distingue esse universo estatístico analisado. Cada quantidade deve ser lida conforme a sua unidade de contagem:

<table fit-page-width="true" header-row="true">
<tr>
<td>
Recorte
</td>
<td>
Unidade
</td>
<td>
Quantidade
</td>
</tr>
<tr>
<td>
Decisão ou Acórdão no extrato oficial do TSE
</td>
<td>
Ato identificado no arquivo
</td>
<td>
933
</td>
</tr>
<tr>
<td>
Processos com ao menos um desses atos
</td>
<td>
CNJ único
</td>
<td>
751
</td>
</tr>
<tr>
<td>
Assunto Propaganda Eleitoral ou classe Direito de Resposta
</td>
<td>
CNJ único do corpus
</td>
<td>
286
</td>
</tr>
<tr>
<td>
Confrontos presidenciais com resultado comparável
</td>
<td>
CNJ único, com exame documental
</td>
<td>
107 (106 no corpus e 1 em suplemento documental)
</td>
</tr>
</table>

Na comparação entre os confrontos das campanhas presidenciais, os resultados registrados em <code>confrontos.csv</code> foram classificados após a leitura das peças indicadas. O arquivo estatístico do TSE não informa o resultado de cada pedido. Portanto, a classificação qualitativa dos resultados depende de avaliação ativa, conforme realizado na seção 5.

O suplemento documental encontrado contém o [processo 0601315-97](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000), cujo resultado está documentado em certidão oficial. Trata-se do caso do vídeo exibido na convenção do PL com imagem e voz recriadas de Jair Bolsonaro, em que o Plenário, por maioria, entendeu que a transmissão do vídeo em convenção partidária pela internet não transformava, por si só, a mensagem dirigida aos convencionais em propaganda eleitoral antecipada. Como esse processo não tem decisão cadastrada no extrato até a data de corte em 30/09/2026, sua inclusão na comparação entre campanhas explica os 107 confrontos: 106 pertencem à base estatística e 1 integra o suplemento documental.

### 3.4 Como reproduzir a análise e compreender seus limites

O [repositório público no GitHub](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026) reúne os arquivos do TSE, as planilhas, os gráficos e o código utilizado nos cálculos. O “leia-me” explica como abrir as planilhas sem saber programar e apresenta as instruções para baixar uma nova extração e executar os programas. A preservação dos arquivos, a explicitação dos filtros e a disponibilização dos cálculos permitem rastrear a origem dos números e reproduzir o recorte adotado.

Essa possibilidade de conferência não elimina os limites da fonte. O TSE pode atualizar os arquivos e alguns resultados anunciados em sessão ainda não aparecem no extrato. Os totais descrevem, assim, o que estava registrado na data de extração em <b>01/10/2026</b>, com atos judiciais datados até <b>30/09/2026</b>.

## 4. Propaganda eleitoral em confrontos presidenciais

### 4.1 Recorte por assunto e classe oficiais

No cadastro, o <b>assunto</b> indica o tema e a <b>classe</b> identifica o tipo de processo. O gráfico reúne <b>220 processos</b> cujo assunto menciona <b>Propaganda Eleitoral</b> e <b>66</b> da classe <b>Direito de Resposta</b>. Nenhum desses 66 tem também o assunto <b>Propaganda Eleitoral</b> na base consultada. Ainda assim, um pedido de direito de resposta pode tratar de propaganda eleitoral. Juntos, os grupos somam <b>286 processos e 364 atos.</b>

<embed source="notion-file-block://5d007f50-07f1-4061-a4ed-c308808b0be8/79a88b66-5f05-4c8e-bd91-1ee58e4a5a77?space_id=f3472195-5c64-81ae-9ad5-00037daf85be&name=06_composicao_comunicacao_notion_agent_chart.html" />

Entre os processos restantes, que ficam <b>fora do gráfico acima</b>, aparecem temas como registro de candidaturas, elegibilidade, financiamento de campanha, pesquisas eleitorais, debates, publicidade institucional e condutas vedadas. Alguns também envolvem a comunicação das campanhas, embora tenham outro assunto ou classe no cadastro. Para entender esses qualitativamente esses resultados, a próxima seção optou por examinar os litígios judiciais entre as duas principais campanhas presidenciais que movimentaram o TSE no ciclo de 2026 em relação à propaganda eleitoral.

### 4.2 O posicionamento do TSE: análise do atendimento dos pedidos das duas principais campanhas presidenciais em 2026

Como destacado nas seções anteriores, o quadro abaixo compara 107 processos em que estão representantes formais das duas principais campanhas presidenciais em lados opostos. Atendimento <b>parcial </b>conta como atendimento positivo. Os casos sem resultado comparável ou sem peça acessível ficaram de fora dos percentuais abaixo discriminados e constam da lista de exclusões e pendências.

<b>Casos ainda em conferência.</b> Foram identificados 132 processos-alvo. Destes, 107 entram na tabela e 25 ficam fora. Em 7 processos na data de 30/09/2026, o teor da decisão ainda não pôde ser lido. O mesmo ocorre com os processos [0600947-88](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600947-88.2026.6.00.0000) e [0600958-20](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600958-20.2026.6.00.0000). Todos estão identificados em <code>confrontos.csv</code>. Já entre os 107 processos disponibilizados na base de dados, 101 entram no filtro oficial de <b>propaganda </b>e <b>direito de resposta</b>. Outros 5 estão no <i>corpus empiricus </i>com classes ou assuntos diferentes ([0601274-33](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601274-33.2026.6.00.0000), [0601374-85](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601374-85.2026.6.00.0000), [0601740-27](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601740-27.2026.6.00.0000), [0601880-61](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601880-61.2026.6.00.0000), [0602140-41](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602140-41.2026.6.00.0000)). Há, ainda, 1 processo incluído com resultado em certidão oficial, como explicado na seção 3.

As campanhas de Lula e de Flávio Bolsonaro figuram como autoras em <b>48 e 59 processos, respectivamente</b>. A unidade é o processo, mesmo quando ele contém mais de uma decisão.

<table fit-page-width="true" header-row="true">
<tr>
<td>
Campanha autora
</td>
<td>
Processos
</td>
<td>
Atendido, total ou parcialmente
</td>
<td>
Não atendido
</td>
<td>
Taxa de atendimento
</td>
</tr>
<tr>
<td>
Lula e representantes formais
</td>
<td>
48
</td>
<td>
29
</td>
<td>
19
</td>
<td>
60,4%
</td>
</tr>
<tr>
<td>
Flávio Bolsonaro e representantes formais
</td>
<td>
59
</td>
<td>
20
</td>
<td>
39
</td>
<td>
33,9%
</td>
</tr>
</table>

<b>Medidas conferidas.</b> Nos 107 processos classificados, <b>68 resultados favoreceram a posição processual de Luiz Inácio Lula da Silva</b>. Foram 29 pedidos da sua campanha atendidos e 39 pedidos da campanha de Flávio Bolsonaro não atendidos. Os <b>outros 39 favoreceram a posição de Flávio</b>. Foram 20 pedidos seus atendidos e 19 pedidos do lado de Lula não atendidos.

<b>Como ler os percentuais acima?</b> Os dados consideram apenas os 107 processos verificados, ou seja, muitas decisões são provisórias e negar uma liminar não significa rejeitar a ação ao final. As taxas não são capazes de demonstrar suposta “preferência política” do TSE.

<toggle>
Processos classificados — andamento no PJe

- <b>Lula, pedidos atendidos (29).</b> [0600468-95](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600468-95.2026.6.00.0000), [0600695-85](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600695-85.2026.6.00.0000), [0600781-56](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600781-56.2026.6.00.0000), [0600782-41](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600782-41.2026.6.00.0000), [0600783-26](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600783-26.2026.6.00.0000), [0600785-93](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600785-93.2026.6.00.0000), [0600950-43](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600950-43.2026.6.00.0000), [0600973-86](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600973-86.2026.6.00.0000), [0600976-41](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600976-41.2026.6.00.0000), [0601015-38](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601015-38.2026.6.00.0000), [0601016-23](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601016-23.2026.6.00.0000), [0601048-28](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601048-28.2026.6.00.0000), [0601049-13](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601049-13.2026.6.00.0000), [0601239-73](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601239-73.2026.6.00.0000), [0601303-83](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601303-83.2026.6.00.0000), [0602140-41](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602140-41.2026.6.00.0000), [0602144-78](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602144-78.2026.6.00.0000), [0602161-17](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602161-17.2026.6.00.0000), [0602197-59](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602197-59.2026.6.00.0000), [0602198-44](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602198-44.2026.6.00.0000), [0602199-29](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602199-29.2026.6.00.0000), [0602200-14](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602200-14.2026.6.00.0000), [0602261-69](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602261-69.2026.6.00.0000), [0602266-91](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602266-91.2026.6.00.0000), [0602267-76](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602267-76.2026.6.00.0000), [0602268-61](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602268-61.2026.6.00.0000), [0602269-46](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602269-46.2026.6.00.0000), [0602371-68](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602371-68.2026.6.00.0000), [0602436-63](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602436-63.2026.6.00.0000).
- <b>Lula, pedidos não atendidos (19).</b> [0600955-65](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600955-65.2026.6.00.0000), [0601014-53](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601014-53.2026.6.00.0000), [0601053-50](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601053-50.2026.6.00.0000), [0601250-05](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601250-05.2026.6.00.0000), [0601315-97](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000), [0601773-17](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601773-17.2026.6.00.0000), [0601849-41](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601849-41.2026.6.00.0000), [0601850-26](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601850-26.2026.6.00.0000), [0601862-40](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601862-40.2026.6.00.0000), [0601894-45](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601894-45.2026.6.00.0000), [0601895-30](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601895-30.2026.6.00.0000), [0601902-22](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601902-22.2026.6.00.0000), [0601937-79](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601937-79.2026.6.00.0000), [0602062-47](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602062-47.2026.6.00.0000), [0602109-21](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602109-21.2026.6.00.0000), [0602111-88](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602111-88.2026.6.00.0000), [0602114-43](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602114-43.2026.6.00.0000), [0602117-95](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602117-95.2026.6.00.0000), [0602148-18](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602148-18.2026.6.00.0000).
- <b>Flávio, pedidos atendidos (20).</b> [0600689-78](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600689-78.2026.6.00.0000), [0600690-63](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600690-63.2026.6.00.0000), [0600697-55](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600697-55.2026.6.00.0000), [0600698-40](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600698-40.2026.6.00.0000), [0600966-94](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600966-94.2026.6.00.0000), [0601374-85](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601374-85.2026.6.00.0000), [0601627-73](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601627-73.2026.6.00.0000), [0601686-61](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601686-61.2026.6.00.0000), [0601690-98](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601690-98.2026.6.00.0000), [0601749-86](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601749-86.2026.6.00.0000), [0601755-93](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601755-93.2026.6.00.0000), [0601763-70](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601763-70.2026.6.00.0000), [0601786-16](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601786-16.2026.6.00.0000), [0601806-07](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601806-07.2026.6.00.0000), [0601817-36](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601817-36.2026.6.00.0000), [0601880-61](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601880-61.2026.6.00.0000), [0601962-92](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601962-92.2026.6.00.0000), [0602025-20](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602025-20.2026.6.00.0000), [0602080-68](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602080-68.2026.6.00.0000), [0602367-31](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602367-31.2026.6.00.0000).
- <b>Flávio, pedidos não atendidos (39).</b> [0600963-42](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600963-42.2026.6.00.0000), [0601181-70](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601181-70.2026.6.00.0000), [0601274-33](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601274-33.2026.6.00.0000), [0601740-27](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601740-27.2026.6.00.0000), [0601765-40](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601765-40.2026.6.00.0000), [0601767-10](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601767-10.2026.6.00.0000), [0601768-92](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601768-92.2026.6.00.0000), [0601845-04](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601845-04.2026.6.00.0000), [0601866-77](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601866-77.2026.6.00.0000), [0601868-47](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601868-47.2026.6.00.0000), [0601871-02](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601871-02.2026.6.00.0000), [0601872-84](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601872-84.2026.6.00.0000), [0601876-24](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601876-24.2026.6.00.0000), [0601877-09](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601877-09.2026.6.00.0000), [0601878-91](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601878-91.2026.6.00.0000), [0601879-76](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601879-76.2026.6.00.0000), [0601882-31](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601882-31.2026.6.00.0000), [0601883-16](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601883-16.2026.6.00.0000), [0601889-23](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601889-23.2026.6.00.0000), [0601890-08](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601890-08.2026.6.00.0000), [0601892-75](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601892-75.2026.6.00.0000), [0601908-29](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601908-29.2026.6.00.0000), [0601911-81](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601911-81.2026.6.00.0000), [0601912-66](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601912-66.2026.6.00.0000), [0601913-51](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601913-51.2026.6.00.0000), [0601926-50](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601926-50.2026.6.00.0000), [0601927-35](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601927-35.2026.6.00.0000), [0601928-20](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601928-20.2026.6.00.0000), [0601929-05](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601929-05.2026.6.00.0000), [0601930-87](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601930-87.2026.6.00.0000), [0601943-86](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601943-86.2026.6.00.0000), [0601944-71](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601944-71.2026.6.00.0000), [0601947-26](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601947-26.2026.6.00.0000), [0602139-56](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602139-56.2026.6.00.0000), [0602238-26](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602238-26.2026.6.00.0000), [0602243-48](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602243-48.2026.6.00.0000), [0602245-18](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602245-18.2026.6.00.0000), [0602273-83](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602273-83.2026.6.00.0000), [0602370-83](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602370-83.2026.6.00.0000).
</toggle>

## 5. Os 107 confrontos entre as duas principais campanhas presidenciais

Os relatos abaixo estão em ordem de data em que a peça oficial que fundamenta cada síntese aparece no Portal de Dados Abertos, da mais recente à mais antiga. Quando o resultado consta apenas de certidão, vale a data da certidão.

### 1. Card impulsionado com frase atribuída a Lula sobre preços: suspensão liminar

Em [<b>0602266-91.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602266-91.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais pediu a suspensão de um anúncio impulsionado na Meta. O card atribuiu a Lula a frase “Se o produto está caro, não compre” e redirecionava ao portal Direita Já. Estela Aranha concedeu a liminar em 30/09. Determinou a retirada em 24 horas e vedou a republicação impulsionada. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/7/58/83a92c463214866219fec386f83db097e676606df4bc82ebe7436dd6adead3ed).

### 2. Card impulsionado com frase atribuída a Lula sobre crime organizado: suspensão liminar

Em [<b>0602267-76.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602267-76.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais pediu a suspensão de um anúncio impulsionado na Meta. O card atribuiu a Lula a frase “Brasil será um dos países mais respeitados no mundo do crime organizado” e redirecionava ao portal Direita Já. Estela Aranha concedeu a liminar em 30/09. Determinou a retirada em 24 horas e vedou a republicação impulsionada. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/4/59/5c34b44f0fb1dc8a2938f786585fe9d51ddd90f18fb948b2e63d6621141d07a2).

### 3. Card impulsionado com frase atribuída a Lula sobre a compra de telefones roubados: suspensão liminar

Em [<b>0602268-61.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602268-61.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais pediu a suspensão de um anúncio impulsionado na Meta. O card atribuiu a Lula a frase “Eu sei que rico não compra telefone roubado, mas eu sei que os pobres compram” e redirecionava ao portal Direita Já. Estela Aranha concedeu a liminar em 30/09. Determinou a retirada em 24 horas e vedou a republicação impulsionada. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/8/32/99c66c94f94f8e21aec6a307d18eb2ba33768d7e2ce1e6c46e7c4c8d30932d14).

### 4. Outro card com frase atribuída a Lula sobre a compra de telefones roubados: suspensão liminar

Em [<b>0602269-46.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602269-46.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais pediu a suspensão de um anúncio impulsionado na Meta. O card atribuiu a Lula a frase “Eu sei que rico não compra telefone roubado, mas eu sei que os pobres compram” e redirecionava ao portal Direita Já. Estela Aranha concedeu a liminar em 30/09. Determinou a retirada em 24 horas e vedou a republicação impulsionada. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/6/33/74ff0dc62026722e27d88258d5924fb7a019858510692c58224e578ddd0b94a2).

### 5. Anúncio impulsionado contestado por Flávio Bolsonaro: suspensão liminar

Em [<b>0602367-31.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602367-31.2026.6.00.0000), Flávio Bolsonaro pediu a suspensão de um anúncio impulsionado na Meta, a proibição de novas veiculações e multa ao final. O card sustenta que o vídeo impulsionado menciona nominalmente o representante 4 vezes em 29 segundos, associando-o reiteradamente à oposição a medidas de interesse da população e encerrando com a expressão “<i>Flávio Bolsonaro, sempre contra o povo</i>”, configurando conteúdo negativo direcionado a adversário político.<br /><br />Estela Aranha concedeu a liminar em 30/09. Determinou a retirada em 24 horas e vedou a republicação impulsionada. O resultado é cautelar; o mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/9/46/5c8ec4002995d4915fd9927b1374bd006f592bdd6c23806418e8529e22ffb8a3).

### 6. Vídeo no Instagram: retirada liminar negada

Em [<b>0602370-83.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602370-83.2026.6.00.0000), Flávio Bolsonaro pediu a retirada urgente de vídeo no Instagram que associava sua imagem a Adriano da Nóbrega, Rodrigo Bacellar, Comando Vermelho e Banco Master. Também requereu preservação de registros e multa ao final. Estela Aranha negou a retirada cautelar em 30/09 por não identificar, no exame inicial, ilicitude flagrante ou probabilidade do direito. A análise do mérito ficou para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/9/11/7cafe5c320213ae0a0ed14b7ad8e12133c2e789a7e6dd762f31008e4f58b0f18).

### 7. Propaganda de TV: identificação do vice exigida

Em [<b>0602371-68.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602371-68.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais contestou propaganda de TV de 26/09 por omitir o nome do vice Alfredo Gaspar e por imagens que, segundo ela, associavam Lula e o PT a organizações criminosas. Estela Aranha concedeu parcialmente a liminar em 30/09. Proibiu nova exibição até a correção da identificação do vice, mas deixou a alegação sobre o conteúdo para exame após o contraditório. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/9/30/0e93d9061254a7a1d36a32064c6c879128affb8684ec3d45acf6b1f12d246145).

### 8. Inserções de TV: identificação do vice exigida

Em [<b>0602436-63.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602436-63.2026.6.00.0000), a Coligação Brasil Pronto Pra Mais contestou inserções de TV de 27/09 por omitir o nome do vice Alfredo Gaspar. Estela Aranha concedeu parcialmente a liminar em 30/09. Impediu nova veiculação até a adequação da peça, mas não determinou que o pool de emissoras apresentasse mapa de transmissões. O mérito final não está documentado neste corte. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/30/14/8/51/92743bd6e3012c3cd0fa963dd4c4099b162d01e54ae80c7d1e22fd9dc64fa730).

### 9. Direito de resposta em site da campanha — atendimento parcial

Em [<b>0601817-36.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601817-36.2026.6.00.0000), Flávio Bolsonaro pediu resposta a três matérias do site ligado à campanha de Lula, “[opiordosbolsonaros.com.br](http://opiordosbolsonaros.com.br)”: uma o associava ao escândalo do Banco Master e ao patrocínio de <i>Dark Horse</i> por Daniel Vorcaro; outra o chamava de “traidor da pátria” que queria “vender o Brasil” aos EUA; a terceira descrevia uma “trajetória de rachadinha, milícia e corrupção”. Nunes Marques negou resposta às duas primeiras e a concedeu parcialmente à terceira, apenas pela associação pessoal à milícia e à corrupção. A divulgação ainda depende da aprovação do texto e de decisão integrativa. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/11/45/2dcef3544e4ff72280c79e9699a401990a35889be5e94313636d638e253ccec5).

### 10. Vídeo com ataques à Justiça Eleitoral e painéis externos

Flávio Bolsonaro contestou vídeo de comício de Lula em Teresina com a frase “que não venha o Tribunal Eleitoral querer falcatrua”. Impugnou também grandes painéis eletrônicos de campanha com efeito de outdoor. Em [<b>0601962-92.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601962-92.2026.6.00.0000), o relator concedeu liminar parcial para retirar o vídeo em 24 horas, proibir republicações e o uso dos painéis com esse efeito visual. A medida é monocrática e provisória; alcança reproduções idênticas ou modificadas, sem encerrar a representação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/19/1/6054c87e0e5136f3a4aced9b97bb6a4f5f9094ef62b7f75331990d9d87b7ff0d).

### 11. Pedido de resposta a críticas em propaganda gratuita

A coligação de Lula pediu resposta a bloco de TV de Flávio Bolsonaro que dizia que o governo integrava um “sistema apodrecido” e que Lula havia “dividido seu poder com Alexandre de Moraes”. Em [<b>0602062-47.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602062-47.2026.6.00.0000), o TSE negou monocraticamente a liminar por não identificar falsidade objetiva, grave descontextualização ou ofensa juridicamente relevante naquele exame inicial. O pedido prosseguiu para contraditório, com citação e posterior manifestação da Procuradoria-Geral Eleitoral. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/11/54/25fde80f6b2739873c257998d5747a1502ea2254fc9c36b48ea52646fe4505ff).

### 12. Chapa de Lula ilegível em peça de TV

A campanha de Flávio Bolsonaro apresentou o pedido contra a de Lula em [<b>0602080-68.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602080-68.2026.6.00.0000). O relator deferiu parcialmente a tutela, pois os nomes dos candidatos não foram exibidos de forma clara e legível, em afronta ao art. 36, § 4º, da Lei nº 9.504/1997. Determinou-se a abstenção de novas veiculações até o saneamento do vício, sem censura definitiva do conteúdo da propaganda. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/11/54/04fe03b296aa1c63e5363d7039527a424e0737f80cb78cdcde165bf56cf7c3be).

### 13. Publicação do PL contestada pela coligação de Lula

A coligação de Lula contestou vídeo do PL e de Valdemar Costa Neto no Instagram com trecho de entrevista de Flávio Bolsonaro e legenda sobre suposta “reunião secreta” em que Lula teria prometido ajudar um banqueiro a resolver problemas do banco. Em [<b>0602109-21.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602109-21.2026.6.00.0000), o relator negou monocraticamente a liminar por considerar a publicação parte do debate político, sem desinformação deliberada evidente. Não houve remoção imediata; a decisão foi submetida ao referendo do Plenário e o processo prosseguiu. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/11/54/37cca9396804bbf6bdd2d1c449b71178d66a668c49f010e143ec4c6498ddfa4a).

### 14. Direito de resposta sobre crítica política ao PT

A coligação de Lula pediu resposta a propaganda de TV de Flávio que exibia uma mira sobre a estrela do PT, afirmava que seu governo colocara os brasileiros “na mira do crime” e propunha tirar o partido do poder. Em [<b>0602148-18.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602148-18.2026.6.00.0000), o TSE negou monocraticamente a liminar por considerar a mensagem crítica política, sem falsidade objetiva manifesta nem imputação pessoal de vínculo com organizações criminosas. Determinou a regularização da mídia e da transcrição para prosseguimento do feito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/28/18/11/45/c3b83ef4b9beee33baf2f9a8ee6478fbdebb8f284aeee5a7467f0d33ed4c68c8).

### 15. Vídeos do PT que associavam Flávio ao tarifaço

O PL impugnou vídeos do PT e de seus dirigentes que atribuíam a Flávio Bolsonaro o pedido do tarifaço norte-americano e apresentavam um agradecimento a Trump como apoio às novas tarifas. Em [<b>0600966-94.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600966-94.2026.6.00.0000), o relator determinou monocraticamente a remoção em 24 horas e proibiu a republicação ou adulteração do material. A liminar se baseou na possível manipulação do contexto e no risco de dano à honra e à imagem do pré-candidato, com submissão posterior ao colegiado. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/32/4edab64f82e68090b802b6bd7411de327e564b92dd2a483f948b12b31b4a3c3e).

### 16. Vídeo exibido na Festa do Peão de Americana

A Federação Brasil da Esperança contestou vídeo de Flávio Bolsonaro projetado na Festa do Peão de Americana, com exaltação ao agronegócio e convite para “resgatar o nosso Brasil”. Alegou propaganda antecipada. Em [<b>0601014-53.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601014-53.2026.6.00.0000), o TSE julgou a representação improcedente porque não identificou pedido explícito de voto nem referência inequívoca ao pleito, à candidatura ou ao cargo pretendido. Considerou o conteúdo crítica política e afastou a multa. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/33/b50bd64ae7437d397543d130af978c0828008aa17a8c11b03e8ab7ac556ff0bd).

### 17. Entrevista de Lula gravada no Palácio da Alvorada

Flávio Bolsonaro contestou entrevista de Lula à Record, gravada no Palácio da Alvorada e exibida durante o debate presidencial da Bandeirantes. Alegou caráter eleitoral e uso de residência e recursos públicos em benefício da candidatura. Em [<b>0601740-27.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601740-27.2026.6.00.0000), o TSE negou monocraticamente a liminar por considerar necessário ouvir os envolvidos e apurar o emprego de servidores, equipamentos, serviços e recursos públicos. Requisitou informações à Presidência e à Secom, sem impor, por ora, as medidas inibitórias nem a preservação cautelar da mídia. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/20/60c81d6ab680a4913eea7823ea480d41d7e7690ecc7a1296d03c1c6b54952fec).

### 18. Entrevista televisiva com referências a terceiros

A coligação de Lula pediu resposta a declarações de Flávio Bolsonaro no Jornal Nacional sobre urnas eletrônicas, o 8 de janeiro, o financiamento de <i>Dark Horse</i> e a responsabilidade de Lula pelo tarifaço, entre outros temas. Em [<b>0601773-17.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601773-17.2026.6.00.0000), o TSE considerou a coligação sem legitimidade quanto às referências exclusivas a terceiros e não identificou falsidade manifesta nem grave ofensa nos demais itens. Extinguiu parcialmente o processo sem exame do mérito e julgou improcedente o restante do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/19/37d1ec491f1915d73feb2fecbfe2ec99216add4df6cee887fe88072054e8d674).

### 19. Inserções de rádio suspensas por possível falsidade

Flávio Bolsonaro contestou a peça de rádio “Foi o Flávio Bolsonaro”, da campanha de Lula, que relacionava seu nome a pedido de dinheiro a Daniel Vorcaro, depósitos em loja de chocolate, “rachadinha”, homenagem a Adriano da Nóbrega e compra de imóveis em dinheiro pela família. Em [<b>0601786-16.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601786-16.2026.6.00.0000), o TSE viu, em análise preliminar, plausibilidade de conteúdo capaz de induzir o eleitor a erro e risco na veiculação reiterada. Suspendeu imediatamente a propaganda e proibiu nova divulgação até o julgamento do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/29/34/579875cab6b5bc96fbc613fbab465339d0bb1fc8412c39c3e17964bb6ad0c415).

### 20. Título que associava Flávio a milícia e corrupção

A campanha de Flávio Bolsonaro apresentou o pedido contra a de Lula em [<b>0601806-07.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601806-07.2026.6.00.0000). O relator deferiu parcialmente a tutela para retirar e impedir a republicação do título que associava Flávio Bolsonaro a “rachadinha, milícia e corrupção”, por exceder os limites da crítica eleitoral com imputação pessoal não suficientemente amparada. Foram mantidas, por ora, as demais publicações e indeferidas a remoção integral do conteúdo e a suspensão do domínio. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/26/3e2ae78fd6d82cf040350c7c420071a0ce70035b3a8041353105b5bcd62f7630).

### 21. Crítica a Flávio em bloco de rádio de 5/9

Flávio Bolsonaro contestou bloco de rádio da campanha de Lula que falava em “ministros corruptos”, dizia que o governo Bolsonaro não comprara vacinas contra a Covid e atribuía a isso o fechamento de escolas, concluindo com “Tal pai, tal filho”. Em [<b>0601882-31.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601882-31.2026.6.00.0000), o TSE negou monocraticamente a liminar por considerar que a crítica não lhe imputava pessoalmente conduta concreta desonrosa. A propaganda foi mantida, com contraditório e posterior exame de mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/26/16/28/26/7e0d1015b30f2f69a5b49b9ea2c79d2a47c070db6e61193ba4222082c0fd7a42).

### 22. Impulsionamento pago de crítica negativa com multa

Flávio Bolsonaro contestou anúncios pagos da campanha de Lula que atribuíam à família Bolsonaro a expansão de armas e munições em circulação e seu acesso por facções, concluindo com “Bolsonaros, nunca mais”. Em [<b>0602025-20.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602025-20.2026.6.00.0000), o TSE julgou monocraticamente a representação procedente: o impulsionamento de propaganda negativa viola o art. 57-C, § 3º, da Lei nº 9.504/1997, embora a crítica possa circular organicamente. Aplicou multa de R\$ 15.000,00 e proibiu reativar ou contratar novo impulsionamento das peças examinadas, sem impor ordem genérica sobre conteúdos futuros. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/18/42/47/dc178756b3bdfe7ea644e2698acc466f6e9cec8551aedab142a21a1a756b7f99).

### 23. Vídeo do PL sobre fatos públicos

A coligação de Lula contestou vídeo do PL que combinava manchetes sobre a Lava Jato e Roberta Luchsinger com a legenda “É difícil pedir desculpas quando não há arrependimento, né, Lula?”. Alegou omissão da anulação das condenações e associação artificial entre as notícias e a fala do candidato. Em [<b>0602111-88.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602111-88.2026.6.00.0000), a relatora negou a remoção liminar por considerar o conteúdo crítica política e rememoração de fatos públicos, sem ilicitude flagrante. A publicação foi mantida provisoriamente, com defesa, parecer da Procuradoria-Geral Eleitoral e posterior exame do pedido de resposta. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/49/10/006ca5f9697db2b64d21303aea0384876c29433578c1889c5d0084d9bba013b8).

### 24. Vídeo do PL alegadamente manipulado

A coligação de Lula contestou montagem de entrevista publicada pelo PL no Instagram que repetia a resposta “porque eu já acabei com a fome duas vezes” após perguntas sobre corrupção, o INSS e seu filho. Alegou que a edição simulava respostas evasivas nunca dadas naquela sequência. Em [<b>0602114-43.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602114-43.2026.6.00.0000), a relatora negou monocraticamente a retirada liminar por não considerar a manipulação e a ilicitude claramente demonstradas. A publicação foi mantida, com citação e manifestação da Procuradoria-Geral Eleitoral. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/50/19/402dd7abeecba27505d18ef14430a67f5fcf74b8dec2fac45c51ccc6c2c57e4e).

### 25. Propaganda sobre suposto esquema de corrupção

A coligação de Lula contestou vídeo do PL sobre o caso do INSS que afirmava que dinheiro roubado de aposentados poderia estar na conta de seu filho, mencionava “propina em forma de joias” e concluía: “A culpa é do Lula”. Em [<b>0602117-95.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602117-95.2026.6.00.0000), o TSE negou monocraticamente a liminar por considerar a propaganda apoiada em reportagens e investigações de interesse público, sem ilicitude flagrante ou perigo irreversível. A retirada foi afastada, e o direito de resposta ficou para exame após o contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/49/28/5388f6d1ba0091c79270b465bd0ca60e8d9a22fc4f3ed3568dd90fd70835e563).

### 26. Entrevista sobre suposto vínculo com milicianos

Flávio Bolsonaro contestou entrevista de Lula à Rádio Tupi, depois publicada no YouTube, em que este afirmava que um candidato à Presidência era “ligado aos milicianos” do Rio e mencionava vínculos da família Bolsonaro com esses grupos. Em [<b>0602139-56.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602139-56.2026.6.00.0000), a relatora negou monocraticamente a remoção liminar por não identificar requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com posterior citação e submissão da decisão ao Plenário. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/52/42/b47c5164098964e09ac9ce135793c8df49233a5a2b85ada6f12652c04992ab0d).

### 27. Nome do vice ilegível em inserções de Flávio

A campanha de Lula apresentou o pedido contra a de Flávio Bolsonaro em [<b>0602144-78.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602144-78.2026.6.00.0000). Em decisão monocrática, a relatora reconheceu, em cognição sumária, a violação objetiva ao dever de identificação clara e legível do candidato a vice nas inserções majoritárias. Determinou a abstenção de novas veiculações até a adequação da propaganda e indeferiu a notificação do pool de emissoras para fornecer mapas de transmissão. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/51/46/0c92886d67d8d9202f971ad723a0c31394a63b6944b529f8257eb8b9f9e67665).

### 28. Outra inserção sem identificação legível do vice

A campanha de Lula apresentou o pedido contra a de Flávio Bolsonaro em [<b>0602161-17.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602161-17.2026.6.00.0000). Em tutela de urgência monocrática, o TSE reconheceu aparente violação ao art. 36, § 4º, da Lei nº 9.504/1997 e ao art. 12 da Res.-TSE nº 23.610/2019, que exigem a identificação clara e legível do vice quando divulgado o titular da chapa. Determinou-se a abstenção de novas veiculações da inserção até sua adequação, mas foi indeferida a notificação do pool de emissoras para fornecimento de mapas de mídia. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/52/5/d66ba54bdb429df146ae3b84c55f2e1d1ce227db075740f588a9af4fa84959e7).

### 29. Anúncio pago que associava Lula à pobreza

A campanha de Lula apresentou o pedido contra a de Flávio Bolsonaro em [<b>0602197-59.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602197-59.2026.6.00.0000). Em decisão liminar, a relatora entendeu que o anúncio impulsionado, ao associar adversário à pobreza e à miséria, veiculou propaganda negativa, e não promoção da candidatura, modalidade vedada pela legislação eleitoral. Determinou-se a suspensão do impulsionamento e a remoção do conteúdo em 24 horas, inclusive pelo provedor, além da proibição de republicação ou difusão de material substancialmente idêntico. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/53/16/5960985b65345e9ea3a6d9a77c3017194bc6305018018c1c16525938613a431f).

### 30. Anúncio pago com crítica negativa a Lula

A coligação de Lula impugnou anúncio pago de Flávio Bolsonaro no Facebook e no Instagram que associava o adversário à pobreza e à miséria e usava a expressão “#ForaPT”. Em [<b>0602198-44.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602198-44.2026.6.00.0000), o TSE concedeu liminar monocrática por entender que o impulsionamento só pode promover ou beneficiar candidaturas, não ampliar críticas negativas ao adversário. Determinou a suspensão e a remoção do anúncio em 24 horas, sob pena de multa, inclusive pelo provedor. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/49/46/c9b04dd2be91da8141b67301c06d545c3c9b165124e8261388c05ecc8502670b).

### 31. Outro anúncio pago com crítica negativa a Lula

A coligação de Lula impugnou anúncio pago de Flávio Bolsonaro no Facebook e no Instagram que associava o adversário à pobreza e à miséria e usava a expressão “#ForaPT”. Em [<b>0602199-29.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602199-29.2026.6.00.0000), o TSE concedeu liminar monocrática por entender que o impulsionamento só pode promover ou beneficiar candidaturas, não ampliar críticas negativas ao adversário. Determinou a suspensão e a remoção do anúncio em 24 horas, sob pena de multa, e vedou sua republicação impulsionada. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/48/15/30f5cadb16a6ff99339c82fdae378c027a4a43196085baa966e0b944b9007161).

### 32. Quarto anúncio pago com crítica negativa a Lula

A coligação de Lula impugnou anúncio pago de Flávio Bolsonaro no Facebook e no Instagram que associava o adversário à pobreza e à miséria e usava a expressão “#ForaPT”. Em [<b>0602200-14.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602200-14.2026.6.00.0000), o TSE concedeu liminar monocrática por entender que o impulsionamento só pode promover ou beneficiar candidaturas, não ampliar críticas negativas ao adversário. Determinou a suspensão e a remoção do anúncio em 24 horas, sob pena de multa, e vedou sua republicação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/48/54/7acbfa3a229eec5fb2ad503d06437aace4aff443c40f57a2acebf396470ca108).

### 33. Publicação sobre suposta rachadinha

Flávio Bolsonaro contestou publicação conjunta do PT, Lindbergh Farias e Rogério Correia no Instagram que o chamava de “rachador” e o relacionava a Fabrício Queiroz. Alegou que a peça insinuava culpa em fatos sem condenação e cuja investigação fora arquivada. Em [<b>0602238-26.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602238-26.2026.6.00.0000), a relatora negou a remoção liminar por considerar o conteúdo predominantemente crítico e sem ilicitude flagrante ou perigo concreto. A postagem foi mantida por ora, com exame aprofundado reservado para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/53/41/f190ec924fad65d88144ddc6e16fc9869be6f5460056531047285e4469620141).

### 34. Publicação sobre o caso “Dark Horse”

Flávio Bolsonaro contestou postagem do PT que o apresentava como investigado por corrupção e lavagem de dinheiro público para financiar conspiração contra o Brasil nos EUA, chamando-o de “candidato a vassalo dos Estados Unidos”. Alegou que o caso <i>Dark Horse</i> tratava de patrocínio privado de filme sobre seu pai. Em [<b>0602243-48.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602243-48.2026.6.00.0000), a relatora negou monocraticamente a liminar por considerar a referência apoiada em informações públicas e a expressão uma metáfora política. A publicação foi mantida até exame posterior com contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/53/53/15c46576ff173f356617e89df6ed4f44dc51a15f974a47f108db490cd3688dbd).

### 35. Publicação com alegação de uso de inteligência artificial

Flávio Bolsonaro contestou vídeo conjunto do PT e de aliados no Instagram que associava <i>Dark Horse</i>, fraudes previdenciárias, desvios de emendas e atividades nos EUA. Alegou imputações sem suporte e uso de IA sem identificação adequada. Em [<b>0602245-18.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602245-18.2026.6.00.0000), o TSE negou a liminar por não identificar ilicitude flagrante, emprego inequívoco de IA ou perigo concreto que justificasse restringir a expressão. A publicação foi mantida, com prosseguimento da representação e exame posterior após o contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/51/8/0e9b309899c72a14961c5c0d97917887cf5e71cb32e815030db8c19575aa1e12).

### 36. Anúncio pago negativo contra Lula

A coligação de Lula impugnou anúncio pago de Flávio Bolsonaro que direcionava usuários ao portal “Direita Já”, com peças de ataque ao adversário disponíveis para replicação por terceiros. Em [<b>0602261-69.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602261-69.2026.6.00.0000), a relatora considerou que o impulsionamento ampliava propaganda negativa, em vez de promover a candidatura contratante. Concedeu liminar para suspender o impulsionamento, remover o anúncio em 24 horas e impedir nova difusão mediante impulsionamento. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/48/36/a81a030d3d281ac68e169a3d44c7610bf0dc3ba85830258b12fa765a46bf5dcf).

### 37. Publicação crítica no Instagram preservada

Flávio Bolsonaro contestou vídeo satírico do PT e de aliados que usava a fala de Jair Bolsonaro “Pretendo beneficiar um filho meu sim, pretendo”. Alegou que a declaração se referia à indicação de Eduardo para a embaixada nos EUA, mas fora editada para sugerir favorecimento a Flávio. Em [<b>0602273-83.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602273-83.2026.6.00.0000), o TSE negou monocraticamente a remoção liminar por considerar o conteúdo crítico e opinativo, sem falsidade objetiva demonstrada nem requisitos para a medida. A publicação foi mantida, com mérito reservado para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/25/16/50/44/c7156a6b5906570dffc03fd56a2004c8a16f7df7c3147c0580bc99f31bc85fdc).

### 38. Vídeo no Palácio da Alvorada divulgado em canais de campanha

Flávio Bolsonaro questionou vídeo gravado por Lula no ambiente da Presidência e posteriormente publicado em canais oficiais de sua campanha. No processo [<b>0601880-61.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601880-61.2026.6.00.0000), Nunes Marques determinou, liminarmente, a remoção das URLs em YouTube, Instagram, Facebook e X e vedou o uso do material na propaganda gratuita. Requisitou dados sobre servidores, equipamentos e custeio da produção. A medida é monocrática e provisória. A decisão não resolve em definitivo a imputação de conduta vedada. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/22/16/16/13/ff6e65222b26b1040690462e3e8372988918a5933a3ab24571a84ad158188ed6).

### 39. Publicações coordenadas e links comerciais em AIJE

A coligação de Lula ajuizou AIJE contra Flávio Bolsonaro, Alfredo Gaspar e Mario Frias por rede de perfis que difundia propaganda em coautoria no Instagram (<i>collabs</i>) e divulgava links de produtos de campanha na Shopee. Alegou burla ao impulsionamento e ausência de contabilização das vendas. Em [<b>0602140-41.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0602140-41.2026.6.00.0000), o TSE concedeu liminar parcial para preservar e fornecer dados das plataformas e suspender endereços comerciais. Negou as demais medidas, fixou multa diária de R\$ 50 mil por descumprimento e determinou a defesa dos investigados. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/22/8/32/22/75c01095268e6b3f5293893f18defb3fd5dc2239e233db7e67d216b234a3e98a).

### 40. Vídeo sobre crime organizado — reversão colegiada da negativa liminar

A Federação Brasil da Esperança contestou vídeo de Flávio Bolsonaro no Instagram que associava Lula ao PCC e ao Comando Vermelho, no debate sobre classificar as facções como organizações terroristas. Em [<b>0600973-86.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600973-86.2026.6.00.0000), o relator inicialmente manteve o conteúdo como crítica política sem ilicitude evidente. O Plenário, por maioria, não referendou a negativa e ordenou a retirada em 24 horas, vedando republicações substancialmente idênticas. Houve reversão da medida urgente, não julgamento definitivo da representação. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/10/48/59/f3a4b81d74aae857a28ec040ae58528a3c2901c20571666432242de481e252da) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/30/7/48cf5eb1efd7140745dc8d6b525d4de40b0ac7f621dcbf1688f1b9715fbea644).

### 41. Deepfake contra Lula retirado em liminar

A Federação Brasil da Esperança impugnou vídeo sintético de Flávio Bolsonaro em que ele aparecia como piloto de caça à procura de “Lulinha”, apresentado como foragido por roubar milhões de idosos. Em [<b>0601239-73.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601239-73.2026.6.00.0000), o relator entendeu que o uso de deepfake para degradar pré-candidato é vedado pelo art. 9º-C, § 1º, da Resolução TSE nº 23.610/2019, mesmo identificado como IA. Determinou monocraticamente a remoção em 24 horas, a proibição de republicação e a comunicação ao provedor. A decisão é provisória. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/10/11ed9b69a761e7393d9058251b4979f3b0eb16bd2ad1198c76d2c3e536cd154c).

### 42. Live com a “Carta aos brasileiros” de Jair Bolsonaro

A Federação Brasil da Esperança contestou live de Flávio Bolsonaro no YouTube que transmitia a “Carta aos brasileiros” de Jair Bolsonaro, indicando o filho como sucessor, seguida de discurso com promessas de campanha e número de urna. Alegou propaganda antecipada. Em [<b>0601250-05.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601250-05.2026.6.00.0000), o relator negou a liminar por não identificar pedido explícito de voto nem desequilíbrio que justificasse restringir a expressão. Determinou a citação e a manifestação da Procuradoria-Geral Eleitoral. O Plenário confirmou a negativa por unanimidade, sem encerrar a representação. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/19/1/7/5c6449404c86fc66a44fd5a538dd0b15cb202f4e0773153e4f99f47051df33b0) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/52/3c11968fada6b2e6b42817de329353bc59c4aedd57d87caf55b7c95bfb78acd8).

### 43. Nota da SECOM com crítica à família Bolsonaro publicada em perfil político

O PL impugnou nota da SECOM sobre tarifas comerciais publicada no Instagram de Lula, que chamava a família Bolsonaro de “falsos patriotas” e afirmava: “Não se pode amar o Brasil apenas quando vencemos eleições”. Alegou uso da estrutura pública para ataque eleitoral. Em [<b>0601374-85.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601374-85.2026.6.00.0000), o TSE ordenou liminarmente a remoção em 24 horas, vedou nova divulgação e requisitou informações à SECOM e ao provedor. A configuração definitiva de conduta vedada segue em exame. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/10/aa9cdbdc93c7e70b606bf6d640e82bd6ddbb5b79987e38ae19ec686862fb66ac).

### 44. Imputações criminais em publicações do PT

Flávio Bolsonaro e Alfredo Gaspar contestaram vídeo do PT em que Paulo Pimenta apresentava a escolha de Gaspar para vice como recompensa por proteger a família Bolsonaro na CPMI do INSS e associava a chapa à milícia e a esquemas criminais. Em [<b>0601686-61.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601686-61.2026.6.00.0000), o relator considerou, em análise liminar, que as imputações ultrapassavam a crítica política e não tinham suporte mínimo. Ordenou a remoção das publicações no Instagram e no X e vedou republicações. Negou, por ora, a preservação genérica de registros e a comunicação preventiva ampla a outros provedores. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/43/b14156aa39ac5fc815c5ac45e54489dabb602cd8d59a90804902bf518900becc).

### 45. Vídeo do portal Dia Dia Notícias usado na TV

A coligação de Lula contestou o uso, na propaganda de TV de Flávio Bolsonaro, de vídeo do portal Dia Dia Notícias com supostos presos comemorando sua vitória em 2022. A peça dizia que “os bandidos comemoraram a vitória do seu candidato” e vinculava o resultado eleitoral à violência no país. Em [<b>0601849-41.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601849-41.2026.6.00.0000), o relator negou monocraticamente a liminar, pois a falsidade e o cumprimento do dever de verificação prévia dependiam do contraditório. Determinou a juntada da mídia e da transcrição em um dia, para posterior citação e prosseguimento do feito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/38/237045e56b306b0c58feb51adcaafc576b0c34df383cea3ec72c6bee353859f5).

### 46. Vídeo do portal Dia Dia Notícias nas redes de Flávio

A coligação de Lula contestou o uso, nos perfis de Flávio Bolsonaro no Instagram e no Facebook, de vídeo do portal Dia Dia Notícias com supostos presos comemorando sua vitória em 2022. A peça dizia que “os bandidos comemoraram a vitória do seu candidato” e vinculava o resultado eleitoral à violência no país. Em [<b>0601850-26.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601850-26.2026.6.00.0000), o relator negou monocraticamente a liminar, pois a falsidade e o cumprimento do dever de verificação prévia dependiam do contraditório. Determinou a citação dos requeridos e posterior manifestação da Procuradoria-Geral Eleitoral. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/39/5fc95b5e6e65ebb0672b961b12238b8852ea17e4756bfad9feafdc25d32ded67).

### 47. Novo uso do vídeo do portal Dia Dia Notícias na TV

A coligação de Lula contestou o uso, em nova veiculação na propaganda de TV de Flávio Bolsonaro, de vídeo do portal Dia Dia Notícias com supostos presos comemorando sua vitória em 2022. A peça dizia que “os bandidos comemoraram a vitória do seu candidato” e vinculava o resultado eleitoral à violência no país. Em [<b>0601862-40.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601862-40.2026.6.00.0000), o relator negou monocraticamente a liminar, pois a falsidade e o cumprimento do dever de verificação prévia dependiam do contraditório. Determinou a regularização da mídia, para posterior citação e prosseguimento do feito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/17/18/32/39/443913c44db933050f010ad31d0ff1c6554eca4abc1383baa28bf6f42f6c4bdf).

### 48. Nome do candidato a vice ilegível em propaganda de Lula

A campanha de Flávio Bolsonaro contestou em [<b>0601749-86.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601749-86.2026.6.00.0000) propaganda de Lula que não indicava Alckmin como vice. O relator viu possível violação ao art. 36, § 4º, da Lei nº 9.504/1997 e ao art. 12 da Res.-TSE nº 23.610/2019. Em decisão inicial, proibiu nova veiculação daquela peça até a correção. Não impôs uma ordem geral para peças futuras e deixou a eventual multa para depois da defesa.

O Plenário confirmou por unanimidade essa liminar parcialmente concedida. Os efeitos ficaram restritos ao alcance da medida inicial. O resumo examinado não descreve outras medidas. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/14/14/40/0d18c690fe46597b5e729087a079bfa28626dd68dae6811a22b40722382f033b) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/16/17/55/20/aa543a228e7772850c79dd980631f43aa69642ef47589ec6eddbe30af46ffdaf).

### 49. Três vídeos que associavam Lula a organizações criminosas

A Federação Brasil da Esperança impugnou três vídeos divulgados no Instagram por Flávio Bolsonaro, Carlos Bolsonaro e o PL, com associação de Lula a organizações criminosas e imagens manipuladas. Em [<b>0600468-95.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600468-95.2026.6.00.0000), a relatora ordenou a remoção em 24 horas e proibiu a republicação do material. Em 09/09, o Plenário referendou a liminar por maioria, vencido André Mendonça. A remoção permanece medida cautelar, sem conclusão de mérito registrada na base. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/36/16/073d8a8cb8f7e6c01ce3632c17507b7c1b28052f4c5c13c84bfceccc959ee306) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/18/35/52/ef38ba9b753579025484a79dac886d3235cc53650c4829b3e53b2a56f67563be).

### 50. Peça conexa no rádio — suspensão parcial da veiculação

Flávio Bolsonaro também contestou a versão de rádio de “Currículo de Flávio Bolsonaro”, que reunia acusações de “funcionário fantasma”, “rachadinha” e pedido de 134 milhões a Daniel Vorcaro. Em [<b>0601763-70.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601763-70.2026.6.00.0000), a relatora suspendeu liminarmente a versão radiofônica; considerou a televisão já abrangida pelo processo anterior. O Plenário referendou a tutela parcial por unanimidade em 09/09. Os dois processos são conexos e não representam controvérsias independentes. A suspensão é provisória. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/2/0/3/25/5e8206289b1109898d2985e8eb9c25296679de7563f09cc44d6acd588121bf61) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/18/35/52/ac51cbe2a15913ced9ff7a6250a3f52a8d4a87c3c8754f9faca601c1b96733cb).

### 51. Discurso de Lula em Itajaí — negativa liminar referendada

O PL contestou discurso de Lula em evento oficial de Itajaí/SC, no qual conclamava o público a comparar governos e criticava racismo e “hegemonia branca”, com referência a Hitler. Alegou propaganda antecipada e discriminação contra catarinenses. Em [<b>0601181-70.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601181-70.2026.6.00.0000), André Mendonça negou a liminar por não identificar ilicitude manifesta e considerar desproporcional retirar o discurso inteiro. O Plenário referendou a negativa por unanimidade. O mérito permaneceu aberto. Fonte — [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/14/22/13/e467e3501c49dfe375288acca854404886dd001ad1967c1b202164fa1cc74e6c).

### 52. Uso do Palácio do Planalto em vídeos dos perfis de Lula

A campanha de Flávio Bolsonaro pediu em [<b>0601274-33.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601274-33.2026.6.00.0000) a retirada de conteúdos ligados à Presidência e à Secom. O relator negou a liminar. Na análise inicial, não encontrou prova suficiente de uso eleitoral de bens públicos e alertou para o risco de controle prévio da comunicação presidencial. Pediu informações à Presidência e à Secom e determinou a citação de Lula.

O Plenário confirmou a negativa por unanimidade. Entendeu que as reuniões administrativas e as publicações em perfis pessoais não demonstravam, naquele momento, finalidade eleitoral nem publicidade institucional vedada pelos arts. 73, I e VI, “b”, da Lei nº 9.504/1997. O processo ainda exigia produção de provas. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/2/20/45/52/e631bc7af95f885045615e892bb627980fb415a7ec2e1c8c1fe6f4c067ac7c7d) [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/17/17/34/38/f3ba6bb2a9855a8b10c4e5551f91b24b7b243cb51ec2177c1c48c087af382930) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/14/23/9/9c98cd43873103c924c5c3cafdf3f9ebbc3678316483994289c22e8b13b20816).

### 53. Acusação de estupro contra candidato a vice — retirada de publicações

Flávio Bolsonaro, seu candidato a vice e a coligação contestaram publicações que atribuíam ao vice o estupro de uma menina de 13 anos. Em [<b>0601690-98.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601690-98.2026.6.00.0000), o relator determinou liminarmente a retirada das publicações especificadas, por considerar insuficiente o suporte para imputação criminal tão grave. O Plenário referendou parcialmente a medida por unanimidade em 09/09. O efeito imediato foi retirar os conteúdos indicados. A representação ainda não recebeu julgamento definitivo no recorte consultado. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/28/19/6/37/6ea743e282d61d6a8d19b39c0fd46796b56e6d7a5eba97cdd85cfa01f95e888d) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/14/22/49/bdb5bef2a4ed9440885b018f8c4ab943469293927a03e31335584aa2d3a1b8c0).

### 54. Inserção televisiva com acusações contra Flávio Bolsonaro suspensa

Flávio Bolsonaro pediu resposta e suspensão da inserção televisiva “Currículo de Flávio Bolsonaro”, da campanha de Lula, que o qualificava como “funcionário fantasma”, mencionava denúncia no caso da “rachadinha” e afirmava que fora “flagrado” pedindo 134 milhões a Daniel Vorcaro. Em [<b>0601755-93.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601755-93.2026.6.00.0000), a relatora suspendeu cautelarmente a peça. O Plenário referendou a liminar por unanimidade em 09/09. A ordem interrompeu a inserção, sem decidir definitivamente o direito de resposta. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/30/20/34/9/461ab285d0d201af3c906d65abdb16d774fd4cb847044f7b557f48080b68cba9) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/18/7/58/310e0c24078156baa32335b9e2cf16ded13645b0adaa9df3f1996afd9c8372a3).

### 55. Site crítico divulgado no horário eleitoral de Lula

Flávio Bolsonaro contestou a divulgação, no horário eleitoral de Lula, do site “[opiordosbolsonaros.com.br](http://opiordosbolsonaros.com.br)”, dedicado a críticas à sua candidatura. Alegou que divulgar o endereço no horário gratuito equivalia a impulsionar propaganda negativa. Em [<b>0601765-40.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601765-40.2026.6.00.0000), o TSE negou a liminar por entender que a vedação ao impulsionamento na internet não se estende automaticamente à indicação de site na propaganda gratuita. Considerou também prejudicada parte do pedido, pois a inserção correspondente já havia sido suspensa em outra representação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/18/7/13/f627ecd441ca1f663a25967f5fb1fdad5cd92d217e9d0ce60853a5a806629bd6).

### 56. Programa de TV sobre Flávio e o caso Banco Master

Flávio Bolsonaro pediu resposta e suspensão de programa de TV de Lula que afirmava que ele fora “flagrado pedindo 134 milhões a Daniel Vorcaro, no escândalo do Banco Master”. Alegou que “flagrado” sugeria falsamente um flagrante delito. Em [<b>0601845-04.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601845-04.2026.6.00.0000), o TSE negou monocraticamente a liminar por não identificar ilicitude flagrante nem perigo concreto que justificasse restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com citação dos requeridos e prosseguimento para exame do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/51/af0c1ad5a381ab2a74690d9034f18560a3a692d45b4501df1ac260f0743997cb).

### 57. Bloco eleitoral de 4/9 contestado por montagem

Flávio Bolsonaro pediu a suspensão de bloco eleitoral da campanha de Lula que combinava falas de Jair Bolsonaro e vídeo do próprio candidato para associá-lo a comportamentos misóginos. Alegou que uma imitação jocosa em ambiente privado havia sido apresentada fora de contexto. Em [<b>0601866-77.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601866-77.2026.6.00.0000), a relatora negou a suspensão liminar por não identificar ilicitude flagrante nem requisitos para restringir a expressão. A relatora manteve a veiculação por ora, reservando exame aprofundado para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/1af5d17ef1aa24df6b021f629f8ed7e233dd739217ad3b382639180c9b42d335).

### 58. Bloco de 4/9 com recortes de falas de Bolsonaro

Flávio Bolsonaro pediu direito de resposta e suspensão de bloco eleitoral da campanha de Lula que combinava falas de Jair Bolsonaro e vídeo do próprio candidato para associá-lo a comportamentos misóginos. Alegou que uma imitação jocosa em ambiente privado havia sido apresentada fora de contexto. Em [<b>0601868-47.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601868-47.2026.6.00.0000), a relatora negou a suspensão liminar por não identificar ilicitude flagrante nem requisitos para restringir a expressão. A relatora determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame do mérito pelo Plenário. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/51/9918829b5a5bd1ea5db2326b6abddad045d7e09c583860d9dd0ead6de829fb35).

### 59. Inserções de rádio e TV de 5/9 sobre Flávio

Flávio Bolsonaro contestou inserções de rádio e TV da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601871-02.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601871-02.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. A propaganda foi mantida por ora, com exame aprofundado reservado para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/57/bcc3f8c19cb9e0100cc5d20cf93e7146d930bfdbc5620ba58a5a3f803b3d6635).

### 60. Crítica política em inserções de 5/9

Flávio Bolsonaro contestou inserções de rádio e TV da campanha de Lula que mencionavam supostos aliados investigados ou presos, questionavam sua capacidade de combater o crime e o chamavam de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601872-84.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601872-84.2026.6.00.0000), o TSE negou a suspensão liminar por considerar, naquele exame inicial, que a mensagem expressava predominantemente juízos de valor e crítica política, sem requisitos para a medida urgente. A propaganda não foi suspensa por essa decisão, e o mérito ficou para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/52/079a1805400956f0fd4911c76d887a8bdc25833c81102b408adc2c924c134629).

### 61. Pedido de resposta a inserção de rádio de 5/9

Flávio Bolsonaro pediu resposta e suspensão de inserções de rádio da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601876-24.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601876-24.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas e o prosseguimento do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/56/4096e27ffffb91e96b30ec51bf8f7b012e8791de2bf9b6b8408fa0f0f3660477).

### 62. Outra inserção de rádio de 5/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de rádio da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601877-09.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601877-09.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com contraditório e posterior julgamento do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/57/3622136d63c17b8cc76780968e40ccf7f84856011d9825ba1658952736271e43).

### 63. Inserção de TV de 5/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de TV da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601878-91.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601878-91.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/56/ee1ef0c8ad641e083adf2f5e6f4f40bea03a006f8e4c697d74e017f9f0547ac9).

### 64. Outra inserção de TV de 5/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de TV da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601879-76.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601879-76.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, para prosseguimento do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/57/cf3522f7a97abf3215af3ceefeb7a24260b4c56d66d724937fb82a9d678071f9).

### 65. Duas peças de TV de 5/9 questionadas por Flávio

Flávio Bolsonaro pediu resposta a duas peças de TV de Lula: uma combinava falas do pai e vídeo seu para associá-lo à misoginia; a outra o apresentava como vindo de “família preconceituosa” e o ligava a homenagem a policial depois condenado pela morte de Marielle Franco e a Daniel Vorcaro. Em [<b>0601883-16.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601883-16.2026.6.00.0000), a relatora negou a suspensão liminar por não identificar requisitos para restringir a expressão. Determinou a apresentação do texto da resposta, a citação e posterior manifestação da Procuradoria-Geral Eleitoral. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/16/9/3fe808a9aaf89a2858d39943ccf74b32f59f424dcd93394b2434be71421845b2).

### 66. Inserção de TV de 6/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de TV da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601889-23.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601889-23.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com posterior citação e prosseguimento do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/51/6a621e2a95845a9ae027fdc126e8e477d1a0c1b87eef514d6c34b416b35659d6).

### 67. Inserção de rádio de 6/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de rádio da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601890-08.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601890-08.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. A propaganda não foi suspensa, e o pedido de resposta prosseguiu condicionado à apresentação do texto pretendido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/58/2224cb86d045fc9db2f90f8dd739ad4240a9c22a40300465ff2c084c81db3aac).

### 68. Outra inserção de rádio de 6/9 sobre Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de rádio da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601892-75.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601892-75.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, sob pena de extinção, com citação e manifestação da Procuradoria-Geral Eleitoral. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/50/8220c05062582cd0467c5b984cab2aae48fc2057a6691089eed5b23778aa813e).

### 69. Peça de rádio de 5/9 sobre suposto currículo falso

A coligação de Lula contestou inserções de rádio de Flávio que diziam que sua campanha havia inventado um “currículo falso” e sido “condenada pela Justiça”. Alegou que uma liminar fora apresentada como condenação definitiva. As peças também contrapunham Lula, descrito como condenado e preso, a Flávio. Em [<b>0601894-45.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601894-45.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/15/8/a24a62f53ccd1d5910c8f0bd4feef128d8c10a5a0aebb487a6c8054d0c0c6338).

### 70. Peça de rádio de 6/9 sobre suposto currículo falso

A coligação de Lula contestou inserções de rádio de Flávio que diziam que sua campanha havia inventado um “currículo falso” e sido “condenada pela Justiça”. Alegou que uma liminar fora apresentada como condenação definitiva. As peças também contrapunham Lula, descrito como condenado e preso, a Flávio. Em [<b>0601895-30.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601895-30.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/15/3/cc70254faf032345ff1d6897fb343c99320b1353e36764ed884c142afc331b12).

### 71. Peça de rádio de 7/9 sobre suposto currículo falso

A coligação de Lula contestou inserções de rádio de Flávio que diziam que sua campanha havia inventado um “currículo falso” e sido “condenada pela Justiça”. Alegou que uma liminar fora apresentada como condenação definitiva. As peças também contrapunham Lula, descrito como condenado e preso, a Flávio. Em [<b>0601902-22.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601902-22.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame de mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/15/4/bac3dd3d0e1013f47e2b0aa84d03fc0482d055bca36d283fdbd270b1793a6a8a).

### 72. Inserção de rádio de 7/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de rádio da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601908-29.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601908-29.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, para prosseguimento do feito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/44/8e69411be692fd8cd6a337a2a302c98655515b6bce68b4d3111ed1a6cbe5dc13).

### 73. Inserção de TV de 7/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de TV da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601911-81.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601911-81.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com contraditório e posterior exame do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/45/2eff1c2ac4d027a44c3e104d6abbd7f60c125d6b9fbb5112e6048a7ad577ccdd).

### 74. Outra inserção de rádio de 7/9 sobre Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de rádio da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601912-66.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601912-66.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com contraditório, parecer da Procuradoria-Geral Eleitoral e posterior julgamento. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/44/6ea554814a422087da2a999f39145669e87f68dcc9d04505e481307e3fdcb4c1).

### 75. Outra inserção de TV de 7/9 sobre Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de TV da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601913-51.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601913-51.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. A propaganda não foi retirada, e o requerente foi intimado a apresentar o texto da resposta em 24 horas. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/45/1b0c9dbf575fb95e28868ca58101521a8170b58b2a0368d5daa8b0f0d110710e).

### 76. Inserção de TV de 8/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de TV da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601926-50.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601926-50.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta antes da citação dos representados e do prosseguimento do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/45/ed01fe28a79e2008fdb49d962db458530ea978680ffab0d75bc124aa557a304f).

### 77. Inserção de rádio de 8/9 questionada por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserção de rádio da campanha de Lula que mencionava supostos aliados investigados ou presos, questionava sua capacidade de combater o crime e o chamava de “<i>o pior dos Bolsonaros</i>”. Em [<b>0601927-35.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601927-35.2026.6.00.0000), o TSE negou monocraticamente a suspensão por não identificar, no exame inicial, os requisitos para restringir a expressão. Determinou a apresentação do texto da resposta em 24 horas, com citação e posterior exame do mérito pelo colegiado. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/44/1c2518ee577ba032ad63fffa80b704cea5753bad8e59d17b7f013a6ce51a1a54).

### 78. Montagem em inserção de TV de 9/9

Flávio Bolsonaro pediu a suspensão de inserção de TV da campanha de Lula que combinava falas de Jair Bolsonaro e vídeo do próprio candidato para associá-lo a comportamentos misóginos. Alegou que uma imitação jocosa em ambiente privado havia sido apresentada fora de contexto. Em [<b>0601928-20.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601928-20.2026.6.00.0000), a relatora negou a suspensão liminar por não identificar ilicitude flagrante nem requisitos para restringir a expressão. A veiculação foi mantida, sem prejuízo de exame aprofundado no julgamento da representação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/c3a39663907337454e58b7ee99634851124b89b71123c030831c4bbdc8870a4e).

### 79. Outra inserção de rádio de 8/9 sobre Flávio

Flávio Bolsonaro contestou propaganda de rádio de Lula que o associava a repasses do Banco Master e ao pedido de 134 milhões a Daniel Vorcaro para <i>Dark Horse</i>. Impugnou também trecho que acusava os Bolsonaros de abandonar a saúde e não comprar vacinas contra a Covid. Em [<b>0601929-05.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601929-05.2026.6.00.0000), a relatora negou monocraticamente a suspensão por não identificar requisitos para restringir a expressão. A propaganda foi mantida por ora, com determinação de apresentar o texto da resposta em 24 horas para prosseguimento do pedido. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/318290d5124a7c68a1c694c8da93483075574c086f49855d98427770146dcbd0).

### 80. Outra inserção de TV de 8/9 sobre Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de TV da campanha de Lula que o associavam ao Banco Master e afirmavam que fora “flagrado pedindo 134 milhões” a Daniel Vorcaro e recebera repasses milionários. Alegou que os valores se destinavam ao filme <i>Dark Horse</i>, não a ele pessoalmente. Em [<b>0601930-87.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601930-87.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar os requisitos para restringir a expressão naquele exame inicial. Determinou a apresentação do texto da resposta em 24 horas, com contraditório e posterior julgamento do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/50/664937efd98260504da410c2e545cb9ede2e6fdfbc8db713b8a0ef98c20aac02).

### 81. Peça de rádio de 8/9 sobre suposto currículo falso

A coligação de Lula contestou inserções de rádio de Flávio que diziam que sua campanha havia inventado um “currículo falso” e sido “condenada pela Justiça”. Alegou que uma liminar fora apresentada como condenação definitiva. As peças também contrapunham Lula, descrito como condenado e preso, a Flávio. Em [<b>0601937-79.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601937-79.2026.6.00.0000), o TSE negou a suspensão liminar por não identificar requisitos para restringir a expressão naquele exame inicial. O direito de resposta não foi decidido definitivamente, e a autora foi intimada a apresentar o texto em 24 horas, sob pena de extinção. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/15/4/7c648aca4e5c5d3de7a066b288fb6374f7de8da263be7e65aa1d87a377e9165b).

### 82. Inserções de rádio e TV de 9/9 questionadas por Flávio

Flávio Bolsonaro pediu a suspensão de inserções de rádio e TV de Lula que o apresentavam como vindo de “família preconceituosa”, lembravam homenagem a policial depois condenado pela morte de Marielle Franco e o ligavam a Daniel Vorcaro. Alegou descontextualização: a homenagem precedia o crime, e os valores negociados se destinavam a <i>Dark Horse</i>. Em [<b>0601943-86.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601943-86.2026.6.00.0000), a suspensão liminar foi negada por não se identificar ilicitude flagrante ou requisitos para restringir a expressão. O TSE manteve a veiculação por ora, reservando exame aprofundado para depois do contraditório. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/91930267f094197c4f05bfa4e1cdd95ac5d110a4cb099908726b6844befe0dd7).

### 83. Inserções de 9 e 10/9 questionadas por Flávio

Flávio Bolsonaro pediu resposta e suspensão de inserções de rádio e TV de Lula que o apresentavam como vindo de “família preconceituosa”, lembravam homenagem a policial depois condenado pela morte de Marielle Franco e o ligavam a Daniel Vorcaro. Alegou descontextualização: a homenagem precedia o crime, e os valores negociados se destinavam a <i>Dark Horse</i>. Em [<b>0601944-71.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601944-71.2026.6.00.0000), a suspensão liminar foi negada por não se identificar ilicitude flagrante ou requisitos para restringir a expressão. A relatora determinou a apresentação do texto da resposta em 24 horas, sob pena de extinção, com posterior citação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/48ddb11511494a87cf0b9ff952520078ef4c4c83cacc14ef3776cb9de477c0e0).

### 84. Recortes de falas de Bolsonaro em peça de TV de 9/9

Flávio Bolsonaro pediu direito de resposta e suspensão de inserção de TV da campanha de Lula que combinava falas de Jair Bolsonaro e vídeo do próprio candidato para associá-lo a comportamentos misóginos. Alegou que uma imitação jocosa em ambiente privado havia sido apresentada fora de contexto. Em [<b>0601947-26.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601947-26.2026.6.00.0000), a relatora negou a suspensão liminar por não identificar ilicitude flagrante nem requisitos para restringir a expressão. A relatora determinou a apresentação do texto da resposta em 24 horas, com contraditório e posterior julgamento do mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/11/19/14/38/a112709462687871e49570b588aea2f266777b151d232face3a8aa2e4717fdaa).

### 85. Vídeo em várias plataformas — Plenário substitui indeferimento por remoção

A representação [<b>0600950-43.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600950-43.2026.6.00.0000) discutiu um vídeo de ataque chamado “Os rastros da trilha do Master”. Segundo a ação, a peça teria usado IA e recortes sobre o Caso Master, a EBAL, o Credcesta, o INSS e pessoas ligadas ao PT. A decisão inicial manteve o vídeo no ar porque não identificou ilicitude manifesta.

Na sessão virtual de 04 a 08/09, o Plenário mudou essa decisão por maioria. Mandou retirar as publicações indicadas em 24 horas e proibiu a divulgação de versões substancialmente iguais. Também determinou a comunicação a Facebook, TikTok, YouTube e Instagram, com medidas coercitivas em caso de descumprimento. A certidão foi emitida em 09/09. A ordem é cautelar e se limita às publicações apontadas. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/4/15/44/21/d4052b9b84d1bade7c2b97e19f565a480c96101ecfddf60b51e91cdb18359145) [(certidão de julgamento)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/25/13/288f0f99aa8b3d4ef8d3bd8fcff41adf3a380012e6a4cf822a2ba056e04d9e4a).

### 86. Publicações sobre Smartmatic e urnas eletrônicas

A Federação Brasil da Esperança questionou publicações de Eduardo Bolsonaro e outros integrantes do grupo político de Flávio que usavam relatório da CIA sobre eleições venezuelanas para levantar suspeitas sobre as urnas brasileiras. Em [<b>0601303-83.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601303-83.2026.6.00.0000), o relator concedeu parte da liminar para retirar as publicações, proibir novas divulgações e determinar atuação das plataformas contra reproduções iguais ou modificadas.

Na sessão virtual de 04 a 08/09, o TSE confirmou a tutela parcial por maioria, vencidos Floriano de Azevedo Marques e Estela Aranha. A certidão é de 09/09/2026. A medida continua cautelar. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/19/1/14/3eef4b8107be2d7b5b1c4ad571716f1ff6020f129a169ce6ab69594dd9300ea6) [(certidão de julgamento)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/25/48/26241ed77fbe34599c955b261083ae1ccfe66407a12dc784944e050071b532dc).

### 87. Propaganda que aproximava Flávio do caso Banco Master

Flávio Bolsonaro contestou bloco de TV da campanha de Lula que ligava o patrocínio do filme <i>Dark Horse</i> por Daniel Vorcaro ao Banco Master, com a frase “flagrado pela Polícia Federal pedindo 134 milhões”. Em [<b>0601767-10.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601767-10.2026.6.00.0000), o relator negou a liminar por não identificar imputação direta de participação nas fraudes nem falsidade objetiva evidente. O conteúdo foi mantido enquanto o processo seguiu para defesa e parecer da Procuradoria-Geral Eleitoral.

Na sessão virtual de 04 a 08/09, o TSE confirmou a negativa por unanimidade. A certidão foi emitida em 09/09/2026. A decisão é provisória. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/19/1/7/2b367fe332dc27d04cf33364e2df50f57b5889a044edf60e5ad9553e1252534b) [(certidão de julgamento)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/29/12/50b94a3773ca927d392c0e5ca4d9a5631e0d23a9aca0e5df45024c65d2a80b13).

### 88. Pedido de resposta a crítica sobre Flávio Bolsonaro e Banco Master

Flávio Bolsonaro pediu resposta e suspensão de inserção de TV da campanha de Lula que associava o financiamento de <i>Dark Horse</i> ao Banco Master e o dizia “flagrado pela Polícia Federal pedindo 134 milhões”. Em [<b>0601768-92.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601768-92.2026.6.00.0000), o relator negou a liminar. Na sessão virtual de 04 a 08/09, conforme certidão de 09/09, o Plenário referendou a negativa por unanimidade. A peça não foi suspensa por essa medida, que não equivale à rejeição definitiva do direito de resposta. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/19/1/7/a4c886fc967d6c891313f1d11862e00d7f64eae186009489309543c143c0b499) [(certidão de julgamento)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/9/1/26/18/7b9e6abd03c8b6dc5f530b3776aca8fc33182e76bc96c681a8fb8fb461d5b49d).

### 89. Vídeo de convenção com imagem sintética de Bolsonaro — tese sobre deepfake

A Federação Brasil da Esperança pediu em [<b>0601315-97.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000) a retirada de vídeo exibido na convenção do PL com imagem e voz recriadas de Jair Bolsonaro. O Plenário explicou que deepfake envolve conteúdo sintético ou manipulado com aparência realista para criar ou alterar imagem, voz ou manifestação. Para aplicar a proibição eleitoral, o conteúdo também precisa ser propaganda eleitoral.

Por maioria, o Tribunal negou a medida urgente. Entendeu que transmitir a convenção pela internet não transforma, por si só, uma mensagem aos convencionais em propaganda antecipada. A certidão registra essa decisão sobre a tutela. Ela não encerra toda a controvérsia. Fonte — [(certidão de julgamento)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/1/22/26/17/976befd03bfb522f74b25d240f808158818419a60d96ba7363c590c3a2f926df).

### 90. Vídeo que imputava estupro a candidatos da oposição

Flávio Bolsonaro e seu vice, Alfredo Gaspar, contestaram vídeo do PT no X que vinculava Gaspar ao estupro de uma adolescente de 13 anos e perguntava: “Você deixaria sua filha sozinha com o vice de Flávio Bolsonaro?”. Em [<b>0601627-73.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601627-73.2026.6.00.0000), o relator considerou, em exame inicial, que a peça apresentava imputação criminal como verdadeira sem suporte mínimo. Ordenou a remoção da URL pelos representados e pelo X em 24 horas. Negou, por ora, a retirada genérica de reproduções não individualizadas e a cientificação preventiva de outros provedores. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/28/19/7/28/ed5e957c6ac0004f25a099b32966b95f354e93c00bc4b0b8c234f17c9c813756).

### 91. Acusação de lobby de Lula pelo PCC e CV — retirada liminar deferida pelo Plenário

A Federação Brasil da Esperança contestou em [<b>0601015-38.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601015-38.2026.6.00.0000) duas publicações de Flávio Bolsonaro no X. Elas afirmavam que Lula havia feito “lobby” em favor do PCC e do Comando Vermelho durante viagem aos Estados Unidos. O relator negou inicialmente a retirada.

Na sessão virtual de 12 a 14/08, o Plenário mudou parcialmente essa decisão por maioria. Ordenou a remoção das duas publicações em 24 horas, proibiu repetir a imputação sem base factual mínima e mandou avisar a plataforma X. André Mendonça ficou vencido. As outras manifestações questionadas ficaram fora da ordem. A medida é cautelar e não encerra o processo. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/4/15/44/23/b5aa7a695a4fdd6dbd7c3a4c3f4ce58afcbbe283ff116360355735223461ddd4) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/26/18/15/12/11d1357487a1cdead5b3772912df571170b8703f9a860c65783ff07a9f5056f6).

### 92. Vídeo de Flávio que associava Lula ao PCC e CV — remoção parcial em referendo

A Federação Brasil da Esperança impugnou vídeo de Flávio Bolsonaro no X que atribuía pessoalmente a Lula atuação como defensor do PCC e do Comando Vermelho. Em [<b>0601016-23.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601016-23.2026.6.00.0000), a liminar foi inicialmente negada. Na sessão virtual de 12 a 14/08, o Plenário, por maioria, não referendou integralmente a negativa e deferiu parcialmente a tutela. Determinou a remoção da publicação indicada e vedou republicações substancialmente idênticas dessa imputação, mantendo as demais manifestações impugnadas. A medida é cautelar, sem encerrar o mérito. Fontes — [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/24/17/59/20/71c70ea9c630e73023fc2fbdbddbd289e697dd5ca6dc70a1cab269ff86f1ef7f) [(andamento)](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601016-23.2026.6.00.0000).

### 93. Vídeo pago “Estrelas da Investigação” — vedação ao impulsionamento negativo

A Federação Brasil da Esperança impugnou o vídeo pago do PL “Estrelas da Investigação”, que apresentava Deolane Bezerra, músicos e o filho de um chefe do Comando Vermelho como “aliados” do governo Lula e do PT ligados a episódios criminais. Em [<b>0601049-13.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601049-13.2026.6.00.0000), o Plenário referendou por unanimidade tutela parcial contra o impulsionamento. A medida restringiu a ampliação paga da propaganda negativa, distinguindo-a da crítica política veiculada organicamente. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/4/15/44/18/cebe82bcfb458612a825362eb34fb823fe5f8a1c4b8a0a773e9b73b4cae2c9c8) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/19/14/27/18/c28fb2748255b411bf7a6ed90cb8f1fca646a0cce2d25e9fcd71f0251bcdd96f).

### 94. Anúncio pago do PL com conteúdo negativo contra Lula

A Federação Brasil da Esperança questionou o impulsionamento do vídeo do PL “Os Rastros da Trilha do Master”, que associava Lula, o PT e agentes do governo a episódios envolvendo o Banco Master e o INSS. Em [<b>0601048-28.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601048-28.2026.6.00.0000), o relator distinguiu a crítica política orgânica da sua ampliação paga, vedada quando negativa. Ordenou liminarmente a interrupção do anúncio em 24 horas, proibiu novo impulsionamento equivalente e determinou à Meta sua inativação e a preservação dos dados da contratação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/17/17/45/24/bb6628ea185510c0eb76d0a358f7fefbd271ea4cb571c222e75d54f5c2ab10d6).

### 95. Declarações sobre o Pix — negativa liminar referendada

O PL pediu a retirada de falas de Lula e de Dario Durigan que atribuíam à família Bolsonaro atuação contra o Pix. Lula teria afirmado que Flávio pedira a Trump intervenção no sistema brasileiro de pagamentos. Em [<b>0600963-42.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600963-42.2026.6.00.0000), o relator negou a liminar por considerar, inicialmente, as declarações crítica política sem falsidade manifesta ou pedido explícito de não voto. O Plenário referendou a negativa por unanimidade em 25/06. O conteúdo não foi retirado por essa medida, e a representação prosseguiu para contraditório e exame de mérito. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/10/48/58/431a9745c8cfa04ee12ff498f000dffb0d9155f25a8d3d0ac8f7d03da47c976d) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/13/16/32/14/885b323a8ff60a37635f4894078ba1999c124701a6de9c8e593762e526547de7).

### 96. Montagem satírica sobre Lula e crime organizado — remoção negada

A Federação Brasil da Esperança pediu a retirada de três publicações de Flávio Bolsonaro no X sobre falas de Lula a respeito do crime organizado. Uma delas usava montagem audiovisual com a frase “Trump, deixe nossos bandidos em paz”. Em [<b>0600955-65.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600955-65.2026.6.00.0000), André Mendonça negou monocraticamente a liminar em 04/08. Considerou a montagem ostensivamente satírica e não identificou, naquele exame, falsidade manifesta ou descontextualização grave. A suficiência da identificação do uso de IA e a licitude final ficaram para o mérito. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/4/15/44/23/a84196aeeae49ba63853588ec7ae22ca2947e10620361632dec3320eea5fe8fc).

### 97. Vídeo sintético com barcos identificados como facções e PT

A Federação Brasil da Esperança pediu remoção de vídeo divulgado por Flávio Bolsonaro no Instagram, produzido com inteligência artificial e mostrando barcos com referências ao CV, ao PCC e ao PT. Em [<b>0601053-50.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601053-50.2026.6.00.0000), a relatora indeferiu a tutela de urgência por não ver demonstrada, no exame preliminar, falsidade manifesta ou grave descontextualização. O conteúdo permaneceu acessível. A regularidade do uso de IA e da propaganda ficou para decisão posterior. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/4/15/44/17/eec2dcac42ec2bbae9836ba1901c149738b12697df01415c56862ed0ce0704f6).

### 98. Anúncio do PT contra Flávio — vídeo retirado e impulsionamento vedado

O PL impugnou vídeo do PT impulsionado no Facebook que contrapunha falas sobre riquezas minerais e interesses estrangeiros com os rótulos “defensor” e “traidor da pátria”. Segundo a inicial, foram ao menos oito impulsionamentos em abril, com quase dois milhões de impressões. Em [<b>0600689-78.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600689-78.2026.6.00.0000), a relatora mandou retirar o vídeo em 24 horas e impedir nova difusão paga, em tutela parcial. Substituiu o PT pela Federação Brasil da Esperança no polo passivo. O Plenário referendou a medida por unanimidade em 25/06, sem encerrar o mérito. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/33/3/5e95529458658659fb5b5c073096cbdbb8d6556af7aa1aefb9b170dfdfa3ceb3) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/37/869f028aa30d9e9e9e3dcaaaf83736212e922e5908bd52c9edaef1f309e8347e).

### 99. Vídeo do PT sobre Flávio e o Pix — retirada liminar referendada

O PL contestou em [<b>0600690-63.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600690-63.2026.6.00.0000) o vídeo do PT “Será que Flávio Bolsonaro quer acabar com o Pix?”, impulsionado no Facebook. Segundo a inicial, houve ao menos 14 impulsionamentos em abril e mais de três milhões de impressões. A relatora ordenou a retirada do vídeo em 24 horas e proibiu novo impulsionamento de conteúdo idêntico.

Em 25/06, o Plenário confirmou a liminar por maioria. A retirada e a proibição da divulgação paga permaneceram. Floriano de Azevedo Marques divergiu em parte porque permitiria a veiculação sem impulsionamento. O mérito da representação continuou aberto. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/36/56/fef35e5d649106456651fd2bb9a2b34c0b450e0c6c64a6e3fd07a58d24319acd) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/37/f985a29dbfbb483e899994bbcb0bdb4a5aff4225bcd0f033e8b8f1e8807b5156).

### 100. Vídeo “Bolsonarismo, nunca mais” — remoção de anúncio pago

O PL questionou vídeo impulsionado pelo PT no Facebook e no Instagram, com a mensagem “Este ano tem eleição. Bolsonarismo, nunca mais”. Segundo a inicial, a peça teve ao menos 13 impulsionamentos e mais de três milhões de impressões. Em [<b>0600697-55.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600697-55.2026.6.00.0000), a relatora determinou liminarmente a remoção dos vídeos e vedou nova difusão paga de conteúdo idêntico. Retificou o polo passivo para a Federação Brasil da Esperança. O Plenário referendou parcialmente a tutela por unanimidade em 25/06. O mérito não foi concluído. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/36/45/9500367fc750738cdf4842cc6b0196c36f121d14c05e482885ee2c5972ca1e5c) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/40/d6de927fd878c0193cf232c6928b7f49f9b96e3a704869d17a5a140112a8d415).

### 101. Vídeo “As mentiras da família Bolsonaro” — remoção de anúncio pago

O PL contestou vídeo impulsionado pelo PT que associava o aumento do preço dos combustíveis a decisões atribuídas à família Bolsonaro e usava a expressão “Bolsonarismo nunca mais”. Segundo a inicial, houve ao menos 15 impulsionamentos, com mais de 4,5 milhões de impressões. Em [<b>0600698-40.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600698-40.2026.6.00.0000), a relatora ordenou a remoção do vídeo em 24 horas, vedou nova difusão patrocinada e substituiu o PT pela Federação Brasil da Esperança no polo passivo. O Plenário referendou parcialmente a tutela por unanimidade em 25/06. A decisão não encerrou a ação. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/36/31/9efcc32045869ef485227cabb0d90fe921fc6e6d7fc6eb9dced08f2417727935) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/39/371c41968268d9b92946d7dacc22bdf41f5d24f1ab12e7e7352fbec54bf6f413).

### 102. Anúncio do PL que associava Lula ao caso INSS

A Federação Brasil da Esperança questionou o impulsionamento pago, pelo PL, de montagem que associava Lula ao chamado “Careca do INSS”. Na representação [<b>0600781-56.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600781-56.2026.6.00.0000), a relatora considerou, em exame preliminar, irregular usar anúncios pagos para difundir crítica negativa. Como os anúncios já estavam inativos, proibiu nova divulgação impulsionada dos vídeos ou de peças substancialmente idênticas. O Plenário referendou por unanimidade essa tutela parcial em 25/06. Não julgou definitivamente a representação. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/37/24/c7da66c13c52c768e94586e743466dbb126e90722302d7c782580f3cf0451020) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/41/8c5ac9df0f79f74c8e77945791d8c47f62354612553c27734daad0dd46c34a7f).

### 103. Vídeo editado sobre uso da máquina pública — impulsionamento restringido

A Federação Brasil da Esperança contestou vídeo impulsionado pelo PL no Facebook e no Instagram, editado com recursos de inteligência artificial e crítico a Lula por suposto uso da máquina pública para autopromoção eleitoral. Em [<b>0600782-41.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600782-41.2026.6.00.0000), a relatora vedou nova difusão paga do material ou de versões substancialmente iguais. Os anúncios já estavam inativos e não havia URL indicada para remoção. A medida incidiu sobre o impulsionamento. O Plenário referendou a liminar parcial por unanimidade em 25/06, sem encerrar o mérito. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/35/21/e41a1c13b4611f22596e9b1329f52bb9911916acd2cfe065ac3f592927032933) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/8/0/a62ab232bba89f7594583cb93caf6e056ce1b262168c7526fe9f2e03c1eb453c).

### 104. Anúncios sobre educação — proibição de nova difusão paga

A Federação Brasil da Esperança impugnou anúncios pagos do PL que acusavam o governo Lula de não investir em educação, enfraquecer o Fundeb e privilegiar medidas populistas, associando seus eleitores a pessoas “sem conhecimento”. Na representação [<b>0600783-26.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600783-26.2026.6.00.0000), a relatora considerou plausível a irregularidade do impulsionamento de crítica negativa, sem exigir laudo técnico como requisito da petição inicial. Os anúncios estavam inativos. A tutela proibiu novo impulsionamento de vídeos idênticos ou substancialmente semelhantes. O Plenário referendou-a por unanimidade em 25/06. A decisão é cautelar. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/37/36/a14f334333d7f49dc320cb937d30a2c5f1ac47154696db86a15b52f23828ad30) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/59/0e8ac62f7ef66fc9ae26e9fca32fd3b649e8c4a99446deb5b9c792a47ea7cd39).

### 105. Anúncio sobre impostos e Haddad — limite ao impulsionamento

A Federação Brasil da Esperança questionou anúncio pago do PL que retratava Fernando Haddad com barras de ouro e criticava impostos do governo Lula. Em [<b>0600785-93.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600785-93.2026.6.00.0000), a relatora entendeu, em juízo preliminar, que o impulsionamento de crítica negativa ao adversário era vedado. Como os anúncios estavam inativos, determinou a abstenção de nova difusão paga do material ou de conteúdo substancialmente idêntico. O Plenário confirmou por unanimidade a liminar parcial em 25/06. Não se trata de proibição geral da crítica orgânica. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/37/9/7e7fea9d2564a00cfd2dfb551b96048aaef311a74c8ad729aab7a9bf00161a90) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/7/1/15/7/42/5143060af2db62801b0f2bf1864a1a115d21e576bbce032ebbe886f8e6d95fc2).

### 106. Impulsionamento pago de ataque ao adversário — anúncio inativado

A Federação Brasil da Esperança contestou anúncio pago do PL que associava Lula a investigados e sugeria que esses vínculos explicavam sua resistência a classificar facções como terroristas. Também apontou corte de fala que fazia parecer que o Brasil era respeitado “no crime organizado”, e não no seu combate. Em [<b>0600976-41.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600976-41.2026.6.00.0000), o TSE ordenou liminarmente a interrupção do impulsionamento em 24 horas, a inativação do anúncio pela Meta e a preservação dos dados. O Plenário referendou a tutela parcial por unanimidade em 25/06. A restrição atingiu a difusão paga, não toda crítica orgânica. Fontes — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/19/17/5/1/100e14d24d248687257238ce5b47a425f1a1cce91f2f0ffef6f7e38c1cd3ab3f) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/30/14/49/5/c2e84d5d94a2f5f75af036c0efd5a750de0c5e76f2c90a6c86327b52905bbcf2).

### 107. Vídeo manipulado contra Lula — retirada de conteúdo sintético

A Federação Brasil da Esperança impugnou vídeo do PL no Instagram que, segundo a inicial, simulava interações e associava Lula e o PT a Uldurico Junior, ex-deputado preso sob suspeita de ligação com facções criminosas. Em [<b>0600695-85.2026.6.00.0000</b>](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600695-85.2026.6.00.0000), a relatora deferiu liminar monocrática para retirar a publicação em 24 horas e impedir a republicação de material idêntico. A medida atingiu o vídeo indicado, sem resolver definitivamente a representação. Fonte — [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/6/22/11/38/25/888c89a1624cfef98215b700f21c59fe10862106c2139710622e00bddad0201d).

## 6. Outros eixos em torno da disputa

<b>Registros de candidatura.</b> O corpus tem <b>59 atos em 40 processos da classe RCand</b>. Dois exemplos vindos das sessões ajudam a entender as disputas. O TSE manteve por maioria o indeferimento do registro de José Roberto Arruda. Considerou que as condenações por improbidade geravam causas autônomas de inelegibilidade [(andamento)](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600957-40.2026.6.07.0000). No recurso sobre o registro de Antônio Paulo de Oliveira Furlan, houve pedido de vista após voto do relator pelo indeferimento. Não havia decisão final do Plenário naquela sessão [(andamento)](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600162-45.2026.6.03.0000).

Recursos ligados a DRAPs e candidaturas na Bahia mostram a importância da legitimidade partidária e os limites para reexaminar provas [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/18/17/28/40/d9b71c95b8712bcccf0a23f6b3840fe30f3cc4e966d0dfaed6bed69251231a82) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/18/45/11/b2afdccb51449c1822fb76bb70200362189105d726c4870cc1cd53350ffd6925).

No caso de Pablo Marçal, o Plenário primeiro restringiu, de forma provisória, o uso de recursos públicos e a participação em propaganda e debates. Depois, em acórdão de 12/09, indeferiu o registro porque a filiação partidária não ocorreu no prazo e havia inelegibilidade. Também confirmou as proibições de campanha, determinou a retirada do nome da urna e permitiu ao partido substituir o candidato. Esse segundo julgamento decidiu o registro e teve alcance maior que a medida provisória. Fontes — [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/27/20/15/23/041282d5066e75c5a71560d33907b2b303252f606623e1198a0605a325bb425f) [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/18/38/33/40a574e420d2776ff01a93f7a8043f76b51b9851675d9bee4115dfa788b4ed43).

<b>Financiamento e acesso à mídia.</b> Em 25/08, o Plenário aprovou o plano de mídia da propaganda gratuita presidencial. A resolução definiu a ordem de veiculação e a divisão do tempo entre partidos e coligações. Ela aparece aqui como contexto [(resolução)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/26/18/56/10/1e6b8315b28b48682aa4ddeaa986135d5d07b403a1df5e84939cd4db242901dd).

A base de dados reúne <b>92 atos em 82 petições cíveis</b>. Esses números abrangem todos os assuntos dessa classe processual, e não apenas financiamento. Em uma delas, o TSE afirmou que cada diretório nacional de partido federado deve pedir seus recursos separadamente, sem um pedido coletivo da federação [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/19/17/32/55/aebea94925af5b41b6f480293d0dd1191f65927f9bc99dcffbb19024af827145). Em outra, manteve os critérios administrativos usados para calcular a representação parlamentar, o tempo de propaganda gratuita e a participação em debates, considerados os marcos de retotalização aplicáveis [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/14/21/37/13/d94e939786158d6b4f43c02029f49ff2b9ceb36c0c630aa31901b726b4ef9974).

<b>Publicidade institucional e organização do pleito.</b> O TSE negou autorização para uma campanha federal de prevenção a crimes contra celulares. Considerou que não foi demonstrada necessidade pública grave e urgente. O programa e seus serviços continuaram em funcionamento [(decisão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/9/4/9/9/28/c98961a104fa4f35e166156b1203a4601e346c295990e54a8f9f959be7122399).

O corpus tem <b>53 atos em 38 processos da classe Processo Administrativo (PA)</b>. O TSE, por exemplo, ajustou o calendário eleitoral em pleno ano eleitoral [(resolução)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/8/5/19/23/27/eef185c6581d1db95e2a6472285ec6aa8c75ce8be95a8b88bc44360a0968090a). Em outro julgamento, afastou a aplicação imediata, naquela eleição, de restrições ao voto de presos provisórios criadas por lei nova, em razão da regra da anualidade [(acórdão)](https://consultaunificadapje.tse.jus.br/consulta-publica-unificada/documento?extensaoArquivo=text/html&path=tse/2026/5/28/10/33/42/0da2f8ce27287543cb8b0d529a8c9ef5582e45613c9cff21b5cb72cc4bee17c0).

## 7. Conclusão / outros tópicos (texto livre)

Bruno
</content>
</page>
