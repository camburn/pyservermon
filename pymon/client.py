import json
import requests
import pymon.protocol as proto
import pymon.messages as messages

msg = messages.ConnectionRequest('Client', 'Server', 'test-client')
mons = messages.MonitorStateUpdate('Client', 'Server', [
    messages.MonitorState('cpu-usage', 'percent')    
])

print(msg.dump())
response = requests.post(
    'http://127.0.0.1:5000/submit', 
    data=msg.dump(),
    headers={'Content-Type': 'application/json'}
)
if response.ok:
    print(response.json())
    print(messages.Message.load(response.json()))
else:
    print('Error', response.status_code)

response = requests.post(
    'http://127.0.0.1:5000/submit', 
    data=mons.dump(),
    headers={'Content-Type': 'application/json'}
)
if response.ok:
    print(response.json())
    print(messages.Message.load(response.json()))
else:
    print('Error', response.status_code)
