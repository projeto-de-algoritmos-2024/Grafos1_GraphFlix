from django.contrib import admin
from .models import Filme, Serie, Avaliacao, Comentario

admin.site.register(Filme)
admin.site.register(Serie)
admin.site.register(Avaliacao)
admin.site.register(Comentario)