import random
from functools import lru_cache

from fastapi import HTTPException, status
from geopy.distance import geodesic
from pony.orm import db_session, select

from src.models import Car, Cargo, Location


def get_and_check_cargo_exist(id: int):
    package = Cargo.get(id=id)
    if package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Посылка не найдена',
        )
    return package


def get_and_check_vehicle_exist(id: int):
    vehicle = Car.get(id=id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транспорт не найден',
        )
    return vehicle


def get_and_check_location_exist(zip_code: int):
    location = Location.get(zip_code=zip_code)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такой zip_code отсутствует',
        )
    return location


@lru_cache
def calculate_distanse_between_points(
    car_location: tuple,
    cargo_location: tuple
):
    distanse = geodesic(car_location, cargo_location).miles
    return distanse


@db_session
def update_location_car():
    cars = select(car for car in Car).for_update()
    for car in cars:
        location_id = random.randint(1, 33789)
        car.location = location_id
