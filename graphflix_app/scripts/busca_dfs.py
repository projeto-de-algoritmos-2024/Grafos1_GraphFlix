import json
from graphflix_app.models import Prefere

def buscar_dfs(usuario):
    print("\n\n\n\n\nChegou na função buscar_filmes_dfs")

    with open('graphflix_app/grafo.json', 'r') as arquivo:
        grafo = json.load(arquivo)

    generos_preferidos = Prefere.objects.filter(usuario=usuario).values_list('genero_id', flat=True)
    nota_minima = usuario.notaMinima
    recomendacoes = []

    print("Gêneros preferidos:", list(generos_preferidos))

    filmes_por_genero = {}
    for titulo_id, genero_ids in grafo["relacionamentos"]["titulo-genero"].items():
        for genero_id in genero_ids:
            if str(genero_id) not in filmes_por_genero:
                filmes_por_genero[str(genero_id)] = []
            filmes_por_genero[str(genero_id)].append({
                "id": titulo_id,  # Adiciona o ID do título
                "titulo": grafo["titulos"][str(titulo_id)]["titulo"],
                "avaliacao": grafo["titulos"][str(titulo_id)]["avaliacao"]
            })

    # busca DFS
    visitados = set()

    def dfs(genero_id):
        print(f"\nChegou na função dfs. Gênero: {genero_id}")
        if genero_id in visitados:
            return []
        visitados.add(genero_id)
        
        filmes = filmes_por_genero.get(str(genero_id), [])
        #print(f"Filmes no gênero {genero_id}: {[filme['titulo'] for filme in filmes]}")
        
        # Filtrar avaliação mínima
        filmes_filtrados = [filme for filme in filmes if filme["avaliacao"] >= nota_minima]
        #print(f"Filmes no gênero {genero_id} após filtrar pela nota mínima {nota_minima}: {[filme['titulo'] for filme in filmes_filtrados]}")

        for relacao in grafo["relacionamentos"]["titulo-titulo"]:
            titulo1, titulo2 = relacao
            if str(genero_id) == titulo1 or str(genero_id) == titulo2:
                proximo_genero_id = titulo2 if str(genero_id) == titulo1 else titulo1
                if proximo_genero_id not in visitados:
                    filmes_filtrados.extend(dfs(proximo_genero_id))

        return filmes_filtrados

    for genero_id in generos_preferidos:
        filmes_relacionados = dfs(genero_id)
        recomendacoes.extend(filmes_relacionados)

    print("\nRecomendações obtidas:", recomendacoes)
    return recomendacoes

