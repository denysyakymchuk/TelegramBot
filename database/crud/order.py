from database.database import session
from database.models import Order


class OrderClass:
    def __init__(self):
        pass

    def get_orders(self):
        return session.query(Order).all()

    def one_order(self, id):
        return session.query(Order).filter_by(id=id).first()

    def store_order(self, name_client, telegram_id,
                    is_accept_op, is_accept_client,
                    reply_message=None):
        data = Order(name_client=name_client,
                     telegram_id=telegram_id, is_accept_op=is_accept_op,
                     is_accept_client=is_accept_client,
                     reply_message=reply_message)
        session.add(data)
        session.commit()
        return data

    def update_order(self, id, name_client=None, telegram_id=None,
                     is_accept_op=None, is_accept_client=None,
                     reply_message=None):
        data = session.query(Order).filter_by(id=id).first()
        if name_client is not None:
            data.name_client = name_client
        if telegram_id is not None:
            data.telegram_id = telegram_id
        if is_accept_op is not None:
            data.is_accept_op = is_accept_op
        if is_accept_client is not None:
            data.is_accept_client = is_accept_client
        if reply_message is not None:
            data.reply_message = reply_message

        session.commit()
        return data

    def delete_order(self, id):
        data = session.query(Order).filter_by(id=id).first()
        session.delete(data)
        session.commit()

