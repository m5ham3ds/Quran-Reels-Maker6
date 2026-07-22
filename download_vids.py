import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

vids = [
    "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4",
]
# Wait, I need nature.
