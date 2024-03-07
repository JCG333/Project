from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from db import add_image_to_db
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from smhi_data_fetch import get_weather_data
import os
import logging
# from datetime import datetime

# --------- info ----------#
# This script runs both the weather fetch, and listening on the filetree if an image has been added.
# It runs in the background in its separate threads.
# ------- end info --------#

#logging.basicConfig(level=logging.INFO)

#Event Handler that checks if a file is added. Then it shall parse the filename and add it to the db.
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info("File added %s", event.src_path)
            add_image_to_db.add_data(event.src_path)


    def on_deleted(self, event):
        print("File deleted")  # Behövs det upptäckas ifall filer tas bort? Isåfall skall de tas bort från db?


def check_for_update():
    # Perform update
    # print("Checking for SMHI update at:", datetime.now())
    get_weather_data()


local_test_path = os.getcwd()
# Observing path to FTP
path = '/images'
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=path, recursive=True)
observer.start()
# print("Listener:", path)

# Create a thread with background scheduler
scheduler = BackgroundScheduler()

# Schedule the job to run every hour
scheduler.add_job(check_for_update, 'cron', id='update_job', hour='*')

# Start the scheduler
scheduler.start()
# Initial weather fetch when program starts
get_weather_data()

# Keep the main thread alive
try:
    while True:
        sleep(1e9)
except (KeyboardInterrupt, SystemExit):
    observer.stop()
    observer.join()
    scheduler.shutdown()
