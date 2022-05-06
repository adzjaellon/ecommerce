from django import forms
from .models import Comment, Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body',
            'type'
        ]


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body',
            'type'
        ]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name',
            'avatar'
        ]


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
