from django.db import models
from datetime import date
from typing import List
from re import match

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, 
        on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers
    
    def get_distribution(self) -> List:
        places = [True if x in range(self.passengers) else False \
            for x in range(self.vehicle_type.max_capacity)]
        distributed_places = [places[place:place + 2] \
            for place in range(0,len(places), 2)]
        return distributed_places

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self):
        if self.end is None:
            return False
        elif self.end <= date.today():
            return True
        else:
            return False

def validate_number_plate(number_plate: str) -> bool:
    try:
        if match(r'^[A-Z][A-Z]-\d\d-\d\d', number_plate):
            return True
        else:
            return False
    except TypeError:
        return False