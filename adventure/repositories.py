from django.utils import timezone
from datetime import timedelta
from adventure import models


class JourneyRepository:
    def get_or_create_car(self) -> models.VehicleType:
        car, _ = models.VehicleType.objects.get_or_create(name="car", 
            max_capacity=5)
        car.save()
        return car

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle.objects.create(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle: models.Vehicle) -> models.Journey:
        return models.Journey.objects.create(
            vehicle=vehicle, start=timezone.now().date()
        )

    def set_end_date(self,journey: models.Journey,date,days = 0) -> None:
        if days > 0:
            date += timedelta(days=days)
        if date is not None:
            journey.end = date
        else:
            journey.end = timezone.now().date()
        return journey