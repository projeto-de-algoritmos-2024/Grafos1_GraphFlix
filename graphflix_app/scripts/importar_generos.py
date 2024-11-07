import requests
from django.conf import settings
from graphflix_app.models import Genero

API_KEY = '33bec3868b8416565cde6c27bae0033c'
TMDB_GENRES_URL_FILME = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=pt-BR'
TMDB_GENRES_URL_TV = f'https://api.themoviedb.org/3/genre/tv/list?api_key={API_KEY}&language=pt-BR'

def importar_generos_filmes():
    response = requests.get(TMDB_GENRES_URL_FILME)
    if response.status_code == 200:
        generos = response.json().get('genres', [])
        for genero in generos:
            Genero.objects.update_or_create(
                id=genero['id'],
                defaults={'nome_genero': genero['name']}
            )
        print("Sucesso!")
    else:
        print(f"Erro: {response.status_code}")

def importar_generos_tv():
    response = requests.get(TMDB_GENRES_URL_FILME)
    if response.status_code == 200:
        generos = response.json().get('genres', [])
        for genero in generos:
            Genero.objects.update_or_create(
                id=genero['id'],
                defaults={'nome_genero': genero['name']}
            )
        print("Sucesso!")
    else:
        print(f"Erro: {response.status_code}")