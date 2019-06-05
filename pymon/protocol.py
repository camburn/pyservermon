"""
# PyMonitor Protocol
This defines the internal protocol object classes.
"""
import dataclasses 
import json
import uuid
from datetime import datetime

from pymon.messages import ConnectionRequest, ConnectionResponse, MonitorStateUpdate, MonitorStateResponse, MonitorRecord
import pymon.database as db
import pymon.io as io


@db.db_session
def connection_request(message):
    try:
        server = db.Server[message.source]
        server.update_date = datetime.utcnow()
        print(f'Server {server.name}, {server.update_date}, {server.create_date}')
    except db.ObjectNotFound:
        print(f'Server {message.name} is new')
        server = db.Server(
            name=message.source,
            create_date=datetime.utcnow(),
            session_token=io.create_token()
        )
    return ConnectionResponse(message.source, 'Server', 'OK', server.session_token)


@db.db_session
def monitor_state_update(message):
    for monitor in message.monitors:
        try:
            mon = db.Monitor[monitor.name, message.source]
            mon.update_date = datetime.utcnow()
            print('MONITOR UPDATE')
        except db.ObjectNotFound:
            print('MONITOR - ', type(monitor),  monitor)
            mon = db.Monitor(
                name=monitor.name,
                server=message.source,
                create_date=datetime.utcnow(),
                datatype=monitor.datatype
            )

    return MonitorStateResponse(message.source, 'Server', 'OK')

@db.db_session
def monitor_record(message):
    try:
        monitor = db.Monitor[message.name, message.source]
    except db.ObjectNotFound:
        return None
    record = db.Record(
        monitor=monitor,
        value=message.value,
        create_date=datetime.utcnow()
    )
    return None


def handle(message):
    if isinstance(message, ConnectionRequest):
        #Is this server registered?
        response = connection_request(message)

    elif isinstance(message, MonitorStateUpdate):
        response = monitor_state_update(message)

    elif isinstance(message, MonitorRecord):
        response = monitor_record(message)
    return response

