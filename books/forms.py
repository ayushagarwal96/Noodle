from django.contrib.auth.models import User
from django import forms
from .models import Book
from .choices import *

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'edition', 'condition', 'cost', 'category', 'cover']



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password']

class UpdateUserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'password']