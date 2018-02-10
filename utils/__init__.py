def get_enc(clazzId: str, userid: str, jobid: str, objectId: str, playingTime: int, duration: int,
            clipTime: str) -> str:
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
    :param clipTime:
    :return: enc string
    """
    _string = '[{cid}][{uid}][{jid}][{oid}][{pt}][d_yHJ!$pdA~5][{d}][{ct}]' \
        .format(cid=clazzId, uid=userid, jid=jobid, oid=objectId, pt=playingTime * 1000,
                d=duration * 1000, ct=clipTime)
    md5 = hashlib.md5()
    md5.update(_string.encode('utf-8'))
    return md5.hexdigest()
