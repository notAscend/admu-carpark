from django.contrib import admin
from .models import CustomUser, CarPass, ParkingZone, ParkingSession

admin.site.register(CustomUser)
admin.site.register(CarPass)
admin.site.register(ParkingZone)
admin.site.register(ParkingSession)