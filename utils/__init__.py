import hashlib

SALT = 'd_yHJ!$pdA~5'


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
