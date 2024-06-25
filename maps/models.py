from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    waypoints = models.TextField(blank=True, null=True)
    distance = models.FloatField(default=0.0) # JSON string of waypoints
    travel_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route from {self.start} to {self.end} by {self.user.username}"
