from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')


from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'description', 'category', 'photo')
        widgets = {
            'Название': forms.TextInput(attrs={'class': 'form-control'}),
            'Описание': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'Категория': forms.Select(attrs={'class': 'form-control'}),
            'Фото': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'photo': 'Фото помещения',
        }