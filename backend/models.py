from backend import db
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    age = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, phone_number={self.phone_number}, age={self.age})"
    

class OTP(db.Model):
    __tablename__ = 'otps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    otp_code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"OTP(id={self.id}, phone_number={self.phone_number}, otp_code={self.otp_code})"


db.create_all()


