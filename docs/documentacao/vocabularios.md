# Vocabulários, vínculos externos e fontes

| Vocabulário avaliado | Decisão |
| --- | --- |
| [Schema.org](https://schema.org/Person) | Reutilizado para nomes, descrições, afiliação, organizações e trabalhos. Seus termos genéricos ajudam na interoperabilidade. As relações acadêmicas do diretório, como matrícula em curso e participação em pesquisa, recebem propriedades locais. |
| [SKOS](https://www.w3.org/TR/skos-reference/) | Reutilizado para descrever as áreas como conceitos de um esquema e vinculá-las a conceitos externos. A lista de áreas é plana e controlada pelos identificadores do JSON. |
| [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) | Reutilizado para origem, licença, data de modificação, título e relação com a ontologia. |
| [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) | Reutilizado para classificar o conjunto publicado como `dcat:Dataset`. |
| [OWL 2](https://www.w3.org/TR/owl2-primer/) | Usado para a ontologia de aplicação, com hierarquia, domínios, alcances, disjunção e cardinalidade. |

As escolhas priorizam um vocabulário comum para cada informação e classes locais quando o enunciado exige distinções específicas. A documentação oficial de cada vocabulário orientou a avaliação.

## Vínculos externos

| Área local | Conceito externo | Justificativa |
| --- | --- | --- |
| Web Semântica | [Wikidata Q54837](https://www.wikidata.org/entity/Q54837) | A área local cobre representação e interligação de dados na Web, tema do conceito externo. |
| Dados Abertos | [Wikidata Q309901](https://www.wikidata.org/entity/Q309901) | A área local trata da publicação e reutilização aberta de dados. |
| Inteligência Artificial | [Wikidata Q11660](https://www.wikidata.org/entity/Q11660) | A área especializa o interesse do projeto em classificação e aprendizado de máquina dentro do tema mais geral. |

Em cada caso, `skos:closeMatch` registra proximidade conceitual entre a área local e um item Wikidata. O catálogo pode recortar esses conceitos para o contexto da pesquisa acadêmica. Os vínculos estão no Turtle e na página de recursos.

## Origem e licença

A identificação da universidade, de seus cursos e de suas unidades segue as fontes institucionais. Sistemas de Informação pertence ao Instituto de Ciências Exatas, em Seropédica. Ciência da Computação pertence ao Instituto Multidisciplinar, em Nova Iguaçu. [Oferta do ICE](https://institutos.ufrrj.br/ice/conhece-as-ofertas-do-instituto-de-ciencias-exatas/) · [Graduação do IM](https://www.ni.ufrrj.br/cursos/graduacao/)

Os perfis, vínculos pessoais, projetos e produções são fictícios. As fichas seguem os modelos fornecidos pelo professor Tiago Cruz de França para a atividade. Os portais ORCID e Lattes são links de referência e os itens Wikidata são referências temáticas.

Os dados criados para a atividade e a ontologia têm indicação de [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). A indicação se aplica aos dados e à ontologia produzidos para o projeto. O CSS adapta o material de referência fornecido para a atividade, que conserva sua atribuição original. O JSON registra a última atualização, em 25 de novembro de 2026.
