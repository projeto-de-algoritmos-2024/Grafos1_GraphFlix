from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import Filme, Serie, Titulo, Genero, Prefere,Favorita,Elenco
from django.utils.text import slugify
from django.db.models import Avg
from django.contrib import messages
from graphflix_app.scripts.busca_dfs import buscar_dfs
from django.db.models import Case, When

User = get_user_model()

def home(request):
    filmes = Filme.objects.all().order_by('-id_filme')[:10]
    series = Serie.objects.all().order_by('-id_serie')[:10]
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

from django.shortcuts import redirect

def realizar_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url if next_url else 'home')
        else:
            erro = 'Usuário ou senha inválidos.'
            return render(request, 'login.html', {'erro': erro})
    else:
        erro = None
        return render(request, 'login.html', {'erro': erro})


@login_required
def perfil(request):
    favoritos = Favorita.objects.filter(usuario=request.user)
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'nome_completo': request.user.get_full_name(),
        'favoritos': favoritos,
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
    generos = Genero.objects.filter(possui__titulo=titulo)
    avaliacao_xdez = round(filme.titulo.avaliacao * 10, 2)
    
    elenco = Elenco.objects.filter(titulo=titulo)
    elenco_str = ', '.join([e.elenco for e in elenco])

    # Se o usuário está logado, verificar se o filme está nos favoritos
    is_favorito = filme.titulo.favorita_set.filter(usuario=request.user).exists() if request.user.is_authenticated else False

    context = {
        'filme': filme,
        'generos': generos,
        'avaliacao_xdez': avaliacao_xdez,
        'elenco': elenco_str,
        'is_favorito': is_favorito,  # Variável indicando se o filme é favorito
    }

    return render(request, 'pagina-filme.html', context)

def pagina_serie(request, url_slug):
    titulo = get_object_or_404(Titulo, slug=url_slug)
    serie = get_object_or_404(Serie, titulo=titulo)
    generos = Genero.objects.filter(possui__titulo=titulo)
    avaliacao_xdez = round(serie.titulo.avaliacao * 10, 2)

    # Verificar se a série é favorita
    is_favorito = serie.titulo.favorita_set.filter(usuario=request.user).exists() if request.user.is_authenticated else False


    elenco = Elenco.objects.filter(titulo=titulo)
    serie.criador = serie.criador.split(", ")

    context = {
        'serie': serie,
        'generos': generos,
        'avaliacao_xdez': avaliacao_xdez,
        'elenco': elenco,
        'is_favorito': is_favorito,
    }
    return render(request, 'pagina-serie.html', context)


@login_required
def recomendacoes(request):
    usuario = request.user
    generos = Genero.objects.all()

    if request.method == 'POST':
        nota_minima = request.POST.get('nota_minima')
        usuario.notaMinima = float(nota_minima)
        usuario.save()

        generos_selecionados = request.POST.getlist('generos')
        Prefere.objects.filter(usuario=usuario).delete()
        for genero_id in generos_selecionados:
            genero = Genero.objects.get(id=genero_id)
            Prefere.objects.create(usuario=usuario, genero=genero)

        return redirect('recomendacoes') 

    generos_preferidos = Prefere.objects.filter(usuario=usuario).values_list('genero_id', flat=True)

    # funcao de buscaaa
    # recomendados = buscar_dfs(usuario)
    ids_recomendados = [recomendado['id'] for recomendado in buscar_dfs(usuario)]
    recomendados = Titulo.objects.filter(id__in=ids_recomendados).order_by(
    Case(*[When(id=id, then=pos) for pos, id in enumerate(ids_recomendados)])
)


    #print("Na views: recomendados:", ids_recomendados)

    context = {
        'generos': generos,
        'generos_preferidos': generos_preferidos,
        'nota_minima': str(usuario.notaMinima).replace(',', '.'),
        'recomendados': recomendados,
    }
    return render(request, 'recomendacoes.html', context)


@login_required
def toggle_favorito(request, titulo_id):
    titulo = get_object_or_404(Titulo, id=titulo_id)
    favorito, created = Favorita.objects.get_or_create(usuario=request.user, titulo=titulo)

    if not created:
        
        favorito.delete()
        messages.success(request, f"'{titulo.titulo}' foi removido dos seus favoritos.")
    else:
   
        messages.success(request, f"'{titulo.titulo}' foi adicionado aos seus favoritos.")

    return redirect('pagina_'+titulo.tipo, url_slug=titulo.slug)