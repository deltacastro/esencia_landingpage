# Django
from django import template
from django.utils import timezone
# App page
from ..models import Secciones, Asesorias_Tramites, Noticias, Eventos
register = template.Library()

@register.inclusion_tag('page/secciones/tag/secciontag.html')
def secciones(sec_for):
    if sec_for == 'public':
        secciones = Secciones.objects.filter(is_published = True)
    if sec_for == 'admin':
        secciones = Secciones.objects.filter(is_disabled = False)
    return {'secciones' : secciones, 'sec_for': sec_for}

@register.inclusion_tag('page/asesorias/tag/asesoriastag.html')
def asesorias(ase_for):
    if ase_for == 'public':
        asesorias = Asesorias_Tramites.objects.filter(is_published = True)
    if ase_for == 'admin':
        asesorias = Asesorias_Tramites.objects.filter(is_disabled = False)
    return {'asesorias' : asesorias, 'ase_for': ase_for}

@register.inclusion_tag('page/noticias/tag/noticiastag.html')
def noticias(not_for):
    if not_for == 'public':
        noticias = Noticias.objects.filter(is_published = True)
    if not_for == 'admin':
        noticias = Noticias.objects.filter(is_disabled = False)
    return {'noticias' : noticias, 'not_for': not_for}

@register.inclusion_tag('page/eventos/tag/eventostag.html')
def eventos(eve_for):
    date_time = timezone.localtime()
    if eve_for == 'public':
        eventos = Eventos.objects.filter(is_published = True, fecha__gte = date_time.date(), hora__gte = date_time.strftime("%H:%M:%S"))
    if eve_for == 'admin':
        eventos = Eventos.objects.filter(is_disabled = False, fecha__gte = date_time.date(), hora__gte = date_time.strftime("%H:%M:%S"))
    return {'eventos' : eventos, 'eve_for': eve_for}

@register.filter
def rightOrLeft(num):
    if num % 2 == 0:
        return True
    else:
        return False