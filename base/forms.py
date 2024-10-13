from django import forms
from  .models import Booking
        
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']
        widgets = {
            "seats": forms.TextInput(
                attrs={
                    "type":"number",
                    "name":"seats",
                    "min":"1",
                }
            ),
        }
