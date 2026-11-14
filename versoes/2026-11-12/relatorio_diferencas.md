# Diferenças entre os cortes de setembro e outubro de 2026

Esta versão foi extraída em **12/11/2026**, de cinco arquivos gerados em **11/11/2026**, e aplica o corte inclusivo de **31/10/2026**. A consulta documental terminou em **14/11/2026**. O [pacote histórico](../2026-10-01/README.md), dos arquivos gerados em 1º/10, mantém integralmente seu corte de 30/09.

## Contagens e revisão da fonte

| Indicador | Versão histórica, até 30/09 | Nova versão, até 31/10 |
| --- | ---: | ---: |
| Atos do extrato | 933 | 2.606 |
| Processos com ato selecionado | 751 | 1.841 |
| Processos no filtro de comunicação | 286 | 1.005 |
| Confrontos comparáveis | 107 | 432 |
| Acórdãos do corpus | 200 | 713 |

A diferença de **1.673 atos** não corresponde apenas a outubro. A nova extração reúne **937 atos até setembro**, quatro a mais que os 933 históricos, e **1.669 atos de outubro**: `937 + 1.669 = 2.606`. Essa separação explicita a revisão retroativa do cadastro.

O diagnóstico em [diferencas.json](diferencas.json) registra 27 assinaturas acrescidas e 23 removidas até setembro, usando CNJ, data, tipo e autor. Essas assinaturas não são identificadores documentais únicos; não demonstram, isoladamente, 27 decisões novas ou 23 eliminadas. `SQ_DECISAO` pode mudar entre extrações. Conclusões sobre peças específicas exigem leitura.

## Curadoria consolidada

A triagem inicial do novo corpus encontrou 591 alvos, incluindo 131 antigos e 460 novos. A consulta dos polos da base integral, junto aos alvos históricos e à documentação suplementar, ampliou o conjunto a **872 candidatos**. As **1.295 consultas concluídas** também abrangem processos relevantes para a votação dos acórdãos; esse total não é o denominador dos confrontos.

O resultado é **432 comparáveis, 201 lacunas documentais e 239 demais exclusões**. Os comparáveis são **427 CNJs do corpus e cinco suplementares**, sem acréscimo artificial às contagens estatísticas. Nos 201 casos com lacuna, não foi localizada peça decisória elegível até o corte após a consulta. Eles não aguardam leitura humana nem demonstram ausência de atos.

As taxas atuais são **121/218 (55,5%)** para a campanha de Lula e **69/214 (32,2%)** para a de Flávio Bolsonaro. Seus denominadores diferem dos de setembro e refletem as medidas documentadas até o novo corte. A mudança dos percentuais não demonstra, por si, alteração de orientação política do tribunal.

## Votação, fontes e apresentação

Os 713 acórdãos apresentam 623 votações unânimes, 89 divergentes e uma não apurada por vínculo documental insuficiente. O recorte presidencial tem 296 julgamentos em 282 processos, sendo 238 unânimes e 58 divergentes. Julgamentos não se confundem com os 432 processos comparáveis nem com ocorrências de ministros vencidos.

O inventário preserva **2.795 entradas por URL distinta em 14 ZIPs**. Há onze gráficos no padrão da página e 432 relatos. A preparação registrou 34 testes aprovados. A edição das seções 1 a 6 conserva integralmente a seção 7.

As referências do fechamento são [resumo.json](resumo.json), [campanha_resumo.json](campanha_resumo.json), [apuracao_colegialidade_resumo.json](apuracao_colegialidade_resumo.json) e [inventario_documental.json](inventario_documental.json). Os campos de triagem e situação em `diferencas.json` descrevem o diagnóstico inicial; não substituem a curadoria consolidada.
