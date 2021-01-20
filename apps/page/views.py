# Django
# Almohadilla
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Page
from .forms import (
    fLogin, fSecciones, fMultimedias, fEventos, fMultimediasOpcional, fAsesorias_Tramites, fMultimediasSimple, fMultimediasSimpleOpcional, fNoticias
)
from .models import Secciones, Multimedias, Asesorias_Tramites, Noticias, Eventos, Loginfo

folio_prefixes = {'seccion': 'sec-', 'asesoria': 'ase-', 'noticia': 'not-', 'evento': 'eve-'}
action_messages = {'error': 'Ha ocurrido un error. Inténtelo de nuevo por favor'}
action_messages_log = {
    'create': 'ha creado',
    'delete': 'ha eliminado',
    'update': 'ha actualizado',
    'publish': 'ha publicado',
    'hide': 'ha ocultado'
}
verbose_object = {
    'seccion': 'una sección',
    'asesoria': 'una asesoría o trámite',
    'noticia': 'una noticia',
    'evento': 'un evento'
}

def main(request):
    return render(request, 'home.html')

def aviso_privacidad(request):
    return render(request, 'base/aviso_privacidad.html')

def vLogin(request):
    if request.user.is_authenticated:
	    return redirect('logout')
    if request.method == 'POST': 
        flogin = fLogin(request.POST)
        if flogin.is_valid():
            username = flogin.cleaned_data['username']
            password = flogin.cleaned_data['password']
            autenticar = authenticate(username = username, password = password)
            if autenticar is not None:
                login(request, autenticar)
                if request.user.is_superuser or request.user.is_staff:
                    return redirect('page:principal')
            else:
                messages.error(request, 'Usuario y/o contraseña no válidos')
            return redirect('login')
        print(flogin.errors)
    else:
        flogin = fLogin()
    context = {'flogin': flogin}
    return render(request, 'base/login.html', context)

def vLogout(request):
    logout(request)
    return redirect('login')

def vPrincipal(request):
    return render(request, 'page/principal.html')

# views for Secciones
@login_required
def vSecciones(request):
    secciones = Secciones.objects.all()
    if request.method == 'POST':
        usuario = request.user
        fseccion = fSecciones(request.POST)
        fmultimedia = fMultimedias(request.POST, request.FILES)
        if fseccion.is_valid() and fmultimedia.is_valid():  
            seccion = fseccion.save(commit = False)
            seccion.created_by = usuario
            seccion.save() 
            seccion.folio =  '{}{}'.format(folio_prefixes['seccion'], seccion.id)
            seccion.save()
            for media in request.FILES.getlist('media'):
                multimedia = Multimedias(media = media, nombre = media.name)
                multimedia.save()
                seccion.media.add(multimedia)
            messages.success(request, 'Sección agregada con éxito')
            # log
            add_log(usuario, 'create', seccion.folio, 'seccion', 
                '{} {} {}'.format(usuario.get_full_name(), action_messages_log['create'], verbose_object['seccion'])
            )
        else:   
            print(fseccion.errors)
            print(fmultimedia.errors)
            messages.error(request, action_messages['error'])
        return redirect('page:secciones')
    else:
        fmultimedia = fMultimedias()
        fseccion = fSecciones(label_suffix = '')
    context = {'secciones': secciones, 'fseccion': fseccion, 'fmultimedia': fmultimedia}
    return render(request, 'page/secciones/secciones.html', context)

