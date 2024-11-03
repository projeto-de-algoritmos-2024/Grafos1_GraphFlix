from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Filme, Serie, Comentario, Avaliacao
from django.utils.text import slugify
from .forms import AvaliacaoForm, ComentarioForm
from django.db.models import Avg
from django.contrib import messages


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
        # Limpar o contexto de erro quando a página é carregada via GET
        erro = None
        return render(request, 'login.html', {'erro': erro})
    
from django.contrib.auth.decorators import login_required
from .models import Comentario

@login_required
def perfil(request):
    comentarios_recentes = Comentario.objects.filter(usuario=request.user).order_by('-data_comentario')[:5]
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'nome_completo': request.user.get_full_name(),
        'comentarios_recentes': comentarios_recentes,
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

        # Atualizar os campos do usuário
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


#############################
# Comentários e avaliações #
#############################

def pagina_filme(request, url_slug):
    filme = get_object_or_404(Filme, url_slug=url_slug)
    comentarios = Comentario.objects.filter(avaliacao__filme=filme)
    
    # Verificar se o usuário já avaliou o filme
    user_avaliou_filme = False
    if request.user.is_authenticated:
        user_avaliou_filme = Avaliacao.objects.filter(filme=filme, usuario=request.user).exists()

    media_avaliacoes = filme.avaliacao_set.aggregate(media=Avg('classificacao'))['media']
    if media_avaliacoes is not None:
        media_avaliacoes = round(media_avaliacoes * 10, 2)

    # Inicializar o formulário de avaliação e o formulário de comentário
    avaliacao_form = None
    comentario_form = None

    # Se o usuário estiver logado, permitir comentar e avaliar
    if request.user.is_authenticated:
        if not user_avaliou_filme:
            if request.method == 'POST':
                avaliacao_form = AvaliacaoForm(request.POST)
                if avaliacao_form.is_valid():
                    avaliacao = avaliacao_form.save(commit=False)
                    avaliacao.usuario = request.user
                    avaliacao.filme = filme
                    avaliacao.save()
                    return redirect('pagina_filme', url_slug=url_slug)
            else:
                avaliacao_form = AvaliacaoForm()

        if request.method == 'POST':
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.avaliacao = Avaliacao.objects.get(filme=filme, usuario=request.user)
                comentario.save()
                return redirect('pagina_filme', url_slug=url_slug)
        else:
            comentario_form = ComentarioForm()

    context = {
        'filme': filme,
        'comentarios': comentarios,
        'avaliacao_form': avaliacao_form,
        'comentario_form': comentario_form,
        'user_avaliou_filme': user_avaliou_filme,
        'media_avaliacoes': media_avaliacoes,
    }
    return render(request, 'pagina-filme.html', context)

def pagina_serie(request, url_slug):
    serie = get_object_or_404(Serie, url_slug=url_slug)
    comentarios = Comentario.objects.filter(avaliacao__serie=serie)
    
    user_avaliou_serie = False
    if request.user.is_authenticated:
        user_avaliou_serie = Avaliacao.objects.filter(serie=serie, usuario=request.user).exists()

    media_avaliacoes = serie.avaliacao_set.aggregate(media=Avg('classificacao'))['media']
    if media_avaliacoes is not None:
        media_avaliacoes = round(media_avaliacoes * 10, 2)

    avaliacao_form = None
    comentario_form = None

    if request.user.is_authenticated:
        if not user_avaliou_serie:
            if request.method == 'POST':
                avaliacao_form = AvaliacaoForm(request.POST)
                if avaliacao_form.is_valid():
                    avaliacao = avaliacao_form.save(commit=False)
                    avaliacao.usuario = request.user
                    avaliacao.serie = serie
                    avaliacao.save()
                    return redirect('pagina_serie', url_slug=url_slug)
            else:
                avaliacao_form = AvaliacaoForm()

        if request.method == 'POST':
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.usuario = request.user
                comentario.avaliacao = Avaliacao.objects.get(serie=serie, usuario=request.user)
                comentario.save()
                return redirect('pagina_serie', url_slug=url_slug)
        else:
            comentario_form = ComentarioForm()

    context = {
        'serie': serie,
        'comentarios': comentarios,
        'avaliacao_form': avaliacao_form,
        'comentario_form': comentario_form,
        'user_avaliou_serie': user_avaliou_serie,
        'media_avaliacoes': media_avaliacoes,
    }
    return render(request, 'pagina-serie.html', context)

@login_required
def editar_comentario(request, tipo, url_slug, comentario_id):
    if tipo == 'filme':
        model_class = Filme
    elif tipo == 'serie':
        model_class = Serie
    else:
        return redirect('pagina_inicial')
    pagina_tipo = 'pagina_'+tipo

    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user == comentario.usuario:
        if request.method == 'POST':
            comentario_form = ComentarioForm(request.POST, instance=comentario)
            if comentario_form.is_valid():
                comentario_form.save()
                messages.success(request, 'Comentário atualizado com sucesso!')
            return redirect(pagina_tipo, url_slug=url_slug)
        else:
            comentario_form = ComentarioForm(instance=comentario)
        return render(request, 'editar-comentario.html', {'comentario_form': comentario_form})
    else:
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect(pagina_tipo, url_slug=url_slug)

@login_required
def excluir_comentario(request, tipo, url_slug, comentario_id):
    if tipo == 'filme':
        model_class = Filme
    elif tipo == 'serie':
        model_class = Serie
    else:
        return redirect('pagina_inicial')
    pagina_tipo = 'pagina_'+tipo

    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.method == 'POST':
        comentario.delete()
        return redirect(pagina_tipo, url_slug=url_slug)
    else:
        return render(request, 'excluir-comentario.html', {'comentario_texto': comentario.texto, 'tipo': tipo, 'url_slug': url_slug})


