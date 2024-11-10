import json
from graphflix_app.models import Titulo, Genero, Possui

def criar_grafo():
    grafo = {
        "generos": {},
        "titulos": {},
        "relacionamentos": {
            "titulo-genero": {},
            "titulo-titulo": []
        }
    }

        # populando o grafo com dados dos título e gêneros
    for genero in Genero.objects.all():
        grafo["generos"][genero.id] = genero.nome_genero

    for titulo in Titulo.objects.all():
        grafo["titulos"][titulo.id] = {"titulo": titulo.titulo, "avaliacao": titulo.avaliacao}

        # título-gênero
        for possui in Possui.objects.filter(titulo=titulo):
            if titulo.id not in grafo["relacionamentos"]["titulo-genero"]:
                grafo["relacionamentos"]["titulo-genero"][titulo.id] = []
            grafo["relacionamentos"]["titulo-genero"][titulo.id].append(possui.genero.id)

        # títulos-título
        generos_do_titulo = [p.genero for p in Possui.objects.filter(titulo=titulo)]
        for compartilha in Possui.objects.filter(genero__in=generos_do_titulo):
            outro_titulo_id = compartilha.titulo.id
            if outro_titulo_id != titulo.id:
                relacao = tuple(sorted((titulo.id, outro_titulo_id)))
                grafo["relacionamentos"]["titulo-titulo"].append(list(relacao))  

    with open('graphflix_app/grafo.json', 'w') as arquivo:
        json.dump(grafo, arquivo, indent=4)

    print("Grafo salvo com sucesso em disco!")
