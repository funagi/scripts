#! /usr/bin/env python3

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base

import settings


Base = declarative_base()


class Pixiv(Base):
    __tablename__ = 'illust'

    illust_id = Column(String, primary_key=True)
    user_id = Column(String)
    illust_ext = Column(String)
    title = Column(String)
    image_server = Column(String)
    user_name = Column(String)
    illust128 = Column(String)
    illust480 = Column(String)
    time = Column(String)
    tags = Column(String)
    software = Column(String)
    vote = Column(String)
    point = Column(String)
    view_count = Column(String)
    description = Column(String)
    pages = Column(String)
    bookmarks = Column(String)
    user_login_id = Column(String)
    user_profile_image_url = Column(String)


    def __repr__(self):
        return "<Pixiv(id={})>".format(self.illust_id)


def db_connect():
    return create_engine(settings.DATABASE)


def create_table(engine):
    Base.metadata.create_all(engine)