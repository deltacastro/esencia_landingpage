# Django
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models 

class Loginfo(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'logs_usuario')
    fecha = models.DateTimeField(auto_now = True)
    accion = models.CharField(max_length = 50)
    folio_objeto = models.CharField(max_length = 10)
    tipo_objeto = models.CharField(max_length = 50)
    mensaje = models.CharField(max_length = 100)

class ExtraInfo(models.Model):
    folio = models.CharField(max_length = 10, unique = True)
    is_published = models.BooleanField(default = False)
    is_disabled = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['created_at']
        abstract = True
    
    def eliminar(self):
        self.is_disabled = True
        self.is_published = False
        self.save()
    
    def publicar(self):
        self.is_published = True
        self.save()
    
    def ocultar(self):
        self.is_published = False
        self.save()

class Multimedias(models.Model):
    media = models.ImageField(upload_to = '')
    nombre = models.CharField(max_length = 200)

    def save(self, *args, **kwargs):
        self.nombre = self.media.name
        super().save(*args, **kwargs)  

class Eventos(ExtraInfo):
    titulo = models.CharField('Título', max_length = 100)
    fecha = models.DateField('Fecha')
    hora = models.TimeField('Hora')
    lugar = models.CharField('Lugar', max_length = 50)
    media = models.ManyToManyField(Multimedias, related_name = 'media_eventos')

    class Meta(ExtraInfo.Meta):
        ordering = ['fecha', 'hora']

class Secciones(ExtraInfo):
    titulo = models.CharField('Título', max_length = 30)
    subtitulo = models.CharField('Subtítulo', max_length = 80)
    media = models.ManyToManyField(Multimedias, related_name = 'media_secciones')
    top = models.BooleanField('Fijar al principio', default = False)
    boton = models.BooleanField('Activar botón', default = False)
    txt_boton = models.CharField('Texto del botón', max_length = 15, null = True, blank = True)
    link_boton = models.URLField('Link del botón', null = True, blank = True)

class Asesorias_Tramites(ExtraInfo):
    titulo = models.CharField('Título', max_length = 50)
    contenido = models.CharField('Contenido', max_length = 200, default = '')
    extra = models.CharField('Contenido extra', max_length = 400, null = True, blank = True, default = '')
    media = models.ManyToManyField(Multimedias, related_name = 'media_asesorias')

class Noticias(ExtraInfo):
    titulo = models.CharField('Título' ,max_length = 100)
    contenido = models.CharField('Contenido', max_length = 150)
    media = models.ManyToManyField(Multimedias, related_name = 'media_noticias')

class Banner(ExtraInfo):
    multimedia = models.FileField(upload_to = 'banner/')