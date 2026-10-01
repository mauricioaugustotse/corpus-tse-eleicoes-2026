#!/usr/bin/env python3
"""Monta o relatório e confere seus denominadores a partir do corpus congelado.

Os relatos jurídicos são curadoria documentada em relatos.csv; o programa não
infere mérito de rótulos processuais. Só usa a biblioteca padrão do Python.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def ler_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def percentual(n: int, total: int) -> str:
    return f"{100 * n / total:.1f}%".replace(".", ",") if total else "—"


def data_br(iso: str) -> str:
    return "/".join(reversed(iso.split("-")))


def tabela(cabecalho: list[str], linhas: list[list[str]]) -> str:
    def linha(vals: list[str]) -> str:
        return "<tr>\n" + "\n".join(f"<td>{v}</td>" for v in vals) + "\n</tr>"
    return '<table fit-page-width="true" header-row="true">\n' + "\n".join(
        linha(v) for v in [cabecalho, *linhas]) + "\n</table>"


def montar(corpus: Path, secao6: str, anexos: dict | None = None) -> tuple[str, dict]:
    resumo = json.loads((corpus / "resumo.json").read_text(encoding="utf-8"))
    atos = ler_csv(corpus / "atos.csv")
    processos = ler_csv(corpus / "processos.csv")
    confrontos = ler_csv(corpus / "confrontos.csv")
    for r in confrontos:
        r["atendido"] = r["atendido"].replace("não", "nao")
    relatos = ler_csv(corpus / "relatos.csv")
    campanha = json.loads((corpus / "campanha_resumo.json").read_text(encoding="utf-8"))
    assert not campanha.get("resultados_provisorios_por_acordao_posterior"), "Há resultado incluído sem conferência de acórdão posterior"
    pendentes = campanha.get("triagem_provisoria_sem_inteiro_teor", [])
    incluidos = [r for r in confrontos if r["incluir_comparativo"].lower() in {"sim", "1", "true"}]
    assert all(r["atendido"] in {"sim", "nao"} for r in incluidos), "Resultado comparável ausente"
    cnjs = {r["cnj"] for r in incluidos}
    cnjs_relatos = {r["cnj"] for r in relatos}
    assert len(cnjs) == len(incluidos), "CNJ duplicado no comparativo"
    assert len(cnjs_relatos) == len(relatos), "CNJ duplicado nos relatos"
    assert cnjs == cnjs_relatos, f"Relatos/comparativo diferentes: {cnjs ^ cnjs_relatos}"
    assert len(atos) == resumo["total_atos"]
    assert len(processos) == resumo["total_processos"]
    assert len({r["CHAVE_ATO"] for r in atos}) == len(atos)
    assert {r["NR_PROCESSO"] for r in atos} == {r["NR_PROCESSO"] for r in processos}
    n, p, c = len(atos), len(processos), len(incluidos)
    fim, inicio = resumo["fim_decisao"], resumo["inicio_decisao"]
    tipos = Counter(r["DS_TIPO_DECISAO"] for r in atos)
    classes = Counter(r["PROCESSO_SG_CLASSE"] for r in atos)
    classes_p = Counter(r["SG_CLASSE"] for r in processos)
    autores = Counter(r["NM_AUTOR_DECISAO"] for r in atos)
    por_cnj = {r["NR_PROCESSO"]: r for r in processos}
    tematicos = {r["NR_PROCESSO"] for r in processos if r["FL_RECORTE_COMUNICACAO"] == "1"}
    atos_tema = sum(r["NR_PROCESSO"] in tematicos for r in atos)
    prop = sum(r["FL_PROPAGANDA_OFICIAL"] == "1" for r in processos)
    dr = sum(r["FL_DIREITO_RESPOSTA"] == "1" for r in processos)
    ambos = sum(r["FL_PROPAGANDA_OFICIAL"] == r["FL_DIREITO_RESPOSTA"] == "1" for r in processos)
    no_corpus = cnjs & por_cnj.keys()
    no_tema = cnjs & tematicos
    fora_tema = no_corpus - tematicos
    suplemento = cnjs - por_cnj.keys()
    cnjs_com_acordao = {r["NR_PROCESSO"] for r in atos if r["DS_TIPO_DECISAO"] == "Acórdão"}
    colegiados_fora_zip = sorted(r["cnj"] for r in incluidos
        if any(tipo in r["tipo_peca_oficial"].lower() for tipo in ("acórdão", "certidão"))
        and r["cnj"] not in cnjs_com_acordao)
    grupos = {}
    for lado in ("Lula", "Flávio"):
        itens = [r for r in incluidos if r["campanha_autora"] == lado]
        atendidos = sum(r["atendido"] == "sim" for r in itens)
        grupos[lado] = {"total": len(itens), "atendidos": atendidos, "nao_atendidos": len(itens) - atendidos}
    assert sum(g["total"] for g in grupos.values()) == c, "Campanha autora não reconhecida"
    anexos = anexos or {}
    def grafico(nome: str) -> str:
        src = anexos.get("graficos", {}).get(nome)
        return f'<embed src="{src}"></embed>' if src else f'[Gráfico — {nome}](graficos/{nome}.html)'
    arquivos = anexos.get("arquivos", {})
    dados = "\n".join(f'<file src="{src}">{nome}</file>' for nome, src in arquivos.items())
    if not dados:
        dados = "[Atos](atos.csv) · [Processos](processos.csv) · [Confrontos](confrontos.csv) · [Relatos](relatos.csv) · [Dicionário](dicionario.md)"
    source = "[Processual – 2026 do TSE](https://dadosabertos.tse.jus.br/id/dataset/processual-2026)"
    period = f'<mention-date start="{inicio}" end="{fim}"/>' if anexos else f"{data_br(inicio)} a {data_br(fim)}"
    maiores_classes = classes.most_common(5)
    lista_classes = "\n".join(f'- **{k}:** {v} atos ({percentual(v, n)}).' for k, v in maiores_classes)
    resto = n - sum(v for _, v in maiores_classes)
    lista_classes += f'\n- **Demais classes:** {resto} atos ({percentual(resto, n)}).'
    top_autores = autores.most_common(3)
    texto_autores = ", ".join(f"{nome.title()} ({q})" for nome, q in top_autores)
    mes_max, qtd_max = max(resumo["atos_por_mes"].items(), key=lambda x: x[1])
    ano_anterior = sum(r["DT_DECISAO_ISO"].startswith("2025-") for r in atos)
    l, f = grupos["Lula"], grupos["Flávio"]
    favor_lula = l["atendidos"] + f["nao_atendidos"]
    favor_flavio = f["atendidos"] + l["nao_atendidos"]
    quadro = tabela(["Campanha autora", "Processos", "Atendido, total ou parcialmente", "Não atendido", "Taxa de atendimento"], [
        ["Lula e representantes formais", str(l["total"]), str(l["atendidos"]), str(l["nao_atendidos"]), percentual(l["atendidos"], l["total"])],
        ["Flávio Bolsonaro e representantes formais", str(f["total"]), str(f["atendidos"]), str(f["nao_atendidos"]), percentual(f["atendidos"], f["total"])],
    ])
    quadro_recortes = tabela(["Recorte", "Unidade", "Quantidade"], [
        ["Decisão ou Acórdão no extrato oficial do TSE", "Ato identificado no arquivo", str(n)],
        ["Processos com ao menos um desses atos", "CNJ único", str(p)],
        ["Assunto Propaganda Eleitoral ou classe Direito de Resposta", "CNJ único do corpus", str(len(tematicos))],
        ["Confrontos presidenciais com resultado comparável", "CNJ único, com exame documental", f"{c} ({len(no_corpus)} no corpus e {len(suplemento)} em suplemento documental)"],
    ])
    lista_grupos = []
    for lado in ("Lula", "Flávio"):
        for outcome, label in (("sim", "atendido"), ("nao", "não atendido")):
            itens = sorted([r for r in incluidos if r["campanha_autora"] == lado and r["atendido"] == outcome], key=lambda r: r["cnj"])
            links = ", ".join(f'[{r["cnj"].split(".2026")[0]}]({r["url_andamento"]})' for r in itens)
            lista_grupos.append(f"\t- **{lado}: {label} ({len(itens)}):** {links}.")
    bloco_lista = '<details>\n<summary>Processos classificados — andamento no PJe</summary>\n' + "\n".join(lista_grupos) + '\n</details>'
    fora_links = ", ".join(f'[{x.split(".2026")[0]}](https://consultaunificadapje.tse.jus.br/#/public/resultado/{x})' for x in sorted(fora_tema))
    pendentes_30set = campanha.get("pendentes_30set", [])
    texto_pendencias = (f"**Casos em conferência.** O inventário tem {len(confrontos)} processos com as campanhas em polos opostos. "
        f"Destes, {c} têm resultado de uma medida de comunicação já conferido e {len(confrontos) - c} ficam fora das taxas. "
        f"Em {len(pendentes)} casos, falta ler o inteiro teor. {len(pendentes_30set)} deles receberam ato em 30/09. "
        "Os nomes e os motivos estão em `confrontos.csv`. Essas pendências podem mudar as taxas após a leitura das peças. "
        "A comparação não representa todos os litígios ajuizados entre as campanhas.") if pendentes else ""
    texto = f'''## 1. Introdução
Este relatório examina a atuação do TSE no **ciclo das Eleições 2026**, com destaque para os conflitos de comunicação entre as campanhas presidenciais. Os gráficos descrevem os registros do extrato oficial; os relatos identificam o conteúdo das medidas e a etapa de cada processo.
O corpus congelado reúne **{n} atos em {p} processos distintos**, entre {period}. Um processo pode produzir várias decisões. A contagem de atos mede registros de atividade, enquanto a contagem por CNJ identifica os processos alcançados, sem pressupor encerramento da ação ou julgamento de mérito.
O arquivo oficial classifica **{tipos['Decisão']} registros como Decisão ({percentual(tipos['Decisão'], n)})** e **{tipos['Acórdão']} como Acórdão ({percentual(tipos['Acórdão'], n)})**. Esses rótulos são preservados no CSV; a leitura da peça continua necessária para distinguir liminares, providências processuais e julgamentos de mérito.
{grafico('01_tipos_ato')}
O maior volume mensal está em **{mes_max[5:]}/{mes_max[:4]}: {qtd_max} atos ({percentual(qtd_max, n)} do corpus)**. O eixo temporal usa a data do ato no arquivo PJe, que pode diferir da data da sessão ou da publicação.
{grafico('02_atos_por_mes')}
A curva acumulada mostra o crescimento dos registros até o corte. Ela não mede o número de ações encerradas nem o resultado dos pedidos.
{grafico('03_ritmo_acumulado')}
## 2. Volume, classes e autoria dos atos
A distribuição dos **{n} atos** pela classe processual registrada no extrato é a seguinte:
{lista_classes}
{grafico('04_classes_por_ato')}
Classe processual e assunto são campos distintos. Uma representação pode versar sobre temas diferentes; propaganda e direito de resposta são identificados pelos critérios descritos nas seções 3 e 4.
O gráfico seguinte usa o campo oficial **autor da decisão**. Esse campo não é tomado como sinônimo da relatoria atual do processo. {texto_autores} são os três autores com mais registros, somando {sum(q for _, q in top_autores)} atos ({percentual(sum(q for _, q in top_autores), n)}).
{grafico('05_autores_dos_atos')}
Um acórdão pode decidir uma etapa ou referendar uma medida provisória. O rótulo, por si só, não informa se o pedido foi acolhido nem se a ação terminou. O extrato também não oferece campo de unanimidade; por isso, os gráficos não estimam concordância entre os ministros.
## 3. Composição e abrangência do corpus
**Fonte e versão.** Os denominadores vêm do conjunto {source}, extraído do sistema PJe pela Secretaria Judiciária. Esta versão conserva os cinco arquivos oficiais gerados em **{resumo['geracao_oficial']}**, com seus hashes e metadados. O recorte abrange a instância do TSE e os registros classificados como Decisão ou Acórdão, de {data_br(inicio)} a {data_br(fim)}, última data disponível no extrato congelado.
**Unidades e filtros.** São selecionados os campos `NR_INSTANCIA=3`, `SG_UF_TRIBUNAL=DF` e `DS_TIPO_DECISAO` igual a Decisão ou Acórdão. Cada linha de `atos.csv` corresponde à combinação do CNJ com `SQ_DECISAO`, o identificador sequencial no arquivo estatístico, que não é o número público da peça. `processos.csv` conta cada CNJ uma vez. Datas de sessão, redação, juntada e publicação podem divergir; os gráficos usam exclusivamente `DT_DECISAO` do arquivo oficial.
{quadro_recortes}
**Ciclo eleitoral.** O ano da eleição identifica o pleito ao qual o processo foi associado, não o ano de sua autuação ou de seu julgamento. Há **{ano_anterior} atos de 2025** no corpus. O início em 03/10/2025 delimita esta extração e não significa que a campanha eleitoral formal já estivesse em curso.
**Suplemento documental identificado.** O processo [0601315-97.2026.6.00.0000](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000) tem resultado registrado em certidão oficial e integra a comparação entre campanhas. Como não possui ato no arquivo de decisões congelado, está marcado em `confrontos.csv` como suplemento e não é acrescentado aos {n} atos ou aos {p} processos do painel geral.
Há **{len(colegiados_fora_zip)} resultados colegiados documentados por certidão sem acórdão no arquivo congelado**: [0600950-43](https://consultaunificadapje.tse.jus.br/#/public/resultado/0600950-43.2026.6.00.0000), [0601303-83](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601303-83.2026.6.00.0000), [0601315-97](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601315-97.2026.6.00.0000), [0601767-10](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601767-10.2026.6.00.0000) e [0601768-92](https://consultaunificadapje.tse.jus.br/#/public/resultado/0601768-92.2026.6.00.0000). Quatro desses CNJs já pertencem ao corpus por decisões anteriores; só o processo suplementar está fora dos {p}. Na primeira certidão, emitida em 09/09, a remoção foi determinada na sessão virtual de 04 a 08/09. As certidões comprovam o resultado proclamado, sem se confundirem com o inteiro teor dos acórdãos. Alimentam a curadoria dos confrontos, com fontes nos relatos, sem acrescentar atos ao painel estatístico.
**Como conferir os números.** O [repositório público](https://github.com/mauricioaugustotse/corpus-tse-eleicoes-2026) traz os arquivos do TSE, as planilhas, os gráficos e o código usado para calculá-los. O leia-me explica como abrir as planilhas, mesmo sem saber programar. Quem quiser repetir a coleta encontra as instruções técnicas no próprio repositório. Os resultados dos pedidos em `confrontos.csv` dependem da leitura das peças indicadas. O arquivo estatístico sozinho não informa se uma medida foi concedida.
{dados}
**Limites.** Este retrato mostra o que constava na extração do TSE feita em 01/10/2026, com atos datados até 30/09. O portal pode atualizar os dados. Nem todo registro chamado “Decisão” resolve um pedido. Alguns são despachos que apenas dão andamento ao processo. Assim, {n} atos não significam {n} julgamentos finais.
## 4. Propaganda e confrontos presidenciais
### 4.1 Recorte por assunto e classe oficiais
O filtro **assunto contendo Propaganda Eleitoral ou classe Direito de Resposta** seleciona **{len(tematicos)} processos**, com **{atos_tema} atos** do corpus: {prop} processos têm assunto de propaganda e {dr} pertencem à classe DR{f', com {ambos} na interseção' if ambos else ', sem sobreposição nesta versão'}. O gráfico mostra esse recorte dentro dos {p} processos.
{grafico('06_composicao_comunicacao')}
Esse filtro é reproduzível a partir dos campos oficiais e não pretende abarcar toda controvérsia possível sobre comunicação eleitoral. Ele não classifica remoções, procedência ou vitória de campanha. A análise de resultados fica restrita aos confrontos documentados a seguir.
### 4.2 Atendimento dos pedidos das duas campanhas presidenciais
O comparativo reúne **{c} processos** com representantes formais das campanhas de Lula e Flávio Bolsonaro em polos opostos e resultado conferido sobre uma medida de comunicação eleitoral. Cada CNJ entra uma vez. Para os processos incluídos, usamos o resultado comparável mais recente que conseguimos documentar até {data_br(fim)}. Atendimento parcial conta como atendimento. Os casos sem resultado comparável ou sem peça acessível constam do registro de exclusões e pendências.
{texto_pendencias}
Dos {c} processos, **{len(no_tema)} pertencem ao recorte oficial de propaganda e direito de resposta**, **{len(fora_tema)} estão no corpus sob outros enquadramentos** ({fora_links}) e **{len(suplemento)} integra o suplemento por certidão oficial**, explicado na seção 3. Todos estão identificados em `confrontos.csv` e são os mesmos relatados na seção 5.
As campanhas de Lula e de Flávio figuram como autoras em **{l['total']} e {f['total']} processos**, respectivamente. A unidade é o processo, mesmo quando ele contém mais de uma pretensão.
{quadro}
**Efeito das medidas conferidas.** Entre os {c} processos classificados, {favor_lula} tiveram resultado favorável à posição de Lula. São {l['atendidos']} pedidos seus atendidos e {f['nao_atendidos']} pedidos do lado adversário não atendidos. Em {favor_flavio} processos, o resultado favoreceu a posição de Flávio. São {f['atendidos']} pedidos seus atendidos e {l['nao_atendidos']} pedidos do lado adversário não atendidos.
**Alcance da comparação.** Os pedidos têm objetos e extensões diferentes. Muitas decisões são cautelares, e sua negativa não equivale a improcedência definitiva. A concessão de resposta também não prova que a veiculação já ocorreu. As taxas descrevem o efeito documentado das medidas até o corte e não demonstram preferência política do Tribunal.
{bloco_lista}
## 5. Os {c} processos comparados entre as campanhas presidenciais
Os relatos abaixo correspondem exatamente aos CNJs incluídos na tabela da seção 4.2 e em `confrontos.csv`. As fontes permitem distinguir decisão monocrática, acórdão e certidão; as datas de sessão eventualmente narradas não substituem a data usada nos gráficos.
'''
    for i, r in enumerate(relatos, 1):
        texto += f"\n### {i}. {r['titulo']}\n{r['texto'].strip()}\n"
    for classe, prefixo in (("RCand", "RCAND"), ("PetCiv", "PETCIV"), ("PA", "PA")):
        secao6 = secao6.replace("{{" + prefixo + "_ATOS}}", str(classes[classe])).replace("{{" + prefixo + "_PROCESSOS}}", str(classes_p[classe]))
    assert "{{" not in secao6
    texto += "\n" + secao6
    auditoria = {"atos": n, "processos": p, "tematicos": len(tematicos), "atos_tematicos": atos_tema,
                 "comparaveis": c, "grupos": grupos, "no_corpus": len(no_corpus), "no_tema": len(no_tema),
                 "fora_tema": sorted(fora_tema), "suplemento_documental": sorted(suplemento),
                 "candidatos_sem_inteiro_teor": pendentes,
                 "resultados_colegiados_sem_acordao_no_zip": colegiados_fora_zip,
                 "cnjs_relato_iguais_comparativo": True, "classes_processos": dict(classes_p),
                 "efeito_imediato": {"Lula": favor_lula, "Flávio": favor_flavio}}
    return texto, auditoria


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--secao6", type=Path, required=True)
    parser.add_argument("--anexos", type=Path)
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()
    anexos = json.loads(args.anexos.read_text(encoding="utf-8")) if args.anexos else None
    texto, auditoria = montar(args.corpus, args.secao6.read_text(encoding="utf-8"), anexos)
    args.saida.write_text(texto, encoding="utf-8")
    (args.corpus / "auditoria_relatorio.json").write_text(json.dumps(auditoria, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(auditoria, ensure_ascii=False))


if __name__ == "__main__":
    main()
