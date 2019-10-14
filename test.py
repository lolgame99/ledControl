import requests
import json


# Get print status
# Read expected time remaining
# Make new call when 2/3 of expected time remaining are done
# if ETR < 2 sec -> wait 2 sec
# if ETC > 5h -> wait 1h

def getValues():
  return json.dumps(requests.get('http://192.168.1.4/api/job').json())

if __name__ == "__main__":
  status = ""
  r = getValues()
  # BUG: What is timeremainvalue if print is done? Wait some time if print is done
  # TODO: If print is done -> check for changed status every 5min??

  # If status hasn't changed -> Wait 2/3 of expected time remaining
  # 2sec < ETR < 5h
  time = 0
  if r["state"] == status:
    if r["progress"]["printTimeLeft"] < 2:
      time = 2
    elif r["progress"]["printTimeLeft"] > 18000:
      time = 3600
    else:
      time = (2/3) * r["progress"]["printTimeLeft"]

    sleep(time)

  else:
    status = r["state"]
    print(status)
