#!/usr/bin/env python3

# MainLoop
from time import sleep, time, localtime

# MC SLP
from StatusPing import StatusPing
import socket

# NTFY
import requests

NTFY_URL = "https://ntfy.sh/topic"
MC_HOST = "127.0.0.1"
MC_PORT = 25565
BAD_PING = 80  # Threshold in ms to consider a response "bad"
BAD_THRESHOLD = 3  # num of consecutive bad responses to trigger alert
CHECK_INTERVAL = 30  # Check every n seconds
NTFY_INTERVAL = 10800  # Suppress alert if previous alert was n seconds ago
IGNORE_HOURS = [3,4,5]  # Suppress alert if current local hour is in this list


def ntfySend(msg):
    headers = {
        "Title": "MC",
        "Tags": "warning",
    }

    response = requests.post(
        NTFY_URL,
        data=msg.encode(encoding='utf-8'),
        headers=headers
    )
    if response.status_code != 200:
        print(f"[ERROR] ntfy bad response! {response.status_code}")


def NotifyUser(latency):
    print((time() + NTFY_INTERVAL), lastNotif)
    if (lastNotif + NTFY_INTERVAL) < time():
        if latency == 99999:
            print("[INFO] Notify! Can't connect.")
            ntfySend("Server is down!")
        else:
            print(f"[INFO] Notify! {latency}ms")
            ntfySend(f"High latency: {latency}ms!")
    else:
        print("[WARN] Attempted notif but INTERVAL not passed, ignoring!")


consecutiveBad = 0
lastNotif = 0

while True:
    try:
        resp = StatusPing(MC_HOST, MC_PORT).get_status()
        ping = resp['ping']
    except:
        # Catch-all excepts are bad practice, but for alerts is okay
        ping = 99999
    print(f"[DEBUG] Current Ping: {ping}ms")

    # Is our connection shit?
    if ping >= BAD_PING:
        # Is bad consecutive x times?
        if consecutiveBad >= BAD_THRESHOLD:
            # Supress notifs during IGNORE_HOURS
            curTime = time()
            if not localtime(curTime)[3] in IGNORE_HOURS:
                NotifyUser(ping)
                lastNotif = curTime
            else:
                # print("[DEBUG]: Suppressed notif due to IGNORE_HOURS.")
                # override counter, to prevent notifs on hour changes.
                consecutiveBad = 0
                # Don't retry for another hour. There's no point!
                sleep(3540)
        else:
            print(f"[DEBUG] BAD: {ping}ms try {consecutiveBad}")
            consecutiveBad += 1
    else:
        consecutiveBad = 0
        # print("[DEBUG] PING dropped below BAD_THRESHOLD")
    sleep(CHECK_INTERVAL)
