import sqlite3
from datetime import datetime

from pony.orm import (PrimaryKey, Database, Required, Optional, Set,
        db_session, select, ObjectNotFound
)

import pymon.settings

db = Database()

def bind():
    db.bind('sqlite', 'pymon.db', create_db=True)
    db.generate_mapping(create_tables=True)


class Server(db.Entity):
    """ """
    name = PrimaryKey(str)
    create_date = Required(datetime)
    update_date = Optional(datetime)
    monitors = Set('Monitor')
    session_token = Required(str)


class Monitor(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    create_date = Required(datetime)
    update_date = Optional(datetime)
    server = Required(Server)
    records = Set("Record")


class Record(db.Entity):
    id = PrimaryKey(int, auto=True)
    monitor = Required(Monitor)
    data = Required(str)
    create_date = Required(datetime)


import random
if __name__ == '__main__':
    with db_session():
        s = Server(name='test-server-01', create_date=datetime.utcnow())
        m = Monitor(name='cpu-usage', create_date=datetime.utcnow(), server=s)
        for x in range(10):
            v = random.randrange(1,100)
            Record(monitor=m, data=f'{v}%', create_date=datetime.utcnow())
        m = Monitor(name='updates-required', 
                    create_date=datetime.utcnow(),
                    server=s) 
        m = Monitor(name='free-memory', create_date=datetime.utcnow(), server=s) 
        db.commit()

        for v in select(p for p in Server):
            print(v.id, v.name, v.create_date)
            for mon in v.monitors:
                print('\t-', mon.name, mon.create_date, len(mon.records))
                for rec in mon.records:
                    print('\t\t-', rec.data)

"""
class Database:
    def __init__(self):
        self.connection = sqlite3.connect(pymon.settings.DB_LOC)

        cursor = self.connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS server
            (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                create_date TEXT,
                last_update TEXT
            )'''
        )
        cursor.execute('''CREATE TABLE IF NOT EXISTS monitor
            (
                id INT PRIMARY KEY,
                serverid INT,
                name TEXT NOT NULL,
                create_date TEXT,
                last_update TEXT,
                FOREIGN KEY(serverid) references server(id)
            )'''
        )
        cursor.execute('''CREATE TABLE IF NOT EXISTS record
            (
                id INT PRIMARY KEY,
                monitorid INT,
                name TEXT NOT NULL,
                create_date TEXT,
                FOREIGN KEY(monitorid) references monitor(id)
            )'''
        )
        self.connection.commit()
        cursor.close()
"""


