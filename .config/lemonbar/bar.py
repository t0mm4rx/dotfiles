import datetime
import time as t
import i3ipc
import threading
import os
import psutil
import urllib.request
import subprocess
import json

green_gray = "#404552"
dark_gray = "#DD383C4A"
gray = "#4B5162"
blue = "#5294E2"
light_gray = "#7C818C"
white = "#EEE"

icons = [
    u"\uf268",
    u"\uf121",
    u"\uf120",
    "4",
    "5",
    "6",
    "7",
    "8",
    u"\uf001",
    u"\uf086"
]

i3 = i3ipc.Connection()

# Buffers
date_buffer = ""
time_buffer = ""
ws_buffer = ""
perf_buffer = ""
spotify_buffer = ""
weather_buffer = ""

def write(content):
    with open(os.path.expanduser("~/.config/lemonbar/bar"), "w+") as file:
        file.write(content)

# Get the string for color
def color(c, type):
    return "%{" + type + c + "}"

def gen_string():
    res = ""
    res += "%{l}"
    res += ws_buffer

    res += color(dark_gray, "B")
    res += "%{c}"
    res += color(white, "F")
    res += time_buffer
    res += " "
    res += color(light_gray, "F")
    res += date_buffer

    res += "%{r}"
    res += color(white, "F") + weather_buffer
    res += color(white, "F") + spotify_buffer + " " + color(light_gray, "F")
    res += perf_buffer

    res += color(dark_gray, "B")
    write(res)

# Modules
def date():
    global date_buffer
    now = datetime.datetime.now()
    date_buffer = now.strftime('%d/%m/%Y')
    gen_string()
    t.sleep(60)
    date()

def time():
    global time_buffer
    now = datetime.datetime.now()
    time_buffer = now.strftime('%H:%M:%S')
    gen_string()
    t.sleep(1)
    time()

def workspaces():
    global ws_buffer
    ws_buffer = ""
    ws = i3.get_workspaces()
    for w in ws:
        if (w.focused):
            ws_buffer += color(blue, "B")
        else:
            ws_buffer += color(dark_gray, "B")
        ws_buffer += color(white, "F")

        ws_buffer += " %{A:i3-go-" + str(w.num) + ":}" + icons[w.num - 1] + "%{A} "
    gen_string()

def perf():
    global perf_buffer
    perf_buffer = "CPU:" + color(white, "F") + str(psutil.cpu_percent()) + "% " + color(light_gray, "F")
    perf_buffer += "RAM:" + color(white, "F") + str(psutil.virtual_memory().percent) + "% " + color(light_gray, "F")
    perf_buffer += "Disk:" + color(white, "F") + str(int(psutil.disk_usage('/')[3])) + "% "
    gen_string()
    t.sleep(1)
    perf()

def spotify():
    global spotify_buffer
    cmd_song = "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:org.mpris.MediaPlayer2.Player string:Metadata | sed -n '/title/{n;p}' | cut -d '\"' -f 2"
    spotify_buffer = ""
    try:
        subprocess.check_output("pgrep spotify", shell=True, stderr=subprocess.DEVNULL)
        song = str(subprocess.check_output(cmd_song, shell=True, stderr=subprocess.DEVNULL), "utf-8").replace("\n", "")
        spotify_buffer = u"\uf1bc " + song[:30] + u" %{A:spotify-previous:}\uf04a%{A} %{A:spotify-pause:}\uf04b%{A} %{A:spotify-next:}\uf04e%{A}"
    except:
        spotify_buffer = ""

    gen_string()
    t.sleep(5)
    spotify()

def weather():
    t.sleep(5)
    global weather_buffer
    url = "http://api.openweathermap.org/data/2.5/weather?q=lyon&appid=77d4b14c8aa6e7d25da6b2aebe4c33b7&units=metric"
    res = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))
    weather_buffer = u"\uf743 " + res['weather'][0]['main'] + color(light_gray, "F") + " - " + str(int(res['main']['temp_min'])) + "°/" + color(white, "F") + str(int(res['main']['temp_max'])) + "°" + color(light_gray, "F")
    gen_string()
    t.sleep(10 * 60)
    weather()


# Callback when the workspace is changed
def workspace_update(a, b):
    workspaces()

workspaces()

i3.on('workspace::focus', workspace_update)

i3_thread = threading.Thread(target=i3.main)
i3_thread.start()

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
