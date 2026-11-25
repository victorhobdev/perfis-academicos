from pathlib import Path
import csv
import re
from urllib.parse import urljoin

from rdflib import DCTERMS, OWL, RDF, SKOS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.compare import isomorphic
from rdflib.namespace import DCAT


SCHEMA = Namespace("https://schema.org/")
COLECOES = {
    "unidades": ("Unidades acadêmicas", "Unidade"),
    "departamentos": ("Departamentos", "Departamento"),
    "cursos": ("Cursos", "Curso"),
    "areas": ("Áreas temáticas", "Area"),
    "disciplinas": ("Disciplinas", "Disciplina"),
    "grupos": ("Grupos de pesquisa", "GrupoPesquisa"),
    "projetos": ("Projetos de pesquisa", "ProjetoPesquisa"),
    "producoes": ("Produções acadêmicas", "Producao"),
}
VINCULOS = {
    "areas": "area", "disciplinas": "disciplina",
    "grupos": "grupo", "projetos": "participaDe",
}


def pagina_perfil(id_perfil):
    return f"perfis/{id_perfil}.html"


def pagina_recurso(id_recurso):
    return f"recursos.html#{id_recurso}"


def nome(item):
    return item if isinstance(item, str) else item["nome"]


def texto(valor):
    return Literal(valor, lang="pt-BR")


def criar_grafo(dados, base):
    acad = Namespace(base + "ontologia.ttl#")
    grafo = Graph(bind_namespaces="none")
    grafo.bind("acad", acad)
    for prefixo, namespace in {
        "schema": SCHEMA, "dct": DCTERMS, "dcat": DCAT,
        "rdf": RDF, "skos": SKOS, "xsd": XSD,
    }.items():
        grafo.bind(prefixo, namespace)

    def uri(caminho):
        return URIRef(urljoin(base, caminho))

    dataset = uri("dados.ttl")
    grafo.add((dataset, RDF.type, DCAT.Dataset))
    grafo.add((dataset, DCTERMS.title, texto("Diretório de perfis acadêmicos")))
    grafo.add((dataset, DCTERMS.source, uri("dados.json")))
    grafo.add((dataset, DCTERMS.description, texto(dados["fonte"])))
    grafo.add((dataset, DCTERMS.license, URIRef(dados["licenca"])))
    grafo.add((dataset, DCTERMS.modified, Literal(dados["atualizadoEm"], datatype=XSD.date)))
    grafo.add((dataset, DCTERMS.conformsTo, uri("ontologia.ttl")))

    instituicao = uri(pagina_recurso("instituicao"))
    grafo.add((instituicao, RDF.type, SCHEMA.CollegeOrUniversity))
    grafo.add((instituicao, SCHEMA.name, texto(dados["instituicao"])))
    esquema = uri(pagina_recurso("areas"))
    grafo.add((esquema, RDF.type, SKOS.ConceptScheme))
    grafo.add((esquema, SKOS.prefLabel, texto("Áreas temáticas do diretório")))

    for colecao, (_, classe) in COLECOES.items():
        for id_recurso, item in dados[colecao].items():
            recurso = uri(pagina_recurso(id_recurso))
            classe_item = "Artigo" if colecao == "producoes" and item["tipo"] == "Artigo" else classe
            grafo.add((recurso, RDF.type, acad[classe_item]))
            grafo.add((recurso, SCHEMA.name, texto(nome(item))))
            if colecao == "unidades":
                grafo.add((recurso, SCHEMA.parentOrganization, instituicao))
            if colecao in ("departamentos", "cursos"):
                grafo.add((recurso, acad.unidade, uri(pagina_recurso(item["unidade"]))))
            if colecao == "areas":
                grafo.add((recurso, SKOS.prefLabel, texto(nome(item))))
                grafo.add((recurso, SKOS.inScheme, esquema))
                if item.get("wikidata"):
                    grafo.add((recurso, SKOS.closeMatch, URIRef(item["wikidata"])))
            if colecao == "projetos":
                grafo.add((recurso, SCHEMA.description, texto(item["descricao"])))
            if colecao == "producoes":
                grafo.add((recurso, acad.ano, Literal(str(item["ano"]), datatype=XSD.gYear)))
                for autor in item["autores"]:
                    grafo.add((recurso, acad.autor, uri(pagina_perfil(autor))))

    for id_perfil, perfil in dados["perfis"].items():
        pessoa = uri(pagina_perfil(id_perfil))
        grafo.add((pessoa, RDF.type, acad[perfil["tipo"]]))
        grafo.add((pessoa, SCHEMA.name, texto(perfil["nome"])))
        grafo.add((pessoa, SCHEMA.jobTitle, texto(perfil["funcao"])))
        grafo.add((pessoa, SCHEMA.description, texto(perfil["apresentacao"])))
        grafo.add((pessoa, SCHEMA.affiliation, instituicao))
        vinculo = "departamento" if perfil["tipo"] == "Docente" else "curso"
        grafo.add((pessoa, acad[vinculo], uri(pagina_recurso(perfil[vinculo]))))
        if "ingresso" in perfil:
            grafo.add((pessoa, acad.ingresso, Literal(str(perfil["ingresso"]), datatype=XSD.gYear)))
        for formacao in perfil.get("formacao", []):
            grafo.add((pessoa, acad.formacao, Literal(formacao)))
        for colecao, propriedade in VINCULOS.items():
            for id_recurso in perfil.get(colecao, []):
                grafo.add((pessoa, acad[propriedade], uri(pagina_recurso(id_recurso))))
        for portal in perfil.get("links", {}).values():
            grafo.add((pessoa, acad.portalAcademico, URIRef(portal)))
    return grafo


