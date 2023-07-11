from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Nombres", max_length=32 )
    last_name = forms.CharField(required=True, label="Apellidos", max_length=32 )
    email = forms.EmailField(required=True, label="E-Mail" )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-50-md'
            field.label_attrs = {'class': 'form-label w-50-md'}

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-50-md'
            field.label_attrs = {'class': 'form-label w-50-md'}

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control w-50-md'
            field.label_attrs = {'class': 'form-label w-50-md'}