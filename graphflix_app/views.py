from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Filme, Serie
from django.utils.text import slugify
from django.db.models import Avg
from django.contrib import messages

User = get_user_model()

def home(request):
    filmes = Filme.objects.all()
    series = Serie.objects.all()
    return render(request, 'index.html', {'filmes': filmes, 'series': series})

def cadastro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'cadastro.html', {'erro': str(e)})
    else:
        return render(request, 'cadastro.html')

def realizar_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            erro = 'Usuário ou senha inválidos.'
            return render(request, 'login.html', {'erro': erro})
    else:
        erro = None
        return render(request, 'login.html', {'erro': erro})

@login_required
def perfil(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'nome_completo': request.user.get_full_name()
    }
    return render(request, 'perfil.html', context)

@login_required
def editar_perfil(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        password = request.POST.get('password', '')
        if password:
            user.set_password(password)
        user.save()
        return redirect('perfil')
    return render(request, 'editar-perfil.html', {'user': user})

def fazer_logout(request):
    logout(request)
    return redirect('home')

def filmes(request):
    filmes = Filme.objects.all()
    return render(request, 'filmes.html', {'filmes': filmes})

def series(request):
    series = Serie.objects.all()
    return render(request, 'series.html', {'series': series})

def pagina_filme(request, url_slug):
    titulo = get_object_or_404(Titulo, slug=url_slug)
    filme = get_object_or_404(Filme, titulo=titulo)
    context = {
        'filme': filme,
    }
    return render(request, 'pagina-filme.html', context)

def pagina_serie(request, url_slug):
    titulo = get_object_or_404(Titulo, slug=url_slug)
    serie = get_object_or_404(Serie, titulo=titulo)
    context = {
        'serie': serie,
    }
    return render(request, 'pagina-serie.html', context)

