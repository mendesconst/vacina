from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Usuario
from cursos.models import Cursos
from django.shortcuts import redirect, get_object_or_404
import hashlib
import time

def cadastro(request):
    if request.session.get('usuario'):
        return sair(request)
    status=request.GET.get('status')
    return render(request,'cadastro.html', {'status': status})


def login(request):
    if request.session.get('usuario'):
        return redirect('/home')
    status = request.GET.get('status')
    return render(request,'login.html', {'status': status})
    
def valida_cadastro(request):
    nome = request.POST.get('nome')
    email=request.POST.get('email')
    senha=request.POST.get('senha')

    usuario_existe=Usuario.objects.filter(email=email)
    if len(senha) < 8 or len(senha) >12:
        return redirect('/auth/cadastro?status=1')

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro?status=2')

    if len(usuario_existe) > 0:
        return redirect('/auth/cadastro?status=3')
    try:
        senha = hashlib.sha256(senha.encode()).hexdigest()
        usuario=Usuario(nome=nome,
                        senha=senha,
                        email=email)
        usuario.save()
        return redirect('/auth/cadastro?status=0')
    except:
        return HttpResponse('ERRO INTERNO DO SISTEMA, TENTE NOVAMENTE EM INSTANTES')

def curso_escolhido(request, id):
        cursoEscolhido = Cursos.objects.get(id = id)
        request_usuario = request.session.get('usuario')
        request_usuario = Usuario.objects.get(id=request_usuario)
        request_usuario.curso_selecionado = cursoEscolhido
        usuario=request_usuario
        usuario.save()
        time.sleep(5) 
        return sair(request) 

def valida_login(request):
    email=request.POST.get('email')
    senha=request.POST.get('senha')
    senha=hashlib.sha256(senha.encode()).hexdigest()
    usuarios=Usuario.objects.filter(email=email).filter(senha=senha)

    if len(usuarios) ==0:
        return redirect('/auth/login?status=1')
    elif len(usuarios) > 0:
        request.session['usuario'] = usuarios[0].id
        return redirect('/home')


def sair(request):
    request.session.flush()
    return redirect('/auth/login')
