# Revisão documental — novos alvos, lote B

O lote contém os 230 últimos CNJs, em ordem crescente, dos 460 novos candidatos da triagem, excluídos os 132 alvos históricos. Foram examinados contexto, ementas e dispositivos pertinentes das peças oficiais coletadas. Casos de reforma, ordem parcial, perda de objeto, duplicidade, suspensão de julgamento e polos processuais exigiram leitura adicional. Os resultados são anotações jurídicas manuais; os scripts apenas materializam as anotações e associam arquivos, URLs e hashes.

## Resultado

- 230 alvos examinados: 141 comparáveis, dos quais 74 com medida atendida total ou parcialmente e 67 sem atendimento na etapa documentada.
- 89 exclusões, sempre com resultado binário vazio. Incluem extinções sem mérito após o pleito, tutela postergada, duplicidade, publicação integralmente indisponível e providências apenas abstratas ou instrutórias.
- Cada entrada de `curadoria_novos_b.json` possui URL da peça de referência, arquivo, SHA-256, testemunho do dispositivo e inventário datado. Todos os 230 hashes de referência foram conferidos com os arquivos locais.
- As 141 sinopses comparáveis foram redigidas com objeto, providência concreta, fundamento e estágio. Há texto específico para os conjuntos de conteúdos repetidos; o CNJ continua sendo a unidade estatística. A numeração e a ordenação finais dos relatos pertencem à integração editorial.

## Controles relevantes

1. **Extinção posterior:** quando existe tutela anterior materialmente examinada e depois extinção do pedido de resposta após o segundo turno, conserva-se o último resultado comunicacional e registra-se o encerramento separado. A extinção, sozinha, não vira improcedência.
2. **Duplicidade entre Rp e DR:** resultado obtido em outra representação não é transplantado para o DR cujo pedido cautelar foi considerado prejudicado. Exemplos: DRs 0602972-74, 0603075-81, 0603113-93 e 0603334-76.
3. **Anúncio/publicação indisponível:** os dez casos marcados como integralmente inativos ficam fora do denominador quando a comunicação não recebe ordem material autônoma, embora a pretensão sancionatória possa continuar. A etiqueta administrativa de indeferimento não resolve a comparabilidade.
4. **Polos formais:** 0602823-78 fica fora porque a ilegitimidade passiva de Flávio foi expressamente reconhecida e a remoção atingiu o terceiro Pablo Marçal. Em 0603123-40, a chapa de Flávio permanece investigada e a tutela restringe comunicações individualizadas dos demais investigados; isso não basta para excluir a ação. O critério exige campanhas em polos formais opostos e decisão de comunicação, sem exigir que o candidato seja pessoalmente o único destinatário da ordem.
5. **Fora de Rp/DR:** 0603256-82 é mandado de segurança com a coligação de Lula como impetrante e Flávio como litisconsorte passivo formal; a liminar protege o funcionamento do canal Exército do Lula. O resultado é parcial e cautelar. 0603321-77, sobre inclusão de pedidos de resposta em pauta e depois encerrado por perda de objeto, permanece fora.
6. **Reforma:** 0602851-46, 0602945-91, 0602953-68 e 0602954-53 passam a negativos porque a tutela concessiva não foi mantida. 0602890-43 é positivo porque o Plenário substituiu a negativa por ordem de remoção.
7. **Datas:** a referência mantém a data do registro da peça. Quando o corpo do acórdão fornece data distinta de julgamento, ambas são registradas; a extração em novembro não é tratada como acontecimento em outubro. Nenhuma referência utilizada ultrapassa 31/10/2026.

## Arquivos e reprodução

Execute `python revisar_novos_b.py` e depois `python enriquecer_novos_b.py` para produzir o lote com as sinopses editoriais. O segundo comando é necessário para preservar as narrativas específicas. `python situacoes_curadoria.py` produz os arquivos de situação das medidas dos históricos e do lote B.

Os arquivos históricos de setembro, o checkpoint da coleta e a página do Notion não foram alterados por esta revisão. A integração deve conservar os motivos de exclusão e os limites documentais, além de verificar a correspondência entre resultados, relatos e gráficos.
