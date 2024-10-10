from django import forms
from  .models import Booking, Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'poster', 'genre', 'show_time')
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Movie name'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Movie description'}),
            'poster':  forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'show_time':  forms.DateTimeInput(attrs={'class': 'form-control',  'type':'datetime-local'}),
        }
        
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats','show_time']
        widgets = {
            'show_time':  forms.DateTimeInput(attrs={'class': 'form-control',  'type':'datetime-local'}),
            
        }