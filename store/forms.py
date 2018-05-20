from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """ Form for Orders """

    # To enable selection of status using choice map
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = Order
        fields = ('id', 'status', 'contact', 'bill_to', 'ship_to',)
