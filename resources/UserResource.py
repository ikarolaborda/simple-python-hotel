from flask_restful import Resource, reqparse
from models.User import User
from flask_jwt_extended import jwt_required

class UserResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, store_missing=False)
        self.reqparse.add_argument('email', type=str, store_missing=False)
        self.reqparse.add_argument('password', type=str, store_missing=False)
        super(UserResource, self).__init__()

    @jwt_required()
    def get(self):
        users = User.findall()
        return {'users': [user.to_json() for user in users]}, 200

    def getOne(self, user_id):
        user = User.findbyid(user_id)
        if user:
            return user.to_json(), 200
        return {'message': 'User not found'}, 404

    def post(self):
        data = self.reqparse.parse_args()
        try:
            user = User(**data)
            user.save()
        except ValueError as e:
            return {'message': str(e)}, 400
        return user.to_json(), 201

    def put(self, user_id):
        user = User.findbyid(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        data = self.reqparse.parse_args()
        try:
            for key, value in data.items():
                if value:
                    setattr(user, key, value)
            user.save()
        except ValueError as e:
            return {'message': str(e)}, 400

        return user.to_json(), 200

    def delete(self, user_id):
        user = User.findbyid(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user.delete()
        return {'message': 'User deleted'}, 200
