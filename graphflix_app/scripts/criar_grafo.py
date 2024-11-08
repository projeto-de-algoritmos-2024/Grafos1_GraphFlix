import django
from neo4j import GraphDatabase
from graphflix_app.models import Titulo, Genero, Possui

NEO4J_URI = 'neo4j+s://c8b255a4.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'SlpNoo6syk3JdrF9rFocv0_rPmtO6UpmSJfAEuh2HyU'
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def criar_grafo():
    grafo = {
        "generos": {},
        "titulos": {},
        "relacionamentos": {
            "titulo-genero": {},
            "titulo-titulo": set()
        }
    }

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
                grafo["relacionamentos"]["titulo-titulo"].add(relacao)

    # salvando no Neo4j
    def cria_genero(tx, id_genero, nome_genero):
        tx.run("MERGE (g:Genero {id: $id, nome_genero: $nome_genero})", 
               id=id_genero, nome_genero=nome_genero)

    def cria_titulo(tx, id_titulo, nome_titulo, avaliacao):
        tx.run("MERGE (t:Titulo {id: $id, titulo: $titulo, avaliacao: $avaliacao})", 
               id=id_titulo, titulo=nome_titulo, avaliacao=avaliacao)

    def cria_relacao_genero_titulo(tx, genero_id, titulo_id):
        tx.run("""
        MATCH (g:Genero {id: $genero_id}), (t:Titulo {id: $titulo_id})
        MERGE (g)-[:POSSUI]->(t)
        """, genero_id=genero_id, titulo_id=titulo_id)

    def cria_relacao_titulo_titulo(tx, titulo_id1, titulo_id2):
        tx.run("""
            MATCH (t1:Titulo {id: $titulo_id1}), (t2:Titulo {id: $titulo_id2})
            MERGE (t1)-[:COMPARTILHA_GENERO]->(t2)
            MERGE (t2)-[:COMPARTILHA_GENERO]->(t1)
            """, titulo_id1=titulo_id1, titulo_id2=titulo_id2)

    # criando nós
    with driver.session() as session:
        # gêneros
        for id_genero, nome_genero in grafo["generos"].items():
            session.write_transaction(cria_genero, id_genero, nome_genero)
        
        # títulos
        for id_titulo, title_data in grafo["titulos"].items():
            session.write_transaction(cria_titulo, id_titulo, title_data["titulo"], title_data["avaliacao"])
        
        # relação título-gênero
        for titulo_id, generos in grafo["relacionamentos"]["titulo-genero"].items():
            for genero_id in generos:
                session.write_transaction(cria_relacao_genero_titulo, genero_id, titulo_id)

        # relação título-título (bidimensional)
        for titulo_id1, titulo_id2 in grafo["relacionamentos"]["titulo-titulo"]:
            session.write_transaction(cria_relacao_titulo_titulo, titulo_id1, titulo_id2)

    print("Sucesso!")
    driver.close()
