from django.forms import ModelForm
from django import forms
from .models import Usuario, Album, DetalleAlbum
from datetime import date
from django.core.exceptions import ValidationError

class UsuarioModelForm(ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    nombre_usuario = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['email', 'nombre_usuario', 'password', 'bio', 'ciudad', 'fecha_nac', 'foto_perfil']
        labels = '__all__'
        help_texts = {
            'email': '100 caracteres como máximo',
            'nombre_usuario': '100 caracteres como máximo',
            'password': '100 caracteres como máximo',
            'ciudad': '150 caracteres como máximo'
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe aquí tu descripción...',
                'rows': 4,
                'cols': 50
            }),
            'fecha_nac': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'})
        }
        localized_fields = ['fecha_nac']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password'].initial = self.instance.password

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data.get('nombre_usuario')
        if self.instance.pk:
            if Usuario.objects.exclude(pk=self.instance.pk).filter(nombre_usuario=nombre_usuario).exists():
                raise forms.ValidationError('Nombre de usuario en uso')
        else:
            if Usuario.objects.filter(nombre_usuario=nombre_usuario).exists():
                raise forms.ValidationError('Nombre de usuario en uso')
        return nombre_usuario

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance.pk:
            if Usuario.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise forms.ValidationError('Email ya registrado')
        else:
            if Usuario.objects.filter(email=email).exists():
                raise forms.ValidationError('Email ya registrado')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if 'password' in self.cleaned_data and self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    nombre_usuario = forms.CharField(
        required=True,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario'
        })
    )
    password = forms.CharField(
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        nombre_usuario = cleaned_data.get('nombre_usuario')
        password = cleaned_data.get('password')

        if nombre_usuario and password:
            try:
                user = Usuario.objects.get(nombre_usuario=nombre_usuario)
                if not user.check_password(password):
                    raise forms.ValidationError('Contraseña incorrecta')
            except Usuario.DoesNotExist:
                 raise forms.ValidationError('Usuario no encotnrado')
        return cleaned_data


class BusquedaAvanzadaUsuarioForm(forms.Form):
    nombre_usuario= forms.CharField(
        label='Nombre usuario',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar usuario por nombre...'
        })
    )

    ciudad=forms.CharField(
        label='Ciudad',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por ciudad...'
        })
    ) 

    edad_min = forms.IntegerField(
        label='edad mínima',
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    
    edad_max = forms.IntegerField(
            label='Edad máxima',
            required=False,
            widget=forms.NumberInput(attrs={
                'class': 'formd-control'
            })
    )

    bio_contains=forms.CharField(
        label='Buscar según biografía',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar en la biografía'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        edad_min = cleaned_data.get('edad_min')
        edad_max = cleaned_data.get('edad_max')

        # Validamos que al menos un campo esté lleno
        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                "Debes especificar al menos un criterio de búsqueda"
            )
        
        # Validamos rango de edad
        if edad_min and edad_max and edad_min > edad_max:
            raise forms.ValidationError(
                "La edad mínima no puede ser mayor que la edad máxima"
            )
        
        return cleaned_data



### CRUD ALBUM
class AlbumModelForm(forms.ModelForm):
    titulo = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    artista = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Album
        fields = ['titulo', 'artista', 'portada', 'descripcion']
        help_texts = {
            'titulo': '200 caracteres como máximo',
            'artista': '200 caracteres como máximo',
            'descripcion': 'Describe tu álbum'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe aquí tu álbum',
                'rows': 4,
                'cols': 50
            }),
            'portada': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        titulo = cleaned_data.get('titulo')
        if not titulo:
            errors['titulo'] = 'El título es obligatorio'
        elif len(titulo) > 200:
            errors['titulo'] = 'El título no puede exceder los 200 caracteres'

        artista = cleaned_data.get('artista')
        if not artista:
            errors['artista'] = 'El artista es obligatorio'
        elif len(artista) > 200:
            errors['artista'] = 'El nombre del artista no puede exceder los 200 caracteres'

        # Comprobar si el álbum existe (pero ignorar si es el mismo álbum que estamos editando)
        if titulo and artista:
            album_id = self.instance.id
            album_existe = Album.objects.filter(titulo=titulo, artista=artista).exclude(id=album_id).exists()
            if album_existe:
                errors['titulo'] = 'Ya existe un álbum con este título y artista'

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class DetalleAlbumModelForm(forms.ModelForm):
    class Meta:
        model = DetalleAlbum
        fields = ['productor', 'numero_pistas', 'estudio_grabacion', 'sello_discografico']
        widgets = {
            'productor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del productor'
            }),
            'estudio_grabacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estudio de grabación'
            }),
            'numero_pistas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de pistas'
            }),
            'sello_discografico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sello discográfico'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

  
        productor = cleaned_data.get('productor')
        if not productor:
            errors['productor'] = 'El productor es obligatorio'
        elif len(productor) > 200:
            errors['productor'] = 'El nombre del productor no puede exceder los 200 caracteres'

      
        numero_pistas = cleaned_data.get('numero_pistas')
        if not numero_pistas or numero_pistas <= 0:
            errors['numero_pistas'] = 'El número de pistas debe ser un número positivo'

        
        estudio = cleaned_data.get('estudio_grabacion')
        if estudio and len(estudio) > 200:
            errors['estudio_grabacion'] = 'El nombre del estudio no puede exceder los 200 caracteres'

       
        sello = cleaned_data.get('sello_discografico')
        if sello and len(sello) > 100:
            errors['sello_discografico'] = 'El nombre del sello no puede exceder los 100 caracteres'

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, inicializar con los valores existentes
        if self.instance and self.instance.pk:
            for field in self.fields:
                if hasattr(self.instance, field):
                    self.fields[field].initial = getattr(self.instance, field)


class BusquedaAvanzadaAlbumForm(forms.Form):

    titulo = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título'
        })
    )

    artista = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por artista'
        })
    )

    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


    def clean(self):
        cleaned_data = super().clean()

        #validamos que al menos un campo esté lleno
        if not any(cleaned_data.values()):
            self.add_error(None, 'Debes especificar al menos un criterio de búesqueda')

        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')

        if fecha_desde and fecha_hasta:
            if fecha_desde > fecha_hasta:
                self.add_error('fecha_desde', 'La fecha inicial no puede ser posterior a la fecha final')
                self.add_error('fecha_hasta', 'La fecha final no puede ser anterior a la fecha inicial')
        
        titulo = cleaned_data.get('titulo')
        if titulo and len(titulo) < 3:
            self.add_error('titulo', 'El título debe tener al menos 3 caracteres de búsqueda')
        

        artista = cleaned_data.get('artista')
        if artista and len(artista) < 3:
            self.add_error('artista', 'Ingresa al menos 3 caracteres para buscar por artista')

        return cleaned_data


