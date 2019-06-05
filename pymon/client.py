import psutil
import json
import time
import requests
import pymon.protocol as proto
import pymon.messages as messages

CLIENT_NAME = 'test-client'


def submit(message):
    response = requests.post(
        'http://127.0.0.1:5000/submit',
        data=message.dump(),
        headers={'Content-Type': 'application/json'}
    )
    if response.ok:
        try:
            print(response.json())
            print(messages.Message.load(response.json()))
        except json.JSONDecodeError:
            pass
    else:
        print('Error', response.status_code)

msg = messages.ConnectionRequest(CLIENT_NAME, 'Server', 'My first server')
mons = messages.MonitorStateUpdate(
    source=CLIENT_NAME,
    destination='Server',
    monitors=[
        messages.MonitorState('cpu-usage', 'percent'),
        messages.MonitorState('disk-free', 'GB'),
        messages.MonitorState('memory-usage', 'percent')
    ]
)

print(msg.dump())
submit(msg)
submit(mons)

while True:
    value = psutil.cpu_percent()
    update = messages.MonitorRecord(CLIENT_NAME, 'Server', 'cpu-usage', value)
    submit(update)

    value = psutil.virtual_memory().percent
    update = messages.MonitorRecord(CLIENT_NAME, 'Server', 'memory-usage', value)
    submit(update)
    time.sleep(10)

