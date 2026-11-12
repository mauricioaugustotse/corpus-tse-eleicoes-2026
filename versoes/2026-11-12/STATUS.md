# Corte de 31/10/2026 — atualização em preparação

Extração realizada em 12/11/2026, com cinco arquivos oficiais gerados em 11/11/2026. O corte inclusivo de 31/10/2026 é aplicado à data do ato; a fonte contém atos posteriores, que foram excluídos.

## Etapa estatística concluída

- 2.606 atos (1.893 decisões e 713 acórdãos), em 1.841 processos distintos.
- 1.669 atos de outubro; 937 atos até setembro na nova extração. A versão histórica possui 933 e permanece preservada.
- 1.005 processos no filtro de comunicação: 671 apenas de propaganda, 326 apenas de direito de resposta e 8 em ambos os grupos. A união evita dupla contagem.
- 591 processos-alvo na triagem: 131 dos alvos anteriores encontrados no extrato e 460 novos candidatos. São candidatos, não resultados classificados.
- O processo suplementar 0601315-97.2026.6.00.0000 e quaisquer alvos antigos ausentes precisam de verificação documental própria.

## Pendências que impedem a publicação integral no Notion

### Retomada da coleta coordenada

O acesso foi validado em duas consultas novas, sem cache, com dez peças conferidas pelo motor `pje_links_motor.py`. A exportação manual deixou de ser requisito para prosseguir. O coletor `coletar_pecas.py` reutiliza esse motor, sua trava global e intervalo mínimo de 65 segundos. Ele cobre 1.015 CNJs: a união dos candidatos a confronto, dos alvos anteriores e dos processos com acórdão. O diretório local `coleta_documental/` contém o checkpoint e o progresso; a coleta não atribui resultados jurídicos.

```powershell
python coletar_pecas.py --motor-dir C:/Users/mauri/ProjetoConversor
```

O caminho indica a instalação local do motor e deve ser adaptado em outra máquina. O checkpoint é atualizado por peça e processo, com escrita atômica e preservação de documentos posteriores já salvos em processos incompletos. Uma trava impede coletores duplicados. A retomada verifica os hashes e a existência dos textos antes de reaproveitar arquivos. Peças do inventário parcial anterior também são reutilizadas por URL e hash; URLs repetidas são deduplicadas.

Para pausar e retomar, use `python controle_coleta.py painel` ou o atalho **Coleta TSE - outubro 2026** criado na Área de Trabalho. Clique em **Pausar** e aguarde **Parada** antes de desligar. A pausa aguarda a operação corrente (uma consulta pode levar até 90 segundos). Depois de ligar o computador, abra o painel e clique em **Retomar**. Fechar o painel não encerra a coleta; a retomada após reinício do computador é manual. Também existem os comandos `python controle_coleta.py pausar`, `retomar` e `status`. Eles não interrompem outros programas.

As consultas compartilham o acesso com outros programas locais. O intervalo de 65 segundos foi preservado; reutilizar arquivos economiza downloads, mas não elimina a necessidade de consultar inventários atualizados. O relatório abaixo preserva o diagnóstico anterior e deve ser lido como histórico da preparação.

O acesso à página de consulta do PJe apresentou verificação humana; o portal de jurisprudência respondeu HTTP 403. Links diretos de peças anteriores foram acessíveis, mas não fornecem o inventário das novas peças. Nenhuma tentativa de contornar a verificação foi realizada.

O atalho indicado pelo usuário abre `pje_links_gui.py`, cujo motor utiliza a listagem documental da Consulta Unificada e mantém um cache local. Uma chamada normal à listagem foi encerrada pelo servidor com WinError 10054. O cache continha links para 39 dos processos-alvo: foram recuperadas 78 das 81 peças públicas distintas selecionadas; três retornaram erro. O inventário com URLs, origem temporal do cache, hashes e falhas está em `inventario_documental_parcial.json`; as peças estão em `pecas_cache/`. O cache é parcial e não comprova que não houve atos posteriores. Nenhum resultado jurídico foi inferido automaticamente.

É necessário obter uma exportação oficial do SJUR/PJe pelos meios normais de acesso, cobrindo os atos selecionados e as peças até o corte, inclusive certidões. A triagem automática está em `triagem_confrontos.csv` e seus atos em `atos_alvos_curadoria.csv`. O inventário de acórdãos está em `acordaos_para_conferencia.csv`. A triagem reaproveita os identificadores nominais das campanhas da versão anterior e também precisa de revisão de eventuais novos representantes formais.

Faltam a curadoria dos novos casos e dos desdobramentos dos antigos; os relatos; a apuração das votações; a atualização dos gráficos interativos e da versão estática; e a revisão final das seções 1 a 6. Os HTMLs desta pasta são as alternativas SVG do coletor, não substitutos dos anexos interativos do Notion. A cópia local dos anexos atuais foi preservada para essa etapa.

Não foram transportadas taxas de atendimento ou de votação de setembro para outubro. A página do Notion e a seção 7 permanecem preservadas. Este pacote é uma preparação verificável, não uma atualização editorial concluída.

## Reprodução

Execute nesta pasta:

```powershell
python verificar_atualizacao.py
python tse_corpus_eleicoes_2026.py --saida . --offline --data-fim 2026-10-31
python verificar_atualizacao.py
python -m unittest discover -s tests -v
```

O verificador confere os cinco hashes oficiais, corte, unicidade, somas, triagem, exclusão de novembro e os arquivos do manifesto. As diferenças de assinaturas registradas em `diferencas.json` não identificam, sozinhas, acréscimos ou remoções documentais: CNJ/data/tipo/autor pode não ser uma chave única, e SQ_DECISAO muda entre extrações.
