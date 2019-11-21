# Django
from django import forms
from django.contrib.auth.models import User
# page Models
from .models import Eventos, Secciones, Asesorias_Tramites, Noticias, Banner, Multimedias

class fLogin(forms.Form):
    username = forms.CharField(label = 'Usuario', label_suffix = '', required = True, max_length = 50, 
        error_messages = {
            'required': 'El usuario es requerido',
            'max_length': 'Ese usuario es demasiado largo',
            'blank': 'El usuario no debe estar vacío'
        }
    )
    password = forms.CharField(label = 'Contraseña', label_suffix = '', 
        widget =  forms.PasswordInput,
        error_messages = { 
            'blank': "La contraseña no debe estar vacía",
            'required': "La contraseña es requerida"
        }
    )

class fMultimedias(forms.ModelForm):
    class Meta:
        model = Multimedias
        fields = ['media']
        widgets = {
            'media': forms.ClearableFileInput(attrs={'multiple': 'true'})
        }

class fMultimediasOpcional(fMultimedias):
    def __init__(self, *args, **kwargs):
        super(fMultimedias, self).__init__(*args, **kwargs)
        self.fields['media'].required = False

class fMultimediasSimple(fMultimedias):
    class Meta(fMultimedias.Meta):
        widgets = {
            'media': forms.ClearableFileInput()
        }

class fMultimediasSimpleOpcional(fMultimediasSimple, fMultimediasOpcional):
    pass

class fSecciones(forms.ModelForm):
    class Meta:
        model = Secciones
        fields = ['titulo', 'subtitulo']

class fAsesorias_Tramites(forms.ModelForm):
    class Meta:
        model = Asesorias_Tramites
        fields = ['titulo', 'contenido', 'extra']
        widgets = {
            'contenido': forms.Textarea(attrs = {'class': 'materialize-textarea'}),
            'extra': forms.Textarea(attrs = {'class': 'materialize-textarea'})
        }

class fNoticias(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ['titulo']

class fEventos(forms.ModelForm):
    class Meta:
        model = Eventos
        fields = ['titulo', 'fecha', 'hora', 'lugar']
        widgets = {
            'fecha': forms.TextInput(attrs = {'class': 'datepicker'}),
            'hora': forms.TextInput(attrs = {'class': 'timepicker'}) 
        }