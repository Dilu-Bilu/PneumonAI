from django import forms 

class PneumoniaForm(forms.Form):
    image = forms.ImageField()