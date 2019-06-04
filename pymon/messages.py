"""
# PyMonitor Protocol
This defines the internal protocol object classes.
"""
from dataclasses import dataclass, field 
import json
import typing
from pymon.io import DataEncoder


@dataclass
class Message:
    """ Base Message implementation """
    source: str
    destination: str

    def dump(self):
        """ Serialise this message for transmission """
        return json.dumps(self, cls=DataEncoder, ensure_ascii=False)

    @staticmethod
    def load(data):
        """ Factory method to load messages from serialised form """
        message_type = data['type']
        print(f'Got a {message_type} message')
        del data['type']
        message = globals()[message_type](**data)
        return message


@dataclass
class ConnectionRequest(Message):
    """ Used for a client to request connection to the server """
    name: str


@dataclass
class ConnectionResponse(Message):
    """ Server response to indicate connection validity """
    status: bool
    session_token: str


@dataclass
class MonitorState:
    """ Monitor state """
    name: str
    datatype: str


@dataclass
class MonitorStateUpdate(Message):
    """ Update the monitors """
    monitors: typing.List[MonitorState] = field(default_factory=list)


@dataclass
class MonitorStateResponse(Message):
    status: bool

