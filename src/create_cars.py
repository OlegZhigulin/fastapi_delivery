import random

from pony.orm import db_session

from models import db, Car


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
    db.bind(provider='sqlite', filename='database.sqlite')
    db.generate_mapping()
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


if __name__ == '__main__':
    create_car()
