# Django
from django.urls import path
# App page
from .views import (
    vPrincipal,
    vSecciones, vSeccionesEliminar, vSeccionesEditar, vSeccionesPublicar, vSeccionesOcultar, vSeccionesEliminarImagen,
    vAsesorias, vAsesoriasEliminar, vAsesoriasPublicar, vAsesoriasOcultar, vAsesoriasEditar,
    vNoticias, vNoticiasEliminar, vNoticiasPublicar, vNoticiasOcultar, vNoticiasEditar,
    vEventos, vEventosEliminar, vEventosPublicar, vEventosOcultar, vEventosEditar
) 

app_name = 'page'

urlpatterns = [
    path('', vPrincipal, name = 'principal'),
    # Secciones
    path('seccion/', vSecciones, name = 'secciones'),
    path('seccion/<str:folio>/eliminar', vSeccionesEliminar, name = 'eSeccion'),
    path('seccion/<str:folio>/editar', vSeccionesEditar, name = 'edSeccion'),
    path('seccion/<str:folio>/publicar', vSeccionesPublicar, name = 'pSeccion'),
    path('seccion/<str:folio>/ocultar', vSeccionesOcultar, name = 'oSeccion'),
    path('seccion/<str:folio>/media/<int:media_id>/eliminar', vSeccionesEliminarImagen, name = 'eMediaSeccion'),
    # Asesorias
    path('asesoria/', vAsesorias, name = 'asesorias'),
    path('asesoria/<str:folio>/eliminar', vAsesoriasEliminar, name = 'eAsesoria'),
    path('asesoria/<str:folio>/editar', vAsesoriasEditar, name = 'edAsesoria'),
    path('asesoria/<str:folio>/publicar', vAsesoriasPublicar, name = 'pAsesoria'),
    path('asesoria/<str:folio>/ocultar', vAsesoriasOcultar, name = 'oAsesoria'),
    # Noticias
    path('noticia/', vNoticias, name = 'noticias'),
    path('noticia/<str:folio>/eliminar', vNoticiasEliminar, name = 'eNoticia'),
    path('noticia/<str:folio>/editar', vNoticiasEditar, name = 'edNoticia'),
    path('noticia/<str:folio>/publicar', vNoticiasPublicar, name = 'pNoticia'),
    path('noticia/<str:folio>/ocultar', vNoticiasOcultar, name = 'oNoticia'),
    # Eventos
    path('evento/', vEventos, name = 'eventos'),
    path('evento/<str:folio>/eliminar', vEventosEliminar, name = 'eEvento'),
    path('evento/<str:folio>/editar', vEventosEditar, name = 'edEvento'),
    path('evento/<str:folio>/publicar', vEventosPublicar, name = 'pEvento'),
    path('evento/<str:folio>/ocultar', vEventosOcultar, name = 'oEvento'),
]