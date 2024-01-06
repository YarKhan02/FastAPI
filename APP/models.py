# To create table in postgres 

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base



class Vote(Base):
    __tablename__ = 'Votes'

    user_id = Column(Integer, ForeignKey('Users.id', ondelete = 'CASCADE'), primary_key = True)
    post_id = Column(Integer, ForeignKey('Posts.id', ondelete = 'CASCADE'), primary_key = True)



class Post(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('NOW()'))
    owner_id = Column(Integer, ForeignKey('Users.id', ondelete = 'CASCADE'), nullable = False)

    owner = Relationship("User")
    


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('NOW()'))
    phone_number = Column(String)