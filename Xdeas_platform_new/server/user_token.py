from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

SECRET_KEY = 'SECRET_KEY'

def create_token(user):
    s = Serializer(SECRET_KEY)
    return s.dumps({ 'id': user }).decode('ascii')

def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
        s.loads(token)
        return True
    except SignatureExpired:
        return False # valid token, but expired
    except BadSignature:
        return False # invalid token