import csv

from pony.orm import db_session

from models import db, Location, State


@db_session
def create_locations():
    """Создаем локации из csv файла, которые содержат:
    - город;
    - штат;
    - почтовый индекс (zip);
    - широта;
    - долгота.
    """
    db.bind(provider='sqlite', filename='database.sqlite')
    db.generate_mapping()
    with open('uszips.csv', encoding='utf-8') as file:
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


if __name__ == '__main__':
    create_locations()
