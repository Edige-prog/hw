import random

from faker import Faker
from faker_vehicle import VehicleProvider

def create_cars(cars_total):
    fake = Faker()
    fake.add_provider(VehicleProvider)

    car_ids = list(range(cars_total))
    random.seed(0)
    random.shuffle(car_ids)

    cars = [
        {
            "id": car_ids[i] + 1,
            "name": fake.vehicle_make_model(),
            "year": fake.machine_year(),
        }
        for i in range(cars_total)
    ]

    return cars

