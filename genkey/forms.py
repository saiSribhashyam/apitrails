from django import forms

class APIKeyForm(forms.Form):
    email = forms.EmailField(label='Your Email', max_length=255)
