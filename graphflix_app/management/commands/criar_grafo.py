from django.core.management.base import BaseCommand
from graphflix_app.scripts.criar_grafo import criar_grafo


class Command(BaseCommand):
    help = 'Criando o grafo'

    def handle(self, *args, **kwargs):
        criar_grafo()
