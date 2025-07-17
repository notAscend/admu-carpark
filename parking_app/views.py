from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
import math
import json
from django.conf import settings
from .forms import SignUpForm, CarDetailsForm, LoginForm, ParkingZoneForm
from .models import CustomUser, CarPass, ParkingZone, ParkingSession, ParkingZone
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Points are given in decimal degrees.
    Returns the distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def main_view(request): return render(request, 'parking_app/main.html')

def signup_view(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        car_form = CarDetailsForm(request.POST)
        
        if signup_form.is_valid() and car_form.is_valid():
            # Save the new user and car pass
            user = signup_form.save()
            car_pass = car_form.save(commit=False)
            car_pass.user = user
            car_pass.save()
            return redirect('main') # Or your login page name
    else:
        signup_form = SignUpForm()
        car_form = CarDetailsForm()

    context = {
        'signup_form': signup_form,
        'car_form': car_form,
    }
    return render(request, 'parking_app/signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('account')
    else: form = LoginForm()
    return render(request, 'parking_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main')

#-------- GOOD UNTIL HERE--------

@login_required
def account_view(request):
    active_session = ParkingSession.objects.filter(user=request.user, is_active=True).first()
    user_car_passes = request.user.car_passes.all()

    context = {
        'active_session': active_session,
        'user_car_passes': user_car_passes,
    }
    return render(request, 'parking_app/account.html', context)

@login_required
def enter_parking_view(request):
    user_cars = request.user.car_passes.all()
    user_lat_default = 14.6394
    user_lon_default = 121.0776

    # Check if user is already in an active parking session
    if ParkingSession.objects.filter(user=request.user, is_active=True).exists():
        messages.warning(request, "You are already in an active parking session. Please exit first.")
        return redirect('account') # Redirect to account/dashboard

    # --- Logic for both GET and POST to prepare parking zone data ---
    parking_zones = ParkingZone.objects.all()
    zones_data = []
    for zone in parking_zones:
        distance_meters = haversine_distance(
            user_lat_default, user_lon_default,
            float(zone.latitude), float(zone.longitude)
        )
        zones_data.append({
            'id': zone.id,
            'name': zone.area, # Use 'area' for the zone name
            'latitude': float(zone.latitude),
            'longitude': float(zone.longitude),
            'total_slots': zone.total_slots,
            'curr_slots': zone.curr_slots,
            'is_full': zone.is_full,
            'zone_code': zone.zone_code,
            'distance_to_user_m': round(distance_meters, 2), # Distance in meters, rounded
        })
    
    # Sort zones by distance (closest first)
    zones_data_sorted = sorted(zones_data, key=lambda x: x['distance_to_user_m'])
    zones_json = json.dumps(zones_data_sorted) # Convert to JSON string

    # --- Handle POST request (when user submits car selection and location) ---
    if request.method == 'POST':
        # These values come from the hidden inputs, populated by JS
        selected_car_id = request.POST.get('car_id') # Note: form uses name="car_id"
        user_lat_from_js = request.POST.get('user_lat')
        user_lon_from_js = request.POST.get('user_lon')
        context = {
            'user_cars': user_cars,
            'zones_json': zones_json, # Pass zones_json for re-rendering
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY, # Still pass for consistency, even if not used by this template
            'user_initial_lat': user_lat_from_js or user_lat_default, # Use actual if available, else default
            'user_initial_lon': user_lon_from_js or user_lon_default,
        }
        return render(request, 'parking_app/enter_parking_init.html', context)
    
    # --- Handle GET request (initial page load) ---
    context = {
        'user_cars': user_cars,
        'zones_json': zones_json, # Pass zones_json for initial rendering of buttons
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY, # Still pass for consistency
        'user_initial_lat': user_lat_default,
        'user_initial_lon': user_lon_default,
    }
    return render(request, 'parking_app/enter_parking_init.html', context)

@login_required
def start_parking_session_view(request):
    if request.method == 'POST':
        # Retrieve data from the form's hidden inputs
        selected_zone_id = request.POST.get('selected_zone_id')
        selected_car_id = request.POST.get('car_id') # Note: the select has name="car_id"
        
        # We need to make sure both IDs were received
        if not selected_zone_id or not selected_car_id:
            messages.error(request, "A car and a parking zone must be selected.")
            return redirect('enter_parking')
            
        try:
            # Fetch the objects from the database
            zone = get_object_or_404(ParkingZone, id=selected_zone_id)
            car = get_object_or_404(CarPass, id=selected_car_id, user=request.user)

            # Check if the zone is full before trying to park
            if zone.total_slots - zone.curr_slots <= 0:
                messages.error(request, f"Sorry, {zone.area} is now full. Please select another zone.")
                return redirect('enter_parking')

            # Decrement the current slot count in the database
            zone.curr_slots += 1
            zone.save()

            # Create a new ParkingSession entry
            new_session = ParkingSession.objects.create(
                user=request.user,
                car=car,
                parking_zone=zone,
                is_active=True)
            
            messages.success(request, f"Parking session started at {zone.area}. You are now parked with your car: {car.plate_number}.")
            
            # Redirect the user to their account page
            return redirect('account')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('enter_parking')
            
    # If a GET request is received, redirect back to the form
    return redirect('enter_parking')

@login_required
def exit_parking_view(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        
        if not session_id:
            messages.error(request, "Invalid parking session.")
            return redirect('account')
            
        try:
            # Get the session, ensuring it belongs to the logged-in user and is active
            session = get_object_or_404(ParkingSession, id=session_id, user=request.user, is_active=True)
            zone = session.parking_zone
            
            # End the session
            session.is_active = False
            session.end_time = timezone.now()
            session.save()
            
            # Increment the available slot count in the zone
            if zone.curr_slots > 0:
                zone.curr_slots -= 1
                zone.save()

            messages.success(request, f"Parking session at {zone.area} has ended.")
            
            return redirect('account')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('account')
            
    return redirect('account')

def parking_zones_api_view(request):
    # This API endpoint might receive user's current location from the frontend
    # if you want distance calculations to be real-time based on the user's browser location.
    # For now, we'll use a default if not provided, or fallback to the backend's knowledge.

    # Try to get user_lat and user_lon from query parameters (e.g., /api/parking_zones/?lat=X&lon=Y)
    try:
        user_lat = float(request.GET.get('lat', 14.6394)) # Default Ateneo main gate
        user_lon = float(request.GET.get('lon', 121.0776)) # Default Ateneo main gate
    except (TypeError, ValueError):
        user_lat = 14.6394
        user_lon = 121.0776

    parking_zones = ParkingZone.objects.all()

    zones_data = []
    for zone in parking_zones:
        distance_meters = haversine_distance(
            user_lat, user_lon,
            float(zone.latitude), float(zone.longitude)
        )
        zones_data.append({
            'id': zone.id,
            'name': zone.area,
            'latitude': float(zone.latitude),
            'longitude': float(zone.longitude),
            'total_slots': zone.total_slots,
            'curr_slots': zone.curr_slots,
            'is_full': zone.is_full,
            'zone_code': zone.zone_code,
            'distance_to_user_m': round(distance_meters, 2),
        })

    # Always sort by distance for API, so frontend can easily pick closest
    zones_data_sorted = sorted(zones_data, key=lambda x: x['distance_to_user_m'])

    # Return the data as a JSON response
    return JsonResponse(zones_data_sorted, safe=False) 

@login_required
def dashboard_view(request):
    user = request.user
    completed_sessions = ParkingSession.objects.filter(
        car__user=user, 
        end_time__isnull=False
    ).order_by('-start_time')

    # Calculate and format duration for each session
    for session in completed_sessions:
        if session.end_time and session.start_time:
            duration = session.end_time - session.start_time
            
            total_minutes = int(duration.total_seconds() / 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            time_string = ''
            if hours > 0:
                time_string += f"{hours} hour{'s' if hours > 1 else ''}"
            if minutes > 0:
                if hours > 0:
                    time_string += ", "
                time_string += f"{minutes} minute{'s' if minutes > 1 else ''}"
            
            if not time_string:
                time_string = "Less than a minute"

            session.formatted_duration = time_string
        else:
            session.formatted_duration = "N/A"

    context = {
        'user': user,
        'completed_sessions': completed_sessions,
    }
    
    return render(request, 'parking_app/dashboard.html', context)

def get_busyness_data(request):
    """
    Returns JSON data for charts showing busy times for each parking zone.
    """
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    # Get all parking sessions that were active in the last week
    sessions = ParkingSession.objects.filter(
        start_time__lte=end_date,
        end_time__gte=start_date
    ).select_related('parking_zone')

    # Get all active parking zones
    parking_zones = ParkingZone.objects.all()

    # Initialize a nested dictionary to store hourly counts for each zone
    zone_hourly_counts = {
        zone.area: defaultdict(int) for zone in parking_zones
    }
    
    # Aggregate data by counting sessions per hour for each zone
    for session in sessions:
        if session.parking_zone and session.start_time:
            start_hour = session.start_time.hour
            zone_area = session.parking_zone.area
            zone_hourly_counts[zone_area][start_hour] += 1
    
    # Prepare the final data structure for Chart.js
    data = {}
    for zone_area, hourly_counts in zone_hourly_counts.items():
        data[zone_area] = {
            'labels': [f'{h}:00' for h in range(24)],
            'datasets': [{
                'label': 'Number of Parked Cars',
                'data': [hourly_counts[h] for h in range(24)],
                'backgroundColor': 'rgba(54, 162, 235, 0.6)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            }]
        }

    return JsonResponse(data)