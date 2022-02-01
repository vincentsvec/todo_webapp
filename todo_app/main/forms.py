from django import forms
from .models import Lists, Task


class NewTask(forms.Form):
    name = forms.CharField(label="", max_length=40, widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'class': 'form-input-task', 'autofocus': 'autofocus'}))


class NewList(forms.Form):
    name = forms.CharField(label='', max_length=20,
                           widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name', 'autofocus': 'autofocus'}))
