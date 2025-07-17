# In parking_app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# Validator to ensure the email is an Ateneo student email
def validate_admu_email(value):
    if not value.endswith('@student.ateneo.edu'):
        raise ValidationError('Only @student.ateneo.edu emails are allowed.')
class CustomUserManager(BaseUserManager):
    def create_user(self, admu_id, email, password=None, **extra_fields):
        if not admu_id:
            raise ValueError('The ADMU ID must be set')
        if not email:
            raise ValueError('The Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(admu_id=admu_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, admu_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(admu_id, email, password, **extra_fields)

class CustomUser(AbstractUser):
    admu_id = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(r'^\d{6}$', 'ADMU ID must be exactly 6 digits.'),
        ]
    )
    email = models.EmailField(
        'email address', 
        unique=True,
        validators=[validate_admu_email]
    )
    
    USERNAME_FIELD = 'admu_id'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.admu_id

class CarPass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_passes')
    car_pass_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(r'^\d{6}$', 'Car Pass Number must be exactly 6 digits.'),
        ]
    )
    plate_number = models.CharField(max_length=10, unique=True)
    car_brand = models.CharField(max_length=50)
    car_type = models.CharField(max_length=50)

    def __str__(self):
        return self.plate_number

class ParkingZone(models.Model):
    area = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    total_slots = models.IntegerField(default=0)
    curr_slots = models.IntegerField(default=0)
    ZONE_CHOICES = [
        ('ARETE', 'North'),
        ('JSEC', 'Central'),
        ('UPPER_EAST', 'Upper East'),
        ('LOWER_EAST', 'Lower East'),
    ]
    zone_code = models.CharField(max_length=20, choices=ZONE_CHOICES, unique=True)
    @property
    def avail_slots(self):
        return max(0, self.total_slots - self.curr_slots)
    @property
    def is_full(self):
        return self.avail_slots <= 0
    def __str__(self):
        return self.area

class ParkingSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey('CarPass', on_delete=models.CASCADE)
    parking_zone = models.ForeignKey('ParkingZone', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username}'s parking session at {self.parking_zone.area}"