from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from src.models import init_database
from src.routers import cargo_router, vehicle_router
from src.utils import (
    update_location_car,
    create_car,
    create_locations,
    get_and_check_location_exist,
    get_and_check_vehicle_exist
)

init_database()
if not get_and_check_location_exist(id=1):
    create_locations()
if not get_and_check_vehicle_exist(id=1):
    create_car()

app = FastAPI(title='Delivery Test')

app.include_router(cargo_router)
app.include_router(vehicle_router)


@app.on_event('startup')
def startup_event():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_location_car, 'cron', minute='*/3')
    scheduler.start()
