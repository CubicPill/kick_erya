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

def get_enc(clazzId: int, userid: int, jobid: int, objectId: str, playingTime: int, duration: int) -> str:
    """
    get the enc field in update requests
    restored from decompiling the flash player
    :rtype: str
    :param clazzId:
    :param userid:
    :param jobid:
    :param objectId:
    :param playingTime:
    :param duration:
    :return: enc string
    """
    _string = '[{cid}][{uid}][{jid}][{oid}][{pt}][{salt}][{d}][{ct}]' \
        .format(cid=clazzId, uid=userid, jid=jobid, oid=objectId, pt=playingTime * 1000,
                d=duration * 1000, ct='0_%d' % duration, salt=SALT)
    md5 = hashlib.md5()
    md5.update(_string.encode('utf-8'))
    return md5.hexdigest()
