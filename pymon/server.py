from flask import Flask, request, abort
import json
import pymon.protocol as proto
import pymon.messages as messages
import pymon.database as db


app = Flask(__name__)
db.bind()

@app.route('/')
def server_home():
    return 'PyMonitor'

@app.route('/submit', methods=['POST'])
def server_data():
    print('DATA', request.json)
    message = messages.Message.load(request.json)
    try:
        response = proto.handle(message)
    except Exception as err:
        print('ERROR', err)
        abort(500) 
    return response.dump()

