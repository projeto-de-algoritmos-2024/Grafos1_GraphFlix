from django.conf import settings
from graphflix_app.models import Prefere
from neo4j import GraphDatabase

NEO4J_URI = 'neo4j+s://c8b255a4.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'SlpNoo6syk3JdrF9rFocv0_rPmtO6UpmSJfAEuh2HyU'
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def buscar_filmes_dfs(usuario):
    print("\n\n\n\n\nChegou na função buscar_filmes_dfs")

    generos_preferidos = Prefere.objects.filter(usuario=usuario).values_list('genero_id', flat=True)
    nota_minima = usuario.notaMinima
    recomendacoes = []

    print("Gêneros preferidos:", generos_preferidos)

    with driver.session() as session:
        # buscando títulos e gêneros relacionados
        query = """
        MATCH p=()-[:POSSUI]->() RETURN p LIMIT 25;
        """

        result = session.run(query)
        registros = list(result)

        print("Registros obtidos:", registros)

        # organiza os dados de filmes e gêneros
        filmes_por_genero = {}
        for record in registros:
            for node in record["p"].nodes:
                if "Titulo" in node.labels:
                    titulo_id = node["id"]
                    nome = node["titulo"]
                    avaliacao = node["avaliacao"]
                    print(f"Registro - Título ID: {titulo_id}, Nome: {nome}, Avaliação: {avaliacao}")
            
                    for rel in record["p"].relationships:
                        if "GENERO" in rel.type:
                            genero_id = rel.end_node["id"]
                            if genero_id not in filmes_por_genero:
                                filmes_por_genero[genero_id] = []
                            filmes_por_genero[genero_id].append({
                                "titulo": nome,
                                "avaliacao": avaliacao
                            })

        # AQUI COMEÇA A BENDITA DA BUSCA
        visitados = set()

        def dfs(genero_id):
            print("Chegou na função dfs. Gênero:", genero_id)
            if genero_id in visitados:
                print("ANTES DO RETURN DA FUNÇÃO DFS")
                return []
            visitados.add(genero_id)
            filmes = filmes_por_genero.get(genero_id, [])
            filmes_filtrados = [filme for filme in filmes if filme["avaliacao"] >= nota_minima]
            
            for filme in filmes_filtrados:
                print("SOCORRO")
                print(f"Filme: {filme['titulo']}, Avaliação: {filme['avaliacao']}")

            return filmes_filtrados
            
        for genero_id in generos_preferidos:
            filmes_relacionados = dfs(genero_id)
            recomendacoes.extend(filmes_relacionados)

    print("Recomendações obtidas:", recomendacoes)
    return recomendacoes


