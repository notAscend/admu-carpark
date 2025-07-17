from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, CarPass, ParkingZone

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('admu_id','email') # Add email to the default fields

class CarDetailsForm(forms.ModelForm):
    CAR_BRAND_CHOICES = [
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Ford', 'Ford'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('Kia', 'Kia'),
        ('Lexus', 'Lexus'),
        ('Mazda', 'Mazda'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Nissan', 'Nissan'),  
        ('Subaru', 'Subaru'),
        ('Suzuki', 'Suzuki'),
        ('Toyota', 'Toyota'),  
        ('Volkswagen', 'Volkswagen'),
        ('Other', 'Other'),
    ]

    # New: Define choices for vehicle type
    VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Motorcycle', 'Motorcycle'),
        ('SUV', 'SUV'),
        ('Van', 'Van'),
        ('Truck', 'Truck'),
        ('Other', 'Other'),
    ]
    
    car_brand = forms.ChoiceField(
        choices=CAR_BRAND_CHOICES,
        label='Brand'
    )
    
    # New: Add the car_type field as a ChoiceField
    car_type = forms.ChoiceField(
        choices=VEHICLE_TYPE_CHOICES,
        label='Type of Vehicle'
    )
    
    class Meta:
        model = CarPass
        fields = ['car_pass_number', 'plate_number', 'car_brand', 'car_type']
        labels = {
            'car_pass_number': 'Car Pass Number',
            'plate_number': 'Vehicle Plate Number',
        }
        help_texts = {
            'car_pass_number': 'e.g., 123456',
            'plate_number': 'e.g., ABC1234',
        }

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