from django import forms
from .models import Todo, Tag

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline', 'tag', 'importance']
        exclude = ('user',)

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'タスク名', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': '詳細', 'class': 'form-control', 'rows': '5'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tag': forms.Select(attrs={'class': 'form-control'}),
            'importance': forms.Select(choices=Todo.IMPORTANCE_CHOICES, attrs={'class': 'form-control'}),
        }
