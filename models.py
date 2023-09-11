from sqlalchemy import Column, Integer, String, create_engine, Float, BigInteger, ForeignKey
from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import DATABASE_NAME

Base = declarative_base()
engine = create_engine(F'sqlite:///{DATABASE_NAME}.db')
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


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    image = Column(String)
    generators = relationship('Generator', back_populates='category')
    generator_field_name = Column(String)


class EngineType(Base):
    __tablename__ = 'engine_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    generators = relationship('Generator', back_populates='engine_type')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Generator(Base):
    __tablename__ = 'generators'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    size = Column(String)
    power = Column(String)
    fuel_consumption = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='generators')
    engine_type_id = Column(Integer, ForeignKey('engine_types.id'))
    engine_type = relationship('EngineType', back_populates='generators')

    def __repr__(self):
        return f"<Generator(name='{self.name}', power={self.power_kbt}, fuel_consumption={self.fuel_consumption})>"


Base.metadata.create_all(engine)
