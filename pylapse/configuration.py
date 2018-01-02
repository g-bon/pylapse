
# List of webcams to fetch.
webcams = {
    "Splugen": {"url": "http://www.albergopostaspluga.it/webcam/image_PE.jpg"},
    "Stelvio": {"url": "http://jpeg.popso.it/webcam/webcam_online/stelviolive_03.jpg"},
}

create_timelapse = False  # Default False, requires ffmpeg
min_fetch_interval = 5
timelapse_creation_interval = 3600  # Default 3600
image_base_folder = "~/Desktop/pylapse/images"  # Default ~/Desktop/pylapse/images/
timelapse_base_folder = "~/Desktop/pylapse/images"  # Default ~/Desktop/pylapse/timelapses/
