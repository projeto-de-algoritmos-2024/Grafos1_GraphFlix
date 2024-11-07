from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Usuario(AbstractUser):
    notaMinima = models.FloatField(null=True, blank=True)

class Titulo(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    dtLancamento = models.DateField()
    classificacao = models.CharField(max_length=5, blank=True)
    posterPath = models.CharField(max_length=100)
    backdropPath = models.CharField(max_length=100)
    sinopse = models.CharField(max_length=500)
    avaliacao = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super(Titulo, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Filme(models.Model):
    id_filme = models.IntegerField(primary_key=True)
    titulo = models.OneToOneField(Titulo, on_delete=models.CASCADE)
    duracao = models.CharField(max_length=10)
    diretor = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Filme: {self.titulo.titulo}"


class Serie(models.Model):
    id_serie = models.IntegerField(primary_key=True)
    titulo = models.OneToOneField(Titulo, on_delete=models.CASCADE)
    qtd_temporadas = models.IntegerField()
    criador = models.CharField(max_length=50, blank=True)
    situacao = models.CharField(max_length=15)

    def __str__(self):
        return f"Série: {self.titulo.titulo}"

class Genero(models.Model):
    id = models.IntegerField(primary_key=True)
    nome_genero = models.CharField(max_length=20)

    def __str__(self):
        return self.nome_genero


class Elenco(models.Model):
    titulo = models.ForeignKey(Titulo, on_delete=models.CASCADE)
    elenco = models.CharField(max_length=50)

class Possui(models.Model):
    titulo = models.ForeignKey(Titulo, on_delete=models.RESTRICT)
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT)

class Prefere(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT)

class Favorita(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    titulo = models.ForeignKey(Titulo, on_delete=models.SET_NULL, null=True)



""" python manage.py makemigrations
python manage.py migrate """
