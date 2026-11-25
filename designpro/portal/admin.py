from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Request

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'email', 'is_staff')
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)