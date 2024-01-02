import base64


def encode_password(string):
    if string:
        password = base64.b64encode(string.encode('utf-8'))
        return str(password, 'utf-8')
    return False