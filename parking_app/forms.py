from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, CarPass, ParkingZone

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',) # Add email to the default fields

class CarDetailsForm(forms.ModelForm):
    class Meta:
        model = CarPass
        fields = ['car_pass_number', 'car_type', 'plate_number']

    def clean_car_pass_number(self):
        car_pass_number = self.cleaned_data['car_pass_number']
        return car_pass_number

class LoginForm(AuthenticationForm):
    pass

class ParkingZoneForm(forms.ModelForm):
    class Meta:
        model = ParkingZone
        fields = [
            'area',      
            'latitude',
            'longitude',
            'total_slots',
            'curr_slots',
            'zone_code'
        ]