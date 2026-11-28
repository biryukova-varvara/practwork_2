from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='ФМО',
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
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True,
        error_messages={
            'required': 'Для регистрации на сайте необходимо дать согласие на обработку персональных данных'
        },
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'description', 'category', 'photo')
        widgets = {
            'Название': forms.TextInput(attrs={'class': 'form-control'}),
            'Описание': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Категория': forms.Select(attrs={'class': 'form-control'}),
            'Фото': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'photo': 'Фото помещения',
        }

        def clean_photo(self):
            photo = self.cleaned_data.get('photo')
            if photo:
                ext = photo.name.split('.')[-1].lower()
                if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                    raise forms.ValidationError('Допустимые форматы файла: jpg, jpeg, png, bmp.')

                if photo.size > 2 * 1024 * 1024:
                    raise forms.ValidationError('Максимальный размер файла — 2 Мб.')

            return photo

class ChangeStatusToInProgressForm(forms.Form):
    design_image = forms.ImageField(
        label='Изображение дизайна',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )

class ChangeStatusToDoneForm(forms.Form):
    design_image = forms.ImageField(
        label='Изображение дизайна',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )

from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название категории',
        }