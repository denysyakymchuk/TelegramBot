import json

from sqlalchemy import Column, Integer, String, Boolean, Text, Nullable

from database.database import Base, engine


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    name_client = Column(String(255))
    city_from = Column(String(255))
    curr_set = Column(String(255))
    total = Column(String(255))
    city_to = Column(String(255))
    curr_get = Column(String(255))
    view_money = Column(String(255))
    telegram_id = Column(String(50))
    telegram_id_operator = Column(String(50))
    is_accept_op = Column(Boolean, default=None)
    is_accept_client = Column(Boolean, default=None)
    reply_message = Column(Text, default=None)

    def __repr__(self):
        data = {"id": self.id,
                "name_client": self.name_client,
                "telegram_id": self.telegram_id,
                "is_accept_op": self.is_accept_op,
                "is_accept_client": self.is_accept_client,
                "reply_message": self.reply_message,
                "city_from": self.city_from,
                "curr_set": self.curr_set,
                "total": self.total,
                "city_to": self.city_to,
                "curr_get": self.curr_get,
                "view_money": self.view_money}
        return json.dumps(data)

    def __str__(self):
        data = {"id": self.id,
                "name_client": self.name_client,
                "telegram_id": self.telegram_id,
                "telegram_id_operator": self.telegram_id,
                "is_accept_op": self.is_accept_op,
                "is_accept_client": self.is_accept_client,
                "reply_message": self.reply_message,
                "city_from": self.city_from,
                "curr_set": self.curr_set,
                "total": self.total,
                "city_to": self.city_to,
                "curr_get": self.curr_get,
                "view_money": self.view_money}
        return json.dumps(data)


class Operator(Base):
    __tablename__ = 'operators'

    id = Column(Integer, primary_key=True)
    name_operator = Column(String(255))
    id_telegram_op = Column(String(50))
    is_free = Column(Boolean)

    def __repr__(self):
        data = {"id_telegram_op": self.id_telegram_op}
        return json.dumps(data)
    
    def __str__(self):
        data = {"id_telegram_op": self.id_telegram_op}
        return json.dumps(data)


Base.metadata.create_all(engine)
