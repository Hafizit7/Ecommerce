from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UpdateRegisterForm(forms.ModelForm):
    class Meta:
        model= User
        fields =[ 'username', 'first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):
    dob = forms.DateField(required=False,
        widget=forms.DateInput( attrs={
        "type":"date",
        'class':'form-control'
    })
    )
    class Meta:
        model = Profile
        fields = ['image', 'phone', 'dob']





class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,
               widget=forms.TextInput(attrs={
                   "class":"form-control",
                   "placeholder":"Enter your first name.."
               }) 
               )
    last_name = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter your second name.."
            }) 
            )
    username = forms.CharField(max_length=30,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"Enter your username.."
        }) 
        )
    email = forms.EmailField(
            widget=forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter your email.."
            }) 
            )
    password1 = forms.CharField(
            widget=forms.PasswordInput(attrs={
                "class":"form-control",
                "placeholder":"Enter your password.."
            }) 
            )
    password2 = forms.CharField(max_length=30,
            widget=forms.PasswordInput(attrs={
                "class":"form-control",
                "placeholder":"Confirme password.."
            }) 
            )   
    class Meta:
        model=User
        fields =['first_name', 'last_name', 'username', 'email', 'password1','password2']

