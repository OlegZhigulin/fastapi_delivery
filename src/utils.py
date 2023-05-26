import csv
import random
from functools import lru_cache

from fastapi import HTTPException, status
from geopy.distance import geodesic
from pony.orm import db_session, select

from src.models import Car, Cargo, Location, State


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


@db_session
def create_locations():
    """Создаем локации из csv файла, которые содержат:
    - город;
    - штат;
    - почтовый индекс (zip);
    - широта;
    - долгота.
    """
    with open('src/uszips.csv', encoding='utf-8') as file:
        cities = csv.DictReader(file)
        for city in cities:
            zip_code = city.get('zip')
            latitude = city.get('lat')
            longitude = city.get('lng')
            city_name = city.get('city')
            state_name = city.get('state_name')
            state = State.get(name=state_name)
            if not state:
                state = State(name=state_name)
            Location(
                zip_code=zip_code,
                latitude=latitude,
                longitude=longitude,
                city=city_name,
                state=state,
            )


@db_session
def create_car():
    """Создаем машины со следующими характеристикими:
    - уникальный номер (
        цифра от 1000 до 9999 +
        случайная заглавная буква английского алфавита в конце,
        пример: "1234A", "2534B", "9999Z")
    - текущая локация;
    - грузоподъемность (1-1000).
    """
    vin_numbers = set()
    while len(vin_numbers) < 20:
        vin = str(random.randint(1000, 9999)) + chr(random.randint(65, 90))
        vin_numbers.add(vin)
    locations = set()
    while len(locations) < 20:
        location_id = random.randint(1, 33789)
        locations.add(location_id)
    capacity_set = set()
    while len(capacity_set) < 20:
        capacity = random.randint(1, 1000)
        capacity_set.add(capacity)
    car_data = list(zip(vin_numbers, locations, capacity_set))
    for car in car_data:
        Car(vin_number=car[0], location=car[1], capacity=car[2])
