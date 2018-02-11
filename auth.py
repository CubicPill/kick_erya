import requests
from PIL import Image

LOGIN_URL = 'http://passport2.chaoxing.com/login'
CAPTCHA_URL = 'http://passport2.chaoxing.com/num/code'


def erya_login(username, password, captcha_mode: int = 0):
    session = requests.session()
    if captcha_mode == 1:
        image = Image.frombytes(mode='RGB', size=(123, 40), data=session.get(CAPTCHA_URL).content)
        # captcha recognition
        raise NotImplementedError
    elif captcha_mode == 0:
        pass
    else:
        raise ValueError('Unrecognized captcha mode %d' % captcha_mode)
    data = {
        'uname': username,
        'password': password,
        'numcode': '',
    }
    session.post('http://passport2.chaoxing.com/login', data=data)
    return session.cookies.get_dict()


class EryaSession:
    def __init__(self, cookies):
        pass
