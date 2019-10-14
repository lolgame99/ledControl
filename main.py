import pigpio
from time import sleep
import requests
import json

pi = pigpio.pi()

# Get print status
# Read expected time remaining
# Make new call when 2/3 of expected time remaining are done
# if ETR < 10 sec -> wait 10 sec
# if ETR < 1h -> wait 10 min
# if ETR > -> wait 30 min

def getValues():
  url = 'http://127.0.0.1/api/job'
  resp = requests.get(url)
  data = resp.json()
  return data

# pi.set_PWM_dutycycle(r[0], r[1])
# red - 17
# green - 22
# blue - 24

def updateLight(red, green, blue):
  pi.set_PWM_dutycycle(17, red)
  pi.set_PWM_dutycycle(22, green)
  pi.set_PWM_dutycycle(24, blue)

# 255 might be too bright
def changeLight(status):
  if status == "Offline":
    # No light
    updateLight(0, 0, 0)
    print("Changed lights to Offline")

  if status == "Error" or status == "Cancelling":
    # Red light
    updateLight(255, 0, 0)
    print("Changed lights to Error")

  if status == "Printing":
    # White light
    updateLight(255, 255, 255)
    print("Changed lights to Printing")

  if status == "Pausing" or status == "Paused":
    # Yellow light
    updateLight(255, 255, 0)
    print("Changed lights to Paused")

  if status == "Operational":
    # Green light
    updateLight(0, 255, 0)
    print("Changed lights to Operational")


if __name__ == "__main__":
  status = ""
  print('Checking Status...')
  r = getValues()

  time = 0
  if r["state"] == status:
    if r["progress"]["printTimeLeft"] <= 600:
      time = r["progress"]["printTimeLeft"] * (1/2)
      if time <= 10:
        time = 10
    elif r["progress"]["printTimeLeft"] <= 3600:
      time = 600
    elif r["progress"]["printTimeLeft"] > 3600:
      time = 1800
    else:
      time = 300

    sleep(time)

  else:
    status = r["state"]
    changeLight(status)
