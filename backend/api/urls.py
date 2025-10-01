#cab_booking/urls.py
from django.urls import path
from .views import booking_views
from .views.auth_views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #booking
    path('calculate-fare/', booking_views.CalculateFareView.as_view(), name='calculate_fare'),
    path('bookings/create/', booking_views.CreateBookingView.as_view(), name='create_booking'),
    path('bookings/', booking_views.BookingListView.as_view(), name='booking_list'),
    # path('test-utilities/', booking_views.test_utilities, name='test_utilities'),#for testing api (hardcoded)

    #auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"), 

]