import datetime
import time as t
import threading
import os
import psutil
import urllib.request
import subprocess
import json
import math

icons = [
    u"\uf268",
    u"\uf121",
    u"\uf120",
    "4",
    "5",
    "6",
    "7",
    u"\uf108",
    u"\uf001",
    u"\uf086"
]

# Buffers
date_buffer = ""
time_buffer = ""
ws_buffer = ""
perf_buffer = ""
spotify_buffer = ""
weather_buffer = ""

def write(content):
    with open(os.path.expanduser("~/.config/sway/bar/bar"), "w+") as file:
        file.write(content)

# Get the string for color
def color(c, type):
    return "%{" + type + c + "}"

def gen_string():
    res = ""
    res += time_buffer
    res += " "
    res += date_buffer

    res += " " + weather_buffer + " "
    res += spotify_buffer
    res += perf_buffer

    write(res)

# Modules
def date():
    global date_buffer
    while True:
        now = datetime.datetime.now()
        date_buffer = now.strftime('%d/%m/%Y')
        gen_string()
        t.sleep(60)

def time():
    global time_buffer
    while True:
        now = datetime.datetime.now()
        time_buffer = now.strftime('%H:%M:%S')
        gen_string()
        t.sleep(1)

def perf():
    global perf_buffer
    while True:
        perf_buffer = "Battery:" + str(math.floor(psutil.sensors_battery().percent)).zfill(2) + "% "
        perf_buffer += "CPU:" + str(math.floor(psutil.cpu_percent())).zfill(2) + "% "
        perf_buffer += "RAM:" + str(math.floor(psutil.virtual_memory().percent)).zfill(2) + "% "
        perf_buffer += "Disk:" + str(int(psutil.disk_usage('/')[3])).zfill(2) + "% "
        gen_string()
        t.sleep(1)

def spotify():
    global spotify_buffer
    while True:
        cmd_song = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n '/title/{n;p}' | cut -d '\"' -f 2"
        spotify_buffer = ""
        try:
            subprocess.check_output("pgrep spotify", shell=True, stderr=subprocess.DEVNULL)
            song = str(subprocess.check_output(cmd_song, shell=True, stderr=subprocess.DEVNULL), "utf-8").replace("\n", "")
            spotify_buffer = song + " "
        except:
            spotify_buffer = ""

        gen_string()
        t.sleep(5)

def weather():
    while True:
        t.sleep(5)
        global weather_buffer
        url = "http://api.openweathermap.org/data/2.5/weather?q=lyon&appid=77d4b14c8aa6e7d25da6b2aebe4c33b7&units=metric"
        res = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
        weather_buffer = res['weather'][0]['main'] + " - " + str(int(res['main']['temp_min'])) + "°/" + str(int(res['main']['temp_max'])) + "°"
        gen_string()
        t.sleep(10 * 60)

time_thread = threading.Thread(target=time)
time_thread.start()

date_thread = threading.Thread(target=date)
date_thread.start()

perf_thread = threading.Thread(target=perf)
perf_thread.start()

spotify_thread = threading.Thread(target=spotify)
spotify_thread.start()

weather_thread = threading.Thread(target=weather)
weather_thread.start()
