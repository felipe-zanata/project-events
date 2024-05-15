from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)



class CadastroForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    class Meta:
        model = User  # Substitua por User se estiver usando o modelo padrão
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']