from django.urls import path
from . import views  # Import all views from the current app's views.py file

urlpatterns = [
    # Main page of the parking app (e.g., http://127.0.0.1:8000/)
    path('', views.main_view, name='main'),

    # Sign-up and Log-in pages
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('car-pass/signup/', views.car_pass_signup, name='car_pass_signup'),
    path('car-pass/delete/<int:car_pass_id>/', views.delete_car_pass, name='delete_car_pass'),

    # Dashboard page
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/busyness_data/', views.get_busyness_data, name='busyness_data'),
    path('park/enter/', views.enter_parking_view, name='enter_parking'),
    path('park/start_session/', views.start_parking_session_view, name='start_parking_session'),
    path('park/exit/', views.exit_parking_view, name='exit_parking'),

    #path('api/parking_zones/', views.parking_zones_api_view, name='parking_zones_api'),

]