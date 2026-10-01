# Votações e revisão de liminares no TSE

Análise documental do mesmo corpus, com corte em **30/09/2026**. Não acrescenta atos aos 933 registros nem processos aos 751 CNJs do extrato oficial. Os dados estatísticos e os cinco ZIPs oficiais estão preservados em `versoes/2026-10-01`.

## Resultados e denominadores

| Universo | Resultado |
| --- | --- |
| 200 registros de acórdão, em 198 processos | 174 unânimes; 15 com divergência; 11 com votação não apurada |
| 107 confrontos presidenciais já incluídos no estudo | 22 liminares mantidas; 4 modificadas; 1 tutela decidida diretamente pelo colegiado; 76 liminares sem revisão colegiada comprovada; 4 decisões individuais de mérito |
| 26 reexames colegiados de liminares nesses confrontos | 22 manutenções (84,6%) e 4 modificações (15,4%) |
| 27 julgamentos colegiados nesses confrontos | 19 unânimes e 8 com divergência |

Os 11 acórdãos sem votação apurada representam **5,5% dos 200 registros**. Permanecem no denominador do gráfico geral, identificados separadamente. Entre os 189 com votação identificada, 174/189 = 92,1% foram unânimes; essa proporção não é extrapolada aos 200.

## Abra as fontes

- [Acórdãos: CSV](acordaos.csv) e [JSON](acordaos.json): uma linha por `CHAVE_ATO`, com CNJ, sequencial do extrato, data do ato, votação, ministros vencidos, transcrição do extrato e endereço oficial.
- [Confrontos: CSV](liminares_confrontos.csv) e [JSON](liminares_confrontos.json): exatamente os 107 CNJs já classificados no estudo, com situação da medida e fonte documental própria.
- [Extratos do SJUR](extratos_sjur.json): 190 registros das exportações oficiais em CSV, relativos aos 162 processos usados como fonte SJUR, incluindo variantes do cadastro para permitir a conferência.
- [Peças do PJe](fontes_pje): cópias dos documentos oficiais utilizados, com SHA-256 registrado nas planilhas.
- [Resumo calculado](resumo.json) e [gráficos](graficos): os HTMLs conservam a apresentação do Notion e carregam Chart.js pela internet; os SVGs oferecem uma apresentação estática para consulta sem conexão, impressão e reutilização.
- [Pendências de votação](pendencias_votacao.csv): os 11 atos ainda sem proclamação localizada, identificados nominalmente.

Os links ao SJUR foram construídos com tribunal, número, classe e data de julgamento do próprio registro exportado. **163 votações usam os extratos das exportações oficiais preservadas e 26 usam o acórdão acessível no PJe**. A fonte documental da primeira categoria é o CSV exportado: o serviço de download do SJUR informou indisponibilidade durante o período eleitoral na conferência dos links. A consulta de documentos por CNJ no PJe também encerrou conexões durante a busca das lacunas; o acesso direto às peças identificadas permaneceu disponível. Nenhum resultado foi atribuído aos 11 acórdãos sem fonte de votação localizada.

## Gráficos HTML

Os cinco arquivos reproduzem os painéis publicados no Notion:

- [Votação no corpus e nos confrontos presidenciais](graficos/07_votacao.html).
- [Situação documentada nos 107 processos](graficos/08_liminares.html).
- [Desfecho dos 26 reexames de liminares](graficos/08b_reexames_liminares.html).
- [Ministros com votos vencidos no corpus](graficos/09_ministros_vencidos.html).
- [Ministros com votos vencidos nos confrontos presidenciais](graficos/09b_ministros_vencidos_confrontos.html).

Baixe o HTML e abra-o no navegador, com conexão à internet para carregar Chart.js. Os arquivos conservam os títulos, cores, dados e controles da página do estudo.

## Coleta e programação

