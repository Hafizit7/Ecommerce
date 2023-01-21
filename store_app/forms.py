from email.mime import image
from django import forms
from .models import *


class ProductReviewForm(forms.ModelForm):
    RATING =(
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5')
    )
    rating  = forms.ChoiceField(choices = RATING,widget=forms.RadioSelect(attrs={
    }))
    image = forms.ImageField(required=False)
    review = forms.CharField(
        widget=forms.Textarea(attrs={
            "class":"form-control",
            "placeholder":"Comment",
            'rows':2
        })
        )
    class Meta:
        model = ProductReview
        fields = ['rating','review','image']
