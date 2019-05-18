from django import forms
from django.core.exceptions import ValidationError
from .models import *

class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('priority', 'deadline','title','text')

        widgets = {
            'deadline' : forms.DateInput(attrs={'type':'date'}),
            'title':forms.TextInput(attrs={
                'placeholder':'해야 할 일(필수입력)',
                'style':'height:3em'
            }),
            'text': forms.Textarea(attrs={
                'placeholder':'구체적인 설명(선택입력)',
            })
        }
    
    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        if not title or title is '':
            raise ValidationError("제목은 반드시 입력해야합니다.")
        return data