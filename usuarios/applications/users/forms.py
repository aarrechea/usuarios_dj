""" Imports """
from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth import authenticate
from django.forms.utils import ErrorList
from .models import User


""" User register form """
class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )
    
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir Contraseña'
            }
        )
    )
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombre',
            'apellido',
            'gender',
        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Contraseñas no son iguales')


""" Login form """
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username'
            }
        )
    )    
    
    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Password'
            }
        )
    )    

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        print(f"Username: {self.cleaned_data['username']} - Password: {self.cleaned_data['password']}")
        
        if not authenticate(username=username, password=password):
            
            print(f"Authenticate: {authenticate}")
            
            raise forms.ValidationError('Los datos no son correctos')
        
        return self.cleaned_data
        
        
""" Update Password Form """
class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Actual'
            }
        )
    )    
    
    password2 = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Nueva'
            }
        )
    )    


""" Verificacion form. To verify the valid user email """
class VerificationForm(forms.Form):
    code_registro = forms.CharField(max_length=50, required=True)
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super().__init__(*args, **kwargs)
    
    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        
        if len(codigo) == 6:
            # Verificación del código de usuario
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            
            if not activo:
                raise forms.ValidationError('Código inválido')
                
        else:
            raise forms.ValidationError('Código inválido')
    
    

