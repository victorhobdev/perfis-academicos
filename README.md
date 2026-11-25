# Diretório de Perfis Acadêmicos

Projeto desenvolvido no contexto da disciplina de Web Semântica e Linked Open Data, com o objetivo de representar, organizar e interligar informações acadêmicas utilizando tecnologias da Web Semântica.

A aplicação disponibiliza um diretório de docentes e discentes, relacionando informações sobre formação, vínculos institucionais, áreas de interesse, disciplinas, grupos de pesquisa, projetos e produções acadêmicas.

Os dados são disponibilizados tanto em páginas web navegáveis quanto em formato estruturado RDF, permitindo sua exploração por meio de consultas SPARQL.

**Acesse o projeto:** [victorhobdev.github.io/perfis-academicos](https://victorhobdev.github.io/perfis-academicos/)

## Funcionalidades

- Diretório de perfis de docentes e discentes.
- Navegação entre perfis e recursos acadêmicos relacionados.
- Representação de informações acadêmicas em um grafo RDF.
- Ontologia própria para modelagem do domínio acadêmico.
- Integração com vocabulários da Web Semântica.
- Vinculação de conceitos a recursos externos do Wikidata.
- Consultas SPARQL com resultados exportados em CSV.
- Geração automatizada das páginas HTML e dos dados estruturados.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
| --- | --- |
| Python | Processamento dos dados e geração automatizada dos arquivos |
| RDFLib | Manipulação de grafos RDF e execução de consultas SPARQL |
| RDF | Representação de dados e relacionamentos |
| Turtle | Serialização dos dados RDF |
| OWL | Definição da ontologia acadêmica |
| SPARQL | Consulta ao grafo de dados |
| JSON | Armazenamento dos dados de origem |
| HTML e CSS | Interface web |
| GitHub Pages | Hospedagem da aplicação |

## Modelagem semântica

O modelo de dados representa entidades e relacionamentos do ambiente acadêmico, incluindo:

- Docentes e discentes;
- Instituições, unidades e departamentos;
- Cursos e disciplinas;
- Áreas de conhecimento;
- Grupos e projetos de pesquisa;
- Artigos e outras produções acadêmicas.

A ontologia define classes, propriedades, hierarquias, domínios, alcances e restrições de cardinalidade.

O projeto reutiliza vocabulários estabelecidos para favorecer a interoperabilidade dos dados:

- [Schema.org](https://schema.org/): representação de pessoas, organizações e produções acadêmicas.
- [SKOS](https://www.w3.org/TR/skos-reference/): representação de conceitos e áreas de conhecimento.
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/): metadados e informações sobre os recursos.
- [DCAT](https://www.w3.org/TR/vocab-dcat-3/): descrição do conjunto de dados.
- [OWL](https://www.w3.org/TR/owl2-primer/): definição da ontologia e das relações do domínio.

As áreas de conhecimento também possuem vínculos com conceitos do Wikidata por meio da propriedade `skos:closeMatch`.

## Recursos semânticos

| Recurso | Descrição |
| --- | --- |
| [Dados RDF](docs/dados.ttl) | Grafo de dados acadêmicos em Turtle |
| [Ontologia Turtle](docs/ontologia.ttl) | Ontologia em formato Turtle |
| [Ontologia OWL](docs/ontologia.owl) | Ontologia em formato RDF/XML |
| [Dados JSON](docs/dados.json) | Conjunto de dados estruturados |
| [Consultas SPARQL](docs/consultas/) | Arquivos das consultas ao grafo |
| [Resultados CSV](docs/consultas/resultados/) | Resultados das consultas |

A aplicação disponibiliza seis consultas SPARQL para explorar os relacionamentos entre as entidades do grafo.

As consultas e seus resultados também podem ser acessados pela [interface web](https://victorhobdev.github.io/perfis-academicos/consultas.html).

## Estrutura do projeto

```text
perfis-academicos/
├── dados/
│   └── perfis.json
├── modelos/
│   ├── pagina.html
│   └── perfil.html
├── docs/
│   ├── consultas/
│   │   └── resultados/
│   ├── documentacao/
│   ├── perfis/
│   ├── consultas.html
│   ├── dados.json
│   ├── dados.ttl
│   ├── estilos.css
│   ├── index.html
│   ├── ontologia.owl
│   ├── ontologia.ttl
│   └── recursos.html
├── gerar.py
├── grafo.py
├── requirements.txt
└── README.md
```

O arquivo `dados/perfis.json` é a fonte central das informações do projeto. A partir dele, os scripts Python geram as páginas HTML, os dados RDF e os resultados das consultas SPARQL.

Os arquivos gerados são armazenados no diretório `docs/`, utilizado para publicação da aplicação.

## Execução local

### Pré-requisitos

- Python 3.10 ou superior
- Git

### Instalação

Clone o repositório:

```bash
git clone https://github.com/victorhobdev/perfis-academicos.git
cd perfis-academicos
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### Geração dos arquivos

Execute o script principal:

```bash
python gerar.py
```

O script realiza a validação dos dados, a geração das páginas HTML e do grafo RDF, a verificação das serializações da ontologia e a execução das consultas SPARQL.

Após a execução, abra o arquivo `docs/index.html` no navegador.

A aplicação é estática e não depende de um servidor backend ou banco de dados externo.

### Atualização dos dados

Para adicionar ou modificar informações acadêmicas, edite o arquivo `dados/perfis.json` e execute novamente:

```bash
python gerar.py
```

Os identificadores dos recursos devem ser preservados para manter a consistência dos relacionamentos e dos IRIs publicados.

## Documentação

A documentação complementar está disponível no diretório `docs/documentacao/`.

- [Proposta e requisitos](docs/documentacao/proposta.md)
- [Modelo conceitual e dicionário de dados](docs/documentacao/modelagem.md)
- [Vocabulários, vínculos externos e fontes](docs/documentacao/vocabularios.md)
- [Declaração de uso de inteligência artificial](docs/documentacao/ia.md)

## Contexto acadêmico

O projeto utiliza a estrutura institucional da Universidade Federal Rural do Rio de Janeiro (UFRRJ) como referência para a modelagem do domínio.

Os perfis pessoais, projetos, vínculos e produções acadêmicas apresentados são fictícios e foram elaborados exclusivamente para fins acadêmicos.

## Licença

Os dados e a ontologia produzidos para este projeto são disponibilizados sob a licença [Creative Commons CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
