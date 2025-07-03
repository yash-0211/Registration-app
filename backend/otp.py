from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
OTP_TTL = 300

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_otp(phone_number, otp_code):
    print("Sending OTP....")
    print(phone_number)
    receiver = "whatsapp:+91"+str(phone_number)
    text_message = f"Your verification code is: {otp_code}"
    try:
        message = client.messages.create(
            from_= TWILIO_WHATSAPP_NUMBER,
            content_sid='HX229f5a04fd0510ce1b071852155d3e75',
            content_variables='{"1":"409173"}',
            to=receiver
            )
        print(message.sid)
        return True
    except:
        return False

