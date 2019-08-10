#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '24560'
__mtime__ = '2018/6/18'
# qq:2456056533

佛祖保佑  永无bug!

"""
import json
from contextlib import contextmanager

from scrapy import Item
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db_name = 'spider'

# HOST = 'localhost'
HOST = '200.200.200.7'
PORT = '3307'
PASSWORD = '123456'
engine = create_engine(
    'mysql+pymysql://root:{password}@{host}:{port}/{db_name}?charset=utf8'.format(password=PASSWORD, host=HOST,
                                                                                  port=PORT, db_name=db_name),
    echo=False)

table_ips = 'ips'


def create_newtable(engine):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)
        raise ('---create_new_table err----')


def get_sqlsession(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as e:
        print(e)
        raise ('--------------engine err--------------')


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @staticmethod
    def set_attrs(attrs_datas, obj):
        if not isinstance(attrs_datas, dict):
            try:
                attrs_datas = json.loads(attrs_datas)
            except Exception as e:
                raise e

        for k, v in attrs_datas.items():
            if hasattr(obj, k) and k != 'id':  # 非id属性
                setattr(obj, k, str(v))

    @classmethod
    def save_mode(cls, session, model, item):
        if item:
            if isinstance(item, Item):

                item_data = dict(item)
                # print(item_data)
            elif isinstance(item, dict):
                item_data = item
            else:
                try:
                    item_data = json.loads(item)
                except:
                    raise ('******************** item must dict ')

            cls.set_attrs(item_data, model)

            try:

                session.add(model)
                session.commit()
            except Exception as e:
                session.rollback()


                # with auto_commit(session):
                #     session.add(model)

    @staticmethod
    @contextmanager
    def auto_commit(session):
        try:
            yield
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

    @staticmethod
    def db_distinct(session, dbmodel, item, keywords):
        '''
        Db 通过url去重
        '''

        # sql = 'SELECT url from {db_name}.{table_name} WHERE url ="{keyword}" limit 1'.format(db_name=db_name,table_name=table_name,keyword=keyword)
        # result = session.execute(sql).fetchall()

        result = session.query(dbmodel).filter_by(url=keywords).first()
        if result:
            raise DropItem('丢弃DB已存在的item:\n')  # DropItem 丢弃
            # pass     # 在close_spider()方法里面调用 DropItem 会报一个异常： ERROR: Scraper close failure,  所以直接pass也行
        else:
            return item


class IPModel(BaseModel):
    __tablename__ = table_ips

    category = Column(String(50))
    protocol = Column(String(10))
    ip = Column(String(50))  # '106.113.242.211:9999'
    niming = Column(String(10))
    speed = Column(String(10))
    connect_time = Column(String(50))
    alive_time = Column(String(50))
    prove_time = Column(String(50))

    @staticmethod
    def db_distinct(session, dbmodel, item, keywords):
        '''
        重写 Db通过ip去重
        '''

        # sql = 'SELECT url from {db_name}.{table_name} WHERE url ="{keyword}" limit 1'.format(db_name=db_name,table_name=table_name,keyword=keyword)
        # result = session.execute(sql).fetchall()

        result = session.query(dbmodel).filter_by(ip=keywords).first()
        if result:
            # raise DropItem('丢弃DB已存在的item:\n')  # DropItem 丢弃
            pass  # 在close_spider()方法里面调用 DropItem 会报一个异常： ERROR: Scraper close failure,  所以直接pass也行
        else:
            return item
