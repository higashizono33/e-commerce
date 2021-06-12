from django import forms
from .models import ShippingInfo, BillingInfo, ProductReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('star', 'content')
        widgets = {
            'star': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control p-2', 'cols': "70", 'rows': "5", 'placeholder': "write here"}),
        }
class ShippingForm(forms.ModelForm):
    address2 = forms.CharField(required=False)
    class Meta:
        model = ShippingInfo
        fields = ('first_name', 'last_name', 'address', 'address2', 'city', 'state', 'zipcode')
class BillingForm(forms.ModelForm):
    address2 = forms.CharField(required=False)
    class Meta:
        model = BillingInfo
        fields = ('first_name', 'last_name', 'address', 'address2', 'city', 'state', 'zipcode', 'card_number', 'card_security', 'expiration')
        widgets = {
            'expiration': forms.TextInput(attrs={'placeholder': 'MM/YYYY'}),
        }