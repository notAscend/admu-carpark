from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, CarPass, ParkingZone

CAR_BRAND_CHOICES = [
        ('', '--- Select Brand ---'),
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Ford', 'Ford'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('Isuzu', 'Isuzu'),
        ('Kia', 'Kia'),
        ('Mazda', 'Mazda'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Nissan', 'Nissan'),
        ('Suzuki', 'Suzuki'),
        ('Toyota', 'Toyota'),
        ('Volkswagen', 'Volkswagen'),
        ('Volvo', 'Volvo'),
        ('Other', 'Other (Please specify)')
    ]

VEHICLE_TYPE_CHOICES = [
    ('', '--- Select Type ---'),
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
    ('MPV', 'MPV'),
    ('Hatchback', 'Hatchback'),
    ('Pickup Truck', 'Pickup Truck'),
    ('Van', 'Van'),
    ('Coupe', 'Coupe'),
    ('Convertible', 'Convertible'),
    ('Other', 'Other (Please specify)')
]  
    
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('admu_id','email') # Add email to the default fields

class CarDetailsForm(forms.ModelForm):  
    
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
        
class CarPassForm(forms.Form):
    plate_number = forms.CharField(max_length=10, label="Plate Number")
    
    car_brand = forms.ChoiceField(
        choices=CAR_BRAND_CHOICES,
        label="Car Brand",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    other_brand_text = forms.CharField(
        max_length=50,
        required=False,
        label="Specify Car Brand"
    )
    
    car_type = forms.ChoiceField(
        choices=VEHICLE_TYPE_CHOICES,
        label="Car Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    other_type_text = forms.CharField(
        max_length=50,
        required=False,
        label="Specify Car Type"
    )

    def clean(self):
        cleaned_data = super().clean()
        car_brand_choice = cleaned_data.get('car_brand')
        other_brand_text = cleaned_data.get('other_brand_text')
        car_type_choice = cleaned_data.get('car_type')
        other_type_text = cleaned_data.get('other_type_text')
        if car_brand_choice == 'Other' and not other_brand_text:
            self.add_error('other_brand_text', 'Please specify the car brand.')
        
        if car_type_choice == 'Other' and not other_type_text:
            self.add_error('other_type_text', 'Please specify the car type.')
            
        return cleaned_data