from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, JSON, BigInteger, create_engine
from sqlalchemy.schema import MetaData
import os

Base = declarative_base(metadata=MetaData(schema='public'))


class User(Base):
    __tablename__ = 'users'
    user_id_seq = Sequence('user_id_seq', metadata=Base.metadata)
    id = Column(BigInteger, user_id_seq, server_default=user_id_seq.next_value(), primary_key=True)
    username = Column(String)
    config = Column(JSON)

    def __repr__(self):
        return {
            'id': self.id,
            'username': self.username,
            'config': self.config
        }


class Product(Base):
    __tablename__ = 'products'
    product_id_seq = Sequence('product_id_seq', metadata=Base.metadata)
    id = Column(BigInteger, product_id_seq, server_default=product_id_seq.next_value(), primary_key=True)
    config = Column(JSON)

    def __repr__(self):
        return {
            'id': self.id,
            'config': self.config
        }
