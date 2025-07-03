from functools import wraps
from flask import request, g, current_app
import jwt
from . import app
from .models import User
from .response import APIResponse

class Params:
    def __init__(self, id=None):
        self.id = id

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers['Authorization'])
        # token is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] # Expecting "Bearer <token>"

        if not token or token == 'null':
            return APIResponse.respond({'message': 'Token is missing!'}, status_code=401)

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['id']

            current_user = User.query.filter_by(id = user_id).first()
            if not current_user:
                return APIResponse.respond({'message': 'User not found!'}, status_code=401)
            
            user_id = Params(id=current_user.id)
            kwargs['user_id'] = user_id
        except Exception as e:
            return APIResponse.respond({'message': f'Invalid token! {str(e)}'}, status_code=401)

        return func(*args, **kwargs)

    return decorated
