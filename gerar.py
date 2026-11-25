from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit
import json
import re
import shutil

from grafo import COLECOES, VINCULOS, escrever_rdf, executar_consultas, nome, pagina_perfil, pagina_recurso


RAIZ = Path(__file__).resolve().parent
SITE = RAIZ / "docs"
FONTE = RAIZ / "dados" / "perfis.json"

CONSULTAS = [
    ("Quais são os docentes cadastrados e seus departamentos ou unidades?",
     "Parte de Docente, segue departamento até Departamento e unidade até Unidade."),
    ("Quais discentes pertencem a determinado curso?",
     "Seleciona o Curso de Sistemas de Informação pelo seu IRI e usa curso para localizar instâncias de Discente."),
    ("Quais docentes atuam em determinada área de pesquisa?",
     "Seleciona a área de Dados Abertos e usa area para encontrar os docentes. O rótulo vem de skos:prefLabel."),
    ("Quais docentes e discentes participam de um mesmo projeto?",
     "Une instâncias de Docente e Discente pelo mesmo ProjetoPesquisa, usando participaDe nos dois lados."),
    ("Quais são as publicações de uma docente e quem são seus coautores?",
     "Filtra as instâncias de Artigo pela propriedade autor ligada a Ana. OPTIONAL mantém artigos individuais e o filtro exclui Ana da coluna de coautoria."),
    ("Quais pessoas estão vinculadas a uma unidade acadêmica específica?",
     "O caminho (departamento|curso)/unidade chega ao Instituto de Ciências Exatas a partir das duas categorias de perfil."),
]


def h(valor):
    return escape(str(valor), quote=True)


def link(url, rotulo):
    return f'<a href="{h(url)}">{h(rotulo)}</a>'


def secao(titulo, conteudo):
    return f'<section class="card"><h2>{h(titulo)}</h2>{conteudo}</section>'


def lista(itens, classe="clean-list"):
    return f'<ul class="{classe}">' + "".join(f"<li>{item}</li>" for item in itens) + "</ul>"


def validar(dados):
    grupos = [dados[chave] for chave in (*COLECOES, "perfis")]
    ids = {"instituicao", "areas"}
    for grupo in grupos:
        for id_recurso in grupo:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", id_recurso) or id_recurso in ids:
                raise ValueError(f"Identificador inválido ou repetido: {id_recurso}")
            ids.add(id_recurso)

    for perfil in dados["perfis"].values():
        if perfil["tipo"] == "Docente" and "curso" not in perfil and "ingresso" not in perfil:
            dados["departamentos"][perfil["departamento"]]
        elif perfil["tipo"] == "Discente" and "departamento" not in perfil:
            dados["cursos"][perfil["curso"]]
        else:
            raise ValueError(f"Tipo ou vínculo incompatível: {perfil['nome']}")
        for colecao in VINCULOS:
            for referencia in perfil.get(colecao, []):
                dados[colecao][referencia]
        for url in perfil.get("links", {}).values():
            if urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
                raise ValueError(f"Portal acadêmico inválido: {url}")

    for producao in dados["producoes"].values():
        if producao["tipo"] not in ("Artigo", "Trabalho acadêmico") or not producao["autores"]:
            raise ValueError(f"Tipo ou autores inválidos: {producao['nome']}")
        for autor in producao["autores"]:
            dados["perfis"][autor]


