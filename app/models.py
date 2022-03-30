from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlite3 import Timestamp
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey


class Post(Base):
    # what do we want to call table in postgres
    __tablename__ = 'posts'

    # define columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    # returns class from another model(USer) so we can show handle of user who made post
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete='CASCADE'), primary_key=True)
