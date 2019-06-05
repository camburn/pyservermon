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
    def load(data, message_type=None):
        """ Factory method to load messages from serialised form """
        '''
        Data takes the form of:
        any dictionary is modelled as a type...

        {... : ..., ... :[{}], ... : {}}
        We need to locate these plural, or non plural subtypes and convert them as well
        '''
        print('CONVERTING', data)
        if not message_type:
            message_type = data['type']
            del data['type']
        print(f'Got a {message_type} message')
        message = globals()[message_type](**data)
        return message


@dataclass
class ConnectionRequest(Message):
    """ Used for a client to request  connection to the server """
    name: str


@dataclass
class ConnectionResponse(Message):
    """ Server response to indicate connecti on validity """
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

    def __post_init__(self):
        monitors = []
        for mon in self.monitors:
            if isinstance(mon, dict):
                mon_obj = Message.load(mon, 'MonitorState')
                monitors.append(mon_obj)
            else:
                monitors.append(mon)
        self.monitors = monitors


@dataclass
class MonitorStateResponse(Message):
    status: bool


@dataclass
class MonitorRecord(Message):
    name: str
    value: float

