from fastapi import APIRouter, status
from pony.orm import db_session, flush

from src.models import Car, Cargo
from src.schemas import (
    CargoCreateModel,
    CargoCreateResponseModel,
    CargoListResponseModel,
    CargoResponseModel,
    CargoUpdateModel,
)
from src.utils import (
    calculate_distanse_between_points,
    get_and_check_cargo_exist,
    get_and_check_location_exist,
    get_and_check_vehicle_exist,
)

cargo_router = APIRouter(
    tags=['cargo'],
    prefix='/cargo'
)


@cargo_router.get(
    '/show_all',
    summary='Получение всех посылок',
    description='Груз(локации, количество ближайших машин до груза 450 миль)',
    status_code=status.HTTP_200_OK,
    response_model=CargoListResponseModel
)
@db_session
def show_all_cargo():
    cargo_data = Cargo.select()
    data = [
        CargoResponseModel(
            description=cargo.description,
            weight=cargo.weight,
            pick_up=cargo.pick_up.to_dict(),
            delivery=cargo.delivery.to_dict(),
            count_cars=10,
        ) for cargo in cargo_data
    ]

    response = {'data': data}
    return response


@cargo_router.post(
    '/create',
    summary='Создание посылки',
    description='Характеристики локаций определяются по введенному zip-коду)',
    status_code=status.HTTP_201_CREATED,
    response_model=CargoCreateResponseModel,
)
@db_session
def create_cargo(cargo_data: CargoCreateModel):
    pick_up = get_and_check_location_exist(zip_code=cargo_data.pick_up)
    delivery = get_and_check_location_exist(zip_code=cargo_data.delivery)
    package = Cargo(
        pick_up=pick_up,
        delivery=delivery,
        weight=cargo_data.weight,
        description=cargo_data.description,
    )
    flush()
    package = package.to_dict(with_collections=True, related_objects=True)
    pick_up = package.get('pick_up').to_dict(related_objects=True)
    pick_up['state'] = pick_up.get('state').to_dict()
    delivery = package.get('delivery').to_dict(related_objects=True)
    delivery['state'] = delivery.get('state').to_dict()

    response = {
        'id': package.get('id'),
        'description': package.get('description'),
        'weight': package.get('weight'),
        'pick_up': pick_up,
        'delivery': delivery,
    }
    return response


@cargo_router.get(
    '/{pk}',
    summary='Получение информации о посылке по ID',
    description='локации, pick-up, delivery, вес, описание, список машин',
    status_code=status.HTTP_200_OK,
    response_model=CargoResponseModel,
)
@db_session
def show_info_about_cargo_via_id(pk: int):
    package = get_and_check_cargo_exist(id=pk)
    package_coordinate = (package.pick_up.latitude, package.pick_up.longitude)
    vin_number_and_dictanse = dict()
    cars = Car.select()
    for car in cars:
        car_coordinate = (car.location.latitude, car.location.longitude)
        distanse = calculate_distanse_between_points(
            car_coordinate,
            package_coordinate,
        )
        vin_number_and_dictanse[car.vin_number] = int(distanse)

    package = package.to_dict(with_collections=True, related_objects=True)
    pick_up = package.get('pick_up').to_dict(related_objects=True)
    pick_up['state'] = pick_up.get('state').to_dict()
    delivery = package.get('delivery').to_dict(related_objects=True)
    delivery['state'] = delivery.get('state').to_dict()

    response = {
        'description': package.get('description'),
        'weight': package.get('weight'),
        'pick_up': pick_up,
        'delivery': delivery,
        'cars_list': vin_number_and_dictanse,
    }
    return response


@ cargo_router.patch(
    '/{pk}',
    summary='Изменение информации о посылке по ID',
    description='Редактирование (вес, описание)',
    status_code=status.HTTP_200_OK,
    response_model=CargoUpdateModel,
)
@ db_session
def update_cargo(pk: int, data: CargoUpdateModel):
    package = get_and_check_cargo_exist(id=pk)
    package.set(**data.dict())
    flush()
    return package.to_dict()


@ cargo_router.delete(
    '/{pk}',
    summary='Удаление груза по ID',
    description='Удаление груза по ID, если нет найдена будет ошибка',
    status_code=status.HTTP_204_NO_CONTENT,
)
@ db_session
def delete_cargo(pk: int):
    package = get_and_check_cargo_exist(id=pk)
    package.delete()


vehicle_router = APIRouter(
    tags=['vehicle'],
    prefix='/vehicle'
)


@ vehicle_router.patch(
    '/{pk}',
    summary='Редактирование машины по ID',
    description='Редактирование локации определяется  zip-коду',
    status_code=status.HTTP_200_OK,
)
@ db_session
def update_vehicle(pk: int, zip_code: str):
    vehicle = get_and_check_vehicle_exist(id=pk)
    location = get_and_check_location_exist(zip_code=zip_code)
    vehicle.set(location=location)
    flush()
    vehicle = vehicle.to_dict(with_collections=True, related_objects=True)
    location = vehicle.get('location').to_dict(related_objects=True)
    location['state'] = location.get('state').to_dict()

    response = {
        'id': vehicle.get('id'),
        'vin_number': vehicle.get('vin_number'),
        'capacity': vehicle.get('capacity'),
        'location': location
    }
    return response


@ vehicle_router.get(
    '/',
    summary='listvenicle',
    description='list venicle',
    status_code=status.HTTP_200_OK,

)
@ db_session
def ads(package_id: int):
    cnt = get_count_near_car(list_venicle(package_id))
    return cnt


def list_venicle(package_id: int):
    package = Cargo.get(id=package_id)
    package_coordinate = (package.pick_up.latitude, package.pick_up.longitude)
    response = dict()
    cars = Car.select()
    for car in cars:
        car_coordinate = (car.location.latitude, car.location.longitude)
        distance = calculate_distanse_between_points(
            car_coordinate, package_coordinate)
        response[car.vin_number] = int(distance)
    return response


def get_near_car_count(list_car: dict):
    cnt = 0
    for val in list_car.values():
        if val <= 450:
            cnt += 1
    return cnt
