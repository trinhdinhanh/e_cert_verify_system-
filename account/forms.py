from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['user_name', 'full_name', 'student_code', 'password1', 'password2', 'date_of_birth', 'is_teacher', 'd_key', 'e_key', 'n_key']