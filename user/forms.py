from django import forms
from .models import Comment


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
