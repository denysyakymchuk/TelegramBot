from database.database import session
from database.models import Operator


class OperatorClass:
    def __init__(self):
        pass

    def get_operators(self):
        return session.query(Operator).all()

    def one_operator(self, id):
        return session.query(Operator).filter_by(id=id).first()

    def store_operator(self, name_operator, id_telegram_op):
        data = Operator(name_operator=name_operator,
                        id_telegram_op=id_telegram_op)
        session.add(data)
        session.commit()
        return data

    def update_operator(self, id_telegram_op, id=None, name_operator=None, is_free=False):
        data = session.query(Operator).filter_by(id_telegram_op=id_telegram_op).first()
        if name_operator is not None:
            data.name_operator = name_operator
        if id_telegram_op is not None:
            data.id_telegram_op = id_telegram_op
        if is_free is not None:
            data.id_telegram_op = id_telegram_op

        session.commit()
        return data

    def delete_operators(self, id):
        data = session.query(Operator).filter_by(id=id).first()
        session.delete(data)
        session.commit()

