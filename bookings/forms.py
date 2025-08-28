from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        widgets = {
            'number_of_seats': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)
        super().__init__(*args, **kwargs)
        if self.travel_option:
            self.fields['number_of_seats'].widget.attrs['max'] = min(10, self.travel_option.available_seats)
            self.fields['number_of_seats'].help_text = f'Available seats: {self.travel_option.available_seats}'
    
    def clean_number_of_seats(self):
        seats = self.cleaned_data['number_of_seats']
        if self.travel_option and seats > self.travel_option.available_seats:
            raise forms.ValidationError(f'Only {self.travel_option.available_seats} seats available.')
        return seats


class FilterForm(forms.Form):
    TYPE_CHOICES = [('', 'All Types')] + [('FLIGHT', 'Flight'), ('TRAIN', 'Train'), ('BUS', 'Bus')]
    
    type = forms.ChoiceField(choices=TYPE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    source = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From'}))
    destination = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To'}))
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))