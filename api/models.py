from django.db import models


class ParkingSpot(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    free = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.x} - {self.y} - {self.free}"
