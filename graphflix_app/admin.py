from django.contrib import admin
from .models import Usuario, Titulo, Filme, Serie, Genero, Elenco, Possui, Prefere, Favorita

admin.site.register(Titulo)
admin.site.register(Filme)
admin.site.register(Serie)
admin.site.register(Genero)
admin.site.register(Elenco)
admin.site.register(Possui)
admin.site.register(Prefere)
admin.site.register(Favorita)
admin.site.register(Usuario)
