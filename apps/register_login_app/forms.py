from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import validators

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30,required=True, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    last_name = forms.CharField(max_length=30,required=True, validators=[validators.MinLengthValidator(2, 'Please make at least 2 charactors')])
    
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields["password1"].help_text = None
    
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        # let's say we wanted to make our data all caps, we could do that here!
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
