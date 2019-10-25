# Django
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# Page Forms
from .forms import fEventos

def vLogin(request):
    if request.user.is_authenticated:
	    return redirect('logout')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        autenticar = authenticate(username = username, password = password)
        if autenticar is not None:
            login(request, autenticar)
            if request.user.is_superuser or request.user.is_staff:
                return redirect('rEvento')
        else:
            messages.error(request, 'Usuario y/o contraseña no válidos')
        return redirect('login')
    return render(request, 'base/login.html')

def vLogout(request):
    logout(request)
    return redirect('login')

def vRegistroEventos(request):
    user = User.objects.latest('id')
    if request.method == 'POST':
        fevento = fEventos(request.POST)
        if fevento.is_valid():
            evento = fevento.save(commit = False)
            print(evento.cleaned_data)
        print(fevento.errors.as_json())
    else:
        fevento = fEventos()
    context = {'fevento': fevento}
    return render(request, 'admin/nvo_evento.html', context)