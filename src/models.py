from pony.orm import Database, Optional, Set, Required, PrimaryKey

db = Database()


class State(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    locations = Set('Location')


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    zip_code = Required(str)
    latitude = Required(str)
    longitude = Required(str)
    city = Required(str)
    state = Required(State)
    cars_in_location = Set('Car', reverse='location')
    package_from = Set('Cargo', reverse='pick_up')
    package_to = Set('Cargo', reverse='delivery')


class Car(db.Entity):
    id = PrimaryKey(int, auto=True)
    vin_number = Required(str, unique=True)
    capacity = Required(int)
    location = Required(Location, reverse='cars_in_location')


class Cargo(db.Entity):
    id = PrimaryKey(int, auto=True)
    description = Optional(str, 250, nullable=True)
    weight = Required(int, min=1, max=1000)
    pick_up = Required(Location, reverse='package_from')
    delivery = Required(Location, reverse='package_to')


def init_database():
    try:
        db.bind(provider='postgres', user='postgres',
                password='2202SuperData', host='db', database='postgres')
        db.generate_mapping(create_tables=True)

    except Exception as error:
        print(error)
