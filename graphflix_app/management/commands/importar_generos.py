from django.core.management.base import BaseCommand
from graphflix_app.scripts.importar_generos import importar_generos_filmes, importar_generos_tv


class Command(BaseCommand):
    help = 'Importa gêneros do TMDb para o banco de dados'

    def handle(self, *args, **kwargs):
        importar_generos_filmes()
        importar_generos_tv()
