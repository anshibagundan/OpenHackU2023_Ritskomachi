from django import forms
from .models import Todo,Tag

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TodoForm, self).__init__(*args, **kwargs)
        if user:
            # 前提として、Tagモデルにuserフィールドが存在すると仮定します。
            self.fields['tag'].queryset = Tag.objects.filter(user=user)
