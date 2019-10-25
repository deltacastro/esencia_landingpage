# Django
from django.contrib.auth.models import User
from django.db import models 

class Eventos(models.Model):
    folio = models.CharField(max_length = 10)
    titulo = models.CharField(max_length = 100)
    fecha = models.DateTimeField()
    imagen = models.ImageField(upload_to = 'eventos/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(null = True)
    deleted_at = models.DateTimeField(null = True)
    created_by = models.OneToOneField(User, on_delete = models.PROTECT, related_name = 'created_events')
    updated_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'updated_events')
    deleted_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'deleted_events')

class Secciones(models.Model):
    orientation_choices = [
        (True, 'Derecha'),
        (False, 'Izquierda')
    ]
    folio = models.CharField(max_length = 10)
    titulo = models.CharField(max_length = 100)
    subtitulo = models.CharField(max_length = 150)
    orientacion = models.BooleanField(default = True, choices = orientation_choices)
    imagen = models.ImageField(upload_to = 'secciones/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(null = True)
    deleted_at = models.DateTimeField(null = True)
    created_by = models.OneToOneField(User, on_delete = models.PROTECT, related_name = 'created_sections')
    updated_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'updated_sections')
    deleted_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'deleted_sections')

class Asesorias_Tramites(models.Model):
    folio = models.CharField(max_length = 10)
    titulo = models.CharField(max_length = 100)
    subtitulo = models.CharField(max_length = 150)
    imagen = models.ImageField(upload_to = 'asesorias_tramites/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    created_by = models.OneToOneField(User, on_delete = models.PROTECT, related_name = 'created_advice')
    updated_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'updated_advice')
    deleted_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'deleted_advice')

class Noticias(models.Model):
    folio = models.CharField(max_length = 10)
    titulo = models.CharField(max_length = 100)
    contenido = models.CharField(max_length = 150)
    imagen = models.ImageField(upload_to = 'noticias/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    created_by = models.OneToOneField(User, on_delete = models.PROTECT, related_name = 'created_news')
    updated_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'updated_news')
    deleted_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'deleted_news')

class Banner(models.Model):
    multimedia = models.FileField(upload_to = 'banner/')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    created_by = models.OneToOneField(User, on_delete = models.PROTECT, related_name = 'created_banner')
    updated_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'updated_banner')
    deleted_by = models.OneToOneField(User, null = True, on_delete = models.PROTECT, related_name = 'deleted_banner')