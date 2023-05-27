from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from src.models import init_database
from src.routers import cargo_router, vehicle_router
from src.utils import (
    update_location_car,
    check_location_from_db,
    check_car_from_db
)

init_database()

app = FastAPI(title='Delivery Test')

app.include_router(cargo_router)
app.include_router(vehicle_router)


check_location_from_db()
check_car_from_db()


@app.on_event('startup')
def startup_event():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_location_car, 'cron', minute='*/3')
    scheduler.start()
