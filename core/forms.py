from django import forms
from .models import Guest, Room

class GuestForm(forms.ModelForm):
    """Form for guest check-in"""
    class Meta:
        model = Guest
        fields = ['name', 'address', 'phone', 'email', 'num_guests', 'room']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available rooms in the form
        self.fields['room'].queryset = Room.objects.filter(is_occupied=False)
        
        # Add classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SearchForm(forms.Form):
    """Form for searching guests"""
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, phone or email'
        })
    )
