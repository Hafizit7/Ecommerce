from django import forms 
from store_app.models import *


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__'