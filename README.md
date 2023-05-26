# fastapi_delivery
## Описание
Delivery - это api где можно добавлять грузы и отслеживать дистанцию до ближайщих машин.

#### Реализован функционал, дающий возможность:
* Добавлять и удалять посылки.
* Редактировать описание и все посылки. 
* Редактировать нахождение машины по zip code.
* Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль)).
* Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза).
* Фильтр списка грузов (вес, мили ближайших машин до грузов)
* Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).
* Подключена документация swagger.

### Технологии
``` 
Fastapi
geopy
apscheduler
ponyORM
postgres
```

# Endpoint:
- Ресурс docs#: Документация проекта
- Ресурс cargo/show_all: Получение информации о всех посылках.
- Ресурс cargo/create: Создание посылки, вес посылки ограничен от 1 до 1000
- Ресурс cargo/{pk}: Получение, удаление, изменение груза. 
- Ресурс vehicle/{pk}: Редактирование машины по ID (локация (определяется по введенному zip-коду)).

# инструкция по запуску и настройке

## в терминале выполнить команду:
git clone git@github.com:OlegZhigulin/fastapi_delivery.git
## для запуска контейнера выполнить команду :
### с логами в терминале:
docker-compose up --build
### без логов в терминале:
docker-compose up -d --build

## Теперь проект доступен по адресу: http://127.0.0.1:8000/docs
# Примеры запросов к API:

### Пример запроса http://127.0.0.1:8000/cargo/show_all на отображение списка грузов, доступна фильтрация по весу и расстояние до машин(по умолчанию <=450)
```
{
  "data": [
    {
      "description": "Апельсины",
      "weight": 100,
      "pick_up": {
        "city": "Pillsbury",
        "state": {
          "id": 32,
          "name": "North Dakota"
        },
        "zip_code": 58065,
        "latitude": "47.20035",
        "longitude": "-97.76612"
      },
      "delivery": {
        "city": "Palos Heights",
        "state": {
          "id": 34,
          "name": "Illinois"
        },
        "zip_code": 60463,
        "latitude": "41.66084",
        "longitude": "-87.79033"
      },
      "count_car": 20
    },
    {
      "description": "asdfgkkkkkh",
      "weight": 600,
      "pick_up": {
        "city": "Adjuntas",
        "state": {
          "id": 1,
          "name": "Puerto Rico"
        },
        "zip_code": 601,
        "latitude": "18.18027",
        "longitude": "-66.75266"
      },
      "delivery": {
        "city": "Hingham",
        "state": {
          "id": 3,
          "name": "Massachusetts"
        },
        "zip_code": 2043,
        "latitude": "42.21678",
        "longitude": "-70.88494"
      },
      "count_car": 12
    },
  ]
}
```
### Пример запроса http://127.0.0.1:8000/cargo/create на создание груза
## Тело запроса
```
{
  "description": " Оливки",
  "weight": 1000,
  "pick_up": "00610",
  "delivery": "02038"
}
```
## Пример ответа
```
{
    "id": 13,
    "description": "Оливки",
    "weight": 1000,
    "pick_up": {
        "city": "Anasco",
        "state": {
            "id": 1,
            "name": "Puerto Rico"
        },
        "zip_code": 610,
        "latitude": "18.2911",
        "longitude": "-67.12243"
    },
    "delivery": {
        "city": "Franklin",
        "state": {
            "id": 3,
            "name": "Massachusetts"
        },
        "zip_code": 2038,
        "latitude": "42.08622",
        "longitude": "-71.41126"
    }
}
```
## При не верных данных: вес, zip code отправления получения
```
{
    "detail": [
        {
            "loc": [
                "body",
                "weight"
            ],
            "msg": "Груз слишком тяжелый нужно меньше 1000",
            "type": "value_error"
        },
        {
            "loc": [
                "body",
                "pick_up"
            ],
            "msg": "Неправильный zip code(кол-во символов)",
            "type": "value_error"
        }
    ]
}
```
### Пример запроса http://127.0.0.1:8000/cargo/12 на получение информации о грузе по ID
```
{
  "description": "Бананы",
  "weight": 100,
  "pick_up": {
    "city": "Adjuntas",
    "state": {
      "id": 1,
      "name": "Puerto Rico"
    },
    "zip_code": 601,
    "latitude": "18.18027",
    "longitude": "-66.75266"
  },
  "delivery": {
    "city": "Franklin",
    "state": {
      "id": 3,
      "name": "Massachusetts"
    },
    "zip_code": 2038,
    "latitude": "42.08622",
    "longitude": "-71.41126"
  },
  "cars_list": {
    "9946I": 3730,
    "4279W": 2170,
    "8277T": 1531,
    "5786Z": 1922,
    "4749Z": 2752,
    "6145I": 2058,
    "5592C": 2116,
    "6677B": 2388,
    "2212D": 2250,
    "6298Q": 2245,
    "4618N": 1807,
    "6755B": 3069,
    "2156G": 3343,
    "7114I": 2344,
    "3358D": 1861,
    "5018Z": 1824,
    "6629P": 2117,
    "6867V": 1750,
    "8220K": 1590,
    "1723E": 1984
  }
}
```
### Пример запроса  http://127.0.0.1:8000/cargo/12 на удаление груза по ID

При успешном запросе получаем статус код 204:

При не успешном:
```
{
  "detail": "Посылка не найдена"
}
```

### Пример запроса  http://127.0.0.1:8000/vehicle/2?zip_code=00601 на изменение локации машины по zip code 


```
{
  "id": 2,
  "vin_number": "4279W",
  "capacity": 390,
  "location": {
    "id": 1,
    "zip_code": "00601",
    "latitude": "18.18027",
    "longitude": "-66.75266",
    "city": "Adjuntas",
    "state": {
      "id": 1,
      "name": "Puerto Rico"
    }
}
```
### При не верном ID машины
```
{
    "detail": "Транспорт не найден"
}
```
### При не верном zip code 
```
{
    "detail": "Такой zip_code отсутствует"
}
```