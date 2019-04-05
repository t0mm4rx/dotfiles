import os

while True:
    cmd = input()

    if (cmd == "spotify-previous"):
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")
    if (cmd == "spotify-next"):
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")
    if (cmd == "spotify-pause"):
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")
    if ("i3-go-" in cmd):
        os.system('i3-msg workspace "' + cmd.split("-")[2] + '"')
