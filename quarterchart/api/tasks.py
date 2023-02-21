import time

from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import daily_update

def update_data():
    daily_update()
    print(time.time())
    return


def start():
    scheduler = BackgroundScheduler()
    print('start scheduler')
    scheduler.add_job(update_data, 'cron', hour=1,minute=0,second=0)#GMT-> 19:00 EST
    scheduler.start()