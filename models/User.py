from database import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_json(self):
        return {
            'id': self.user_id,
            'name': self.name,
            'email': self.email
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findbyid(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def findall(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
