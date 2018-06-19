import requests
from PIL import Image
from io import BytesIO
from erya import EryaSession
import time
from utils import HEADERS

LOGIN_URL = 'http://passport2.chaoxing.com/login?fid={fid}&refer=http://i.mooc.chaoxing.com/space/index.shtml'
CAPTCHA_URL = 'http://passport2.chaoxing.com/num/code?{ts}'
ERYA_S = 'a7b6c438cbba8ac6bdd24a7c60844b93'  # copied from capture, what is that?


def validate_cookies(cookies: dict, init_url):
    session = requests.session()
    session.cookies.update(cookies)
    session.headers.update(HEADERS)
    response = session.get(init_url, allow_redirects=False)
    if response.status_code == 200:
        return True
    return False


def erya_login(username, password, school_id) -> dict:
    session = requests.session()
    session.get(LOGIN_URL.format(fid=school_id))
    captcha = ''
    while not captcha:
        captcha_image_content = session.get(CAPTCHA_URL.format(ts=int(time.time() * 1000))).content
        captcha_image = Image.open(BytesIO(captcha_image_content))

        captcha_image.show()
        captcha = input('Enter code (Press enter to get a new code): ')

    data = {
        'uname': username,
        'password': password,
        'numcode': captcha,
        'fid': school_id,
        'fidName': '',
        'vercode': '',
        'refer_0x001': 'http%253A%252F%252Fi.mooc.chaoxing.com%252Fspace%252Findex.shtml',
        'pid': '-1',
        'pidName': '',
        'allowJoin': '0',
        'isCheckNumCode': '1',
        'f': '0',
        'productid': '',
        'verCode': '',

    }
    login_resp = session.post(
        'http://passport2.chaoxing.com/login?refer=http%3A%2F%2Fi.mooc.chaoxing.com%2Fspace%2Findex.shtml', data=data,
        allow_redirects=False, headers=HEADERS)
    if login_resp.status_code == 302:
        # set cookies
        session.get('http://i.mooc.chaoxing.com/space/index.shtml', headers=HEADERS)
        session.get('http://www.fanya.chaoxing.com/passport/allHead.shtml', headers=HEADERS)
        session.get('http://passport2.chaoxing.com/mooc.jsp?v=0&s={}'.format(ERYA_S), headers=HEADERS)
        return session.cookies.get_dict()
    else:
        # TODO: login failure information
        raise RuntimeError('Login failed')


class EryaAuth(EryaSession):
    def __init__(self, username, password, school_id):
        cookies = erya_login(username, password, school_id)
        EryaSession.__init__(self, cookies)
