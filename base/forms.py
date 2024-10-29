from django import forms
from .models import Booking
from typing import Type


class BookingForm(forms.ModelForm):
    class Meta:
        model: Type[Booking] = Booking
        fields: list[int] = ["seats"]
        widgets: dict[str, Type[forms.Widget]] = {
            "seats": forms.TextInput(
                attrs={
                    "type": "number",
                    "name": "seats",
                    "min": "1",
                }
            ),
        }
