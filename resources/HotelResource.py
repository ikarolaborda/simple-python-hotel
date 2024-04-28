from flask_restful import Resource, reqparse
from models.Hotel import Hotel
from flask_jwt_extended import jwt_required


def min_max_validator(value, name, min_val, max_val):
    if not (min_val <= value <= max_val):
        raise ValueError(f"The field {name} must be between {min_val} and {max_val}")
    return value


def stars_validator(value):
    return min_max_validator(value, 'stars', 1, 5)


def price_validator(value):
    return min_max_validator(value, 'price', 50, 9999)


class HotelResource(Resource):
    @jwt_required()
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, store_missing=False)
        self.reqparse.add_argument('stars', type=stars_validator, store_missing=False)
        self.reqparse.add_argument('price', type=price_validator, store_missing=False)
        self.reqparse.add_argument('city', type=str, store_missing=False)
        super(HotelResource, self).__init__()

    def get(self):
        hotels = Hotel.findall()
        return {'hotels': [hotel.to_json() for hotel in hotels]}, 200

    def getOne(self, hotel_id):
        hotel = Hotel.findbyid(hotel_id)
        if hotel:
            return hotel.to_json(), 200
        return {'message': 'Hotel not found'}, 404

    def post(self):
        data = self.reqparse.parse_args()
        try:
            hotel = Hotel(**data)
            hotel.save()
        except ValueError as e:
            return {'message': str(e)}, 400
        return hotel.to_json(), 201

    def put(self, hotel_id):
        hotel = Hotel.findbyid(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404

        data = self.reqparse.parse_args()
        try:
            for key, value in data.items():
                if value:
                    setattr(hotel, key, value)
            hotel.save()
        except ValueError as e:
            return {'message': str(e)}, 400

        return hotel.to_json(), 200

    def delete(self, hotel_id):
        hotel = Hotel.findbyid(hotel_id)
        if not hotel:
            return {'message': 'Hotel not found'}, 404

        hotel.delete()
        return {'message': 'Hotel deleted'}, 200
