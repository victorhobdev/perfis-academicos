# Diretório de perfis acadêmicos

Trabalho de Web Semântica e Linked Open Data. A aplicação reúne dois perfis de docentes e dois de discentes fictícios. Um JSON alimenta as páginas estáticas e o grafo de dados.

**Integrantes do trio** · preencher os três nomes antes da entrega.

## Abrir e reproduzir

Abra [docs/index.html](docs/index.html) no navegador. As páginas e os resultados estão prontos para consulta local, inclusive sem servidor.

Para alterar os dados ou reproduzir os resultados, use Python 3.10 ou superior. Execute os comandos na raiz do projeto.

```sh
python -m pip install -r requirements.txt
python gerar.py
```

Edite [dados/perfis.json](dados/perfis.json) para incluir perfis e dados. Preserve os identificadores já publicados. O script valida vínculos, gera HTML e RDF, compara as duas serializações da ontologia, executa as consultas e atualiza as tabelas e os CSVs.

## Arquivos

| Caminho | Conteúdo |
| --- | --- |
| `dados/perfis.json` | Fonte única dos perfis e dos seus relacionamentos. |
| `modelos/` | Modelo de página e modelo visual comum aos perfis. |
| `gerar.py` e `grafo.py` | Geração de páginas, RDF e resultados SPARQL. |
| `docs/` | Site pronto para hospedagem, incluindo RDF, OWL e documentação. |
| `docs/consultas/` | Seis arquivos SPARQL e os CSVs em `resultados/`. |

- [Proposta e requisitos](docs/documentacao/proposta.md)
- [Modelo conceitual, dicionário e ontologia](docs/documentacao/modelagem.md)
- [Pesquisa de vocabulários, links externos, fontes e licença](docs/documentacao/vocabularios.md)
- [Perguntas, consultas, explicações e resultados](docs/consultas.html)
- [Declaração de uso de IA](docs/documentacao/ia.md)

## Publicação

O pacote pode ser publicado como um site estático. No GitHub Pages, envie a pasta do projeto para um repositório. Em **Settings → Pages**, selecione **Deploy from a branch**, o branch escolhido e a pasta **/docs**. [Site no GitHub Pages](https://victorhobdev.github.io/perfis-academicos/) · [Repositório do trabalho](https://github.com/victorhobdev/perfis-academicos) [Documentação do GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

Os IRIs relativos são resolvidos pela URL do documento RDF. Assim, ao publicar o site, `dados.ttl`, `ontologia.ttl`, `ontologia.owl`, `perfis/ana-martins.html` e `recursos.html#area-web-semantica` ficam sob a mesma base pública, inclusive se houver um subdiretório. Mantenha os arquivos nessas posições. Para evidenciar a publicação, confira esses caminhos numa janela anônima e registre as URLs reais.

Para executar as consultas em outro ambiente, carregue `dados.ttl` a partir de sua URL ou informe essa URL como base de leitura do Turtle. Antes do `PREFIX` de cada consulta, insira `BASE <URL-DO-SITE/consultas/>`, substituindo pela URL absoluta da pasta. A barra final é necessária para resolver `../`. O comando `python gerar.py` configura a base local automaticamente.

## Roteiro de apresentação

1. Abra um perfil do diretório e siga um projeto até a página de recursos.
2. Mostre o mesmo perfil e seu vínculo no Turtle. Abra a ontologia para identificar as classes e os domínios.
3. Rode `python gerar.py` e veja os CSVs. A consulta 4 junta duas categorias de pessoa por projeto. A consulta 5 usa `OPTIONAL` para manter o artigo sem coautor cadastrado.
4. Abra um conceito no Wikidata a partir de **Recursos do grafo** e mostre o mesmo vínculo no Turtle.

Os CSVs são as evidências de execução reproduzível com RDFLib. O projeto usa hospedagem estática e execução local de SPARQL.
