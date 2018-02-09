from hashlib import md5
import requests
import time

CHPTCHA_URL = 'http://passport2.chaoxing.com/num/code'


def main():
    for i in range(1000):
        m = md5()
        m.update(str(time.time()).encode())
        filename = m.hexdigest()
        try:
            with open('./data/{}.jpg'.format(filename), 'wb') as f:
                f.write(requests.get(CHPTCHA_URL).content)
        except:
            pass


if __name__ == '__main__':
    main()
