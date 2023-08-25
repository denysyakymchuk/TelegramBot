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

    def update_operator(self, id, name_operator, id_telegram_op):
        data = session.query(Operator).filter_by(id=id).first()
        data.name_operator = name_operator
        data.id_telegram_op = id_telegram_op
        session.commit()
        return data

    def delete_operators(self, id):
        data = session.query(Operator).filter_by(id=id).first()
        session.delete(data)
        session.commit()

