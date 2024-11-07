from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Usuario(AbstractUser):
    notaMinima = models.FloatField(null=True, blank=True)

class Titulo(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    dtLancamento = models.DateField()
    classificacao = models.CharField(max_length=5)
    posterPath = models.CharField(max_length=100, blank=True)
    backdropPath = models.CharField(max_length=100, blank=True)
    sinopse = models.CharField(max_length=500, blank=True)
    avaliacao = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super(Titulo, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Filme(models.Model):
    titulo = models.OneToOneField(Titulo, on_delete=models.CASCADE, primary_key=True)
    duracao = models.CharField(max_length=10)
    diretor = models.CharField(max_length=50)

    def __str__(self):
        return f"Filme: {self.titulo.titulo}"


class Serie(models.Model):
    titulo = models.OneToOneField(Titulo, on_delete=models.CASCADE, primary_key=True)
    qtd_temporadas = models.IntegerField()
    criador = models.CharField(max_length=50)
    situacao = models.CharField(max_length=15)

    def __str__(self):
        return f"Série: {self.titulo.titulo}"

class Genero(models.Model):
    nome_genero = models.CharField(max_length=20)

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
