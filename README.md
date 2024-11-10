# Grafos1_GraphFlix

**Número da Lista**: 52<br>
**Conteúdo da Disciplina**: Grafos1<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/1031265  |  Carlos Eduardo Rodrigues |
| 22/1037993  |  Patrícia Helena Macedo da Silva |

## Sobre 
O GraphFlix propõe um sistema de recomendação de filmes e séries que se baseia no gosto do usuário, oferecendo sugestões personalizadas com base nos gêneros e na avaliação mínima escolhida. Por meio de um grafo de relacionamento entre títulos e gêneros, o sistema permite que o usuário selecione seus gêneros favoritos e defina uma nota mínima, retornando filmes e séries que atendem a esses critérios.

O sistema organiza as informações em um grafo, onde cada título (filme ou série) é ligado a seus gêneros associados, e cada título também possui relações com outros títulos que compartilham ao menos um gênero. 

## Screenshots

### Página inicial
![Página inicial](/graphflix_app/static/imgs/paginaInicial.png)
### Página recomendações
![Página recomendações](/graphflix_app/static/imgs/recomendacoes1.png)
### Página recomendações/Filmes
![Página recomendações/Filmes](/graphflix_app/static/imgs/recomendacoesFilmes.png)
### Página recomendações/Series
![Página recomendações/Series](/graphflix_app/static/imgs/recomendacoesSeries.png)
### Página Perfil
![Perfil](/graphflix_app/static/imgs/PaginaPerfil.png)
### Página Série
![Pagina Serie](/graphflix_app/static/imgs/PaginaSeries.png)
### Visualização no neo4j relacionamento compartilha entre títulos e títulos (limite máximo de 1000 nós)
![Relacionamento Compartilha](/graphflix_app/static/imgs/RelacionamentoCompartilha.png)
### Visualização no neo4j relacionamento possui entre títulos e gêneros (limite máximo de 1000 nós)
![Relacionamento Possui](/graphflix_app/static/imgs/RelacionamentoPossui.png)


## Instalação 
**Linguagem**: Python <br> 
***Versão***: 3.12.3 ou superior <br>
**Framework**: Django <br>
***Versão***: 4.2.2 ou superior <br>

⚠️ Pré-requisitos
- [Docker 27.3.1 ou superior ](https://www.docker.com/get-started)

### ⏬ Clonar o Repositório
Para começar, abra o terminal e clone o repositório em um diretório local da seguinte maneira:

```
https://github.com/projeto-de-algoritmos-2024/Grafos1_GraphFlix.git
```

### 💻 Construir a imagem e executar com o Docker
Use o seguinte comando para construir a imagem Docker:

```
docker build -t graphflix_app .
```

Inicie o contêiner Docker:

```
docker compose up
```
Acesse em um navegador digitando `http://0.0.0.0:8000/`



## Uso 

# Recomendações GraphFlix

Para obter recomendações personalizadas de filmes e séries do **GraphFlix**, siga os passos abaixo:

1. **Cadastro e Login**  
   Primeiro, é necessário se cadastrar no site e fazer login para acessar as funcionalidades de recomendações.

2. **Acesso à Página de Recomendações**  
   Após o login, acesse a página de **Recomendações**.

3. **Definição de Preferências**  
   - Na página de Recomendações, defina seus critérios de busca.
   - Escolha o **gênero** ou **gêneros** que você prefere (ex.: ação, drama,comédia romântica etc.).
   - Defina a **nota mínima** que deseja para os conteúdos sugeridos.

4. **Recebimento dos Resultados**  
   O site irá exibir uma lista de filmes e séries que correspondem às suas preferências.

5. **Favoritar Conteúdos**  
   Clique no filme ou série que mais chamou sua atenção e adicione-o aos favoritos. Isso permite que você guarde e acesse rapidamente seus conteúdos preferidos.

6. **Acesso aos Favoritos no Perfil**  
   Todos os seus favoritos ficam salvos na aba exclusiva de **Favoritos** dentro do seu perfil, onde você pode visualizá-los a qualquer momento.

> Aproveite suas recomendações personalizadas e explore novos conteúdos!

## Vídeo 
Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.




