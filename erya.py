import requests
import time
from utils import get_enc, parse_course_id_list
from bs4 import BeautifulSoup

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


class EryaSession:
    def __init__(self, cookies: dict):
        self.session = requests.session()
        for _k, _v in cookies.items():
            self.session.cookies.set(name=_k, value=_v)

    def get_course_chapter_id_list(self, course_id, class_id, enc):
        data = {
            'courseId': course_id,
            'clazzid': class_id,
            'enc': enc
        }
        response = self.session.get('http://mooc1-1.chaoxing.com/mycourse/studentcourse', params=data, headers=HEADERS)
        chapter_id_list = parse_course_id_list(response.text)
        return chapter_id_list

    def get_video(self):
        pass

    def request_log(self, duration: int, user_id: int, job_id: int, object_id: str, class_id: int, playing_time: int):
        data = {
            'dtype': 'Video',
            'duration': duration,
            'userid': user_id,
            'rt': '0.9',
            'jobid': job_id,
            'objectId': object_id,
            'clipTime': '0_%d' % duration,
            'otherInfo': '',
            'clazzId': class_id,
            'view': 'pc',
            'playingTime': playing_time,
            'isdrag': '3',
            'enc': get_enc(class_id, user_id, job_id, object_id, playing_time, duration)
        }
        url = ''

        self.session.post(url, data=data)

    def request_checkpoint(self, mid):
        url = 'https://mooc1-1.chaoxing.com/richvideo/initdatawithviewer?&start=undefined&mid={mid}'.format(mid=mid)
        return self.session.get(url).json()

    def request_monitor(self, version: str, jsoncallback: str, referer='http://i.mooc.chaoxing.com',
                        t: int = int(time.time())):
        """
        the periodic request to detect multi client login

        :param version:
        :param jsoncallback:
        :param referer:
        :param t:
        :return:
        """

        data = {
            'version': version,
            'jsoncallback': jsoncallback,
            'referer': referer,
            't': t
        }
        self.session.get('https://passport2.chaoxing.com/api/monitor', data=data)
