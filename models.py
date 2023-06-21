from sqlalchemy import Column, Integer, String, create_engine
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
    chat_id = Column(Integer, unique=True)
    language = Column(String)

    def __init__(self, chat_id, language):
        self.chat_id = chat_id
        self.language = language

    def __repr__(self):
        return f'<UserLanguage(chat_id={self.chat_id}, language={self.language})>'


Base.metadata.create_all(engine)

#
#
# class FSMStorage(Base):
#     __tablename__ = 'fsm_storage'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, index=True)
#     chat_id = Column(Integer, index=True)
#     state = Column(String)
#     data = Column(String)
#
#     def __init__(self, user_id, chat_id, state, data):
#         self.user_id = user_id
#         self.chat_id = chat_id
#         self.state = state
#         self.data = data
#
#     def __repr__(self):
#         return f'<FSMStorage(user_id={self.user_id}, chat_id={self.chat_id}, state={self.state}, data={self.data})>'
