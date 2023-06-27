from flask import Flask
import time
import requests
from dateutil import parser


# The last appointment that we've notified about, to prevent duplicate notifications
prevstart = None

def check():
    global prevstart

    # Check if any appointments are available, and if so, notify
    # Return True on error

    # TODO: Update the URL to match your location. (Use network monitor to find the URL in their appointment selector.) This URL points to Seattle's NEXUS center.
    resp = requests.get('https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId=5300&minimum=1')
    if not resp.ok:
        return True
    appts = resp.json()
    if len(appts) > 0:
        appt = appts[0]
        start = appt.get('startTimestamp', '2099-01-01T00:00')
        # Prevent duplicates
        if start != prevstart:
            print(f'Found appt on {start}')
            prevstart = start
            date = parser.parse(start)
            if date.year == 2023:
                print('found')
    print(f'Found 0 appts')
    return False

while True:
    if check():
        # Wait for 15 mins after error
        time.sleep(60*15)
    else:
        # Wait 1 min otherwise
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


