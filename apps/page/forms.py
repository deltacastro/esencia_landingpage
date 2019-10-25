# Django
from django import forms
# page Models
from .models import Eventos, Secciones, Asesorias_Tramites, Noticias, Banner

class fEventos(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['titulo', 'fecha']
        

class fSecciones(forms.ModelForm):
    class Meta:
        model = Secciones
        fields = ['titulo', 'subtitulo', 'orientacion', 'imagen']

class fAsesorias_Tramites(forms.ModelForm):
    class Meta:
        model = Asesorias_Tramites
        fields = ['titulo', 'subtitulo', 'imagen']

class fNoticias(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ['titulo', 'contenido', 'imagen']

class fBanner(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['multimedia']