A coleta utilizou Python e Playwright para operar a interface pública do [SJUR](https://jurisprudencia.tse.jus.br/): pesquisar por tipo de decisão e intervalo de datas de julgamento, percorrer as páginas de resultados e salvar a saída oficial de **Exportar → CSV**. As exportações conservam os campos de identificação, relatores, proclamação (`textoDecisao`) e ementa (`textoEmenta`). Não é necessário automatizar o navegador para reproduzir a seleção; os mesmos arquivos podem ser exportados manualmente.

O tratamento em Python lê os CSVs, normaliza o CNJ para 20 dígitos, seleciona acórdãos do TSE e cruza os números com o corpus. [extrair_sjur.py](extrair_sjur.py) disponibiliza essa seleção sem dependências externas e permite comparar outra exportação com os extratos preservados. O [guia técnico](../../REPRODUCAO.md#reproduzir-a-apuração-das-votações) apresenta os comandos, os campos e as diferenças entre selecionar documentos e classificar juridicamente os julgamentos.

## Como as unidades foram conciliadas

O arquivo estatístico usa a data do ato no sistema; o SJUR usa a data do julgamento. Não se exige igualdade artificial entre essas datas. A associação usa o CNJ, a sequência de atos e o conteúdo do extrato. Nos dois processos com mais de um acórdão no corpus, as etapas são separadas. Variantes do SJUR com datas ou pontuação diferentes para o mesmo resultado não geram novos atos: cada `CHAVE_ATO` continua contando uma vez. As variantes de data permanecem indicadas na planilha. Onde há peça PJe, a identidade do CNJ no cabeçalho, o tipo documental e a data do caminho da peça foram conferidos.

O campo `extrato` transcreve a proclamação do julgamento, não uma ementa de precedente citado dentro do voto. A identificação dos ministros vencidos inclui a resolução do nome do relator quando a proclamação registra apenas “vencido o relator”. A contagem é de **uma ocorrência por ministro por julgamento**, inclusive quando vencido apenas em parte. Um voto divergente que se torna vencedor não é contado como voto vencido. Vários ministros podem ficar vencidos no mesmo julgamento; a soma das ocorrências não é o número de julgamentos.

O indicador de votos vencidos abrange os julgamentos com divergência identificados, e não todos os julgamentos da carreira dos ministros ou todas as sessões do TSE. Os denominadores dos dois recortes são distintos. O ministro Ricardo Villas Bôas Cueva, por exemplo, figura como vencido no processo suplementar 0601315-97, incluído nos confrontos, mas ausente dos 200 registros de acórdão do corpus.

## O que significa manter, modificar ou não localizar revisão

**Manutenção** inclui referendo de liminar concedida, parcialmente concedida ou negada. “Referendou a liminar parcialmente deferida” significa manutenção do que havia sido decidido, salvo mudança expressa do dispositivo. Não é confundido com “referendou em parte a decisão”, que pode modificar a ordem. No processo 0600690-63, a manutenção ocorreu por maioria, com Floriano de Azevedo Marques vencido parcialmente.

**Modificação** compreende alteração total ou parcial do efeito da decisão individual. Nos quatro confrontos classificados assim — 0600950-43, 0600973-86, 0601015-38 e 0601016-23 — o colegiado alterou negativas anteriores de tutela e determinou remoção de conteúdo. A mudança permanece cautelar; não é convertida em julgamento final da representação.

**Tutela decidida diretamente pelo colegiado** identifica o processo 0601315-97, cuja certidão registra o indeferimento do pedido de urgência e a fixação de teses. Não foi contado como confirmação de uma liminar individual. A votação da tutela foi majoritária; a certidão permite distinguir os votos nas questões decididas.

**Sem revisão colegiada comprovada** é uma lacuna documental delimitada: há peça individual sobre liminar nos 76 processos, mas não foi localizado pronunciamento colegiado correspondente nas fontes examinadas até o corte. Não é prova de que o processo estava parado nem de que todos os pedidos ainda aguardavam julgamento. A existência de uma liminar, a necessidade de seu referendo e a pendência do mérito são questões diferentes.

As **quatro decisões individuais de mérito** são 0601014-53, 0601773-17, 0601817-36 e 0602025-20. No terceiro caso, a procedência parcial do direito de resposta ainda exige decisão integrativa sobre o texto e as condições de divulgação. Esse grupo não é contado como liminares pendentes de referendo. Não se infere trânsito em julgado de nenhuma dessas categorias.

Cinco julgamentos do recorte presidencial possuem comprovação por certidão na documentação utilizada: 0600950-43, 0601303-83, 0601315-97, 0601767-10 e 0601768-92. São usados para classificar o efeito sobre as medidas e a votação no recorte dos 107, sem criar linhas de acórdão no extrato estatístico. A certidão não é rotulada como inteiro teor de acórdão.

## Reprodução

Na raiz do repositório, execute:

```bash
python analises/colegialidade/reproduzir.py
```

O comando usa apenas a biblioteca padrão para conferir identidades, hashes das peças e equivalência entre CSV e JSON, e recalcular `resumo.json`. A curadoria jurídica é explícita nas planilhas: o programa não decide mérito com base em palavras soltas da ementa.

Para refazer os gráficos estáticos em SVG, instale a versão de Matplotlib indicada em `requirements-graficos.txt` e execute:

```bash
python -m pip install -r analises/colegialidade/requirements-graficos.txt
python analises/colegialidade/reproduzir.py --graficos
```

Os HTMLs conservam os gráficos publicados no Notion e não são sobrescritos por `--graficos`. O manifesto desta pasta é independente do manifesto do corpus estatístico.