def renderizar_perfil(dados, id_perfil, perfil, modelo):
    docente = perfil["tipo"] == "Docente"
    tipo_vinculo = "departamento" if docente else "curso"
    id_vinculo = perfil[tipo_vinculo]
    vinculo = dados["departamentos" if docente else "cursos"][id_vinculo]
    id_unidade = vinculo["unidade"]
    secoes = [secao("Apresentação", f'<p>{h(perfil["apresentacao"])}</p>')]
    if perfil.get("formacao"):
        secoes.append(secao("Formação acadêmica", lista(map(h, perfil["formacao"]))))
    for colecao in VINCULOS:
        referencias = perfil.get(colecao, [])
        if referencias:
            itens = [
                link("../" + pagina_recurso(ref), nome(dados[colecao][ref]))
                for ref in referencias
            ]
            classe = "tag-list" if colecao == "areas" else "clean-list"
            secoes.append(secao(COLECOES[colecao][0], lista(itens, classe)))

    producoes = [
        link("../" + pagina_recurso(ref), item["nome"]) + f' ({h(item["ano"])})'
        for ref, item in dados["producoes"].items() if id_perfil in item["autores"]
    ]
    if producoes:
        secoes.append(secao("Produções acadêmicas", lista(producoes)))

    links = perfil.get("links", {})
    portais = lista((link(url, rotulo) for rotulo, url in links.items()), "social-links")
    ingresso = f'<div><dt>Ingresso</dt><dd>{h(perfil["ingresso"])}</dd></div>' if "ingresso" in perfil else ""
    palavras = perfil["nome"].split()
    return modelo.substitute(
        iniciais=h(palavras[0][0] + palavras[-1][0]) if len(palavras) > 1 else h(palavras[0][0]),
        nome=h(perfil["nome"]), tipo=h(perfil["tipo"].lower()), funcao=h(perfil["funcao"]),
        vinculo=h(vinculo["nome"]), secoes="\n    ".join(secoes),
        instituicao=link("../" + pagina_recurso("instituicao"), dados["instituicao"]),
        unidade=link("../" + pagina_recurso(id_unidade), dados["unidades"][id_unidade]),
        vinculo_tipo=tipo_vinculo.capitalize(),
        vinculo_link=link("../" + pagina_recurso(id_vinculo), vinculo["nome"]),
        ingresso=ingresso, links=secao("Portais acadêmicos", portais) if links else "",
    )


def renderizar_indice(dados):
    partes = [
        "<h1>Diretório acadêmico</h1>",
        '<p class="role">Docentes e discentes por curso, departamento e área de pesquisa.</p>',
    ]
    for tipo, titulo, colecao, chave in [
        ("Docente", "Docentes", "departamentos", "departamento"),
        ("Discente", "Discentes", "cursos", "curso"),
    ]:
        fichas = []
        for id_perfil, perfil in dados["perfis"].items():
            if perfil["tipo"] == tipo:
                vinculo = dados[colecao][perfil[chave]]["nome"]
                fichas.append(
                    f'<article class="card"><h3>{link(pagina_perfil(id_perfil), perfil["nome"])}</h3>'
                    f'<p>{h(perfil["funcao"])}</p><p class="note">{h(vinculo)}</p></article>'
                )
        partes.append(f'<section><h2>{titulo}</h2><div class="directory-grid">{"".join(fichas)}</div></section>')
    arquivos = [
        link("dados.ttl", "Dados RDF (Turtle)"), link("dados.json", "Fonte estruturada (JSON)"),
        link("ontologia.ttl", "Ontologia (Turtle)"), link("ontologia.owl", "Ontologia (OWL/RDF-XML)"),
        link("documentacao/proposta.md", "Proposta"), link("documentacao/modelagem.md", "Modelo e dicionário de dados"),
        link("documentacao/vocabularios.md", "Vocabulários e fontes"), link("documentacao/ia.md", "Declaração de uso de IA"),
        link("consultas.html", "Consultas e resultados"),
    ]
    partes.append(secao("Dados e documentação", lista(arquivos)))
    return "\n".join(partes)


