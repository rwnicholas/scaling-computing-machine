from django import forms

class MainForm(forms.Form):
    productTitle = forms.CharField(label="Nome", max_length=200)