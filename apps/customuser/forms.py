from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre:', max_length=30, required=False)
    last_name = forms.CharField(label='Apellido:', max_length=60, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )


class ProfileForm(UserChangeForm):
    birth_date = forms.DateField(help_text='YYYY-MM-DD')
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birth_date',)
