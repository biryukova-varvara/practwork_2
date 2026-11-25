from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё\s\-]+$',
                message='Имя пользователя может содержать только кириллические буквы, дефис и пробелы'
            )
        ]
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\-]+$',
                message='Логин может содержать только латиницу и дефис'
            )
        ]
    )
    email = models.EmailField(max_length=100, unique=True)
    last_name = None

    REQUIRED_FIELDS = ['first_name', 'email']

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, help_text='Краткое описание заявки')
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='request/', blank=True)

    status = models.CharField(
        max_length=20,
        choices=[('new', 'Новая'), ('in_progress', 'Принято в работу'), ('done', 'Выполнено')],
        default='new',
        verbose_name='Статус'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'