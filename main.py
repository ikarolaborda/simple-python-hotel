from flask import Flask, jsonify
from flask_restful import Api
from resources.HotelResource import HotelResource
from resources.UserResource import UserResource
from resources.AuthResource import AuthResource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt
)
from flask_jwt_extended.exceptions import (
    NoAuthorizationError, InvalidHeaderError,
    WrongTokenError, RevokedTokenError, FreshTokenRequired
)
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotels.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '5d743878c9ba26c78cada6641c565d2ee375ead2e94b4450d9181366e0520929'
jwt = JWTManager(app)


# Custom response for missing JWTs
@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify({
        'message': 'Missing or invalid token. Please log in or provide a valid token.'
    }), 401


# Custom response for expired tokens
@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return jsonify({
        'ok': False,
        'message': 'The token has expired. Please log in again.'
    }), 403


# Handle other JWT errors
@jwt.invalid_token_loader
def custom_invalid_token_loader(callback):
    return jsonify({
        'ok': False,
        'message': 'Invalid token. Please log in with a valid token.'
    }), 422


@jwt.needs_fresh_token_loader
def custom_needs_fresh_token_callback():
    return jsonify({
        'ok': False,
        'message': 'Fresh token required. Please reauthenticate.'
    }), 403


@jwt.revoked_token_loader
def custom_revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'ok': False,
        'message': 'Token has been revoked. Please log in again.'
    }), 401


# Example route protected by JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


api = Api(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return jsonify({'message': 'The API is Running! Visit /hotels to see the hotels list'})


api.add_resource(HotelResource, '/hotels', endpoint='hotels')
api.add_resource(HotelResource, '/hotels/<int:hotel_id>', endpoint='hotel', methods=['GET'])
api.add_resource(HotelResource, '/hotels/<int:hotel_id>', endpoint='hotel_update', methods=['PUT'])
api.add_resource(HotelResource, '/hotels/<int:hotel_id>', endpoint='hotel_delete', methods=['DELETE'])

api.add_resource(AuthResource, '/login', endpoint='login')
api.add_resource(AuthResource, '/register', endpoint='register', methods=['POST'])
api.add_resource(AuthResource, '/me', endpoint='me', methods=['GET'])


api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(UserResource, '/user/<int:user_id>', endpoint='user', methods=['GET'])

if __name__ == '__main__':
    from database import db

    db.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
