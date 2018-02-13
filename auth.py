import requests
from PIL import Image
from io import BytesIO

LOGIN_URL = 'http://passport2.chaoxing.com/login'
CAPTCHA_URL = 'http://passport2.chaoxing.com/num/code'


def erya_login(username, password, captcha_mode: int = 0):
    session = requests.session()
    captcha = ''
    captcha_image_content = requests.get(CAPTCHA_URL).content
    captcha_image = Image.open(BytesIO(captcha_image_content))
    if captcha_mode == 1:
        # auto recognition

        # captcha recognition
        raise NotImplementedError
    elif captcha_mode == 0:
        # enter by user
        captcha_image.show()
        captcha = input('Code: ')
    else:
        raise ValueError('Unrecognized captcha mode %d' % captcha_mode)
    data = {
        'uname': username,
        'password': password,
        'numcode': captcha,
    }
    if session.post('http://passport2.chaoxing.com/login', data=data).status_code == 302:
        # TODO: login failure information
        return session.cookies.get_dict()
    else:
        raise RuntimeError('Login failed')



