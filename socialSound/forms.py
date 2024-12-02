from django.forms import ModelForm
from django import forms
from .models import Usuario

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
        required =True,
        widget=forms.TextInput(attrs={
            'class': 'formd-control',
            'placeholder': 'nombre de usuario'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
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


