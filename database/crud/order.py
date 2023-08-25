from database.database import session
from database.models import Order


class OrderClass:
    def __init__(self):
        pass

    def get_orders(self):
        return session.query(Order).all()

    def one_order(self, id):
        return session.query(Order).filter_by(id=id).first()

    def store_order(self, name_client, telegram_id, is_accept_op, is_accept_client):
        data = Order(name_client=name_client,
                     telegram_id=telegram_id, is_accept_op=is_accept_op,
                     is_accept_client=is_accept_client)
        session.add(data)
        session.commit()
        return data

    def update_order(self, id, name_client, telegram_id, is_accept_op, is_accept_client):
        data = session.query(Order).filter_by(id=id).first()
        data.name_client = name_client
        data.telegram_id = telegram_id
        data.is_accept_op = is_accept_op
        data.is_accept_client = is_accept_client
        session.commit()
        return data

    def delete_order(self, id):
        data = session.query(Order).filter_by(id=id).first()
        session.delete(data)
        session.commit()