def renderizar_recursos(dados):
    partes = [
        "<h1>Recursos do grafo</h1>",
        f'<p id="instituicao"><strong>Instituição</strong> · {h(dados["instituicao"])}</p>',
    ]
    for colecao, (titulo, _) in COLECOES.items():
        itens = []
        for id_recurso, item in dados[colecao].items():
            extra = ""
            if colecao in ("cursos", "departamentos"):
                ref = item["unidade"]
                extra = " · " + link(pagina_recurso(ref), dados["unidades"][ref])
            if colecao == "areas" and item.get("wikidata"):
                extra = " · " + link(item["wikidata"], "Conceito no Wikidata")
            if colecao == "projetos":
                extra = " · " + h(item["descricao"])
            if colecao == "producoes":
                autores = [link(pagina_perfil(ref), dados["perfis"][ref]["nome"]) for ref in item["autores"]]
                extra = f' · {h(item["tipo"])} ({h(item["ano"])}) · ' + ", ".join(autores)
            itens.append(f'<li id="{id_recurso}"><strong>{h(nome(item))}</strong>{extra}</li>')
        ancora = ' id="areas"' if colecao == "areas" else ""
        partes.append(f'<section class="card"{ancora}><h2>{titulo}</h2><ul class="clean-list">{"".join(itens)}</ul></section>')
    return "\n".join(partes)


def renderizar_consultas(resultados):
    partes = [
        "<h1>Consultas SPARQL</h1>",
        '<p class="role">Resultados gerados pelo RDFLib a partir do arquivo dados.ttl.</p>',
    ]
    for (pergunta, explicacao), (arquivo, consulta, colunas, linhas) in zip(CONSULTAS, resultados, strict=True):
        nome_csv = Path(arquivo).stem + ".csv"
        cabecalho = "".join(f"<th scope='col'>{h(coluna)}</th>" for coluna in colunas)
        corpo = "".join("<tr>" + "".join(f"<td>{h(valor) if valor else '—'}</td>" for valor in linha) + "</tr>" for linha in linhas)
        conteudo = (
            f'<p>{h(explicacao)}</p><p>{link("consultas/" + arquivo, "Arquivo SPARQL")} · '
            f'{link("consultas/resultados/" + nome_csv, "Resultado CSV")}</p>'
            f'<details><summary>Ver consulta</summary><pre><code>{h(consulta)}</code></pre></details>'
            f'<div class="table-scroll"><table><thead><tr>{cabecalho}</tr></thead>'
            f'<tbody>{corpo}</tbody></table></div>'
        )
        partes.append(secao(pergunta, conteudo))
    return "\n".join(partes)


def main():
    dados = json.loads(FONTE.read_text(encoding="utf-8"))
    validar(dados)
    modelo = Template((RAIZ / "modelos" / "pagina.html").read_text(encoding="utf-8"))
    perfil_modelo = Template((RAIZ / "modelos" / "perfil.html").read_text(encoding="utf-8"))

    def escrever_pagina(caminho, titulo, conteudo, raiz=""):
        pagina = modelo.substitute(titulo=h(titulo), instituicao=h(dados["instituicao"]), conteudo=conteudo, raiz=raiz)
        (SITE / caminho).write_text(pagina, encoding="utf-8")

    (SITE / "perfis").mkdir(exist_ok=True)
    shutil.copyfile(FONTE, SITE / "dados.json")
    grafo = escrever_rdf(dados, SITE)
    resultados = list(executar_consultas(SITE, grafo))
    escrever_pagina("index.html", "Diretório acadêmico", renderizar_indice(dados))
    escrever_pagina("recursos.html", "Recursos do grafo", renderizar_recursos(dados))
    escrever_pagina("consultas.html", "Consultas SPARQL", renderizar_consultas(resultados))
    for id_perfil, perfil in dados["perfis"].items():
        conteudo = renderizar_perfil(dados, id_perfil, perfil, perfil_modelo)
        escrever_pagina(pagina_perfil(id_perfil), perfil["nome"], conteudo, "../")
    for arquivo in (SITE / "perfis").glob("*.html"):
        if arquivo.stem not in dados["perfis"]:
            arquivo.unlink()
    print(f'Gerados {len(dados["perfis"])} perfis, {len(grafo)} triplas e {len(resultados)} resultados.')


if __name__ == "__main__":
    main()
