from itsdangerous import TimedSerializer
from decouple import config

def generate_confirmation_token(email):
    serializer = TimedSerializer(config('SECRET_KEY'))
    return serializer.dumps(email, salt = config('PASSWORD_SALT'))


def confirm_token(token, expiration = 7200):
    serializer = TimedSerializer(config('SECRET_KEY'))
    try:
        email = serializer.loads(token, salt = config('PASSWORD_SALT'),max_age=expiration)
    except Exception as err:
        print(err)
        return False
    return email