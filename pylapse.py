import asyncio
import configuration as config
from periodictask import PeriodicTask
from utils import get_image, create_timelapse
from functools import partial

for webcam_name, webcam_params in config.webcams.items():
    # Create async tasks for image scraping
    scrape_images_task = PeriodicTask(func=partial(get_image, webcam_name, webcam_params["url"]),
                                      interval=webcam_params["refreshTime"])

    # Create async tasks for timelapse creation
    if config.create_timelapse:
        create_timelapse_task = PeriodicTask(func=partial(create_timelapse, webcam_name),
                                             interval=config.timelapse_creation_interval)

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    print('Stopping all tasks')
    for pending_task in asyncio.Task.all_tasks():
        pending_task.stop()
