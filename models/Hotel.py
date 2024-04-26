from database import db


class Hotel(db.Model):
    __tablename__ = 'hotels'

    hotel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    stars = db.Column(db.Float(precision=1), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    city = db.Column(db.String(40), nullable=False)

    def __init__(self, name, stars, price, city):
        self.name = name
        self.stars = stars
        self.price = price
        self.city = city

    def to_json(self):
        return {
            'id': self.hotel_id,
            'name': self.name,
            'stars': self.stars,
            'price': self.price,
            'city': self.city
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findbyid(cls, hotel_id):
        return cls.query.filter_by(hotel_id=hotel_id).first()

    @classmethod
    def findall(cls):
        return cls.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
