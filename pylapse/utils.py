import os
import hashlib
import urllib
import subprocess
import time
import sys

from datetime import datetime
from pylapse.configuration import image_base_folder, timelapse_base_folder, min_fetch_interval
from urllib.request import urlopen, urlretrieve


class FetchTimeStrategy:
    """Base class for fetch time strategy"""

    def __init__(self):
        self.timeout = min_fetch_interval
        self.fs_thresh_reached = False

    def increase(self, max_timeout=sys.maxsize):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))

    def decrease(self, min_timeout=1):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))


class TcpLikeStrategy(FetchTimeStrategy):
    """Timing strategy inspired by TCP collision avoidance strategy"""

    def fs_thresh_on_reach(self):
        self.fs_thresh_reached = True
        self.timeout = (self.timeout - 1) * 2

    def increase(self, max_timeout=sys.maxsize):
        # Fast start threshold strategy
        if self.fs_thresh_reached:
            self.timeout += 1

        # General strategy
        else:
            self.timeout = self.timeout * 2

    def decrease(self, min_timeout=1):
        self.timeout = max(self.timeout - 1, min_timeout)


def get_image(name, url, last_md5=0):
    timestamp = str(int(time.time()))

    md5 = None
    try:
        md5 = _get_remote_md5_sum(url)
    except (urllib.error.ContentTooShortError, urllib.error.HTTPError, urllib.error.URLError) as err:
        print(err)

    if md5 and md5 != last_md5:
        image_base_folder_full_path = os.path.expanduser(image_base_folder)
        image_folder = "{}/{}/".format(image_base_folder_full_path, name)
        file_path = "{}{}_{}.jpg".format(image_folder, name, timestamp)

        print("{} - New image fetched from webcam '{}'... Saved to {}".format(str(datetime.now()), name, file_path))

        _check_folder(image_folder)
        try:
            urlretrieve(url, file_path)
            return md5, last_md5
        except (urllib.error.ContentTooShortError, urllib.error.HTTPError, urllib.error.URLError) as err:
            print(err)

        if os.path.exists(file_path):
            if os.stat(file_path).st_size == 0:
                os.remove(file_path)

    return md5, last_md5


def create_timelapse(name):
    timestamp = str(int(time.time()))
    _check_folder("{}/{}/".format(timelapse_base_folder, name))

    ffmpeg_command = "ffmpeg -r 24 -pattern_type glob -i '{0}/{2}/*.jpg' -s hd480 -vcodec libx264 {1}/{2}/{2}_{3}.mp4"
    subprocess.call(ffmpeg_command.format(image_base_folder, timelapse_base_folder, name, timestamp), shell=True)


def calculate_interval(strategy, action="increase"):
    """Calculate the next timeout before fetching a new image"""

    if action == "increase":
        strategy.increase()
    elif action == "decrease":
        if strategy.fs_thresh_reached:
            strategy.decrease(min_fetch_interval)
        else:
            strategy.fs_thresh_on_reach()

    return strategy.timeout


def _check_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def _get_remote_md5_sum(url, max_file_size=100 * 1024 * 1024):
    remote = urlopen(url)
    md5_hash = hashlib.md5()

    total_read = 0
    while True:
        data = remote.read(4096)
        total_read += 4096

        if not data or total_read > max_file_size:
            break

        md5_hash.update(data)

    return md5_hash.hexdigest()
