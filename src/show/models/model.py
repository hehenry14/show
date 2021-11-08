from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, JSON
from sqlalchemy.schema import MetaData

Base = declarative_base(metadata=MetaData(schema='public'))


class User(Base):
    __tablename__ = 'users'
    user_id_seq = Sequence('user_id_seq', metadata=Base.meta_data)
    id = Column(Integer, primary_key=True, server_default=user_id_seq)
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
    product_id_seq = Sequence('product_id_seq', metadata=Base.meta_data)
    id = Column(Integer, primary_key=True, server_default=product_id_seq)
    config = Column(JSON)

    def __repr__(self):
        return {
            'id': self.id,
            'config': self.config
        }

