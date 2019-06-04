"""
# PyMonitor Protocol
This defines the internal protocol object classes.
"""
import dataclasses 
import json
import uuid
from datetime import datetime

from pymon.messages import ConnectionRequest, ConnectionResponse, MonitorStateUpdate, MonitorStateResponse
import pymon.database as db
import pymon.io as io


def connection_request(message):
    with db.db_session():
        try:
            server = db.Server[message.name]
            server.update_date = datetime.utcnow()
            print(f'Server {server.name}, {server.update_date}, {server.create_date}')
        except db.ObjectNotFound:
            print(f'Server {message.name} is new')
            server = db.Server(
                name=message.name,
                create_date=datetime.utcnow(),
                session_token=io.create_token()
            )
    return ConnectionResponse(message.source, 'Server', 'OK', server.session_token)


def monitor_state_update(message):

    return MonitorStateResponse(message.source, 'Server', 'OK')


def handle(message):
    if isinstance(message, ConnectionRequest):
        #Is this server registered?
        response = connection_request(message)

    elif isinstance(message, MonitorStateUpdate):
        response = monitor_state_update(message)
    return response

