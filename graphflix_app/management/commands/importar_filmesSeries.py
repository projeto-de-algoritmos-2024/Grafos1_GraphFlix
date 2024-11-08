from django.core.management.base import BaseCommand
from graphflix_app.scripts.importar_filmesSeries import importar_filmes, importar_series


class Command(BaseCommand):
    help = 'Importa gêneros do TMDb para o banco de dados'

    def handle(self, *args, **kwargs):  
        importar_series()
        importar_filmes()