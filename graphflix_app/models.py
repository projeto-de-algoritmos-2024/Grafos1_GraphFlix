from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    sinopse = models.TextField()
    genero = models.CharField(max_length=50)
    duracao = models.CharField(max_length=50)
    ano_lancamento = models.PositiveIntegerField()
    diretor = models.CharField(max_length=100)
    imagem_capa = models.ImageField(upload_to='filmes/', null=True, blank=True)
    imagem_bg = models.ImageField(upload_to='filmes/', null=True, blank=True)
    url_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Serie(models.Model):
    titulo = models.CharField(max_length=100)
    sinopse = models.TextField()
    genero = models.CharField(max_length=50)
    qtd_temporadas = models.CharField(max_length=50)
    ano_estreia = models.PositiveIntegerField()
    criador = models.CharField(max_length=100)
    imagem_capa = models.ImageField(upload_to='series/', null=True, blank=True)
    imagem_bg = models.ImageField(upload_to='series/', null=True, blank=True)
    url_slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, null=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True)
    classificacao = models.DecimalField(max_digits=3, decimal_places=1)
    comentario = models.TextField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario.username} para {self.filme or self.serie}"


class Comentario(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.avaliacao.filme or self.avaliacao.serie}"


""" python manage.py makemigrations
python manage.py migrate """
