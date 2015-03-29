from django import forms
from .models import Question
from .models import Option


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['statement',]

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['name',]

