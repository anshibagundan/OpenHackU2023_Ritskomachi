from django import forms
from .models import Todo, Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline','importance']
