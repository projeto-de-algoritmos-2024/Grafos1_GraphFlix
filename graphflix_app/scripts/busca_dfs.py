import json
import random
from graphflix_app.models import Prefere

def buscar_dfs(usuario):
    #print("\n\n\n\n\nChegou na função buscar_filmes_dfs")

    with open('graphflix_app/grafo.json', 'r') as arquivo:
        grafo = json.load(arquivo)

    generos_preferidos = Prefere.objects.filter(usuario=usuario).values_list('genero_id', flat=True)
    nota_minima = usuario.notaMinima
    recomendacoes = []

    #print("Gêneros preferidos:", list(generos_preferidos))

    filmes_por_genero = {}
    for titulo_id, genero_ids in grafo["relacionamentos"]["titulo-genero"].items():
        for genero_id in genero_ids:
            if str(genero_id) not in filmes_por_genero:
                filmes_por_genero[str(genero_id)] = []
            filmes_por_genero[str(genero_id)].append({
                "id": titulo_id, 
                "titulo": grafo["titulos"][str(titulo_id)]["titulo"],
                "avaliacao": grafo["titulos"][str(titulo_id)]["avaliacao"]
            })

    # busca DFS
    visitados = set()

    def dfs(genero_id):
        #print(f"\nChegou na função dfs. Gênero: {genero_id}")
        if genero_id in visitados:
            return []
        visitados.add(genero_id)
        
        filmes = filmes_por_genero.get(str(genero_id), [])
        random.shuffle(filmes) 
        
        filmes_filtrados = [filme for filme in filmes if filme["avaliacao"] >= nota_minima]

        conexoes = [
            (titulo1, titulo2) for titulo1, titulo2 in grafo["relacionamentos"]["titulo-titulo"]
            if str(genero_id) in (str(titulo1), str(titulo2))
        ]
        random.shuffle(conexoes)

        for titulo1, titulo2 in conexoes:
            proximo_genero_id = titulo2 if str(genero_id) == titulo1 else titulo1
            if proximo_genero_id not in visitados:
                filmes_filtrados.extend(dfs(proximo_genero_id))

        return filmes_filtrados

    for genero_id in generos_preferidos:
        filmes_relacionados = dfs(genero_id)
        recomendacoes.extend(filmes_relacionados)

    #print("\nRecomendações obtidas:", recomendacoes)
    return recomendacoes
