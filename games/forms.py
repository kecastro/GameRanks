from django import forms
from django.contrib.auth.models import User
from .models import *
from django.core.validators import RegexValidator

username_validator = RegexValidator(r'^[0-9a-z]*$',
                                    "Solo letras y numeros (sin espacios ni mayusculas)")
first_name_validator = RegexValidator(r'^[0-9a-zA-Z]*$',
                                      "Ingrese un nombre valido (solo primer nombre)")
last_name_validator = RegexValidator(r'^[0-9a-zA-Z]*$',
                                     "Ingrese un apellido valido (solo primer apellido)")


class UserForm(forms.ModelForm):
    username = forms.CharField(validators=[username_validator], max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(validators=[first_name_validator], label='Nombre', max_length=20, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(validators=[last_name_validator], label='Apellido', max_length=20, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar contraseña',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password:
            if len(password) < 6:
                raise forms.ValidationError("La contraseña debe tener una longitud minima de 6 caracteres")
        if not password2:
            raise forms.ValidationError("Debe confirmar la contraseña")
        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class UserProfileForm(forms.ModelForm):
    CITIES = (
        ('Arauca', 'Arauca'),
        ('Armenia', 'Armenia'),
        ('Barranquilla', 'Barranquilla'),
        ('Bogotá', 'Bogotá'),
        ('Bucaramanga', 'Bucaramanga'),
        ('Cali', 'Cali'),
        ('Cartagena', 'Cartagena'),
        ('Cúcuta', 'Cúcuta'),
        ('Florencia', 'Florencia'),
        ('Ibagué', 'Ibagué'),
        ('Leticia', 'Leticia'),
        ('Manizales', 'Manizales'),
        ('Medellín', 'Medellín'),
        ('Mitú', 'Mitú'),
        ('Mocoa', 'Mocoa'),
        ('Montería', 'Montería'),
        ('Neiva', 'Neiva'),
        ('Pasto', 'Pasto'),
        ('Pereira', 'Pereira'),
        ('Popayán', 'Popayán'),
        ('Puerto Carreño', 'Puerto Carreño'),
        ('Puerto Inírida', 'Puerto Inírida'),
        ('Quibdó', 'Quibdó'),
        ('Riohacha', 'Riohacha'),
        ('San Andres', 'San Andres'),
        ('San José del Guaviare', 'San José del Guaviare'),
        ('Santa Marta', 'Santa Marta'),
        ('Sincelejo', 'Sincelejo'),
        ('Tunja', 'Tunja'),
        ('Valledupar', 'Valledupar'),
        ('Villavicencio', 'Villavicencio'),
        ('Yopal', 'Yopal'),
    )

    picture = forms.CharField(label='Foto de perfil', max_length=250, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    gamer_id = forms.CharField(label='Gamertag', max_length=20, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Celular', max_length=15, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.ChoiceField(label='Ciudad', required=True, choices=CITIES,
                             widget=forms.Select(attrs={'class': 'selectpicker show-tick form-control'}))

    class Meta:
        model = UserAccount
        fields = ['gamer_id', 'picture', 'phone', 'city']

