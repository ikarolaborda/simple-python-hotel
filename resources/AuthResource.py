from flask import jsonify, request
from flask_restful import Resource, reqparse
from models.User import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


class AuthResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    @jwt_required()
    def get(self):
        if request.path.endswith('/me'):
            user_id = get_jwt_identity()
            user = User.findbyid(user_id)
            if user:
                return user.to_json(), 200
            return {'message': 'User not found'}, 404




    def post(self):
        # Dynamically add arguments based on the endpoint
        self.reqparse.add_argument('email', type=str, required=True, help='Email is required')
        self.reqparse.add_argument('password', type=str, required=True, help='Password is required')
        data = self.reqparse.parse_args()

        # Check if the request path is for registration
        if request.path.endswith('/register'):
            # Handle registration
            self.reqparse.add_argument('name', type=str, required=True, help='Name is required')
            data = self.reqparse.parse_args()
            return self.register(data)

        # Handle login
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            refresh_token = create_refresh_token(identity=user.user_id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

    def register(self, data):
        print("Registering user:", data)  # Debugging output
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'message': 'A user with that email already exists'}, 409

        hashed_password = generate_password_hash(data['password'])
        user = User(name=data['name'], email=data['email'], password=hashed_password)
        user.save()

        return jsonify({
            'message': 'User created successfully',
            'user': user.to_json()
        }), 201