def escrever_rdf(dados, site):
    base_local = site.resolve().as_uri() + "/"
    grafo = criar_grafo(dados, base_local)
    ttl = grafo.serialize(format="turtle", base=base_local)
    ttl = re.sub(r"^@base [^\n]+\n", "", ttl).replace(f"<{base_local}", "<")
    (site / "dados.ttl").write_text(ttl, encoding="utf-8")

    ontologia = Graph().parse(site / "ontologia.ttl", publicID=base_local + "ontologia.ttl")
    xml = ontologia.serialize(format="xml", base=base_local)
    xml = xml.replace(f' xml:base="{base_local}"', "")
    # RDF/XML exige namespaces absolutos. Esta ontologia usa URIs de propriedades
    # locais só como recursos, de modo que não há QNames locais a preservar.
    (site / "ontologia.owl").write_text(xml, encoding="utf-8")

    publicado = Graph().parse(site / "dados.ttl")
    if not isomorphic(publicado, grafo):
        raise ValueError("O RDF publicado não preservou as URIs relativas dos dados.")
    ttl_local = Graph().parse(site / "ontologia.ttl")
    xml_local = Graph().parse(
        site / "ontologia.owl", format="xml", publicID=base_local + "ontologia.ttl"
    )
    if not isomorphic(ttl_local, xml_local):
        raise ValueError("A ontologia Turtle e o arquivo OWL/RDF-XML divergem.")
    if (URIRef(base_local + "ontologia.ttl"), RDF.type, OWL.Ontology) not in ttl_local:
        raise ValueError("A ontologia está sem a declaração owl:Ontology.")
    return publicado


def executar_consultas(site: Path, grafo: Graph):
    pasta = site / "consultas"
    base_consultas = pasta.resolve().as_uri() + "/"
    resultados = pasta / "resultados"
    resultados.mkdir(exist_ok=True)
    for arquivo in sorted(pasta.glob("consulta*.rq")):
        consulta = arquivo.read_text(encoding="utf-8")
        resultado = grafo.query(f"BASE <{base_consultas}>\n{consulta}")
        colunas = [str(variavel) for variavel in resultado.vars]
        linhas = [[str(valor) if valor is not None else "" for valor in linha] for linha in resultado]
        saida = resultados / f"{arquivo.stem}.csv"
        with saida.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, lineterminator="\n")
            writer.writerow(colunas)
            writer.writerows(linhas)
        print(f"{arquivo.stem}: {len(linhas)} linha(s)")
        yield arquivo.name, consulta, colunas, linhas
