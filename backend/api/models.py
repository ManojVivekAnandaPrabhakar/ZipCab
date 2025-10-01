#cab_booking/models.py
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings") 
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pickup_location} to {self.drop_location}"

#under updation will be done later
# class PasswordResetCode(models.Model):
    
#     email = models.EmailField(unique=True)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.email} - {self.code}"

#     class Meta:
#         indexes = [
#             models.Index(fields=['email']),
#         ]