@login_required
def vSeccionesEliminar(request, folio):
    if Secciones.objects.filter(folio = folio).exists():
        usuario = request.user
        seccion = Secciones.objects.get(folio = folio)
        seccion.eliminar()
        messages.success(request, 'Sección eliminada con éxito')
        # log
        add_log(usuario, 'delete', seccion.folio, 'seccion', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['delete'], verbose_object['seccion'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:secciones')

@login_required
def vSeccionesPublicar(request, folio):
    if Secciones.objects.filter(folio = folio).exists():
        usuario = request.user
        seccion = Secciones.objects.get(folio = folio)
        seccion.publicar()
        messages.success(request, 'Sección publicada con éxito')
        # log
        add_log(usuario, 'publish', seccion.folio, 'seccion', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['publish'], verbose_object['seccion'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:secciones')

@login_required
def vSeccionesOcultar(request, folio):
    if Secciones.objects.filter(folio = folio).exists():
        usuario = request.user
        seccion = Secciones.objects.get(folio = folio)
        seccion.ocultar()
        messages.success(request, 'Sección ocultada con éxito')
        # log
        add_log(usuario, 'hide', seccion.folio, 'seccion', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['hide'], verbose_object['seccion'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:secciones')

@login_required
def vSeccionesEditar(request, folio):
    if Secciones.objects.filter(folio = folio).exists():
        usuario = request.user
        seccion = Secciones.objects.get(folio = folio)
        if request.method == 'POST':
            fseccion = fSecciones(request.POST, instance = seccion)
            fmultimedia = fMultimediasOpcional(request.POST, request.FILES) 
            if not fseccion.has_changed() and not request.FILES.__contains__('media'):
                messages.warning(request, 'No se actualizó ningún dato')
            else:
                if fseccion.is_valid() and fmultimedia.is_valid():
                    if fseccion.has_changed():
                        fseccion.save()
                    if request.FILES.__contains__('media'):
                        for media in request.FILES.getlist('media'):
                            multimedia = Multimedias(media = media, nombre = media.name)
                            multimedia.save()
                            seccion.media.add(multimedia) 
                else:
                    messages.error(request, action_messages['error'])
                    return redirect('page:edSeccion', folio = seccion.folio)
                messages.success(request, 'Sección editada con éxito')
                # log
                add_log(usuario, 'update', seccion.folio, 'seccion', 
                    '{} {} {}'.format(usuario.get_full_name(), action_messages_log['update'], verbose_object['seccion'])
                )
            return redirect('page:secciones')
        else:
            fseccion = fSecciones(instance = seccion)
            fmultimedia = fMultimediasOpcional(request.POST, request.FILES)
        context = {'fseccion': fseccion, 'fmultimedia': fmultimedia, 'seccion': seccion}
        return render(request, 'page/secciones/edsecciones.html', context)
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:secciones')

@login_required
def vSeccionesEliminarImagen(request, folio, media_id):
    if Secciones.objects.filter(folio = folio).exists():
        seccion = Secciones.objects.get(folio = folio)
        if seccion.media.filter(id = media_id).exists():
            media = seccion.media.get(id = media_id)
            seccion.media.remove(media)
            messages.success(request, 'Multimedia eliminada con éxito')
        else:
            messages.error(request, action_messages['error'])
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:secciones')

# views for Asesorias y Trámites
@login_required
def vAsesorias(request):
    asesorias = Asesorias_Tramites.objects.all()
    if request.method == 'POST':
        usuario = request.user
        fasesoria = fAsesorias_Tramites(request.POST)
        fmultimedia = fMultimediasSimple(request.POST, request.FILES)
        if fasesoria.is_valid() and fmultimedia.is_valid():  
            asesoria = fasesoria.save(commit = False)
            asesoria.created_by = usuario
            asesoria.save() 
            asesoria.folio =  '{}{}'.format(folio_prefixes['asesoria'], asesoria.id)
            asesoria.save()
            asesoria.media.add(fmultimedia.save())
            messages.success(request, 'Asesoría o trámite agregada con éxito')
            # log
            add_log(usuario, 'create', asesoria.folio, 'asesoria', 
                '{} {} {}'.format(usuario.get_full_name(), action_messages_log['create'], verbose_object['asesoria'])
            )
        else:   
            print(fasesoria.errors)
            print(fmultimedia.errors)
            messages.error(request, action_messages['error'])
        return redirect('page:asesorias')
    else:
        fmultimedia = fMultimediasSimple()
        fasesoria = fAsesorias_Tramites(label_suffix = '')
    context = {'asesorias': asesorias, 'fasesoria': fasesoria, 'fmultimedia': fmultimedia}
    return render(request, 'page/asesorias/asesorias.html', context)

@login_required
def vAsesoriasEliminar(request, folio):
    if Asesorias_Tramites.objects.filter(folio = folio).exists():
        usuario = request.user
        asesoria = Asesorias_Tramites.objects.get(folio = folio)
        asesoria.eliminar()
        messages.success(request, 'Asesoria eliminada con éxito')
        # log
        add_log(usuario, 'delete', asesoria.folio, 'asesoria', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['delete'], verbose_object['asesoria'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:asesorias')

@login_required
def vAsesoriasPublicar(request, folio):
    if Asesorias_Tramites.objects.filter(folio = folio).exists():
        usuario = request.user
        asesoria = Asesorias_Tramites.objects.get(folio = folio)
        asesoria.publicar()
        messages.success(request, 'Asesoría publicada con éxito')
        # log
        add_log(usuario, 'publish', asesoria.folio, 'asesoria', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['publish'], verbose_object['asesoria'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:asesorias')

@login_required
def vAsesoriasOcultar(request, folio):
    if Asesorias_Tramites.objects.filter(folio = folio).exists():
        usuario = request.user
        asesoria = Asesorias_Tramites.objects.get(folio = folio)
        asesoria.ocultar()
        messages.success(request, 'Asesoría ocultada con éxito')
        # log
        add_log(usuario, 'hide', asesoria.folio, 'asesoria', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['hide'], verbose_object['asesoria'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:asesorias')

@login_required
def vAsesoriasEditar(request, folio):
    if Asesorias_Tramites.objects.filter(folio = folio).exists():
        usuario = request.user
        asesoria = Asesorias_Tramites.objects.get(folio = folio)
        if request.method == 'POST':
            fasesoria = fAsesorias_Tramites(request.POST, instance = asesoria)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES) 
            if not fasesoria.has_changed() and not request.FILES.__contains__('media'):
                messages.warning(request, 'No se actualizó ningún dato')
            else:
                if fasesoria.is_valid() and fmultimedia.is_valid():
                    if fasesoria.has_changed():
                        fasesoria.save()
                    if request.FILES.__contains__('media'):
                        asesoria.media.clear()
                        asesoria.media.add(fmultimedia.save()) 
                else:
                    messages.error(request, action_messages['error'])
                    return redirect('page:edAsesoria', folio = asesoria.folio)
                messages.success(request, 'Asesoría editada con éxito')
                # log
                add_log(usuario, 'update', asesoria.folio, 'asesoria', 
                    '{} {} {}'.format(usuario.get_full_name(), action_messages_log['update'], verbose_object['asesoria'])
                )
            return redirect('page:asesorias')
        else:
            fasesoria = fAsesorias_Tramites(instance = asesoria)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES)
        context = {'fasesoria': fasesoria, 'fmultimedia': fmultimedia, 'asesoria': asesoria}
        return render(request, 'page/asesorias/edasesorias.html', context)
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:asesorias')

# views for Noticias
@login_required
def vNoticias(request):
    noticias = Noticias.objects.all()
    if request.method == 'POST':
        usuario = request.user
        fnoticia = fNoticias(request.POST)
        fmultimedia = fMultimediasSimple(request.POST, request.FILES)
        if fnoticia.is_valid() and fmultimedia.is_valid():  
            noticia = fnoticia.save(commit = False)
            noticia.created_by = usuario
            noticia.save() 
            noticia.folio =  '{}{}'.format(folio_prefixes['noticia'], noticia.id)
            noticia.save()
            for media in request.FILES.getlist('media'):
                multimedia = Multimedias(media = media, nombre = media.name)
                multimedia.save()
                noticia.media.add(multimedia)
            messages.success(request, 'Noticia agregada con éxito')
            # log
            add_log(usuario, 'create', noticia.folio, 'noticia', 
                '{} {} {}'.format(usuario.get_full_name(), action_messages_log['create'], verbose_object['noticia'])
            )
        else:   
            print(fnoticia.errors)
            print(fmultimedia.errors)
            messages.error(request, action_messages['error'])
        return redirect('page:noticias')
    else:
        fmultimedia = fMultimedias()
        fnoticia = fNoticias(label_suffix = '')
    context = {'noticias': noticias, 'fnoticia': fnoticia, 'fmultimedia': fmultimedia}
    return render(request, 'page/noticias/noticias.html', context)

@login_required
def vNoticiasEliminar(request, folio):
    if Noticias.objects.filter(folio = folio).exists():
        usuario = request.user
        noticia = Noticias.objects.get(folio = folio)
        noticia.eliminar()
        messages.success(request, 'Noticia eliminada con éxito')
        # log
        add_log(usuario, 'delete', noticia.folio, 'noticia', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['delete'], verbose_object['noticia'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:noticias')

@login_required
def vNoticiasPublicar(request, folio):
    if Noticias.objects.filter(folio = folio).exists():
        usuario = request.user
        noticia = Noticias.objects.get(folio = folio)
        noticia.publicar()
        messages.success(request, 'Noticia publicada con éxito')
        # log
        add_log(usuario, 'publish', noticia.folio, 'noticia', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['publish'], verbose_object['noticia'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:noticias')

@login_required
def vNoticiasOcultar(request, folio):
    if Noticias.objects.filter(folio = folio).exists():
        usuario = request.user
        noticia = Noticias.objects.get(folio = folio)
        noticia.ocultar()
        messages.success(request, 'Noticia ocultada con éxito')
        # log
        add_log(usuario, 'hide', noticia.folio, 'noticia', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['hide'], verbose_object['noticia'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:noticias')

@login_required
def vNoticiasEditar(request, folio):
    if Noticias.objects.filter(folio = folio).exists():
        usuario = request.user
        noticia = Noticias.objects.get(folio = folio)
        if request.method == 'POST':
            fnoticia = fNoticias(request.POST, instance = noticia)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES) 
            if not fnoticia.has_changed() and not request.FILES.__contains__('media'):
                messages.warning(request, 'No se actualizó ningún dato')
            else:
                if fnoticia.is_valid() and fmultimedia.is_valid():
                    if fnoticia.has_changed():
                        fnoticia.save()
                    if request.FILES.__contains__('media'):
                        noticia.media.clear()
                        noticia.media.add(fmultimedia.save()) 
                else:
                    print(fnoticia.errors)
                    print(fmultimedia.errors)
                    messages.error(request, action_messages['error'])
                    return redirect('page:edNoticia', folio = noticia.folio)
                messages.success(request, 'Noticia editada con éxito')
                # log
                add_log(usuario, 'update', noticia.folio, 'noticia', 
                    '{} {} {}'.format(usuario.get_full_name(), action_messages_log['update'], verbose_object['noticia'])
                )  
            return redirect('page:noticias')
        else:
            fnoticia = fNoticias(instance = noticia)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES)
        context = {'fnoticia': fnoticia, 'fmultimedia': fmultimedia, 'noticia': noticia}
        return render(request, 'page/noticias/ednoticias.html', context)
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:noticias')

# views for Eventos
@login_required
def vEventos(request):
    eventos = Eventos.objects.all()
    if request.method == 'POST':
        usuario = request.user
        fevento = fEventos(request.POST)
        fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES)
        if fevento.is_valid() and fmultimedia.is_valid():  
            evento = fevento.save(commit = False)
            evento.created_by = usuario
            evento.save() 
            evento.folio =  '{}{}'.format(folio_prefixes['evento'], evento.id)
            evento.save()
            for media in request.FILES.getlist('media'):
                multimedia = Multimedias(media = media, nombre = media.name)
                multimedia.save()
                evento.media.add(multimedia)
            messages.success(request, 'Evento agregado con éxito')
            # log
            add_log(usuario, 'create', evento.folio, 'evento', 
                '{} {} {}'.format(usuario.get_full_name(), action_messages_log['create'], verbose_object['evento'])
            )
        else:   
            print(fevento.errors)
            print(fmultimedia.errors)
            messages.error(request, action_messages['error'])
        return redirect('page:eventos')
    else:
        fmultimedia = fMultimediasSimpleOpcional()
        fevento = fEventos(label_suffix = '')
    context = {'eventos': eventos, 'fevento': fevento, 'fmultimedia': fmultimedia}
    return render(request, 'page/eventos/eventos.html', context)

@login_required
def vEventosEliminar(request, folio):
    if Eventos.objects.filter(folio = folio).exists():
        usuario = request.user
        evento = Eventos.objects.get(folio = folio)
        evento.eliminar()
        messages.success(request, 'Evento eliminado con éxito')
        # log
        add_log(usuario, 'delete', evento.folio, 'evento', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['delete'], verbose_object['evento'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:eventos')

@login_required
def vEventosPublicar(request, folio):
    if Eventos.objects.filter(folio = folio).exists():
        usuario = request.user
        evento = Eventos.objects.get(folio = folio)
        evento.publicar()
        messages.success(request, 'Evento publicado con éxito')
        # log
        add_log(usuario, 'publish', evento.folio, 'evento', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['publish'], verbose_object['evento'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:eventos')

@login_required
def vEventosOcultar(request, folio):
    if Eventos.objects.filter(folio = folio).exists():
        usuario = request.user
        evento = Eventos.objects.get(folio = folio)
        evento.ocultar()
        messages.success(request, 'Evento ocultado con éxito')
        # log
        add_log(usuario, 'hide', evento.folio, 'evento', 
            '{} {} {}'.format(usuario.get_full_name(), action_messages_log['hide'], verbose_object['evento'])
        )
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:eventos')

@login_required
def vEventosEditar(request, folio):
    if Eventos.objects.filter(folio = folio).exists():
        usuario = request.user
        evento = Eventos.objects.get(folio = folio)
        if request.method == 'POST':
            fevento = fEventos(request.POST, instance = evento)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES) 
            if not fevento.has_changed() and not request.FILES.__contains__('media'):
                messages.warning(request, 'No se actualizó ningún dato')
            else:
                if fevento.is_valid() and fmultimedia.is_valid():
                    if fevento.has_changed():
                        fevento.save()
                    if request.FILES.__contains__('media'):
                        evento.media.clear()
                        evento.media.add(fmultimedia.save()) 
                else:
                    print(fevento.errors)
                    print(fmultimedia.errors)
                    messages.error(request, action_messages['error'])
                    return redirect('page:edEvento', folio = evento.folio)
                messages.success(request, 'Evento editado con éxito')
                # log
                add_log(usuario, 'update', evento.folio, 'evento', 
                    '{} {} {}'.format(usuario.get_full_name(), action_messages_log['update'], verbose_object['evento'])
                )
            return redirect('page:eventos')
        else:
            fevento = fEventos(instance = evento)
            fmultimedia = fMultimediasSimpleOpcional(request.POST, request.FILES)
        context = {'fevento': fevento, 'fmultimedia': fmultimedia, 'evento': evento}
        return render(request, 'page/eventos/edeventos.html', context)
    else:
        messages.error(request, action_messages['error'])
    return redirect('page:eventos')

# functions for LogInfo
def add_log(user, action, folio, object_type, message):
    try:
        Loginfo.objects.create(
            usuario = user, 
            accion = action, 
            folio_objeto = folio, 
            tipo_objeto = object_type, 
            mensaje = message
        )
    except Exception as e:
        print(e)












