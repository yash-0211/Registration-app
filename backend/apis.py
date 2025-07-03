from flask import Blueprint, request
from .decorators import token_required
from .response import APIResponse
from datetime import datetime, timedelta
import jwt
import random
from datetime import datetime, timedelta
from .models import User, OTP
from . import app, db
from .otp import send_whatsapp_otp

def generate_otp():
    return str(random.randint(100000, 999999))

auth_resource = Blueprint('auth_resource', __name__)

@auth_resource.route('/', methods=['GET'])
@token_required
def index(**kwargs):
    user_id = kwargs['user_id'].id
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return APIResponse.respond({'message': 'User does not exists'}, status_code=400)

    return APIResponse.respond({'username': user.username}, status_code=200)



@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    phone_number = data.get('phone_number')
    
    if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
        return APIResponse.respond({'message': 'Invalid phone number. It must be numeric and 10 digits long.'}, status_code=400)

    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=1)
    otp_entry = OTP.query.filter_by(phone_number=phone_number).first()

    if otp_entry:
        time_since_last_otp = datetime.utcnow() - otp_entry.created_at
        if time_since_last_otp < timedelta(minutes=5):
            return APIResponse.respond({'message': 'OTP already sent. Please wait 5 minutes before requesting a new one.'}, status_code=429)
        otp_entry.otp_code = otp_code
        otp_entry.created_at = datetime.utcnow()
        otp_entry.expires_at = expires_at
    else:
        new_otp = OTP(phone_number=phone_number, otp_code=otp_code, expires_at=expires_at)
        db.session.add(new_otp)
    db.session.commit()

    if send_whatsapp_otp(phone_number, otp_code):
        return APIResponse.respond({'message': 'OTP sent to your WhatsApp.'}, status_code=200)
    else:
        return APIResponse.respond({'message': 'Failed to send OTP.'}, status_code=500)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    phone_number = data.get('phone_number')
    otp_code = data.get('otp_code')
    
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return APIResponse.respond({'message': 'User does not exist. Please register first.'}, status_code=400)

    otp_entry = OTP.query.filter_by(phone_number=phone_number, otp_code=otp_code).first()
    
    if not otp_entry:
        return APIResponse.respond({'message': 'Invalid OTP or phone number.'}, status_code=400)

    if datetime.utcnow() > otp_entry.expires_at:
        db.session.delete(otp_entry)
        db.session.commit()
        return APIResponse.respond({'message': 'OTP expired.'}, status_code=400)

    db.session.delete(otp_entry)
    db.session.commit()
    
    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return APIResponse.respond({'token': token, 'message': 'OTP verified successfully.'})



@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    phone_number = data.get('phone_number')
    age = data.get('age')
    otp_code = data.get('otp_code')
    
    if not username or not phone_number or not age or not otp_code:
        return APIResponse.respond({'message': 'Enter all details !'}, status_code=400)

    age = int(age)
    if age>150 or age<0:
        return APIResponse.respond({'message': 'Enter valid age !'}, status_code=400)

    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        return APIResponse.respond({'message': 'Phone number already exists!'}, status_code=400)

    otp_entry = OTP.query.filter_by(phone_number=phone_number, otp_code=otp_code).first()
    
    if not otp_entry:
        return APIResponse.respond({'message': 'Invalid OTP or phone number.'}, status_code=400)

    if datetime.utcnow() > otp_entry.expires_at:
        db.session.delete(otp_entry)
        db.session.commit()
        return APIResponse.respond({'message': 'OTP expired.'}, status_code=400)

    db.session.delete(otp_entry)
    db.session.commit()
    
    new_user = User(username=username, phone_number=phone_number, age=age)
    db.session.add(new_user)
    db.session.commit()
    user = new_user
    message = 'Registration complete and OTP verified.'

    token = jwt.encode({
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return APIResponse.respond({'token': token, 'message': message})

