import requests
from PIL import Image

LOGIN_URL = 'http://passport2.chaoxing.com/login'


def erya_login(username, password):
    session = requests.session()
    image = Image.frombytes(mode='RGB', size=(123, 40), data=session.get(LOGIN_URL).content)


class EryaSession:
    def __init__(self):
        pass
