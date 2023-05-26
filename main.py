import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import BackgroundTasks, Depends, FastAPI

from src.models import init_database
from src.routers import cargo_router, vehicle_router
from src.utils import update_location_car

init_database()

app = FastAPI(title='Delivery Test')

app.include_router(cargo_router)
app.include_router(vehicle_router)


@app.on_event('startup')
def startup_event():
    # background_tasks = BackgroundTasks()
    # background_tasks.add_task(run_update)
    # background_tasks()
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_location_car, 'cron', minute='*/3')
    scheduler.start()


if __name__ == '__main__':
    uvicorn.run('__main__:app', host="127.0.0.1", port=8000, reload=True)
