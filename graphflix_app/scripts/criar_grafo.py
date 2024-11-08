import django
from neo4j import GraphDatabase
from graphflix_app.models import Titulo, Genero, Possui


NEO4J_URI = 'neo4j+s://c8b255a4.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'SlpNoo6syk3JdrF9rFocv0_rPmtO6UpmSJfAEuh2HyU'

def criar_grafo():

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    driver.close()
    print("Ok")