from sqlalchemy import Column, Integer, String, create_engine, Float, BigInteger
from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME

Base = declarative_base()
engine = create_engine(F'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
session = Session()


class UserLanguage(Base):
    __tablename__ = 'users_language'
    __table_args__ = (
        Index('idx_chat_id', 'chat_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)
    language = Column(String)

    def __init__(self, chat_id, language):
        self.chat_id = chat_id
        self.language = language

    def __repr__(self):
        return f'<UserLanguage(chat_id={self.chat_id}, language={self.language})>'


class Generator(Base):
    __tablename__ = 'generators'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    height = Column(Integer)
    length = Column(Integer)
    width = Column(Integer)
    power_kbT = Column(Integer)
    power_kbA = Column(Integer)
    fuel_consumption = Column(Float)

    def __repr__(self):
        return f"<Generator(name='{self.name}', power={self.power_kbT}, fuel_consumption={self.fuel_consumption})>"


Base.metadata.create_all(engine)
