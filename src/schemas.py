from typing import Optional

from pydantic import BaseModel, validator


class CargoModel(BaseModel):
    description: Optional[str] = None
    weight: int

    @validator('weight')
    def validate_weight(cls, value):
        if value > 1000:
            raise ValueError('Груз слишком тяжелый нужно меньше 1000')
        if value < 1:
            raise ValueError('Груз слишком легкий')
        if not isinstance(value, int):
            raise ValueError('Груз должен содержать только цифры')
        return value


class CargoCreateModel(CargoModel):
    pick_up: str
    delivery: str

    @validator('pick_up', 'delivery')
    def validate_zip_code(cls, value):
        if len(value) != 5:
            raise ValueError('Неправильный zip code(кол-во символов)')
        if not value.isdigit():
            raise ValueError('zip code должен содержать только цифры')
        return value

    class Config:
        schema_extra = {
            "example": {
                "description": "Бананы",
                "weight": 100,
                "pick_up": "00601",
                "delivery": "02038"
            }
        }


class CargoUpdateModel(CargoModel):
    class Config:
        schema_extra = {
            "example": {
                "description": "Апельсины",
                "weight": 100,
            }
        }


class StateModel(BaseModel):
    id: int
    name: str


class LocationResponseModel(BaseModel):
    city: str
    state: StateModel
    zip_code: int
    latitude: str
    longitude: str


class CarsDictanseResponseModel(BaseModel):
    vin_number: str
    distanse: int


class CargoCreateResponseModel(BaseModel):
    id: int
    description: Optional[str] = None
    weight: int
    pick_up: LocationResponseModel
    delivery: LocationResponseModel


class CargoResponseModel(BaseModel):
    description: Optional[str] = None
    weight: int
    pick_up: LocationResponseModel
    delivery: LocationResponseModel
    cars_list: dict[str, int] = None


class CargoCountResponseModel(BaseModel):
    description: Optional[str] = None
    weight: int
    pick_up: LocationResponseModel
    delivery: LocationResponseModel
    count_car: int


class CargoListResponseModel(BaseModel):
    data: list[CargoCountResponseModel]


class CarUpdateModel(BaseModel):
    zip_code: int
