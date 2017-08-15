import os
import hashlib
import urllib
import subprocess
from configuration import image_base_folder, timelapse_base_folder, verbose
from urllib.request import urlopen, urlretrieve

import time


def get_image(name, url, last_md5=0):
    timestamp = str(int(time.time()))
    md5 = get_remote_md5_sum(url)
    if md5 != last_md5:
        if verbose:
            print("New image from webcam {}\nlast image md5 hash: {}\nnew image md5 hash: {}".format(name, last_md5, md5))
        else:
            print("New image from webcam {}".format(name))

        image_base_folder_full_path = os.path.expanduser(image_base_folder)
        image_folder = "{}/{}/".format(image_base_folder_full_path, name)
        file_path = "{}{}_{}.jpg".format(image_folder, name, timestamp)
        check_folder(image_folder)
        try:
            urlretrieve(url, file_path)
            return md5
        except (urllib.error.ContentTooShortError, urllib.error.HTTPError, urllib.error.URLError) as err:
            print(err)
            if os.path.exists(file_path):
                if os.stat(file_path).st_size == 0:
                    os.remove(file_path)

    if verbose: print("Duplicate image from webcam {}... skip".format(name))
    return last_md5


def create_timelapse(name):
    timestamp = str(int(time.time()))
    check_folder("{}/{}/".format(timelapse_base_folder, name))

    ffmpeg_command = "ffmpeg -r 24 -pattern_type glob -i '{0}/{2}/*.jpg' -s hd480 -vcodec libx264 {1}/{2}/{2}_{3}.mp4"
    subprocess.call(ffmpeg_command.format(image_base_folder, timelapse_base_folder, name, timestamp), shell=True)


def check_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_remote_md5_sum(url, max_file_size=100*1024*1024):
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
