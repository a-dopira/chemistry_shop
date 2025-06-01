from django import forms
from django.contrib.auth import get_user_model

from store.models import Order

User = get_user_model()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "address",
            "zipcode",
            "city",
        )

