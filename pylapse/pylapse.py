import asyncio
from functools import partial
from pylapse.periodictask import PeriodicTask
from pylapse.utils import get_image, create_timelapse
from pylapse.configuration import webcams, timelapse_creation_interval


def main():
    for webcam_name, webcam_params in webcams.items():
        # Create async tasks for image scraping
        PeriodicTask(func=partial(get_image, webcam_name, webcam_params["url"]))

        # Create async tasks for timelapse creation
        if create_timelapse:
            PeriodicTask(func=partial(create_timelapse, webcam_name),
                         interval=timelapse_creation_interval)

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('Stopping all tasks')
        for pending_task in asyncio.Task.all_tasks():
            pending_task.stop()


if __name__ == '__main__':
    main()
