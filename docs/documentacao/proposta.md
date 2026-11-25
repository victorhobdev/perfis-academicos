# Proposta

O trabalho apresenta um diretório de docentes e discentes no contexto acadêmico da UFRRJ. Ele permite que visitantes encontrem informações acadêmicas no navegador e que estudantes de Web Semântica consultem os mesmos vínculos em RDF. O público inclui a comunidade acadêmica e quem avalia ou reutiliza os dados do trabalho.

## Funcionalidades

- Navegar entre dois docentes e dois discentes, com uma ficha por pessoa.
- Consultar o vínculo institucional, a formação, as disciplinas, as áreas, os projetos, os grupos, as produções e os portais acadêmicos disponíveis.
- Navegar até os recursos compartilhados e as referências externas para as áreas.
- Baixar os dados, a ontologia e as consultas SPARQL com os resultados obtidos.

Nome, função e vínculo ajudam a identificar o perfil. Formação, disciplinas e áreas descrevem a trajetória. Projetos, grupos e produção acadêmica fornecem relações compartilhadas que podem ser percorridas no grafo. Os links acadêmicos apontam para portais gerais, e são identificados assim na interface.

Um JSON mantém a fonte de dados estruturada. Um script Python com RDFLib gera a apresentação e o grafo a partir das mesmas referências. HTML e CSS seguem a estrutura dos modelos fornecidos na disciplina. A geração é feita antes da hospedagem e o navegador recebe arquivos estáticos.
