import hashlib
from .parser import *

SALT = 'd_yHJ!$pdA~5'

HEADERS = {
    'Connection': 'keep-alive',

    'Cache-Control': 'max-age=0',

    'Upgrade-Insecure-Requests': '1',

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

    'DNT': '1',

    'Accept-Encoding': 'gzip, deflate, br',

    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_log_enc(clazzId, user_id, job_id, objectId, playingTime, duration) -> str:
    """
    get the enc field in log requests
    restored from decompiling the flash player
    :rtype: str
    :param clazzId:
    :param user_id:
    :param job_id:
    :param objectId:
    :param playingTime:
    :param duration:
    :return: enc string
    """
    clazzId, user_id, job_id, playingTime, duration = \
        list(map(int, [clazzId, user_id, job_id, playingTime, duration]))
    _string = '[{cid}][{uid}][{jid}][{oid}][{pt}][{salt}][{d}][{ct}]' \
        .format(cid=clazzId, uid=user_id, jid=job_id, oid=objectId, pt=playingTime * 1000,
                d=duration * 1000, ct='0_%d' % duration, salt=SALT)
    md5 = hashlib.md5()
    md5.update(_string.encode())
    return md5.hexdigest()


def get_quiz_enc():
    pass
