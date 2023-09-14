from django import forms
from .models import Todo, Tag, COLOR_CHOICES

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'deadline','importance','tag']
        tag = forms.ModelChoiceField(queryset=Tag.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TodoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['tag'].queryset = Tag.objects.filter(user=user)
