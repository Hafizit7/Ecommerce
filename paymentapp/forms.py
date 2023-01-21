from django import forms
from .models import *

from django import forms
from store_app.models import Order
from .models import *

class CheckoutForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    
    full_addres = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'cols': 30,
        'rows': 4
    }))
    order_summary = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class':'form-control',
        'cols': 30,
        'rows': 4
    }))

PAYMENT_METHOD =(
        ('Cash on Delivery','Cash on Delivery'),
        ('Bkash','Bkash')
    )

# Order model a     payment_option = models.CharField(max_length = 150) add korte hobe 

class PaymentMethodForm(forms.ModelForm):
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(attrs={
        'class':'collapsed'       
    }), choices=PAYMENT_METHOD)

    class Meta:
        model = Order
        fields = ['payment_option']

        