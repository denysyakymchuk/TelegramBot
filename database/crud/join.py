from database.database import session
from database.models import Join


class JoinClass:
    def __init__(self):
        pass

    def get_joins(self):
        return session.query(Join).all()

    def one_join(self, id=None, id_client=None):
        if id_client is None:
            return session.query(Join).filter_by(id=id).first()
        else:
            return session.query(Join).filter_by(id_client=id_client).first()

    def store_join(self, id_client, is_instructed):
        data = Join(id_client=id_client, is_instructed=is_instructed)
        session.add(data)
        session.commit()
        return data

    def update_join(self, id, id_client=None, is_instructed=None):
        data = session.query(Join).filter_by(id=id).first()
        if id_client:
            data.id_client = id_client
        if is_instructed:
            data.is_instructed = is_instructed
        session.commit()
        return data

    def delete_join(self, id=None, id_client=None):
        if id_client is not None:
            data = session.query(Join).filter_by(id_client=id_client).first()
        elif id is not None:
            data = session.query(Join).filter_by(id=id).first()

        session.delete(data)
        session.commit()

