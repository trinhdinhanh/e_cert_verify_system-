from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import  Textarea
from django.db import models

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('user_name', 'full_name',)
    list_filter = ('user_name', 'full_name', 'is_active', 'is_staff', 'is_teacher')
    list_display = ('user_name', 'full_name', 'is_active', 'is_staff', 'is_teacher')
    ordering = ('-full_name',)
    fieldsets = (
        (None, {'fields': ('user_name', 'full_name', 'date_of_birth', 'student_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_teacher')}),
        ('Password', {'fields': ('password',)}),
        ('Teacher Public Key', {'fields': ('e_key','n_key')}),
    )
    readonly_fields = ['e_key','n_key']
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'full_name', 'password1', 'password2', 'is_active', 'is_staff','is_teacher',)}
         ),
    )

admin.site.register(User, UserAdminConfig)