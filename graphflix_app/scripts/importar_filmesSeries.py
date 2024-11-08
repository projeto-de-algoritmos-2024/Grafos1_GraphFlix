import requests
import time
from django.utils.text import slugify
from graphflix_app.models import Genero, Titulo, Filme, Serie, Possui, Elenco

API_KEY = '33bec3868b8416565cde6c27bae0033c'
TMDB_MOVIES_URL = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=pt-BR'
TMDB_SERIES_URL = f'https://api.themoviedb.org/3/tv/popular?api_key={API_KEY}&language=pt-BR'
TMDB_MOVIE_DETAILS_URL = f'https://api.themoviedb.org/3/movie/{{movie_id}}?api_key={API_KEY}&language=pt-BR'
TMDB_SERIE_DETAILS_URL = f'https://api.themoviedb.org/3/tv/{{tv_id}}?api_key={API_KEY}&language=pt-BR'
TMDB_CREDITS_URL = f'https://api.themoviedb.org/3/{{media_type}}/{{media_id}}/credits?api_key={API_KEY}&language=pt-BR'
RATE_LIMIT = 0.02  # Limite de 50 requisições por segundo (1/50 = 0.02s)

def importar_filmes():
    page = 1
    while True:
        response = requests.get(f"{TMDB_MOVIES_URL}&page={page}")
        if response.status_code != 200:
            print(f"Erro ao buscar filmes: {response.status_code}")
            break

        filmes = response.json().get('results', [])
        print(f"Página {page}: Encontradas {len(filmes)} filmes.")
        if not filmes:
            break

        for filme_data in filmes:
            detalhes_response = requests.get(TMDB_MOVIE_DETAILS_URL.format(movie_id=filme_data['id']))
            duracao = detalhes_response.json().get('runtime', 'N/A') if detalhes_response.status_code == 200 else 'N/A'
            
            credits_response = requests.get(TMDB_CREDITS_URL.format(media_type='movie', media_id=filme_data['id']))
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                crew = credits_data.get('crew', [])
                elenco = credits_data.get('cast', [])
                diretor = next((pessoa['name'] for pessoa in crew if pessoa['job'] == 'Director'), 'N/A')
            else:
                diretor = 'N/A'
                elenco = []

            try:
                slug = slugify(f"{filme_data['name']}-{filme_data['id']}")
                titulo, _ = Titulo.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'titulo': filme_data['title'],
                        'dtLancamento': filme_data.get('release_date'),
                        'classificacao': filme_data.get('vote_average'),
                        'posterPath': filme_data.get('poster_path', ''),
                        'backdropPath': filme_data.get('backdrop_path', ''),
                        'sinopse': filme_data.get('overview', ''),
                        'avaliacao': filme_data.get('vote_average'),
                    }
                )
            except Exception as e:
                print(f"Erro ao criar título {filme_data['title']}: {e}")
                continue  # Pula se der erro

            print(f"Importando filme: {filme_data['title']}")

            filme, _ = Filme.objects.update_or_create(
                id_filme=filme_data['id'],
                defaults={'titulo': titulo, 'duracao': duracao, 'diretor': diretor}
            )

            for genero_id in filme_data.get('genre_ids', []):
                genero, _ = Genero.objects.get_or_create(id=genero_id)
                Possui.objects.get_or_create(titulo=titulo, genero=genero)

            for ator in elenco:
                nome_ator = ator['name']
                ator_obj, _ = Elenco.objects.get_or_create(titulo=titulo, elenco=nome_ator)
                ator_obj.save()

            time.sleep(RATE_LIMIT)

        print(f"Página {page} de filmes importada com sucesso.")
        if page == 30:
            break
        page += 1

def importar_series():
    page = 1
    while True:
        response = requests.get(f"{TMDB_SERIES_URL}&page={page}")
        if response.status_code != 200:
            print(f"Erro ao buscar séries: {response.status_code}")
            break

        series = response.json().get('results', [])
        print(f"Página {page}: Encontradas {len(series)} séries.")
        if not series:
            break

        for serie_data in series:
            detalhes_response = requests.get(TMDB_SERIE_DETAILS_URL.format(tv_id=serie_data['id']))
            qtd_temporadas = detalhes_response.json().get('number_of_seasons', 0) if detalhes_response.status_code == 200 else 0
            
            credits_response = requests.get(TMDB_CREDITS_URL.format(media_type='tv', media_id=serie_data['id']))
            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                crew = credits_data.get('crew', [])
                elenco = credits_data.get('cast', [])
                criador_lista = [pessoa['name'] for pessoa in crew if pessoa['job'] in ['Executive Producer', 'Writer']]
                criador = ', '.join(criador_lista) if criador_lista else 'N/A'
            else:
                criador = 'N/A'
                elenco = []

            try:
                slug = slugify(f"{serie_data['name']}-{serie_data['id']}")
                titulo, _ = Titulo.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'titulo': serie_data['name'],
                        'dtLancamento': serie_data.get('first_air_date'),
                        'classificacao': serie_data.get('vote_average'),
                        'posterPath': serie_data.get('poster_path', ''),
                        'backdropPath': serie_data.get('backdrop_path', ''),
                        'sinopse': serie_data.get('overview', ''),
                        'avaliacao': serie_data.get('vote_average'),
                    }
                )
            except Exception as e:
                print(f"Erro ao criar título {serie_data['name']}: {e}")
                continue

            print(f"Importando série: {serie_data['name']}")

            serie_obj, _ = Serie.objects.update_or_create(
                id_serie=serie_data['id'],
                defaults={'titulo': titulo, 'qtd_temporadas': qtd_temporadas, 'criador': criador}
            )

            for genero_id in serie_data.get('genre_ids', []):
                genero, _ = Genero.objects.get_or_create(id=genero_id)
                Possui.objects.get_or_create(titulo=titulo, genero=genero)

            for ator in elenco:
                nome_ator = ator['name']
                ator_obj, _ = Elenco.objects.get_or_create(titulo=titulo, elenco=nome_ator)
                ator_obj.save()

            time.sleep(RATE_LIMIT)

        print(f"Página {page} de séries importada com sucesso.")
        if page == 30:
            break
        page += 1
