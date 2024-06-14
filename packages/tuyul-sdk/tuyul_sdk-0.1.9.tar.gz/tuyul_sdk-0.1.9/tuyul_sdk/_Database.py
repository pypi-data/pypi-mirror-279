from enum import Enum, auto
import os
from typing import Union
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database

class TypeConnection(Enum):
    
    ONLINE  = auto()
    OFFLINE = auto()
    HIDDEN  = auto()

class Database:

    @property
    def declarative(self) -> DeclarativeMeta:
        return declarative_base()

    class Connection:

        FileName: Union[str, None] = None
        PathName: Union[str, None] = None
        Type: Union[TypeConnection, None] = None

        @classmethod
        def BaseMetaData(cls, declarative: DeclarativeMeta) -> MetaData:
            return declarative.metadata
        
        def __init__(self) -> None:
            if self.Type == TypeConnection.ONLINE:
                DATABASE_URI = str(os.getenv('DATABASE_URI'))
            else:
                if self.FileName is not None:
                    if self.Type == TypeConnection.HIDDEN:
                        if os.path.exists(self.PathName) is False: os.mkdir(self.PathName)
                        DATABASE_URI = 'sqlite:///{}/{}.sqlite'.format(self.PathName, self.FileName)
                    else:
                        if os.path.exists('Database') is False: os.mkdir('Database')
                        DATABASE_URI = 'sqlite:///Database/{}.sqlite'.format(self.FileName)
                else:
                    raise Exception('No filename provided for the Engine.\nPlease set command Engine.build({filename})')
            self.Engine = create_engine(DATABASE_URI, echo=False, pool_pre_ping=True)

        def Connect(self):
            return self.Engine.connect()

        def Session(self) -> Session:
            Session = sessionmaker(bind=self.Engine)
            return Session()

        @staticmethod
        def build(declarative: DeclarativeMeta, Type: TypeConnection = None, PathName: str = None, FileName: str = None):
            setattr(Database.Connection, 'PathName', PathName)
            if FileName is not None:
                setattr(Database.Connection, 'FileName', FileName)
            if not Type:
                setattr(Database.Connection, 'Type', TypeConnection.OFFLINE)
            else:
                setattr(Database.Connection, 'Type', Type)
            Conn = Database.Connection()
            if not database_exists(Conn.Engine.url):
                create_database(Conn.Engine.url)
                Conn.BaseMetaData(declarative).create_all(Conn.Engine)
            else:
                #create_database(Conn.Engine.url)
                Conn.BaseMetaData(declarative).create_all(Conn.Engine)
            return Conn
