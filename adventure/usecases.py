from __future__ import annotations

from adventure import models

from .notifiers import Notifier
from .repositories import JourneyRepository


class StartJourney:
    def __init__(self, repository: JourneyRepository, notifier: Notifier):
        self.repository = repository
        self.notifier = notifier

    def set_params(self, data: dict) -> StartJourney:
        self.data = data
        return self

    def execute(self) -> tuple:
        car = self.repository.get_or_create_car()
        vehicle = self.repository.create_vehicle(vehicle_type=car, **self.data)
        if not vehicle.can_start():
            raise StartJourney.CantStart("vehicle can't start")
        journey = self.repository.create_journey(vehicle)
        self.notifier.send_notifications(journey)
        journey_saved = SaveJourney(journey).save_journey()
        return journey,journey_saved

    class CantStart(Exception):
        pass

class StopJourney:
    def __init__(self, repository: JourneyRepository):
        self.repository = repository

    def set_params(self, data: dict, end_date = None) -> StartJourney:
        self.data = None
        self.vehicle = models.Vehicle.objects.filter(name=data['name'])[0].id
        self.date = end_date
        return self

    def execute(self) -> tuple:
        self.data = GetJourney(self.vehicle).get_journey()
        journey = self.repository.set_end_date(self.data,self.date)
        journey_saved = SaveJourney(journey).save_journey()
        return journey,journey_saved

class SaveJourney:
    def __init__(self, journey: models.Journey):
        self.journey = journey

    def save_journey(self) -> bool:
        try:
            self.journey.vehicle.vehicle_type.save()
            self.journey.vehicle.save()
            self.journey.save()
        except Exception:
            return False
        return True

class GetJourney:
    def __init__(self, vehicle: models.Vehicle.name):
        self.vehicle = vehicle

    def get_journey(self) -> None:
        try:
            return models.Journey.objects.filter(vehicle=self.vehicle)[0]
        except Exception:
            return None