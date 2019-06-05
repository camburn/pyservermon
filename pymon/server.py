from flask import Flask, request, abort
import json
import pymon.protocol as proto
import pymon.messages as messages
import pymon.database as db


app = Flask(__name__)
db.bind()

@app.route('/')
def server_home():
    data = '<h1>PyMonitor</h1></b>'
    with db.db_session():
        for server in db.select(s for s in db.Server):
            data += f'<p>{server.name} - {server.create_date} - {server.update_date}</p>'
            for monitor in server.monitors:
                data += f'<p>\t- {monitor.name} - {monitor.create_date} - {monitor.update_date}- {len(monitor.records)}</p>'
                for record in monitor.records:
                    data+= f'&emsp; {record.value}<br>'
    return data


@app.route('/submit', methods=['POST'])
def server_data():
    print('DATA', request.json)
    message = messages.Message.load(request.json)
    #try:
    response = proto.handle(message)
    #except Exception as err:
    #    print('ERROR', err)
    #    abort(500)
    if response is None:
        return '', 200
    return response.dump()
